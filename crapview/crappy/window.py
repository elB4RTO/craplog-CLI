
import curses

from os import get_terminal_size

from crappy.interface import TUI


class Window():
    """
    Base window (the terminal)
    """
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
        #
        self.dry_run = False
    
    
    
    def checkResized(self):
        """
        If the window has been resized, updates new values
        """
        n_cols, n_rows = get_terminal_size()
        if n_cols != self.n_cols\
        or n_rows != self.n_rows:
            self.n_cols, self.n_rows = n_cols, n_rows
            curses.resize_term( n_rows, n_cols )
            self.ui.resize( n_cols, n_rows )
            self.ui.redraw()
            self.dry_run = True
    
    
    
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
            if self.dry_run is True:
                self.dry_run = False
            else:
                # wait for an input
                loop = self.ui.feed( self.screen.getch() )
            # update the screen
            curses.doupdate()
            #self.screen.refresh() # <-- DELETE IF USELESS
        self.ui.quitting()
    
