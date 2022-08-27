from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List


@dataclass
class Result:
    str_repr: str
    results: List[Any]


@dataclass
class InferError(Exception):
    message: str


class Handler(ABC):
    @abstractmethod
    def infer(self, path: str) -> Result:
        return NotImplemented
