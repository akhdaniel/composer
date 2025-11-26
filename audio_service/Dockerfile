# Python 3.10 (Demucs-compatible)
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

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# OPTIONAL: Download Demucs models during build
RUN demucs --help >/dev/null 2>&1 || true
RUN demucs --dl >/dev/null 2>&1 || true

# Copy the rest of the app
COPY app.py .

# Expose FastAPI port
EXPOSE 8000

# Run the API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]


