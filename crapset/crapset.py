
from sys import argv
from time import sleep
from os.path import abspath

from crappy import aux
from crappy.crapup import UpSet
from crappy.crapset import SetSet
from crappy.craplog import LogSet
from crappy.crapview import ViewSet


class Crapset():
    def __init__(self, args:list ):
        """ Initialize Crapset """
        # get the path to the configuration files
        crappath = abspath(__file__)
        crappath = crappath[:crappath.rfind('/')]
        self.confpath = "%s/crapconf" %(crappath[:crappath.rfind('/')])
        self.file_path = "%s/crapset.crapconf" %(self.confpath)
        #
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
        #                 END OF THE EDITABLE SECTION
        ################################################################
        #
        #
        # DO NOT MODIFY THE FOLLOWING CONTENT
        #
        # initialize text messages
        self.initMessages()
        # read configs if not unset
        if self.use_configs is True:
            self.readConfigs()
        # parse arguments if not unset
        if self.use_arguments is True:
            self.parseArguments( args )
        # load the objects
        self.upset = UpSet( self )
        self.setset = SetSet( self )
        self.logset = LogSet( self )
        self.viewset = ViewSet( self )
        # read the configurations
        self.upset.readConfigs( self )
        self.setset.readConfigs( self )
        self.logset.readConfigs( self )
        self.viewset.readConfigs( self )


    def readConfigs(self):
        """
        Read the saved configuration
        """
        with open(self.file_path,'r') as f:
            tmp = f.read().strip().split('\n')
        configs = []
        for f in tmp:
            f = f.strip()
            if f == ""\
            or f[0] == "#":
                continue
            configs.append(f)
        # check the length
        if len(configs) != 5:
            print("\n{err}Error{white}[{grey}crapset.crapconf{white}]{red}>{default} invalid number of lines: {rose}%s{default}"\
                .format(**self.text_colors)\
                %( len(configs) ))
            if self.less_output is False:
                print("""
                         if you have manually edited the configurations file, please un-do the changes
                         else, please report this issue""")
            print("\n{err}CRAPSET ABORTED{default}\n"\
                .format(**self.text_colors))
            exit()
        # apply the configs
        self.use_configs = bool(int(configs[0]))
        if self.use_configs is True:
            self.use_arguments: bool(int(configs[1]))
            self.less_output: bool(int(configs[2]))
            self.more_output: bool(int(configs[3]))
            self.use_colors:  bool(int(configs[4]))
            self.initMessages()
    
    
    def parseArguments(self, args:list ):
        """ Initialize Crapset """
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
                print("\n%s\n\nHelp can be found using {cyan}h{default} {italic}or{default} {cyan}help{default} while running Crapset\n"\
                    .format(**self.text_colors)\
                    %( self.MSG_craplogo ))
                exit()
            elif arg == "--examples":
                print("\n%s\n\nHelp can be found using {cyan}h{default} {italic}or{default} {cyan}help{default} while running Crapset\n"\
                    .format(**self.text_colors)\
                    %( self.MSG_craplogo ))
                exit()
            # auxiliary arguments
            elif arg in ["-l", "--less"]:
                self.less_output = True
            elif arg in ["-m", "--more"]:
                self.more_output = True
            elif arg == "--no-colors":
                self.use_colors = False
                self.initMessages()
            else:
                print("{err}Error{white}[{grey}argument{white}]{red}>{default} not an available option: {rose}%s{default}"\
                    .format(**self.text_colors)\
                    %(arg))
                exit("")
    
    
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
        self.MSG_craplogo = aux.craplogo()
        self.MSG_crapset  = aux.crapup( self.text_colors )
        self.MSG_fin      = aux.fin( self.text_colors )
        self.TXT_fin      = "{orange}F{grass}I{cyan}N{default}".format(**self.text_colors)
        self.TXT_crapset  = "{red}c{orange}r{grass}a{cyan}p{white}SET{default}".format(**self.text_colors)
        self.TXT_crapup   = "{red}c{orange}r{grass}a{cyan}p{white}UP{default}".format(**self.text_colors)
        self.TXT_craplog  = "{red}c{orange}r{grass}a{cyan}p{white}LOG{default}".format(**self.text_colors)
        self.TXT_crapview = "{red}c{orange}r{grass}a{cyan}p{white}VIEW{default}".format(**self.text_colors)


    def welcomeMessage(self):
        """
        Print the welcome message
        """
        if self.less_output is False:
            print("\n%s\n" %( self.MSG_crapset ))
            sleep(1)
        else:
            print("{bold}%s"\
                .format(**self.text_colors)\
                %( self.TXT_crapset ))


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
    
    
    def printWarning(self, err_key:str, message:str ):
        """
        Print a warning message
        """
        if self.less_output is False:
            print()
        print("{warn}Warning{white}[{grey}%s{white}]{red}>{default} %s{default}"\
            .format(**self.text_colors)\
            %( err_key, message ))
    
    
    def printError(self, err_key:str, message:str ):
        """
        Print an error message
        """
        if self.less_output is False:
            print()
        print("{err}Error{white}[{grey}%s{white}]{red}>{default} %s{default}"\
            .format(**self.text_colors)\
            %( err_key, message ))
    
    
    def exitAborted(self):
        """
        Print the abortion message and exit
        """
        print("{err}CRAPSET ABORTED{default}"\
            .format(**self.text_colors))
        if self.less_output is False:
            print()
        exit()
    
    
    def saveConfigs(self):
        """
        Save all the changes to all the tools
        """
        # crapup
        if self.upset.unsaved_changes is True:
            self.upset.writeConfigs( self )
        # crapset
        if self.setset.unsaved_changes is True:
            self.setset.writeConfigs( self )
        # craploh
        if self.logset.unsaved_changes is True:
            self.logset.writeConfigs( self )
        # crapview
        if self.viewset.unsaved_changes is True:
            self.viewset.writeConfigs( self )
    
    
    def checkUnsavedChanges(self):
        """
        Check if there is any unsaved modification before to quit
        """
        unsaved = []
        if self.upset.unsaved_changes is True:
            unsaved.append("crapup")
        if self.setset.unsaved_changes is True:
            unsaved.append("crapset")
        if self.logset.unsaved_changes is True:
            unsaved.append("craplog")
        if self.viewset.unsaved_changes is True:
            unsaved.append("crapview")
        if len(unsaved) > 0:
            while True:
                self.printWarning("unsaved","{yellow}There are unsaved modifications to:{default}"\
                    .format(**self.text_colors))
                if self.more_output is True:
                    print()
                space = "\n "
                if self.less_output is True:
                    space = ""
                else:
                    print(" ",end="")
                for tool in unsaved:
                    print(" {rose}%s{default}%s"\
                        .format(**self.text_colors)\
                        %( tool, space ), end="", flush=True)
                if self.more_output is True:
                    sleep(0.5)
                if self.less_output is False:
                    print()
                choice = input("What do you want to do? {white}[{green}save{grey}/{rose}quit{white}] :{default} "\
                    .format(**self.text_colors)).strip().lower()
                if choice in ["q","quit","exit"]:
                    break
                elif choice in ["s","save","w","write"]:
                    self.saveConfigs()
                    break
                else:
                    # leave this normal yellow, it's secondary and doesn't need real attention
                    if self.less_output is False:
                        print()
                    print("{yellow}Warning{white}[{grey}choice{white}]{yellow}>{default} not a valid choice: {bold}%s{default}"\
                        .format(**self.text_colors)\
                        %(choice))
                    if self.less_output is False:
                        print()
                        sleep(1)
            
    
    
    def main(self):
        """
        Run Crapset
        """
        space = ""
        morespace = ""
        if self.less_output is False:
            space = "\n"
            if self.more_output is True:
                morespace = "\n"
        loop = True
        redirect = None
        while loop is True:
            if redirect is not None:
                user_input = redirect
                redirect = None
            else:
                space = ""
                if self.less_output is False:
                    print("{grey}(Enter {white}help{default}{grey} to view a help message){default}"\
                        .format(**self.text_colors))
                    space = "\n"
                user_input = input("{bold}Which {cyan}tool{default}{bold} do you want to configure{default}?%s {paradise}:{default} "\
                    .format(**self.text_colors)%(space)).lower().strip()
            if user_input.startswith('-'):
                self.printWarning("input","dashes {grey}[{default}{bold}-{default}{grey}]{default} are not required"\
                    .format(**self.text_colors))
                if self.more_output is True:
                    print("                honestly, you better totally avoid them here")
                if self.less_output is False:
                    print()
            elif user_input in ["q","quit","exit","bye"]:
                loop = False
            elif user_input in ["s","w","save","write"]:
                self.saveConfigs()
            
            elif user_input in ["h","help","help me","show help"]:
                print("""%s{cyan}Available choices{default}%s
  {grey}[{paradise}h{white}/{paradise}help{grey}]{default}  {italic}view this help message{default}
  {grey}[{paradise}q{white}/{paradise}quit{grey}]{default}  {italic}quit Crapset{default}
  {grey}[{paradise}s{white}/{paradise}save{grey}]{default}  {italic}save the changes to all of the configurations{default}%s
   {grey}[{paradise}craplog{grey}]{default}  {italic}edit Craplog's configuration file{default}
  {grey}[{paradise}crapview{grey}]{default}  {italic}edit Crapview's configuration file{default}
   {grey}[{paradise}crapset{grey}]{default}  {italic}edit Crapset's configuration file{default}
    {grey}[{paradise}crapup{grey}]{default}  {italic}edit Crapup's configuration file{default}%s\
""".format(**self.text_colors) %( space,morespace,space,space ))

            elif user_input in ["e","ex","eg","example","examples","show example","show examples"]:
                print("""%s{cyan}Examples{default}%s
  {italic}Save any the modification to any of the tools{default}%s\n{bold}    : save{default}%s
  {italic}Start editing Craplog's configurations{default}%s\n{bold}    : craplog{default}%s\
""".format(**self.text_colors) %(space,morespace,morespace,morespace,morespace,space))
            
            elif user_input in ["log","craplog"]:
                if self.less_output is False:
                    print()
                loop, redirect = self.logset.run( self )
            
            elif user_input in ["view","crapview"]:
                if self.less_output is False:
                    print()
                loop, redirect = self.viewset.run( self )
            
            elif user_input in ["set","crapset"]:
                if self.less_output is False:
                    print()
                loop, redirect = self.setset.run( self )
            
            elif user_input in ["up","crapup"]:
                if self.less_output is False:
                    print()
                loop, redirect = self.upset.run( self )
            
            else:
                # leave this normal yellow, it's secondary and doesn't need real attention
                if self.less_output is False:
                    print()
                print("{yellow}Warning{white}[{grey}choice{white}]{yellow}>{default} not a valid choice: {bold}%s{default}"\
                    .format(**self.text_colors)\
                    %( user_input ))
                if self.less_output is False:
                    print()
                    sleep(1)
    



if __name__ == "__main__":
    failed = False
    crapset = Crapset( argv )
    
    crapset.welcomeMessage()
    crapset.main()
    try:
        pass
        #crapset.welcomeMessage()
        #crapset.main()
        #crapset.exitMessage()
    except (KeyboardInterrupt):
        failed = True
        crapset.printError("failed","{yellow}keyboard interruption".format(**crapset.text_colors))
    except:
        failed = True
        crapset.printError("failed","{rose}an error occured".format(**crapset.text_colors))
    finally:
        if failed is True:
            # failing succesfully
            crapset.exitAborted()
        crapset.checkUnsavedChanges()
        crapset.exitMessage()
        del crapset
