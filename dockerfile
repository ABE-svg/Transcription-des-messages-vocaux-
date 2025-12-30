FROM python:3.11-slim

WORKDIR /app

# installation de ffmpeg obligatoire pour whisper
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn","app.api:create_app()","--bind", "0.0.0.0:5000", "--timeout", "300", "--workers", "1"]

