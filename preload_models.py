import logging

from app.handlers.easyocr.handler import EasyOCR
from app.handlers.yolov5.handler import YoloV5

if __name__ == "__main__":
    logging.info("preloading models...")

    logging.info("preloading yolov5...")
    YoloV5()

    logging.info("preloading easyocr...")
    EasyOCR()

    logging.info("done preloading models.")
