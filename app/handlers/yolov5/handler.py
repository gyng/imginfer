import contextlib
import io
import logging

import torch

from .. import Handler, InferError, Result


class YoloV5(Handler):
    def __init__(self, variant="yolov5s"):
        self.model = torch.hub.load("ultralytics/yolov5", variant)

    def infer(self, filepath: str) -> Result:
        if not filepath:
            raise InferError(message=f"bad filepath: {filepath}")

        try:
            results = self.model([filepath])
            # yolov5 prints results to stdout instead when doing str()
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                str(results)
            output = f.getvalue()

            pandas = results.pandas()
            serialized = pandas.xyxy[0].to_dict(orient="records")

            return Result(output, serialized)
        except Exception as e:
            logging.error(e, exc_info=True)
            raise InferError(message="could not infer yolov5")
