from __future__ import annotations
from typing import Any, List, Tuple, NewType
from typing import Optional
from typing import Set
from dataclasses import dataclass
import random
import itertools
from curses import wrapper
import curses

Row = NewType("Row", Tuple[int])
Cells = NewType("Cells", Tuple[Row])
XY = NewType("XY", Tuple[int])

@dataclass(frozen=True)
class State:
    cells: Cells = tuple(tuple(0 for _ in range(4)) for _ in range(4))
    has_2048: bool = False
    has_moves: bool = True

    def __str__(self) -> str:
        s = [
            "has_2048:" + str(self.has_2048) + '\n', 
            "has_moves:" + str(self.has_moves) + '\n',
            ''.join([ ''.join([ str(i) + '\t' for i in r ]) + '\n' for r in self.cells ])
        ]
        return ''.join(s)

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
         
    def place_random_val(self, state: State) -> State:
        used_xys = self.get_used_xys(state.cells)

        dim = len(state.cells[0])
        xy = self.get_rand_xy(dim, excludes=used_xys)
        
        if xy == (-1,-1): return state

        set_val = lambda x, y: self.get_next_rand_val() if (x,y) == xy else state.cells[y][x] 
        cells = tuple(tuple(set_val(x,y) for x in range(dim)) for y in range(dim))

        return State(cells, has_moves=self.has_moves(cells), has_2048=self.has_2048(cells))

    def move_row_horizontal(self, row: Row, dir: str) -> Row:
        ns = list(filter(lambda i: i > 0, row))

        ps = self.pairs(ns)
        offset_ps = self.offset_pairs(ns) 

        pair_sums = tuple(itertools.chain.from_iterable(self.pair_sum(ps)))
        offset_pair_sums = tuple(itertools.chain.from_iterable(self.pair_sum(offset_ps)))

        summed = min([pair_sums, offset_pair_sums], key=len)
        zeros = tuple(0 for _ in range(len(row) - len(summed)))

        return summed + zeros if dir == 'l' else zeros + summed

    def pairs(self, ns) -> Tuple[Tuple[int]]:
        return tuple( (ns[i],ns[i+1]) if i+1 < len(ns) else (ns[i],) for i in range(0,len(ns),2) )

    def offset_pairs(self, ns: Row) -> Tuple[Tuple[int]]:
        if len(ns) == 0: return ()
        return ((ns[0],),) + tuple( (ns[i],ns[i+1]) if i+1 < len(ns) else (ns[i],) for i in range(1,len(ns),2) )

    def pair_sum(self, ns: Row) -> Tuple[Tuple[int]]:
        return tuple( (n[0]+n[1],) if len(n)==2 and n[0]==n[1] else n for n in ns )

    def rotate_cells(self, cells: Cells, dir: str) -> Cells:
        zipped_cells = tuple(zip(*cells[::-1])) if dir == 'l' else tuple(zip(*cells))[::-1]
        return tuple(tuple(row) for row in zipped_cells)

    def move_cells_horizontal(self, cells: Cells, dir: str) -> Cells:
        return tuple(map(lambda r: self.move_row_horizontal(r, dir), cells))

    def move_cells_vertical(self, cells: Cells, dir: str) -> Cells:
        rotated_cells = self.rotate_cells(cells, 'l')
        horizontal_dir = 'l' if dir == 'd' else 'r'
        cells = self.move_cells_horizontal(rotated_cells, horizontal_dir)

        return self.rotate_cells(cells, 'r')

    def move_horizontal(self, state: State, dir: str) -> State:
        cells = self.move_cells_horizontal(state.cells, dir)
        return State(cells, has_2048=self.has_2048(cells), has_moves=self.has_moves(cells))

    def move_vertical(self, state: State, dir: str) -> State:
        cells = self.move_cells_vertical(state.cells, dir)
        return State(cells, has_2048=self.has_2048(cells), has_moves=self.has_moves(cells))

    def move(self, state: State, dir: str) -> State:
        if dir in ('u', 'd'):
            moved = self.move_vertical(state, dir)
            return self.place_random_val(moved)
        else:
            moved = self.move_horizontal(state, dir)
            return self.place_random_val(moved)
        
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

def main(stdscr):
    stdscr = curses.initscr()
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    
    game = Game()
    state = game.init_state()

    stdscr.addstr(str(state))

    while state.has_moves:
        key_press = stdscr.getch()
        if key_press == curses.KEY_UP:
            state = game.move_up(state)
        elif key_press == curses.KEY_DOWN:
            state = game.move_down(state)
        elif key_press == curses.KEY_LEFT:
            state = game.move_left(state)
        elif key_press == curses.KEY_RIGHT:
            state = game.move_right(state)

        stdscr.clear()
        stdscr.addstr(str(state))
    
    key_press = stdscr.getch()
    while key_press != curses.KEY_UP:
        stdscr.clear()
        stdscr.addstr(str(state))
        stdscr.addstr("You did" + ("" if state.has_2048 else " not") + " get 2048\n Press up arrow to quit")
        key_press = stdscr.getch()

if __name__ == '__main__':
    wrapper(main)
