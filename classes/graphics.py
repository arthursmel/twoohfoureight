from .state import State
from .state import Cells
import curses
import math

class Graphics:
    TILE_WIDTH = 11
    TILE_HEIGHT = 5
    TILE_MARGIN = 2
    TILE_X_OFFSET = 4
    TILE_Y_OFFSET = 3
    MAIN_Y_PADDING = 2
    MAIN_X_PADDING = 4
    
    def __init__(self) -> None:
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.init_color_pairs()

    def init_color_pairs(self) -> None:
        curses.init_pair(1, 227, curses.COLOR_BLACK)
        curses.init_pair(2, 226, curses.COLOR_BLACK)
        curses.init_pair(3, 220, curses.COLOR_BLACK)
        curses.init_pair(4, 221, curses.COLOR_BLACK)
        curses.init_pair(5, 215, curses.COLOR_BLACK)
        curses.init_pair(6, 214, curses.COLOR_BLACK)
        curses.init_pair(7, 208, curses.COLOR_WHITE)
        curses.init_pair(8, 209, curses.COLOR_WHITE)
        curses.init_pair(9, 203, curses.COLOR_WHITE)
        curses.init_pair(10, 202, curses.COLOR_WHITE)
        curses.init_pair(11, 196, curses.COLOR_WHITE)
        curses.init_pair(12, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(13, curses.COLOR_RED, curses.COLOR_WHITE)

    def draw_board(self, state: State) -> None:
        dim = len(state.cells[0])
        cells = state.cells

        self.draw_border(dim)
        self.draw_cells(dim, cells)
        self.draw_score(dim, state.score)

    def draw_score(self, dim: int, score: int) -> None:
        main_width = self.MAIN_X_PADDING + (dim * self.TILE_WIDTH) + (dim * self.TILE_MARGIN)
        score_text = "SCORE: " + str(score)
        self.stdscr.addstr(1, main_width//2 - len(score_text)//2, score_text, curses.color_pair(12) | curses.A_BOLD | curses.A_REVERSE)
        self.stdscr.refresh()

    def draw_cells(self, dim: int, cells: Cells) -> None:
        for r in range(dim):
            for c in range(dim):
                self.draw_cell(cells, r, c)
                
    def draw_cell(self, cells: Cells, r: int, c: int) -> None:
        cell_val = cells[r][c]
        if cell_val == 0: return

        tile_y = self.TILE_Y_OFFSET + (self.TILE_HEIGHT*r) + (self.TILE_MARGIN*r)
        tile_x = self.TILE_X_OFFSET + (self.TILE_WIDTH*c) + (self.TILE_MARGIN*c)
        tile = curses.newwin(self.TILE_HEIGHT, self.TILE_WIDTH, tile_y, tile_x)

        log_cell_val = int(math.log2(cell_val))
        color_pair = min(log_cell_val, 11)
        tile.bkgd(' ', curses.color_pair(color_pair) | curses.A_BOLD | curses.A_REVERSE)

        tile_text = str(cell_val)
        tile_text_x = (self.TILE_WIDTH//2) - len(tile_text)//2
        tile_text_y = (self.TILE_HEIGHT//2)
        tile.addstr(tile_text_y, tile_text_x, tile_text)
        tile.refresh()

    def draw_border(self, dim: int) -> None:
        main_width = self.MAIN_X_PADDING + (dim * self.TILE_WIDTH) + (dim * self.TILE_MARGIN)
        main_height = self.MAIN_Y_PADDING + (dim * self.TILE_HEIGHT) + (dim * self.TILE_MARGIN)
        main_win = curses.newwin(main_height, main_width, 1, 1)
        main_win.border('|', '|', '-', '-', '+', '+', '+', '+')
        main_win.refresh()

    def draw_end(self, has_2048: bool) -> None:
        self.stdscr.addstr(1, 1,
            "GAME OVER. You did" + ("" if has_2048 else " not") + " get 2048", 
            curses.color_pair(13) | curses.A_BOLD | curses.A_REVERSE)
