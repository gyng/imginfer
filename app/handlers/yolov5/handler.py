import contextlib
import io
import logging

import torch

from .. import Handler, InferError, Result


class YoloV5(Handler):
    def __init__(self, variant="yolov5s"):
        self.model = torch.hub.load("ultralytics/yolov5", variant)

    def infer(self, url: str) -> Result:
        if not url:
            raise InferError(message=f"bad url: {url}")

        try:
            results = self.model([url])
        except Exception as e:
            logging.error(e)
            raise InferError(message=f"could not infer {url}")

        # yolov5 prints results to stdout instead when doing str()
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            str(results)
        output = f.getvalue()

        pandas = results.pandas()
        serialized = pandas.xyxy[0].to_dict(orient="records")

        return Result(output, serialized)
