import base64
import io
import math
from pydub import AudioSegment

class AudioSplitterBase64:
    def __init__(self, base64_audio, chunk_length=10):
        self.base64_audio = base64_audio
        self.chunk_length = chunk_length  # seconds

        # Decode Base64 to bytes
        audio_bytes = base64.b64decode(base64_audio)

        # Load into AudioSegment
        self.audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

    def split(self):
        chunk_ms = self.chunk_length * 1000
        total_length = len(self.audio)
        total_chunks = math.ceil(total_length / chunk_ms)

        chunk_list = []

        for i in range(total_chunks):
            start = i * chunk_ms
            end = min((i + 1) * chunk_ms, total_length)
            chunk = self.audio[start:end]

            chunk_list.append(self.audio_to_base64(chunk))

        return chunk_list

    # -------------------------------------------------------
    # 🔹 Convert AudioSegment → Base64
    # -------------------------------------------------------
    def audio_to_base64(self, segment, format="mp3"):
        buffer = io.BytesIO()
        segment.export(buffer, format=format)
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")
        
    # -------------------------------------------------------
    # 🔹 NEW: Extract audio by start–end range (in seconds)
    # -------------------------------------------------------
    def split_range(self, start_sec, end_sec):
        """
        Extract audio from start_sec → end_sec (in seconds)
        Returns base64 encoded MP3.
        """
        start_ms = int(start_sec * 1000)
        end_ms = int(end_sec * 1000)

        # safety limits
        start_ms = max(0, start_ms)
        end_ms = min(len(self.audio), end_ms)

        if start_ms >= end_ms:
            raise ValueError("End time must be greater than start time")

        clipped_segment = self.audio[start_ms:end_ms]

        return self.audio_to_base64(clipped_segment)

# ============================
# Example Usage
# ============================
if __name__ == "__main__":
    with open("song.mp3", "rb") as f:
        sample_b64 = base64.b64encode(f.read()).decode()

    splitter = AudioSplitterBase64(sample_b64, chunk_length=10)
    chunks = splitter.split()

    print("Generated", len(chunks), "chunks")
    print(chunks[0][:100])  # print first 100 chars
