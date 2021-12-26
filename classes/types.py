from typing import Tuple, NewType


Row = NewType("Row", Tuple[int])
Cells = NewType("Cells", Tuple[Row])
XY = NewType("XY", Tuple[int])
