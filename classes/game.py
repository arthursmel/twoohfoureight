from typing import Set
from .state import State
from .types import Row, Cells, XY, SumResult, MoveResult
import random
import itertools

class Game:
    def init_state(self, dim: int=4) -> State:
        x1, y1 = self.get_rand_xy(dim)
        xy2 = self.get_rand_xy(dim, excludes={(x1, y1)})
        xys = {(x1,y1), xy2}
        set_val = lambda x, y: self.get_next_rand_val() if (x,y) in xys else 0 
        cells = tuple(tuple(set_val(x,y) for x in range(dim)) for y in range(dim))

        return State(cells, has_2048=False, has_moves=True)
        
    def get_rand_xy(self, dim: int, excludes: Set[XY] = {(-1,-1)}) -> XY:
        choices = {(x,y) for x in range(dim) for y in range(dim)} - excludes
        if len(choices) == 0: return (-1,-1)
        return random.sample(choices, 1)[0]

    def get_next_rand_val(self) -> int:
        return random.choice([2,4])

    def get_used_xys(self, cells: Cells) -> Set[XY]:
        dim = len(cells[0])
        zeros = lambda xy: xy != (-1,-1)
        to_add_xy = lambda x,y: (x,y) if cells[y][x] != 0 else (-1,-1)
        return set(filter(zeros, { to_add_xy(x,y) for y in range(dim) for x in range(dim) }))
         
    def place_random_val(self, cells: Cells) -> Cells:
        used_xys = self.get_used_xys(cells)

        dim = len(cells[0])
        xy = self.get_rand_xy(dim, excludes=used_xys)
        
        if xy == (-1,-1): return cells

        set_val = lambda x, y: self.get_next_rand_val() if (x,y) == xy else cells[y][x] 
        return tuple(tuple(set_val(x,y) for x in range(dim)) for y in range(dim))

    def move_row_horizontal(self, row: Row, dir: str) -> SumResult:
        ns = tuple(filter(lambda i: i > 0, row))

        summed, score = self.get_pair_sums(ns if dir == 'l' else ns[::-1])
        zeros = tuple(0 for _ in range(len(row) - len(summed)))

        return SumResult(summed + zeros if dir == 'l' else zeros + summed[::-1], score)

    def get_pair_sums(self, ns: Row) -> SumResult:
        if len(ns) in (0,1): return SumResult(ns, 0)
        fst, snd = ns[0], ns[1]

        if fst == snd:
            next_pair_sums, score = self.get_pair_sums(ns[2:])
            pair_sums = SumResult((fst + snd,) + next_pair_sums, score + fst+snd)
        else:
            next_pair_sums, score = self.get_pair_sums(ns[1:])
            pair_sums = SumResult((fst,) + next_pair_sums, score)
        return pair_sums

    def rotate_cells(self, cells: Cells, dir: str) -> Cells:
        zipped_cells = tuple(zip(*cells))[::-1] if dir == 'l' else tuple(zip(*cells[::-1]))
        return tuple(tuple(row) for row in zipped_cells)

    def move_cells_horizontal(self, cells: Cells, dir: str) -> MoveResult:
        sum_results = tuple(map(lambda r: self.move_row_horizontal(r, dir), cells))

        score = sum(tuple(map(lambda r: r.score, sum_results)))
        new_cells = tuple(map(lambda r: r.row, sum_results))

        return MoveResult(new_cells, score, new_cells != cells)

    def move_cells_vertical(self, cells: Cells, dir: str) -> MoveResult:
        rotated_cells = self.rotate_cells(cells, 'l')
        horizontal_dir = 'r' if dir == 'd' else 'l'

        rotated_new_cells, score, _ = self.move_cells_horizontal(rotated_cells, horizontal_dir)
        new_cells = self.rotate_cells(rotated_new_cells, 'r')

        return MoveResult(new_cells, score, new_cells != cells)
        
    def move(self, state: State, dir: str) -> State:
        if dir in ('u', 'd'):
            new_cells, score, valid = self.move_cells_vertical(state.cells, dir)
        else:
            new_cells, score, valid = self.move_cells_horizontal(state.cells, dir)

        new_cells = self.place_random_val(new_cells) if valid else new_cells
        new_score = score + state.score
        return State(new_cells, new_score, has_2048=self.has_2048(new_cells), has_moves=self.has_moves(new_cells))
        
    def move_up(self, state: State) -> State:
        return self.move(state, dir='u')

    def move_down(self, state: State) -> State:
        return self.move(state, dir='d')

    def move_left(self, state: State) -> State:
        return self.move(state, dir='l')

    def move_right(self, state: State) -> State:
        return self.move(state, dir='r')

    def has_val(self, val: int, cells: Cells) -> bool:
        cell_vals = list(itertools.chain.from_iterable(cells))
        return val in cell_vals

    def has_2048(self, cells: Cells) -> bool:
        return self.has_val(2048, cells)

    def has_zero(self, cells: Cells) -> bool:
        return self.has_val(0, cells)

    def has_moves(self, cells: Cells) -> bool:
        if self.has_zero(cells): return True

        dim = len(cells[0])
        horizontal_has_move = any([ r[i] == r[i+1] for r in cells for i in range(dim-1) ])
        veritical_has_move = any([ 
            cells[r][c] == cells[r+1][c] for c in range(dim) for r in range(dim-1) 
        ])
        return horizontal_has_move or veritical_has_move
