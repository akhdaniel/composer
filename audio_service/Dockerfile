FROM python:3.10-slim

RUN apt update && apt install -y --no-install-recommends \
        ffmpeg \
        git \
        curl \
        libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# 🔥 Install python-multipart separately (FastAPI requires it BEFORE route load)
RUN pip install --no-cache-dir python-multipart

# Install Torch CPU (MUST be separate line)
RUN pip install --no-cache-dir torch==2.1.0 --index-url https://download.pytorch.org/whl/cpu

# Install other Python deps
RUN pip install --no-cache-dir -r requirements.txt

RUN demucs --help >/dev/null 2>&1 || true
RUN demucs --dl >/dev/null 2>&1 || true

COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]


