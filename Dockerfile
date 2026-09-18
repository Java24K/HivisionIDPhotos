FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements-app.txt ./

RUN pip install --no-cache-dir -r requirements.txt -r requirements-app.txt

COPY . .

EXPOSE 8080

CMD ["python3", "-u", "deploy_api.py"]
