import curses
import socket


class window():
    def __init__(self):
        pass

    def __init__(self, size_x, size_y, contents = ''):
        pass

    def __keypress__(self, key):
        pass
    
    def draw(self, screen):
        pass

class subreddit_window(window):
    def __init__(self):
        sublist = ["sub1", "sub2", "sub3"]

    def keypress(self, char):
        pass

    def draw(self, screen):
        pass
    


if __name__ == "__main__":    
    #Init curses library
    screen = curses.initscr()
    curses.noecho()
    screen.addch(10,10,curses.ACS_ULCORNER)
    screen.addch(11,10,curses.ACS_LLCORNER)
    screen.addch(10,11,curses.ACS_URCORNER)
    screen.addch(11,11,curses.ACS_LRCORNER)
    #curses.ACS_VLINE
    #curses.ACS_HLINE
    screen.refresh()
    screen.keypad(True)
    screen.getch()
    curses.nocbreak()
    screen.keypad(False)
    curses.endwin()






