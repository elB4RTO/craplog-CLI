
import curses

from crappy.interface import TUI

class Window():
    def __init__(self, stdscr, crappath ):
        """
        Crapview's initializer
        """
        # 
        self.screen = stdscr
        #
        self.n_cols = curses.COLS
        self.n_rows = curses.LINES
        # 
        self.ui = TUI( stdscr, crappath )
    
    
    def checkResized(self):
        """
        If the window has been resized, updates new values
        """
        if curses.is_term_resized( self.n_rows, self.n_cols ) is True:
            self.n_cols = curses.COLS
            self.n_rows = curses.LINES
            self.ui.resize( self.n_rows, self.n_cols )
    
    
    def run(self):
        """
        If the screen has been resized, updates new values
        """
        loop = True
        self.checkResized()
        self.ui.redraw()
        curses.doupdate()
        while loop is True:
            # fit the available space
            self.checkResized()
            # wait for an input
            self.ui.feed( self.screen.getch() )
            # update the screen
            curses.doupdate()
            #self.screen.refresh() # <-- DELETE IF USELESS
