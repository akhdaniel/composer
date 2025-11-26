from fastapi import FastAPI, UploadFile
import subprocess
import uuid
import os
import base64

app = FastAPI()

@app.post("/separate")
async def separate_audio(file: UploadFile):
    # Save temp input file
    temp_id = str(uuid.uuid4())
    input_path = f"/tmp/{temp_id}.mp3"
    output_dir = f"/tmp/{temp_id}_out"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Run demucs
    cmd = ["demucs", input_path, "-o", output_dir]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Read output vocals
    vocals_path = os.path.join(output_dir, "htdemucs", "vocals.wav")
    with open(vocals_path, "rb") as f:
        vocals_b64 = base64.b64encode(f.read()).decode()

    # Cleanup optional
    # os.remove(input_path)

    return {
        "vocals_base64": vocals_b64,
        "output_dir": output_dir
    }
