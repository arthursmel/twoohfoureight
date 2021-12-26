from curses import wrapper
from classes.game import Game
import curses

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
