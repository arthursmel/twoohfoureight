from curses import wrapper
from classes.game import Game
from classes.graphics import Graphics
import curses

def main(stdscr):
    game = Game()
    graphics = Graphics()
    state = game.init_state()
    graphics.draw_board(state)

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

        graphics.draw_board(state)
    
    graphics.draw_end(state.has_2048)
    key_press = stdscr.getch()
    
if __name__ == '__main__':
    wrapper(main)
