# app/Dockerfile

FROM python:3.13-slim

WORKDIR /app

# Install system dependencies including FFmpeg
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY . .

# Install Python dependencies using uv
RUN pip install uv && \
    uv sync --frozen

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]