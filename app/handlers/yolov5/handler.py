import contextlib
import io

import torch

from .. import Handler, Result


class YoloV5(Handler):
    def __init__(self, variant="yolov5s"):
        self.model = torch.hub.load("ultralytics/yolov5", variant)

    def infer(self, url: str) -> Result:
        f = io.StringIO()

        # yolov5 prints results to stdout instead when doing str()
        with contextlib.redirect_stdout(f):
            results = self.model([url])
            str(results)

        output = f.getvalue()
        pandas = results.pandas()
        serialized = pandas.xyxy[0].to_dict(orient="records")

        return Result(output, serialized)
