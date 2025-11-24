import os
import io
import base64
import math
import tempfile
import subprocess
from pydub import AudioSegment
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter


class AudioProcessor:
    def __init__(self, base64_audio, output_dir="output", chunk_length=10):
        self.base64_audio = base64_audio
        self.chunk_length = chunk_length
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        # decode base64 → bytes
        audio_bytes = base64.b64decode(base64_audio)

        # load pydub audio for splitting / exporting
        self.audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

        # Create temp WAV file (Demucs, UVR require path)
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        self.audio.export(self.temp_file.name, format="wav")

    # -------------------------------------------------------
    # 🔹 Convert audio segment → base64
    # -------------------------------------------------------
    def audio_to_b64(self, segment, format="wav"):
        buffer = io.BytesIO()
        segment.export(buffer, format=format)
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode()

    # -------------------------------------------------------
    # 🔹 Base64 split into chunks
    # -------------------------------------------------------
    def split_into_chunks(self, segment):
        chunk_ms = self.chunk_length * 1000
        total_length = len(segment)
        total_chunks = math.ceil(total_length / chunk_ms)

        chunks = []
        for i in range(total_chunks):
            start = i * chunk_ms
            end = min((i + 1) * chunk_ms, total_length)
            chunk = segment[start:end]

            chunks.append(self.audio_to_b64(chunk, format="wav"))

        return chunks

    # -------------------------------------------------------
    # 🔹 Spleeter (in-memory)
    # -------------------------------------------------------
    def separate_spleeter(self):
        loader = AudioAdapter.default()
        waveform, sr = loader.load(self.temp_file.name)

        separator = Separator("spleeter:2stems")
        pred = separator.separate(waveform)

        # Convert numpy arrays → pydub segments
        vocals_seg = AudioSegment(
            pred["vocals"].tobytes(),
            frame_rate=sr,
            sample_width=pred["vocals"].dtype.itemsize,
            channels=pred["vocals"].shape[1],
        )

        music_seg = AudioSegment(
            pred["accompaniment"].tobytes(),
            frame_rate=sr,
            sample_width=pred["accompaniment"].dtype.itemsize,
            channels=pred["accompaniment"].shape[1],
        )

        return vocals_seg, music_seg

    # -------------------------------------------------------
    # 🔹 Demucs (CLI)
    # -------------------------------------------------------
    def separate_demucs(self):
        out = os.path.join(self.output_dir, "demucs")
        os.makedirs(out, exist_ok=True)

        cmd = [
            "demucs",
            "-n", "htdemucs",
            self.temp_file.name,
            "-o", out,
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Results
        demucs_dir = os.path.join(out, "htdemucs")
        parts = {}
        for stem in ["vocals", "other", "drums", "bass"]:
            path = os.path.join(demucs_dir, f"{stem}.wav")
            parts[stem] = AudioSegment.from_file(path) if os.path.exists(path) else None

        return parts["vocals"], parts["other"]

    # -------------------------------------------------------
    # 🔹 UVR (CLI)
    # -------------------------------------------------------
    def separate_uvr(self, uvr_script="uvr.py", model="vr_model"):
        out = os.path.join(self.output_dir, "uvr")
        os.makedirs(out, exist_ok=True)

        cmd = [
            "python", uvr_script,
            "-i", self.temp_file.name,
            "-o", out,
            "-m", model,
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        vocals = None
        music = None

        for f in os.listdir(out):
            fp = os.path.join(out, f)
            if "Vocals" in f:
                vocals = AudioSegment.from_file(fp)
            if "Instrumental" in f:
                music = AudioSegment.from_file(fp)

        return vocals, music

    # -------------------------------------------------------
    # 🔹 Unified API
    # -------------------------------------------------------
    def separate(self, method="spleeter", split_chunks=False):
        """
        Returns:
        {
            "vocals": <base64>,
            "music": <base64>,
            "chunks": [<base64>, ...] (optional)
        }
        """

        if method == "spleeter":
            vocals_seg, music_seg = self.separate_spleeter()

        elif method == "demucs":
            vocals_seg, music_seg = self.separate_demucs()

        elif method == "uvr":
            vocals_seg, music_seg = self.separate_uvr()

        else:
            raise ValueError("method must be: spleeter | demucs | uvr")

        result = {
            "vocals": self.audio_to_b64(vocals_seg),
            "music": self.audio_to_b64(music_seg),
        }

        if split_chunks:
            result["chunks"] = self.split_into_chunks(vocals_seg)

        return result
