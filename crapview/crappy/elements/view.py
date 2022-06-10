
import curses

from crappy.elements.model import UIobj


class View( UIobj ):
    """
    Sub-Class for the CLI interface
    """
    def initContent(self):
        """
        Correctly initialize the content variable
        """
        self.content = []
