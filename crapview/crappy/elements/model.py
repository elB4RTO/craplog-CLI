
import curses


class UIobj():
    """
    Class Model to hold an interface element
    """
    def __init__(self, height, width, y, x, window=None, focus=False ):
        self.y = y
        self.x = x
        self.h = height
        self.w = width
        self.focus = focus
        self.window = window
    
    def initContent(self):
        """
        Model for the Sub-Classes
        """
        pass
    
    def config(self, new_h, new_w, new_y, new_x ):
        """
        Set up a new configuration
        """
        self.y = new_y
        self.x = new_x
        self.h = new_h
        self.w = new_w
        # adapt the window
        self.window.mvwin( self.y, self.x )
        self.window.resize( self.h, self.w )
    
    def feed(self, key:int ):
        """
        Model for the Sub-Classes
        """
        pass
    
    def endY(self):
        """
        Returns the last drawable point on the Y axis
        """
        return self.y + self.h-1
    
    def endX(self):
        """
        Returns the last drawable point on the X axis
        """
        return self.x + self.w-1
    
    def drawBorder(self):
        """
        Draw the window border
        """
        color = curses.color_pair(7)
        if self.focus is True:
            color = curses.color_pair(2)
        # draw upper border
        self.window.addstr(
            0, 0,
            "╒%s╕" %("═"*(self.w-2)),
            color )
        # draw left and right border
        for row in range( 1, self.h-1 ):
            self.window.addstr(
                row, 0,
                "│", color )
            self.window.addstr(
                row, self.w-1,
                "│", color )
        # draw lower border
        self.window.addstr(
            row, 0,
            "╘%s╛" %("═"*(self.w-2)),
            color )
        self.window.noutrefresh()
    
    def drawContent(self):
        """
        Model for the Sub-Classes
        """
        pass
    
    def redraw(self):
        """
        Redraw the entire window
        """
        self.window.clear()
        self.drawBorder()
        self.drawContent()
    
