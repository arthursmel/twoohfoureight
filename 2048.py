from typing import Any, List, Tuple
from typing import Optional
from typing import Set
import random
import itertools

class Board:
    def __init__(self, dim=4) -> None:
        self.dim = dim
        self.cells =  [ [0] * dim for _ in range(dim) ]

    def frm(self, cells, dim=4):
        self.cells = cells
        return self

    def __str__(self) -> str:
        return ''.join([ str(row) + '\n' for row in self.cells ])

class Game:
    def __init__(self, dim=4) -> None:
        self.dim = dim

    def init_board(self) -> Board:
        board = Board(self.dim)

        fst_x, fst_y = self.get_rand_xy()
        snd_x, snd_y = self.get_rand_xy(excludes={(fst_x, fst_y)})

        board.cells[fst_y][fst_x] = random.choice([2,4])
        board.cells[snd_y][snd_x] = random.choice([2,4])

        return board
        
    def get_rand_xy(self, excludes: Set[Tuple[int, int]] = {(-1,-1)}) -> Tuple[int, int]:
        choices = {(x,y) for x in range(self.dim) for y in range(self.dim)} - excludes
        return random.sample(choices, 1)[0]

    def move_row(self, r, dir: str) -> List[int]:
        ns = list(filter(lambda i: i > 0, r))
        r_ns = list(reversed(ns))
        ps = self.pair(ns)
        r_ps = self.pair(r_ns) 

        pair_sums = list(itertools.chain.from_iterable(self.pair_sum(ps)))
        r_pair_sums = list(itertools.chain.from_iterable(self.pair_sum(r_ps)))

        summed = min([pair_sums, r_pair_sums], key=len)
        zeros = [0] * (self.dim - len(summed))

        return summed + zeros if dir == 'l' else zeros + summed

    def pair(self, ns):
        return [ [ns[i],ns[i+1]] if i+1 < len(ns) else [ns[i]] for i in range(0,len(ns),2) ]

    def pair_sum(self, ns):
        return [ [n[0]+n[1]] if len(n)==2 and n[0]==n[1] else n for n in ns ]

    def move_horizontal(self, board: Board, dir: str) -> Board:
        return Board().frm(map(lambda r: self.move_row(r, dir), board.cells), dim=self.dim)

    def rotate_board(self, board: Board, dir: str) -> Board:
        zipped_cells = zip(*board.cells[::-1]) if dir == 'l' else list(zip(*board.cells))[::-1]
        rotated_cells = list(list(t) for t in zipped_cells)
        return Board().frm(rotated_cells, dim=self.dim)

    def move_vertical(self, board: Board, dir: str) -> Board:
        rot_ccw = self.rotate_board(board, 'l')
        rot_dir = 'l' if dir == 'd' else 'r'
        res = self.move_horizontal(rot_ccw, rot_dir)
        return self.rotate_board(res, 'r')

    def move_up(self, board: Board) -> Board:
        return self.move_vertical(board, 'u')

    def move_down(self, board: Board) -> Board:
        return self.move_vertical(board, 'd')

    def move_left(self, board: Board) -> Board:
        return self.move_horizontal(board, 'l')

    def move_right(self, board: Board) -> Board:
        return self.move_horizontal(board, 'r')

    def has_won(self, Board) -> bool:
        pass

    def has_lost(self, Board) -> bool:
        return False 

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
