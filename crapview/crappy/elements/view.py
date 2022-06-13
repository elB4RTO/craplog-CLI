from time import sleep
import curses

from crappy.elements.model import UIobj


class View( UIobj ):
    """
    Sub-Class for the VIEW interface
    """
    def initContent(self):
        """
        Correctly initialize the content variable
        """
        self.field = ""
        self.bars   = []
        self.items  = []
        self.counts = []
        self.max_clen = 0
        self.max_ilen = 0
        # viewth shifts
        self.vertical_shift = 0
        self.horizontal_shift = 0
        # graphs
        self.BLOCK = "█"
        self.HALF  = "▒"
        self.colors = {
            'IP'  : curses.color_pair(5), # magenta
            'UA'  : curses.color_pair(5), # magenta
            'REQ' : curses.color_pair(3), # yellow
            'RES' : curses.color_pair(3), # yellow
            'ERR' : curses.color_pair(1), # red
            'LEV' : curses.color_pair(1), # red
            'T' : curses.color_pair(7), # white
            'H' : curses.color_pair(2) # green
        }
    
    
    def inputStats(self, file_path:str ):
        """
        Read and show the statistics
        """
        self.max_clen = 0
        self.max_ilen = 0
        self.vertical_shift = 0
        self.horizontal_shift = 0
        self.field = file_path[file_path.rfind('/')+1:file_path.rfind('.crapstat')]
        self.counts.clear()
        self.items.clear()
        self.bars.clear()
        try:
            # try read the file
            with open( file_path, 'r' ) as f:
                # read old statistics from file
                stats = f.read().strip().split('\n')
        except:
            # failed to read, put an error message here
            raise Exception("\033[1;31m!-> PUT AN ERROR MESSAGE HERE !!!\033[0m")
        else:
            # successfully read
            for stat in stats:
                stat = stat.lstrip()
                s = stat.find(' ')
                if s < 0:
                    # no separator found, put an error message here
                    raise Exception("\033[1;31m!-> PUT AN ERROR MESSAGE HERE !!!\033[0m")
                # get item and count
                try:
                    count = int(stat[:s].strip())
                except:
                    # can't convert to number, put an error message here
                    raise Exception("\033[1;31m!-> PUT AN ERROR MESSAGE HERE !!!\033[0m")
                try:
                    item = stat[s+1:].strip()
                except:
                    item = ""
                self.counts.append( count )
                self.items.append( item )
            # set the longhest lengths
            self.max_clen = len(str(max(self.counts)))+4
            self.max_ilen = max([len(item) for item in self.items])+2
            # scale counts to make bars
            self.makeBars()
            # stats collected, check integrity
            if len(self.counts) != len(self.items) != len(self.bars):
                # something went wrong, put an error message here
                raise Exception("\033[1;31m!-> PUT AN ERROR MESSAGE HERE !!!\033[0m")
            self.drawContent()
            self.cleanContentArea()
            self.drawContent()
    
    
    def makeBars(self):
        """
        Normalize the counts to get the bars
        """
        k = sum(self.counts) / (self.w-2)
        self.bars = [ int(x/k) for x in self.counts ]
    
    
    def clearAll(self):
        """
        Clear the content viewth and delete data
        """
        self.field = ""
        self.bars.clear()
        self.items.clear()
        self.counts.clear()
        self.max_clen = self.max_ilen = 0
        self.vertical_shift = self.horizontal_shift = 0
        self.cleanContentArea()
            
    
    
    def cleanContentArea(self):
        """
        Clear the content viewth
        """
        soap  = " "*(self.w-2)
        brush = self.h-2
        for i in range(1,brush):
            self.window.addstr(
                i, 1,
                soap )
        # push the updates
        self.window.noutrefresh()
    
    
    def drawContent(self):
        """
        Draws the entire content
        """
        self.cleanContentArea()
        # pick the colors
        b_col = self.colors[self.field]
        c_col = self.colors['H']
        i_col = self.colors['T']
        if self.focus is False:
            b_col = self.colors['H']
        # get the viewable section
        start = self.vertical_shift
        stop  = self.vertical_shift + ((self.h-2)//3)
        if stop > len(self.counts):
            stop = len(self.counts)
        # bring the viewable items
        bars   = self.bars[ start:stop ]
        items  = self.items[ start:stop ]
        counts = self.counts[ start:stop ]
        # get the longest count to display
        clen = self.max_clen
        # set the horizontal shift for the text
        shift = self.horizontal_shift
        # draw the stats
        y = 2
        for bar,count,item in zip(bars,counts,items):
            # prepare the objects
            b_str = "%s" %( self.BLOCK )*bar
            c_str = "%s%s  " %( " "*(clen-len(str(count))-2), count )
            i_str = " %s " %( item )
            # adapt bar
            if len(b_str) == 0:
                b_str = self.HALF
            # adapt count and item
            if shift < clen:
                # only the viewable parts
                c_str = c_str[-(clen-shift):]
                if len(i_str) > (self.w-2-len(c_str)):
                    i_str = i_str[:(self.w-2-len(c_str))]
            else:
                # count is not in the viewth
                c_str = ""
                if shift-clen < len(i_str):
                    # partially in the viewth
                    try:
                        i_str = i_str[ shift-clen : (self.w-2+(shift-clen)) ]
                    except:
                        i_str = ""
                else:
                    # item is not in the viewth
                    i_str = ""
            i_pos = len(c_str)+1
            # draw the graph-bar first
            self.window.addstr(
                y, 1,
                b_str, b_col )
            # the count next
            y += 1
            self.window.addstr(
                y, 1,
                c_str, c_col )
            # and the item last
            self.window.addstr(
                y, i_pos,
                i_str, i_col )
            
            # prepare for the next line
            y += 2
            # break if exceeding the available height
            if y+2 > self.h-2:
                break
        self.window.noutrefresh()
        
    
    
    def feed(self, key:int ):
        """
        Manages a keyboard input
        """ 
        # help
        if key == curses.KEY_HELP:
            # help mode
            pass # 2 COMPLETE !!!
        # arrow up
        elif key == curses.KEY_UP:
            # one shift content up
            if self.field != ""\
            and self.vertical_shift > 0:
                self.vertical_shift -= 1
                self.drawContent()
        # arrow down
        elif key == curses.KEY_DOWN:
            # shift content down
            if self.field != ""\
            and self.vertical_shift < len(self.counts)-((self.h-2)//3):
                self.vertical_shift += 1
                self.drawContent()
        # arrow right
        elif key == curses.KEY_RIGHT:
            # shift content right
            if self.field != ""\
            and self.horizontal_shift < self.max_ilen-(self.w-2):
                self.horizontal_shift += 1
                self.drawContent()
        # arrow left
        elif key == curses.KEY_LEFT:
            # shift content left
            if self.field != ""\
            and self.horizontal_shift > 0:
                self.horizontal_shift -= 1
                self.drawContent()
        # begin
        elif key == curses.KEY_HOME:
            # reset the horizontal shift
            self.horizontal_shift = 0
            self.drawContent()
        # end
        elif key == curses.KEY_END:
            # full horizontal shift
            self.horizontal_shift = self.max_ilen-(self.w-2)
            self.drawContent()
        # page-up
        elif key == curses.KEY_PPAGE:
            # vertical shift
            if self.vertical_shift > 0:
                self.vertical_shift -= (self.h-2)//3
                if self.vertical_shift < 0:
                    self.vertical_shift = 0
                self.drawContent()
        # page-down
        elif key == curses.KEY_NPAGE:
            # vertical shift
            if self.vertical_shift < len(self.counts)-((self.h-2)//3):
                self.vertical_shift += (self.h-2)//3
                if self.vertical_shift > len(self.counts)-((self.h-2)//3):
                    self.vertical_shift = len(self.counts)-((self.h-2)//3)
                self.drawContent()
        # enter
        elif key == curses.KEY_ENTER\
          or key == 10:
            # switch to the cli
            self.ui.switch2cli()
        # backspace
        elif key == curses.KEY_BACKSPACE\
          or key == 127:
            # switch back to the tree
            self.ui.switch2tree()
        # canc
        elif key == curses.KEY_CANCEL\
          or key == 330:
            # erase the drawable area
            self.clearAll()
        # canc + shift
        elif key == 383:
            # erase the drawable area and switch to the tree
            self.clearAll()
            self.ui.switch2tree()
        
        # assume everything else is text
        else:
            if key > 19\
            and key < 127:
                # skip non-ascii chars
                try:
                    # convert to char
                    char = str(chr( key ))
                    # skip invalid chars
                    if char in [':','c']:
                        self.ui.switch2cli()
                    elif char == 't':
                        self.ui.switch2tree()
                except:
                    # failed to convert to char
                    pass
    
    
    
    def redraw(self):
        """
        Redraw the entire window
        """
        self.window.clear()
        self.drawBorder()
        if self.field != "":
            self.makeBars()
            self.drawContent()
    

