
from sys import argv
from time import sleep
from os.path import abspath

from crappy import aux
from crappy.git import gitPull
from crappy.get import versionCheck


class Crapup():
    def __init__(self, args:list ):
        # declare variables
        self.use_configs:   bool
        self.use_arguments: bool
        self.less_output: bool
        self.more_output: bool
        self.use_colors:  bool
        self.use_git: bool
        # paths
        self.crappath: str
        # messages
        self.text_colors:  dict
        self.MSG_elbarto:  str
        self.MSG_craplogo: str
        self.MSG_help:     str
        self.MSG_examples: str
        self.MSG_crapup:   str
        self.MSG_fin:      str
        self.TXT_crapup:   str
        self.TXT_fin:      str
        self.TXT_craplog:  str
        
        # get Craplog's main path
        crappath = abspath(__file__)
        crappath = crappath[:crappath.rfind('/')]
        self.statpath = "%s/crapstats" %(crappath[:crappath.rfind('/')])
        # initialize variables
        self.initVariables()
        self.initMessages()
        # read configs if not unset
        if self.use_configs is True:
            self.readConfigs()
        # parse arguments if not unset
        if self.use_arguments is True:
            self.parseArguments( args )
    
    
    def initVariables(self):
        """
        Initialize Crapup's variables
        This section can be manually edited to pre-set Crapup
          and avoid having to pass arguments every time
        """
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
        self.use_configs = True
        #
        # USE COMMAND LINE ARGUMENTS
        # [  ]
        # IF SET TO 'False' MEANS THAT EVERY ARGUMENT WILL BE IGNORED
        self.use_arguments = True
        #
        # REDUCE THE OUTPUT ON SCREEN
        # [ -l  /  --less ]
        self.less_output = False
        #
        # PRINT MORE INFORMATIONS ON SCREEN
        # [ -m  /  --more ]
        self.more_output = False
        #
        # USE COLORS WHEN PRINTING TEXT ON SCREEN
        # CAN BE DISABLED PASSING [ --no-colors ]
        self.use_colors = True
        #
        # UPDATE CRAPLOG USING git pull
        # [ --git ]
        # IF THE git IS NOT INITIALIZED YET, ASKS TO INITIALIZE ONE
        self.use_git = False
        #
        #                 END OF THE EDITABLE SECTION
        ################################################################
        #
        #
        # DO NOT MODIFY THE FOLLOWING VARIABLES
        #
        self.version = 3.07
        self.repo = "https://github.com/elB4RTO/craplog-CLI"
        self.crappath = ""
        self.MSG_elbarto = self.MSG_craplogo =\
        self.MSG_help = self.MSG_examples =\
        self.MSG_crapup = self.MSG_fin =\
        self.TXT_crapup = self.TXT_fin =\
        self.TXT_craplog = ""


    def readConfigs(self):
        """
        Read the saved configuration
        """
        crappath = abspath(__file__)
        crappath = crappath[:crappath.rfind('/')]
        self.crappath = crappath[:crappath.rfind('/')]
        path = "%s/crapconf/crapup.crapconf" %(self.crappath)
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
        if len(configs) != 6:
            print("\n{err}Error{white}[{grey}configs{white}]{red}>{default} invalid number of lines: {rose}%s{default}"\
                .format(**self.text_colors)\
                %( len(configs) ))
            if self.less_output is False:
                print("""
                if you have manually edited the configurations file, please un-do the changes
                else, please report this issue""")
            print("\n{err}CRAPUP ABORTED{default}\n"\
                .format(**self.text_colors))
            exit()
        # apply the configs
        self.use_configs = bool(int(configs[0]))
        if self.use_configs is True:
            self.use_arguments = bool(int(configs[1]))
            self.less_output   = bool(int(configs[2]))
            self.more_output   = bool(int(configs[3]))
            self.use_colors    = bool(int(configs[4]))
            self.use_git       = bool(int(configs[5]))
            self.initMessages()
    
    
    def initMessages(self):
        """
        Bring message strings
        """
        # set-up colors
        if self.use_colors is True:
            self.text_colors = aux.colors()
        else:
            self.text_colors = aux.no_colors()
        self.MSG_elbarto  = aux.elbarto()
        self.MSG_help     = aux.help( self.text_colors )
        self.MSG_examples = aux.examples( self.text_colors )
        self.MSG_craplogo = aux.craplogo()
        self.MSG_crapup   = aux.crapup( self.text_colors )
        self.MSG_fin      = aux.fin( self.text_colors )
        self.TXT_crapup   = "{red}c{orange}r{grass}a{cyan}p{white}UP{default}".format(**self.text_colors)
        self.TXT_fin      = "{orange}F{grass}I{cyan}N{default}".format(**self.text_colors)
        self.TXT_craplog  = "{red}C{orange}R{grass}A{cyan}P{white}LOG{default}".format(**self.text_colors)


    def parseArguments(self, args: list ):
        """
        Finalize Craplog's variables (if not manually unset)
        """
        n_args = len(args)-1
        i = 0
        while i < n_args:
            i += 1
            arg = args[i]
            if arg == "":
                continue
            # elB4RTO
            elif arg in ["elB4RTO","elbarto","-elbarto-"]:
                print("\n%s\n" %( self.MSG_elbarto ))
                exit()
            # help
            elif arg in ["help", "-h", "--help"]:
                print("\n%s\n\n%s\n\n%s\n" %( self.MSG_craplogo, self.MSG_help, self.MSG_examples ))
                exit()
            elif arg == "--examples":
                print("\n%s\n\n%s\n" %( self.MSG_craplogo, self.MSG_examples ))
                exit()
            # auxiliary arguments
            elif arg in ["-l", "--less"]:
                self.less_output = True
            elif arg in ["-m", "--more"]:
                self.more_output = True
            elif arg == "--no-colors":
                self.use_colors = False
                self.initMessages()
            # git argument
            elif arg == "--git":
                self.git_update = True
            else:
                print("{err}Error{white}[{grey}argument{white}]{red}>{default} not an available option: {rose}%s{default}"\
                    .format(**self.text_colors)\
                    %(arg))
                if self.more_output is True:
                    print("                 use {cyan}crapup --help{default} to view an help screen"\
                        .format(**self.text_colors))
                exit("")


    def welcomeMessage(self):
        """
        Print the welcome message
        """
        if self.less_output is False:
            print("\n%s\n" %( self.MSG_crapup ))
            sleep(1)
        else:
            print("{bold}%s"\
                .format(**self.text_colors)\
                %( self.TXT_crapup ))


    def exitMessage(self):
        """
        Print the exit message
        """
        if self.less_output is False:
            print("\n%s\n" %( self.MSG_fin ))
        else:
            print("{bold}%s"\
                .format(**self.text_colors)\
                %( self.TXT_fin ))
    
    
    def printError(self, err_key:str, message:str ):
        """
        Print an error message
        """
        print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} %s{default}"\
            .format(**self.text_colors)\
            %( err_key, message ))
    
    
    def exitAborted(self):
        """
        Print the abortion message and exit
        """
        print("{err}CRAPUP ABORTED{default}"\
            .format(**self.text_colors))
        if self.less_output is False:
            print()
        exit()


    def main(self):
        """
        Main function to call
        """
        # CRAPUP
        self.welcomeMessage()
        if self.use_git is True:
            # directly pull from the git
            gitPull( self )
        else:
            # just query the version number
            versionCheck( self )
        # everything went fine
        self.exitMessage()
    


if __name__ == "__main__":
    failed = False
    crapup = Crapup( argv )
    try:
        crapup.main()
    except (KeyboardInterrupt):
        failed = True
    except:
        failed = True
    finally:
        del crapup
