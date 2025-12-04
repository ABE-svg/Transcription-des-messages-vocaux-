FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /python-docker

# Installer ffmpeg et git
RUN apt-get update && apt-get install -y ffmpeg git && rm -rf /var/lib/apt/lists/*

# Copier et installer requirements
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Installer Whisper depuis GitHub
RUN pip install --no-cache-dir "git+https://github.com/openai/whisper.git"

# Copier le code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
