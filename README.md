# imginfer

Simple Python webserver that runs inference on images given a URL.

Features

- yolov5s
- Flask + API key auth
- gunicorn + Docker images for serving

## Usage

POST `/infer`, with Authorization header

```bash
$ curl -X POST http://localhost:8080/infer \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer letmein' \
  -d '{ "uri": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Cat_poster_1.jpg/390px-Cat_poster_1.jpg" }'
```

Response

```json
{
  "yolov5": {
    "results": [
      {
        "class": 15,
        "confidence": 0.9151156544685364,
        "name": "cat",
        "xmax": 287.8982238769531,
        "xmin": 220.71005249023438,
        "ymax": 116.89944458007812,
        "ymin": 15.380263328552246
      }
    ],
    "str_repr": "image 1/1: 256x390 1 cat\nSpeed: 37.8ms pre-process, 50.8ms inference, 0.8ms NMS per image at shape (1, 3, 448, 640)\n"
  }
}
```

### Environment variables

`.env` is supported.

|Key|Default value|
|-|-|
|`API_KEY`|`""` (auth disabled)|
|`HOST`|`"0.0.0.0"`|
|`PORT`|`"8080"`|

## Local install

```bash
$ pip install -r requirements.txt

# Or if on pip3
$ pip3 install -r requirements.txt
```

You might need to run one of

- `TORCH_CUDA=cu113 install-torch-cuda.sh`
- `TORCH_CUDA=cu116 install-torch-cuda.sh`
- `TORCH_CUDA=cpu install-torch-cuda.sh`

to install the correct Torch libraries if `pip` fails to grab the right ones.

```bash
# Start the Flask server
$ python main.py
$ open http://localhost:8080/

# Require header `Authorization: Bearer <API_KEY>`
$ API_KEY=letmein python main.py
```

## Docker

`docker-compose` must be > v1.28.0 for GPU support.

```bash
# Use CPU for Torch inference
$ docker-compose -f docker-compose.cpu.yml up --build
$ API_KEY=letmein docker-compose -f docker-compose.cpu.yml up --build

# Use GPU for Torch inference
$ docker-compose -f docker-compose.cuda.yml up --build
$ API_KEY=letmein docker-compose -f docker-compose.cuda.yml up --build
```

## Test & lint

The test suite is running integration tests so it is recommended that you use `docker-compose.test.yml` to run the tests.
It starts up a Flask server that serves an image for the test suite to run against.

```bash
$ do-test.sh
$ docker-compose -f docker-compose.test.yml up --build --exit-code-from server
$ do-lint-fix.sh

$ docker-compose -f docker-compose.test.yml up --build cat_server
$ python -m pytest
```
