import logging

import easyocr

from .. import Handler, InferError, Result


class EasyOCR(Handler):
    def __init__(self, languages=["en", "ja"]):
        self.model = easyocr.Reader(languages)

    def infer(self, filepath: str) -> Result:
        if not filepath:
            raise InferError(message=f"bad filepath: {filepath}")

        try:
            output = self.model.readtext(filepath, output_format="dict")
            json_safe_output = [
                {
                    "boxes": [[int(bx), int(by)] for [bx, by] in x["boxes"]],
                    "text": x["text"],
                    "confident": x["confident"],
                }
                for x in output
            ]
            str_repr = " ".join(x["text"] for x in json_safe_output)
        except Exception as e:
            logging.error(e)
            raise InferError(message="could not infer easyocr")

        return Result(str_repr, json_safe_output)
