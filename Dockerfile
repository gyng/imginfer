FROM python:3.10

WORKDIR /app

# OpenCV dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

# Set TORCH_CUDA to cu113, cu116, or cpu by default
COPY ./install-torch.sh .
RUN ["./install-torch.sh", "$TORCH_CUDA"]

# Minor optimisation to cache model downloads
COPY app/handlers app/handlers/
COPY preload_models.py .
RUN ["python", "preload_models.py"]

COPY . .

EXPOSE 8080

# Used for dev
# CMD ["python", "main.py"]

# Used for production
# workers=1 so we don't load duplicate models to save resources
CMD ["gunicorn", "--workers=1", "--threads=1", "--bind=0.0.0.0:8080", "--log-level=debug", "--access-logfile=-", "main:flask_app"]
