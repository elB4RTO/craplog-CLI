
import curses

from os import walk as climb

from crappy.elements.model import UIobj


class Tree( UIobj ):
    """
    Sub-Class for the CLI interface
    """
    def initContent(self, crappath:str ):
        """
        Correctly initialize the content variable
        """
        self.root_path = crappath
        self.tree = {}
        self.climbTree()
        # the actual branch on the tree
        self.branch = {}
        # holds the actual branch's content
        self.content = []
        # holds every step needed to climb-up to the actual branch
        self.steps = []
        self.index = 0
        self.x_pos = 0
        self.y_pos = 0
    
    
    def climbTree(self):
        """
        Scan the crapstats to make the directory tree
        """
        def cutDriedBranches( branch ):
            for k,v in branch.items():
                if type(v) is dict:
                    if len(v) == 0:
                        _ = branch.pop( k )
                    else:
                        cutDriedBranches( v )
                        if len(v) == 0:
                            _ = branch.pop( k )
        
        # dig the soil
        self.tree.clear()
        # climb the tree
        trunk_path = "%s/crapstats" %( self.root_path )
        trunk_len = len(trunk_path)+1
        for path,dirs,files in climb( trunk_path ):
            if 'CVS' in dirs:
                dirs.remove('CVS')
            # step in the correct position
            branch = self.tree
            if len(path) > trunk_len:
                chunks = path[trunk_len:].split('/')
                for i in range(len(chunks)):
                    if chunks[i] == "":
                        continue
                    branch = branch[ chunks[i] ]
            # append directories as dictionaries
            for dir_name in dirs:
                branch.update({ dir_name : {} })
            # append crapstat files as paths
            for file_name in files:
                if file_name.endswith(".crapstat"):
                    branch.update({ file_name : "%s/%s" %( path, file_name ) })
        # recursively remove empty folders
        cutDriedBranches( self.tree )
    
    
    def climb(self, steps:list ) -> dict :
        """
        Draw the tree
        """
        branch = self.tree
        for step in self.steps:
            branch = branch[ step ]
        return branch
    
    
    def drawContent(self):
        """
        Draw the tree
        """
        # set the color for the content
        t_color = curses.color_pair(7)
        h_color = curses.color_pair(2)
        if self.focus is True:
            t_color = curses.color_pair(2)
            h_color = curses.color_pair(12)
        # define the printable content
        
        
        printable = self.content
        if len(printable) > (self.w-5):
            printable = self.tree[len(printable)-(self.w-5):]
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
            printable, t_color )
        # push the updates
        self.window.noutrefresh()
    
    
    
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
            self.index -= 1
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
