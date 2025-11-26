FROM python:3.10-slim

# Install system dependencies
RUN apt update && apt install -y ffmpeg git curl && rm -rf /var/lib/apt/lists/*

# Create app folder
WORKDIR /app

# Install Python deps (torch CPU and demucs)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Optional: Install Spleeter CLI binary
RUN curl -L -o spleeter.tar.gz https://github.com/deezer/spleeter/archive/refs/tags/v2.3.0.tar.gz \
    && tar -xvf spleeter.tar.gz \
    && mv spleeter /usr/local/bin/spleeter \
    && chmod +x /usr/local/bin/spleeter \
    && rm spleeter.tar.gz

# Copy API code
COPY app.py .

EXPOSE 8000

# Start the API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
