
import curses

from os.path import abspath

from crappy.window import Window


def initscr( screen ):
    # disable input-to-screen
    curses.noecho()
    # get single keys without waiting for Enter
    curses.cbreak()
    # turn on colors if supported
    if curses.has_colors() is True:
        curses.start_color()
        curses.use_default_colors()
        # system defaults
        curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK )
        # text
        curses.init_pair( 1, curses.COLOR_RED,     curses.COLOR_BLACK )
        curses.init_pair( 2, curses.COLOR_GREEN,   curses.COLOR_BLACK )
        curses.init_pair( 3, curses.COLOR_YELLOW,  curses.COLOR_BLACK )
        curses.init_pair( 4, curses.COLOR_BLUE,    curses.COLOR_BLACK )
        curses.init_pair( 5, curses.COLOR_MAGENTA, curses.COLOR_BLACK )
        curses.init_pair( 6, curses.COLOR_CYAN,    curses.COLOR_BLACK )
        curses.init_pair( 7, curses.COLOR_WHITE,   curses.COLOR_BLACK )
        curses.init_pair( 8, curses.COLOR_BLACK,   curses.COLOR_BLACK )
        # underlined text
        curses.init_pair( 11, curses.COLOR_RED,     curses.COLOR_WHITE )
        curses.init_pair( 12, curses.COLOR_GREEN,   curses.COLOR_WHITE )
        curses.init_pair( 13, curses.COLOR_YELLOW,  curses.COLOR_WHITE )
        curses.init_pair( 14, curses.COLOR_BLUE,    curses.COLOR_WHITE )
        curses.init_pair( 15, curses.COLOR_MAGENTA, curses.COLOR_WHITE )
        curses.init_pair( 16, curses.COLOR_CYAN,    curses.COLOR_WHITE )
        curses.init_pair( 17, curses.COLOR_WHITE,   curses.COLOR_WHITE )
        curses.init_pair( 18, curses.COLOR_BLACK,   curses.COLOR_WHITE )
    # activate keypad mode
    #screen.keypad( True )

def deinitscr( screen ):
    """
    De-initialize terminal screen
    """
    # disable all
    screen.keypad( False )
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def main( screen ):
    """
    Main function
    """
    # get craplog's path
    crappath = abspath(__file__)
    crappath = crappath[:crappath.rfind('/')]
    crappath = crappath[:crappath.rfind('/')]
    crapview = Window( screen, crappath )
    crapview.run()



# RUN CRAPLOG
if __name__ == "__main__":
    # init screen
    screen = curses.initscr()
    initscr( screen )
    
    curses.wrapper( main ) # 2 TEST
    try:
        #curses.wrapper( main ) # <-- REAL
        print("SUCCESSFUL")
    except (KeyboardInterrupt):
        print("INTERRUPTED")
    except:
        print("FAILED")
    finally:
        print("EXITING")
        import time
        time.sleep(3)
        deinitscr( screen )
