from dataclasses import dataclass
from typing import Tuple, NewType

Row = NewType("Row", Tuple[int])
Cells = NewType("Cells", Tuple[Row])

@dataclass(frozen=True)
class State:
    cells: Cells = tuple(tuple(0 for _ in range(4)) for _ in range(4))
    score: int = 0
    has_2048: bool = False
    has_moves: bool = True

    def __str__(self) -> str:
        s = [
            "score:" + str(self.score) + '\n',
            "has_2048:" + str(self.has_2048) + '\n', 
            "has_moves:" + str(self.has_moves) + '\n',
            ''.join([ ''.join([ str(i) + '\t' for i in r ]) + '\n' for r in self.cells ])
        ]
        return ''.join(s)
