import uuid
import subprocess
import base64
import os
from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/separate")
async def separate_audio(file: UploadFile):

    # Generate UUID
    file_id = str(uuid.uuid4())

    # Paths
    input_mp3 = f"/tmp/{file_id}.mp3"
    input_wav = f"/tmp/{file_id}.wav"
    model_root = "/tmp/mdx_extra_q"   # important fix

    # Save uploaded file
    with open(input_mp3, "wb") as f:
        f.write(await file.read())

    # Convert to WAV
    subprocess.run(["ffmpeg", "-y", "-i", input_mp3, input_wav], check=True)

    # Run demucs
    subprocess.run([
        "demucs", "-n", "mdx_extra_q", input_wav, "-o", "/tmp"
    ], check=True)

    # After demucs, structure is:
    # /tmp/mdx_extra_q/<UUID>/
    stems_dir = os.path.join(model_root, file_id)

    if not os.path.isdir(stems_dir):
        raise Exception(f"Stems directory not found: {stems_dir}")

    # Build JSON return
    result = {}

    for fname in os.listdir(stems_dir):
        if fname.endswith(".wav"):
            path = os.path.join(stems_dir, fname)
            with open(path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            result[fname.replace(".wav", "")] = encoded

    return result

