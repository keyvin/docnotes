import curses
import socket


class window():
    def __init__(self, screen):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.size_x = 20
        self.size_y = 20
        pass

    def __keypress__(self, key):
        pass

    def fill(self):
        func = lambda y,x : self.screen.addstr(y, x, " ", curses.color_pair(1))
        for j in range(self.x, self.x+self.size_x):
            for i in range(self.y, self.y+self.size_y):
                func(i, j)
        
    def draw(self):
        #basic border
        self.fill()
        self.screen.addch(self.y,self.x,curses.ACS_ULCORNER, curses.color_pair(1))
        self.screen.addch(self.y +self.size_y,self.x,curses.ACS_LLCORNER, curses.color_pair(1))
        self.screen.addch(self.y, self.x+ self.size_x,curses.ACS_URCORNER, curses.color_pair(1))
        self.screen.addch(self.y+self.size_y,self.x+self.size_x,curses.ACS_LRCORNER, curses.color_pair(1))
        for i in range(1, self.size_y):
            self.screen.addch(self.y+i, self.x, curses.ACS_VLINE, curses.color_pair(1))
            self.screen.addch(self.y+i, self.x+self.size_x, curses.ACS_VLINE, curses.color_pair(1))
        for i in range(1, self.size_x):
            self.screen.addch(self.y, self.x+i, curses.ACS_HLINE, curses.color_pair(1))
            self.screen.addch(self.y+self.size_y, self.x+i, curses.ACS_HLINE, curses.color_pair(1))
           

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
    curses.start_color()
    curses.noecho()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLUE)
    screen.refresh()
    screen.keypad(True)
    s = window(screen)
    s.draw()
    screen.getch()
    curses.nocbreak()
    screen.keypad(False)
    curses.endwin()

     
     




