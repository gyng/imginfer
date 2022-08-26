FROM python:3.10

WORKDIR /app

# OpenCV dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.cat.txt .
RUN pip install -r requirements.cat.txt

COPY . .

EXPOSE 8888

CMD ["python", "cat_server.py"]
