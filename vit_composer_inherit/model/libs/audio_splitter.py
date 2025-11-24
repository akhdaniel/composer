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
        """
        Returns: list of Base64 strings (10s chunks)
        """
        chunk_ms = self.chunk_length * 1000
        total_length = len(self.audio)
        total_chunks = math.ceil(total_length / chunk_ms)

        chunk_base64_list = []

        for i in range(total_chunks):
            start = i * chunk_ms
            end = min((i + 1) * chunk_ms, total_length)
            chunk = self.audio[start:end]

            # Export chunk to memory buffer
            buffer = io.BytesIO()
            chunk.export(buffer, format="mp3")
            buffer.seek(0)

            # Convert buffer → Base64 string
            b64 = base64.b64encode(buffer.read()).decode("utf-8")
            chunk_base64_list.append(b64)

        return chunk_base64_list


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
