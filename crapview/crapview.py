
import curses

from sys import argv

from os.path import abspath

from crappy import aux
from crappy.window import Window


def initCrapview( args ) -> bool :
    ################################################################
    #                 START OF THE EDITABLE SECTION
    #
    # HIERARCHY FOR APPLYING SETTINGS:
    #  - HARDCODED VARIABLES (THESE)
    #  - CONFIGURATIONS FILE
    #  - COMMAND LINE ARGUMENTS
    # THE ELEMENTS ON TOP ARE REPLACED BY THE ONES WHICH FOLLOW THEM,
    # IF HARDCODED VARIABLES ARE SET TO DO SO
    #
    # READ THE CONFIGURATIONS FILE AND LOAD THE SETTING
    # [  ]
    # IF SET TO 'False' MEANS THAT THE SAVED CONFIGS WILL BE IGNORED
    use_configs = True
    #
    # USE COMMAND LINE ARGUMENTS
    # [  ]
    # IF SET TO 'False' MEANS THAT EVERY ARGUMENT WILL BE IGNORED
    use_arguments = True
    #
    # USE COLORS WHEN PRINTING TEXT ON SCREEN
    # CAN BE DISABLED PASSING [ --no-colors ]
    use_colors = True
    #
    #                 END OF THE EDITABLE SECTION
    ################################################################
    #
    # DO NOT MODIFY THE FOLLOWING VARIABLES
    #
    MSG_help = MSG_examples =\
    MSG_elbarto = MSG_craplogo = ""
    
    def initMessages():
        nonlocal use_colors, text_colors
        nonlocal MSG_elbarto, MSG_help, MSG_examples, MSG_craplogo
        MSG_elbarto = aux.elbarto()
        MSG_help = aux.help( text_colors )
        MSG_examples = aux.examples( text_colors )
        MSG_craplogo = aux.craplogo()
    
    if use_colors is True:
        text_colors = aux.colors()
    else:
        text_colors = aux.no_colors()
    initMessages()
    
    if use_configs is True:
        crappath = abspath(__file__)
        crappath = crappath[:crappath.rfind('/')]
        path = "%s/crapset/crapview.conf" %(crappath[:crappath.rfind('/')])
        with open(path,'r') as f:
            tmp = f.read().strip().split('\n')
        configs = []
        for f in tmp:
            f = f.strip()
            if f == ""\
            or f[0] == "#":
                continue
            configs.append(f)
        # check the length
        if len(configs) != 3:
            print("\n{err}Error{white}[{grey}configs{white}]{red}>{default} invalid number of lines: {rose}%s{default}"\
                .format(**text_colors)\
                %( len(configs) ))
            if self.less_output is False:
                print("""
                if you have manually edited the configurations file, please un-do the changes
                else, please report this issue""")
            print("\n{err}CRAPVIEW ABORTED{default}\n"\
                .format(**text_colors))
            exit()
        # apply the configs
        use_configs = bool(int(configs[0]))
        if use_configs is True:
            use_arguments = bool(int(configs[1]))
            use_colors = bool(int(configs[2]))
    
    if use_arguments is True:
        # parse args
        n_args = len(args)-1
        i = 0
        while i < n_args:
            i += 1
            arg = args[i]
            if arg == "":
                continue
            # elB4RTO
            elif arg == "-elbarto-":
                print("\n%s\n" %( MSG_elbarto ))
                exit()
            # help
            elif arg in ["help", "-h", "--help"]:
                print( "\n%s\n%s\n%s\n" %( MSG_craplogo, MSG_help, MSG_examples ))
                exit()
            # auxiliary arguments
            elif arg == "--no-colors":
                use_colors = False
                initMessages()
            else:
                print("""{err}Error{white}[{grey}argument{white}]{red}>{default} not an available option: {rose}%s{default}
             use {cyan}crapview --help{default} to view an help screen\n"""\
                    .format(**text_colors)\
                    %(arg))
                exit()
    return use_colors


def initCurses( screen, use_colors ):
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
        if use_colors is True:
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
        else:
            for i in range(1,9):
                curses.init_pair( i, curses.COLOR_WHITE, curses.COLOR_BLACK )
                curses.init_pair( i+10, curses.COLOR_WHITE, curses.COLOR_BLACK )
    # activate keypad mode
    #screen.keypad( True )

def deinitscr( screen ):
    """
    De-initialize terminal screen
    """
    # disable all
    #screen.keypad( False )
    curses.curs_set(1)
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
    failed = False
    use_colors = initCrapview( argv )
    # init screen
    screen = curses.initscr()
    try:
        initCurses( screen, use_colors )
        # run crapview
        curses.wrapper( main )
    except (KeyboardInterrupt):
        failed = True
    except:
        failed = True
    finally:
        deinitscr( screen )
