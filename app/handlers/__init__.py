from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Result:
    str_repr: str
    results: List[dict]


@dataclass
class InferError(Exception):
    message: str


class Handler(ABC):
    @abstractmethod
    def infer(self, url: str) -> Result:
        return NotImplemented
