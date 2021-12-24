from __future__ import annotations
from typing import Any, List, Tuple
from typing import Optional
from typing import Set
import random
import itertools

class Board:
    def __init__(self, dim: int=4) -> None:
        self.dim = dim
        self.cells =  [ [0] * dim for _ in range(dim) ]

    def frm(self, cells: List[List[int]]) -> Board:
        self.dim = len(cells[0])
        self.cells = cells
        return self

    def __str__(self) -> str:
        return ''.join([ ''.join([ str(i) + '\t' for i in r ]) + '\n' for r in self.cells ])

class Game:
    def init_board(self, dim: int=4) -> Board:
        board = Board(dim)

        fst_x, fst_y = self.get_rand_xy(dim)
        snd_x, snd_y = self.get_rand_xy(dim, excludes={(fst_x, fst_y)})

        board.cells[fst_y][fst_x] = self.get_next_rand_val()
        board.cells[snd_y][snd_x] = self.get_next_rand_val()

        return board
        
    def get_rand_xy(self, dim: int, excludes: Set[Tuple[int, int]] = {(-1,-1)}) -> Tuple[int, int]:
        choices = {(x,y) for x in range(dim) for y in range(dim)} - excludes
        if len(choices) == 0: return (-1,-1)
        return random.sample(choices, 1)[0]

    def get_next_rand_val(self) -> int:
        return random.choice([2,4])

    def get_used_xys(self, board: Board) -> Set[Tuple[int, int]]:
        zeros = lambda xy: xy != (-1,-1)
        to_add_xy = lambda x,y: (x,y) if board.cells[y][x] != 0 else (-1,-1)
        return set(filter(zeros, { to_add_xy(x,y) for y in range(board.dim) for x in range(board.dim) }))
         
    def place_random_val(self, board: Board) -> Board:
        used_xys = self.get_used_xys(board)
        x, y = self.get_rand_xy(board.dim, excludes=used_xys)
        
        if (x,y) == (-1,-1): return board
        new_cells = board.cells[:]
        new_cells[y][x] = self.get_next_rand_val()
        return Board().frm(new_cells)

    def move_row(self, r, dir: str) -> List[int]:
        ns = list(filter(lambda i: i > 0, r))

        ps = self.pairs(ns)
        offset_ps = self.offset_pairs(ns) 

        pair_sums = list(itertools.chain.from_iterable(self.pair_sum(ps)))
        offset_pair_sums = list(itertools.chain.from_iterable(self.pair_sum(offset_ps)))

        summed = min([pair_sums, offset_pair_sums], key=len)
        zeros = [0] * (len(r) - len(summed))

        return summed + zeros if dir == 'l' else zeros + summed

    def pairs(self, ns) -> List[int]:
        return [ [ns[i],ns[i+1]] if i+1 < len(ns) else [ns[i]] for i in range(0,len(ns),2) ]

    def offset_pairs(self, ns) -> List[int]:
        if len(ns) == 0: return []
        return [[ns[0]]] + [ [ns[i],ns[i+1]] if i+1 < len(ns) else [ns[i]] for i in range(1,len(ns),2) ]

    def pair_sum(self, ns):
        return [ [n[0]+n[1]] if len(n)==2 and n[0]==n[1] else n for n in ns ]

    def rotate_board(self, board: Board, dir: str) -> Board:
        zipped_cells = zip(*board.cells[::-1]) if dir == 'l' else list(zip(*board.cells))[::-1]
        rotated_cells = list(list(t) for t in zipped_cells)
        return Board().frm(rotated_cells)

    def move_horizontal(self, board: Board, dir: str) -> Board:
        moved_cells = list(map(lambda r: self.move_row(r, dir), board.cells))
        return Board().frm(moved_cells)

    def move_vertical(self, board: Board, dir: str) -> Board:
        rot_ccw = self.rotate_board(board, 'l')
        rot_dir = 'l' if dir == 'd' else 'r'
        res = self.move_horizontal(rot_ccw, rot_dir)
        return self.rotate_board(res, 'r')

    def move(self, board: Board, dir: str) -> Board:
        if dir in ('u', 'd'):
            moved = self.move_vertical(board, dir)
            return self.place_random_val(moved)
        else:
            moved = self.move_horizontal(board, dir)
            return self.place_random_val(moved)
        
    def move_up(self, board: Board) -> Board:
        return self.move(board, dir='u')

    def move_down(self, board: Board) -> Board:
        return self.move(board, dir='d')

    def move_left(self, board: Board) -> Board:
        return self.move(board, dir='l')

    def move_right(self, board: Board) -> Board:
        return self.move(board, dir='r')

    def has_won(self, board: Board) -> bool:
        cell_vals = list(itertools.chain.from_iterable(board.cells))
        return 2048 in cell_vals

    def has_lost(self, board: Board) -> bool:
        horizontal_has_move = any([ r[i] == r[i+1] for r in board.cells for i in range(board.dim-1) ])
        veritical_has_move = any([ 
            board.cells[r][c] == board.cells[r+1][c] for c in range(board.dim) for r in range(board.dim-1) 
        ])
        return not(horizontal_has_move or veritical_has_move)

def main():
    game = Game()
    board = game.init_board()
    print(board)

    while not game.has_lost(board):
        move = input("u/d/l/r")
        if move == 'u':
            board = game.move_up(board)
        elif move == 'd':
            board = game.move_down(board)
        elif move == 'l':
            board = game.move_left(board)
        elif move == 'r':
            board = game.move_right(board)
        else:
            print("Invalid move")

        print(board)

if __name__ == '__main__':
    main()
