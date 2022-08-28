# Danbooru2018 pretrained model: M Baas (https://github.com/RF5/danbooru-pretrained)

import json
import logging
import os

import torch
from PIL import Image
from torchvision import transforms

from app.handlers.danbooru2018.cpu import resnet50

from .. import Handler, InferError, Result


class Danbooru2018(Handler):
    def __init__(self):
        dirname = os.path.dirname(__file__)
        classdef = os.path.join(dirname, "class_names_6000.json")
        with open(classdef) as f:
            self.class_names = json.loads(f.read())

        if not torch.cuda.is_available():
            self.model = resnet50()
            self.model.eval()
        else:
            self.model = torch.hub.load("RF5/danbooru-pretrained", "resnet50")
            self.model.eval()

    def infer(self, filepath: str) -> Result:
        if not filepath:
            raise InferError(message=f"bad filepath: {filepath}")

        try:
            input_image = Image.open(filepath)
            preprocess = transforms.Compose(
                [
                    transforms.Resize(360),
                    transforms.ToTensor(),
                    transforms.Normalize(
                        mean=[0.7137, 0.6628, 0.6519], std=[0.2970, 0.3017, 0.2979]
                    ),
                ]
            )
            input_tensor = preprocess(input_image)
            input_batch = input_tensor.unsqueeze(
                0
            )  # create a mini-batch as expected by the model

            if torch.cuda.is_available():
                input_batch = input_batch.to("cuda")
                self.model.to("cuda")

            with torch.no_grad():
                output = self.model(input_batch)
                output = torch.sigmoid(output[0])

            def to_table(probs, thresh=0.4):
                tmp = probs[probs > thresh]
                inds = probs.argsort(descending=True)
                table = []
                for i in inds[0 : len(tmp)]:
                    table.append([self.class_names[i], float(probs[i])])
                return table

            threshold = 0.4
            results = to_table(output, threshold)

            row_strings = []
            for [cls, p] in results:
                row_strings.append(f"{cls}: {'{:.3g}'.format(p)}")
            str_repr = ", ".join(row_strings)

            return Result(str_repr, [results])
        except Exception as e:
            logging.error(e, exc_info=True)
            raise InferError(message="could not infer danbooru2018")
