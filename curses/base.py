import curses
import socket


class window():
    def __init__(self, screen,title = ''):
        self.screen = screen
        self.x = 0
        self.y = 0
        self.size_x = 20
        self.size_y = 20
        self.title = title 
        self.contents = """SQUIRE TRELAWNEY, Dr. Livesey, and the rest of these gentlemen having asked me to write down the whole particulars about Treasure Island, from the beginning to the end, keeping nothing back but the bearings of the island, and that only because there is still treasure not yet lifted, I take up my pen in the year of grace 17__ and go back to the time when my father kept the Admiral Benbow inn and the brown old seaman with the sabre cut first took up his lodging under our roof.
I remember him as if it were yesterday, as he came plodding to the inn door, his sea-chest following behind him in a hand-barrow--a tall, strong, heavy, nut-brown man, his tarry pigtail falling over the
shoulder of his soiled blue coat, his hands ragged and scarred, with black, broken nails, and the sabre cut across one cheek, a dirty, livid white. I remember him looking round the cover and whistling to himself
as he did so, and then breaking out in that old sea-song that he sang so often afterwards:
in the high, old tottering voice that seemed to have been tuned andbroken at the capstan bars. Then he rapped on the door with a bit of stick like a handspike that he carried, and when my father appeared,
called roughly for a glass of rum. This, when it was brought to him, he drank slowly, like a connoisseur, lingering on the taste and still looking about him at the cliffs and up at our signboard.
This is a handy cove, says he at length; and a pleasant sittyated grog-shop. Much company, mate? My father told him no, very little company, the more was the pity. Well, then, said he, this is the berth for me. Here you, matey, he
cried to the man who trundled the barrow; bring up alongside and help up my chest. I'll stay here a bit, he continued. I'm a plain man; rum and bacon and eggs is what I want, and that head up there for to watch
ships off. What you mought call me? You mought call me captain. Oh, I see what you're at--there; and he threw down three or four gold pieces on the threshold. You can tell me when I've worked through that, says
he, looking as fierce as a commander. 
And indeed bad as his clothes were and coarsely as he spoke, he had none of the appearance of a man who sailed before the mast, but seemed like a mate or skipper accustomed to be obeyed or to strike. The man who came
with the barrow told us the mail had set him down the morning before at the Royal George, that he had inquired what inns there were along the coast, and hearing ours well spoken of, I suppose, and described as lonely, had chosen it from the others for his place of residence. And that was all we could learn of our guest."""
        pass

    def __keypress__(self, key):
        pass

    def fill(self):
        func = lambda y,x : self.screen.addstr(y, x, " ", curses.color_pair(1))
        for j in range(self.x, self.x+self.size_x):
            for i in range(self.y, self.y+self.size_y):
                func(i, j)
        
    def draw_border(self):
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
        if self.size_x < len(self.title):
            pass
        else:
            place_x = int(self.size_x/2 - len(self.title))
            self.screen.addstr(self.y, self.y+2, self.title, curses.color_pair(1))

    def draw_text(self, text=""):
        x = self.x + 1
        x_max = x + self.size_x - 1
        y = self.y + 1
        y_max = y + self.size_y - 1
        for i in text:
            
            if i == '\n':
                x = self.x+1
                y = y + 1
                continue
            if x >= x_max:
                x = self.x+1
                y = y + 1
            if y >= y_max:
                return
            self.screen.addch(y, x, i, curses.color_pair(1))
            x = x + 1
                
            
        pass

    def calc_lines(self):
        return int(len(self.contents)/(self.size_x-2))+1


class v_scrolled_window(window):
    def __init__(self, screen, title):
        window.__init__(self, screen, title)
        self.lines = self.calc_lines()
        self.scroll_pos = 0
        self.view_y = 0
        self.view_y_max = self.view_y + self.size_y - 2
        self.scroll_count = 0
        
    def scroll_up(self):
        if self.view_y == 0:
            return
        self.view_y = self.view_y -1
        self.view_y_max = self.view_y_max -1
        return

    def scroll_down(self):
        if self.view_y_max == self.lines:
            return
        self.view_y = self.view_y + 1
        self.view_y_max = self.view_y_max + 1
        return
    
    def get_text(self):
        string = []
        curr_on_line = 0
        curr_pos = 0
        curr_line = 0
        for i in self.contents:
            curr_pos = curr_pos + 1
            curr_on_line = curr_on_line + 1
            if curr_on_line >= self.size_x-1:
                curr_line = curr_line + 1
                curr_on_line = 0
            if i == '\n':
                curr_line = curr_line+1
                curr_on_line = 0
            if curr_line >= self.view_y_max:
                return string
            if curr_line >= self.view_y:
                string.append(i)
        return string
    

class subreddit_window(window):
    def __init__(self,screen, title = ''):
        window.__init__(self,screen, title)
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
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    screen.refresh()
    screen.keypad(True)
    s = v_scrolled_window(screen, "Text")
    s.draw_border()
#    screen.addstr(0,0,''.join(s.get_text()))
    s.draw_text(''.join(s.get_text()))
    while not screen.getch() == 'q':
        s.scroll_down()
        s.draw_border()
        s.draw_text(''.join(s.get_text()))

    curses.nocbreak()
    screen.keypad(False)
    curses.endwin()

     
     




