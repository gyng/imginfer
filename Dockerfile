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

COPY . .

EXPOSE 8080

CMD ["python", "main.py"]
