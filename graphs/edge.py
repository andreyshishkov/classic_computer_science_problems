from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Edge:
    start: int
    end: int

    def reversed(self) -> Edge:
        return Edge(self.end, self.start)

    def __str__(self):
        return f'{self.start} -> {self.end}'

    