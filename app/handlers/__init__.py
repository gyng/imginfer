from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Result:
    str_repr: str
    results: List[dict]


class Handler(ABC):
    @abstractmethod
    def infer(self, url: str) -> Result:
        return NotImplemented
