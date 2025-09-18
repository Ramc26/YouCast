FROM python:3.13
RUN apt-get update && apt-get install -y ffmpeg
COPY . .
RUN uv sync
