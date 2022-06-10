
import curses

from crappy.elements.model import UIobj
from crappy.elements.cli import CommandLine
from crappy.elements.tree import Tree
from crappy.elements.view import View


class TUI():
    """
    Text-based User Inteface
    """
    def __init__(self, stdscr, crappath ):
        """
        Interface constructor
        """
        # height and width
        self.cols = curses.COLS
        self.rows = curses.LINES
        # bind to the screen object
        self.screen = stdscr
        # window border
        self.terminal = UIobj(
            self.rows, self.cols,
            0, 0 )
        # command line
        self.cli = CommandLine(
            4, self.terminal.w-2, # height, width
            self.terminal.endY()-2, self.terminal.x+1 ) # y start, x start
        self.cli.window = curses.newwin(
            self.cli.h, self.cli.w, # height, width
            self.cli.y, self.cli.x ) # y_start, x_start
        self.cli.initContent()
        # navigation menu
        self.tree = Tree(
            self.terminal.h-2, # h
            int(((self.terminal.w-2)/100)*33.3)-2, # w
            self.terminal.y, # x
            self.terminal.x+1) # y
        self.tree.window = curses.newwin(
            self.tree.h, self.tree.w,
            self.tree.y, self.tree.x )
        self.tree.initContent( crappath )
        # stats view
        self.view = View(
            self.terminal.h-2,
            self.terminal.w-self.tree.w-3,
            self.terminal.y,
            self.terminal.x+self.tree.w+2)
        self.view.window = curses.newwin(
            self.view.h, self.view.w,
            self.view.y, self.view.x )
        self.view.initContent()
        # the element with focus
        self.focusel = 0
        self.switchFocus( +1 )
        
    
    
    def resize(self, new_rows, new_cols ):
        """
        Update values about window size
        """
        self.rows = new_rows
        self.cols = new_cols
        self.adapt()
        self.redraw()
    
    
    def adapt(self):
        """
        Adapt the elements to fit the available space
        """
        self.terminal.config(
            self.rows, self.cols,
            0, 0 )
        # command line
        self.cli.config(
            4, self.terminal.w-2,
            self.terminal.endY()-3, self.terminal.x+1 )
        # navigation menu
        self.tree.config(
            self.terminal.h-2,
            int(((self.terminal.w-2)/100)*33.3)-2,
            self.terminal.y,
            self.terminal.x+1)
        # stats view
        self.view.config(
            self.terminal.h-2,
            self.terminal.w-self.tree.w-3,
            self.terminal.y,
            self.terminal.x+self.tree.w+2)
    
    
    def feed(self, key:int ):
        """
        Pass a keyboard input to the element with focus
        """
        #print("\r",key)
        # switch element if tab is pressed
        if key == 9:
            # forward (TAB)
            self.switchFocus( +1 )
        elif key == 353:
            # backward (BACK-TAB)
            self.switchFocus( -1 )
        else:
            # or feed it otherwise
            if self.focusel == 1:
                self.cli.feed( key )
            elif self.focusel == 2:
                self.tree.feed( key )
            elif self.focusel == 3:
                self.view.feed( key )
            else:
                # put an error message here
                raise Exception("\033[1;31m!-> PUT AN ERROR MESSAGE HERE !!!\033[0m")
    
    
    def switchFocus(self, way:int ):
        """
        Transfer focus to the next element
        """
        self.focusel += way
        if self.focusel < 1:
            self.focusel = 3
        elif self.focusel > 3:
            self.focusel = 1
        # remove all focuses
        self.cli.focus = False
        self.tree.focus = False
        self.view.focus = False
        # switch element
        if self.focusel == 1:
            self.cli.focus = True
        elif self.focusel == 2:
            self.tree.focus = True
        elif self.focusel == 3:
            self.view.focus = True
        else:
            # put an error message here
            raise Exception("\033[1;31m!-> PUT AN ERROR MESSAGE HERE !!!\033[0m")
        # redraw every window
        self.redraw()
            
    
    
    def redraw(self):
        """
        Redraw the entire screen
        """
        # redraw every window without updating the screen
        self.tree.redraw(  )
        self.view.redraw()
        self.cli.redraw()
    
    
    def redrawFocus(self):
        """
        Redraw the screen
        """
        if self.tree.focus is True:
            self.tree.redraw()
        if self.view.focus is True:
            self.view.redraw()
        if self.cli.focus is True:
            self.cli.redraw()
