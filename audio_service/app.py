from fastapi import FastAPI, UploadFile
import subprocess
import uuid
import os
import base64

app = FastAPI()

@app.post("/separate")
async def separate_audio(file: UploadFile):
    # temporary ID
    uid = str(uuid.uuid4())

    input_path = f"/tmp/{uid}.mp3"
    output_dir = f"/tmp/{uid}_out"

    # save the uploaded file
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # run demucs
    cmd = ["demucs", input_path, "-o", output_dir]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # vocals output
    vocals_path = os.path.join(output_dir, "htdemucs", "vocals.wav")

    with open(vocals_path, "rb") as f:
        vocals_b64 = base64.b64encode(f.read()).decode()

    return {
        "vocals": vocals_b64,
        "output_path": vocals_path
    }
