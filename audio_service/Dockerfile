# Use Python 3.10 (Demucs + PyTorch compatible)
FROM python:3.10-slim

# Install system dependencies
RUN apt update && apt install -y --no-install-recommends \
        ffmpeg \
        git \
        curl \
        libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Install PyTorch CPU first (required before installing Demucs)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install Demucs + FastAPI service
RUN pip install --no-cache-dir \
        demucs \
        fastapi \
        uvicorn[standard] \
        ffmpeg-python

# OPTIONAL: Download Demucs models during build
# Makes first request much faster
RUN demucs --help >/dev/null 2>&1 || true
RUN demucs --dl >/dev/null 2>&1 || true

# Copy API source code
COPY app.py .

# Expose API port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
