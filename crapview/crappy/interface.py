
import curses

from time import sleep

from crappy.elements.model import UIobj
from crappy.elements.cli   import CommandLine
from crappy.elements.tree  import Tree
from crappy.elements.view  import View


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
        self.terminal.window = curses.newwin(
            self.terminal.h, self.terminal.w,
            self.terminal.y, self.terminal.x )
        # command line
        self.cli = CommandLine(
            4, self.terminal.w-2, # height, width
            self.terminal.endY()-2, self.terminal.x+1 ) # y start, x start
        self.cli.window = curses.newwin(
            self.cli.h, self.cli.w, # height, width
            self.cli.y, self.cli.x ) # y_start, x_start
        self.cli.ui = self
        self.cli.initContent()
        # navigation menu
        tree_width = int(((self.terminal.w-2)/100)*33.3)-2
        if tree_width > 32:
            tree_width = 32
        self.tree = Tree(
            self.terminal.h-2, # h
            tree_width, # w
            self.terminal.y, # x
            self.terminal.x+1) # y
        self.tree.window = curses.newwin(
            self.tree.h, self.tree.w,
            self.tree.y, self.tree.x )
        self.tree.ui = self
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
        self.view.ui = self
        self.view.initContent()
        # the element with focus
        self.focusel = 1
        self.switchFocus( +1 )
        
    
    
    def resize(self, new_cols, new_rows ):
        """
        Update values about window size
        """
        self.cols = new_cols
        self.rows = new_rows
        self.adapt()
        self.redraw()
    
    
    
    def adapt(self):
        """
        Adapt the elements to fit the available space
        """
        self.terminal.config(
            self.rows, self.cols, # height, width
            0, 0 ) # y start, x start
        # command line
        self.cli.config(
            4, self.terminal.w-2,
            self.terminal.endY()-2, self.terminal.x+1 )
        # navigation menu
        tree_width = int(((self.terminal.w-2)/100)*33.3)-2
        if tree_width > 32:
            tree_width = 32
        self.tree.config(
            self.terminal.h-3,
            tree_width,
            self.terminal.y,
            self.terminal.x+1)
        # stats view
        self.view.config(
            self.terminal.h-3,
            self.terminal.w-self.tree.w-3,
            self.terminal.y,
            self.terminal.x+self.tree.w+2)
    
    
    
    def feed(self, key:int ) -> bool :
        """
        Pass a keyboard input to the element with focus
        """
        #print("\r",key)
        loop = True
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
                loop = self.cli.feed( key )
            elif self.focusel == 2:
                self.tree.feed( key )
            elif self.focusel == 3:
                self.view.feed( key )
            else:
                # unexpected value
                raise Exception("interface.feed&unexpected value for element focus&%s" %(self.focusel))
        return loop
    
    
    
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
        self.cli.focus  = False
        self.tree.focus = False
        self.view.focus = False
        # switch element
        if self.focusel == 1:
            curses.curs_set(1)
            self.cli.focus = True
        elif self.focusel == 2:
            curses.curs_set(0)
            self.tree.focus = True
        elif self.focusel == 3:
            curses.curs_set(0)
            self.view.focus = True
        else:
            # unexpected value
            raise Exception("interface.switch&unexpected value for element focus&%s" %(self.focusel))
        # redraw every window
        self.redraw()
    
    
    
    def switch2cli(self):
        """
        Transfer focus to the cli window
        """
        self.focusel = 1
        curses.curs_set(1)
        self.cli.focus  = True
        self.tree.focus = False
        self.view.focus = False
        self.redraw()
    
    
    def switch2tree(self):
        """
        Transfer focus to the cli window
        """
        self.focusel = 2
        curses.curs_set(0)
        self.cli.focus  = False
        self.tree.focus = True
        self.view.focus = False
        self.redraw()
    
    
    def switch2view(self):
        """
        Transfer focus to the cli window
        """
        self.focusel = 3
        curses.curs_set(0)
        self.cli.focus  = False
        self.tree.focus = False
        self.view.focus = True
        self.redraw()
            
    
    
    def redraw(self):
        """
        Redraw the entire screen
        """
        # redraw every window without updating the screen
        self.screen.clear()
        self.screen.refresh()
        self.tree.redraw()
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
    
    
    
    def resetCli(self):
        """
        Signal to the cli window to clear the content
        """
        self.view.clearAll()
    
    
    def resetTree(self):
        """
        Signal to the tree window to clear the content
        """
        self.tree.clearAll()
    
    
    def resetView(self):
        """
        Signal to the view window to clear the content
        """
        self.view.clearAll()
    
    
    
    def cli2tree(self, steps:list ):
        """
        Signal to the tree window to follow these steps
        """
        self.tree.cliTree( steps )
    
    
    def tree2view(self, file_path:str ):
        """
        Signal to the view window to show these stats
        """
        self.view.inputStats( file_path )
        self.switch2view()
    
    
    
    def quitting(self):
        """
        Prepare to qui
        """
        # redraw every window in red
        curses.curs_set(0)
        self.screen.clear()
        self.screen.refresh()
        self.view.redrawQuit()
        self.tree.redrawQuit()
        self.cli.redrawQuit()
        curses.doupdate()
        sleep(0.7)
    
