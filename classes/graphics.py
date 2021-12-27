from .state import State
import curses, _curses

class Graphics:

    TILE_WIDTH = 9
    TILE_HEIGHT = 5
    TILE_MARGIN = 2
    TILE_X_OFFSET = 4
    TILE_Y_OFFSET = 3
    MAIN_Y_PADDING = 2
    MAIN_X_PADDING = 4

    dim = 4

    COLOR_PAIRS = {

    }
    
    def __init__(self) -> None:
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

    def draw_board(self, state: State):

        main_width = self.MAIN_X_PADDING + (self.dim * self.TILE_WIDTH) + (self.dim * self.TILE_MARGIN)
        main_height = self.MAIN_Y_PADDING + (self.dim * self.TILE_HEIGHT) + (self.dim * self.TILE_MARGIN)
        main_win = curses.newwin(main_height,main_width,1,1)
        main_win.border('|', '|', '-', '-', '+', '+', '+', '+')
        main_win.refresh()

        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        score_text = "SCORE: " + str(state.score)
        self.stdscr.addstr(1, main_width//2 - len(score_text)//2, score_text)

        for r in range(self.dim):
            for c in range(self.dim):
                cell_val = state.cells[r][c]
                if cell_val == 0: continue

                tile_y = self.TILE_Y_OFFSET + (self.TILE_HEIGHT*r) + (self.TILE_MARGIN*r)
                tile_x = self.TILE_X_OFFSET + (self.TILE_WIDTH*c) + (self.TILE_MARGIN*c)
                tile = curses.newwin(self.TILE_HEIGHT, self.TILE_WIDTH, tile_y, tile_x)
                tile.border('|', '|', '-', '-', '+', '+', '+', '+')
                tile.bkgd(' ', curses.color_pair(1) | curses.A_BOLD | curses.A_REVERSE)

                tile_text = str(cell_val)
                tile_text_x = (self.TILE_WIDTH//2) - len(tile_text)//2
                tile_text_y = (self.TILE_HEIGHT//2)
                tile.addstr(tile_text_y, tile_text_x, tile_text)
                tile.refresh()
