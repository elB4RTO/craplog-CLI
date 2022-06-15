
from sys import argv
from time import sleep

from crappy import aux
form crappy.crapup import UpSet
form crappy.craplog import LogSet
form crappy.craplview import ViewSet


class Crapset():
    def __init__(self, args:list ):
        """ Initialize Crapset """
        # get the path to the configuration files
        crappath = abspath(__file__)
        crappath = crappath[:crappath.rfind('/')]
        self.confpath = "%s/crapconf" %(crappath[:crappath.rfind('/')])
        self.file_path = "%s/crapset.conf" %(confpath)
        # initialize crapset's variables
        self.use_configs   = True
        self.use_arguments = True
        self.less_output   = False
        self.more_output   = False
        self.use_colors    = True
        # True when something have been changed
        self.upset_changed   = False
        self.setset_changed  = False
        self.logset_changed  = False
        self.viewset_changed = False
        # initialize text messages
        self.initMessages()
        # read configs if not unset
        if self.use_configs is True:
            self.readConfigs()
        # parse arguments if not unset
        if self.use_arguments is True:
            self.parseArguments( args )
        # load the objects
        self.upset = UpSet()
        self.setset = SetSet()
        self.logset = LogSet()
        self.viewset = ViewSet()
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
            print("\n{err}Error{white}[{grey}crapset.conf{white}]{red}>{default} invalid number of lines: {rose}%s{default}"\
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
            elif arg == "-elbarto-":
                print("\n%s\n" %( self.MSG_elbarto ))
                exit()
            # help
            elif arg in ["help", "-h", "--help"]:
                print("\n%s\nHelp can be found using {cyan}h{default} {italic}or{default} {cyan}help{default} while running Crapset\n"\
                    .format(**self.text_colors)\
                    %( self.MSG_craplogo ))
                exit()
            elif arg == "--examples":
                print("\n%s\nHelp can be found using {cyan}h{default} {italic}or{default} {cyan}help{default} while running Crapset\n"\
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
        self.MSG_help     = aux.help( self.text_colors )
        self.MSG_examples = aux.examples( self.text_colors )
        self.MSG_craplogo = aux.craplogo()
        self.MSG_crapset  = aux.crapup( self.text_colors )
        self.MSG_fin      = aux.fin( self.text_colors )
        self.TXT_fin      = "{orange}F{grass}I{cyan}N{default}".format(**self.text_colors)
        self.TXT_crapset  = "{red}c{orange}r{grass}a{cyan}p{white}SET{default}".format(**self.text_colors)
        self.TXT_crapup   = "{red}c{orange}r{grass}a{cyan}p{white}UP{default}".format(**self.text_colors)
        self.TXT_craplog  = "{red}C{orange}R{grass}A{cyan}P{white}LOG{default}".format(**self.text_colors)
        self.TXT_crapview = "{red}C{orange}R{grass}A{cyan}P{white}VIEW{default}".format(**self.text_colors)


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
        print("\n{warn}Warning{white}[{grey}%s{white}]{red}>{default} %s{default}"\
            .format(**self.text_colors)\
            %( err_key, message ))
    
    
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
        if self.upset_changed is True:
            self.upset.writeConfigs( self )
    
    
    def main(self):
        """
        Run Crapset
        """
        loop = True
        redirect = None
        while loop is True:
            if redirect is not None:
                user_input = redirect
                redirect = None
            else:
                if self.less_output is False:
                    print("{grey}(Enter {white}help{default}{grey} to view a help message)"\
                        .format(**self.text_colors))
                user_input = input("{bold}Which {cyan}tool{default}{bold} do you want to configure{default}? {paradise}:{default} "\
                    .format(**self.text_colors)).lower().strip()
            if user_input.startswith('-'):
                self.printWarning("input","dashes {grey}[{default}{bold}-{default}{grey}]{default} are not required"\
                    .format(**self.text_colors))
                if self.more_output is True:
                    print("                honestly, you better totally avoid them here")
                if self.less_output is False:
                    print()
            elif user_input in ["q","quit","exit","bye"]:
                loop = False
            elif user_input in ["h","help","help me"]:
                if self.less_output is False:
                    print()
                print("""Available choices
  {grey}[{paradise}h{grey}/{white}help{grey}]{default}    {italic}view this help message{default}
  {grey}[{paradise}q{grey}/{white}quit{grey}]{default}    {italic}quit Crapset{default}
  {grey}[{paradise}s{grey}/{white}save{grey}]{default}    {italic}save the changes to all of the configurations{default}
  
  {grey}[{paradise}craplog{grey}]{default}   {italic}edit Craplog's configuration file{default}
  {grey}[{paradise}crapview{grey}]{default}  {italic}edit Crapview's configuration file{default}
  {grey}[{paradise}crapset{grey}]{default}   {italic}edit Crapset's configuration file{default}
  {grey}[{paradise}crapup{grey}]{default}    {italic}edit Crapup's configuration file{default}\
""".format(**self.text_colors))
            
            elif user_input in ["s","save"]:
                self.saveConfigs()
            
            elif user_input in ["log","craplog"]:
                loop, redirect = self.logset.run( self )
            
            elif user_input in ["view","crapview"]:
                loop, redirect = self.viewset.run( self )
            
            elif user_input in ["set","crapset"]:
                loop, redirect = self.setset.run( self )
            
            elif user_input in ["up","crapup"]:
                loop, redirect = self.upset.run( self )
            
            else:
                # leave this normal yellow, it's secondary and doesn't need real attention
                print("\n{yellow}Warning{white}[{grey}choice{white}]{yellow}>{default} not a valid choice: {bold}%s{default}"\
                    .format(**self.text_colors))
                if self.less_output is False:
                    print()
                    sleep(1)
        



if __name__ == "__main__":
    failed = False
    crapset = Crapset( argv )
    try:
        crapset.welcomeMessage()
        crapset.main()
        crapset.exitMessage()
    except (KeyboardInterrupt):
        failed = True
    except:
        failed = True
    finally:
        del crapset
