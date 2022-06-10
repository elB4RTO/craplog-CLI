
import curses

from crappy.elements.model import UIobj


class CommandLine( UIobj ):
    """
    Sub-Class for the CLI interface
    """
    def initContent(self):
        """
        Correctly initialize the content variable
        """
        # user input
        self.command = ""
        self.aux_command = None
        # store previous commands
        self.history = ["help"]
        self.history_index = 1
    
    
    def drawContent(self):
        """
        Draw the command string
        """
        # set the color for the content
        color = curses.color_pair(7)
        if self.focus is True:
            color = curses.color_pair(2)
        # define the printable content
        printable = self.command
        if len(printable) > (self.w-5):
            printable = self.command[len(printable)-(self.w-5):]
        # clear the area with text
        self.window.addstr(
            1, 3,
            " "*(self.w-4),
            curses.color_pair(7) )
        # draw the prefix
        self.window.addstr(
            1, 1,
            ":", curses.color_pair(7) )
        # draw the content
        self.window.addstr(
            1, 3,
            printable, color )
        # push the updates
        self.window.noutrefresh()
    
    
    def clearAll(self):
        """
        Clean-up variables: commands history and actual string
        """
        self.history.clear()
        self.history.append("help")
        self.history_index = 1
        self.aux_command = None
        self.clear()
    
    
    def fromHistory(self, jump:int ):
        """
        Bring a previous command back
        """
        # save the newely type string
        if self.aux_command is None\
        and self.command != "":
            self.aux_command = self.command
        # jump in history
        new_index = self.history_index + jump
        if new_index > len(self.history):
            self.history_index = len(self.history)+1
            self.command = ""
        elif new_index < 0:
            pass
        else:
            # get the relative content
            if new_index == len(self.history):
                self.command = self.aux_command
                if self.command == ""\
                and self.history_index > new_index:
                    new_index -= 1
                    self.command = self.history[ new_index ]
                if self.command is None:
                    self.command = ""
                
            else:
                self.command = self.history[ new_index ]
            self.history_index = new_index
        # draw the new content
        self.drawContent()
    
    
    def feed(self, key:int ):
        """
        Manage a keyboard input
        """
        # help
        if key == curses.KEY_HELP:
            # help mode
            pass # 2 COMPLETE !!!
        # arrow up
        elif key == curses.KEY_UP\
          or key == 259:
            # one step behind in commands history
            self.fromHistory( -1 )
        # arrow down
        elif key == curses.KEY_DOWN\
          or key == 258:
            # one step forward in commands history
            self.fromHistory( +1 )
        # backspace
        elif key == curses.KEY_BACKSPACE\
          or key == 127:
            # delete the last char
            self.canc()
        # canc
        elif key == curses.KEY_CANCEL\
          or key == 330:
            # delete the entire string
            self.clear()
        # canc + shift
        elif key == 383:
            # erase commands history and actual string
            self.clearAll()
        # enter
        elif key == curses.KEY_ENTER\
          or key == 10:
            # run the actual command
            self.run()
        # assume everything else is text
        else:
            if key < 127:
                # skip non-ascii chars
                try:
                    # convert to char
                    char = str(chr( key ))
                    # skip invalid chars
                    if char.isalnum()\
                    or char.isspace()\
                    or char == "-":
                        self.push( char )
                except:
                    # failed to convert to char
                    pass
                
            
        
    
    def clear(self):
        """
        Clear the command string
        """
        self.command = ""
        self.drawContent()
    
    def canc(self):
        """
        Remove the last character from the actual command
        """
        self.command = self.command[:-1]
        self.drawContent()
    
    def push(self, char:chr ):
        """
        Append a character to the actual command
        """
        if self.history_index == len(self.history):
            self.aux_command = None
        self.command += char
        self.drawContent()
    
    
    def run(self):
        """
        Execute the actual command
        """
        # manage the commands history
        self.aux_command = None
        self.command = self.command.strip().lower()
        if self.command != ""\
        and self.command != self.history[-1]:
            # append to history if not empty and different by the last one
            self.history.append( self.command )
        self.history_index = len(self.history)
        self.clear()

