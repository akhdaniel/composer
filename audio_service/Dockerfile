FROM python:3.10-slim

RUN apt update && apt install -y --no-install-recommends \
        ffmpeg \
        git \
        curl \
        libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Force numpy 1.x (required)
RUN pip install --no-cache-dir "numpy==1.26.4"

RUN pip install --no-cache-dir python-multipart

# CPU compatible versions
RUN pip install --no-cache-dir \
    torch==1.13.1+cpu \
    torchaudio==0.13.1+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# Install Demucs v3
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

