from collections import namedtuple
from typing import Tuple, NewType

Row = NewType("Row", Tuple[int])
Cells = NewType("Cells", Tuple[Row])
XY = NewType("XY", Tuple[int])
SumResult = namedtuple("SumResult", ["row", "score"])
MoveResult = namedtuple("MoveResult", ["cells", "score", "valid"])
