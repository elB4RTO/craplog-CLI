
from random import choice, shuffle
from crappy.check import checkFile, checkFolder


class ViewSet():
    def __init__(self, confpath:str ):
        self.use_configs   = True
        self.use_arguments = True
        self.use_colors    = True
        
        self.confpath = confpath
        self.file_path = "%s/crapview.conf" %(confpath)
        
    
    def readConfigs(self, supercrap:object ):
        """ Read the configuration file """
        if not checkFolder( supercrap, "crapconf", self.confpath )
            exit()
        if not checkFile( supercrap, "crapview", self.file_path, create=False ):
            exit()
        try:
            with open(self.file_path,'r') as f:
                tmp = f.read().strip().split('\n')
        except:
            # failed to read
            print("\n{err}Error{white}[{grey}crapview{white}]{red}>{default} failed to read configuration file: {rose}%s{default}\n"\
                .format(**supercrap.text_colors)\
                %( self.file_path ))
            if supercrap.less_output is False:
                print("                the error is most-likely caused by a lack of permissions")
                print("                please add read/write permissions to the whole crapconf folder and retry")
            print()
            exit()
        
        configs = []
        for f in tmp:
            f = f.strip()
            if f == ""\
            or f[0] == "#":
                continue
            configs.append(f)
        # check the length
        if len(configs) != 3:
            print("\n{err}Error{white}[{grey}crapview.conf{white}]{red}>{default} invalid number of lines: {rose}%s{default}"\
                .format(**supercrap.text_colors)\
                %( len(configs) ))
            print("""
                      if you have manually edited the configurations file, please un-do the changes
                      else, please report this issue""")
            print("\n{err}CRAPSET ABORTED{default}\n"\
                .format(**supercrap.text_colors))
            exit()

        # apply the configs
        self.use_configs = bool(int(configs[0]))
        self.use_arguments = bool(int(configs[1]))
        self.use_colors = bool(int(configs[2]))
    
    
    
    def writeConfigs(self, supercrap:object ):
        """ Write the configuration file """
        result = True
        result = self.checkIntegrity( supercrap )
        if result is True:
            result = checkFolder( supercrap, "crapconf", self.confpath )
        if result is True:
            result = checkFile( supercrap, "crapview", self.file_path ):
        
        if result is True:
            configs = ""
            configs += "%s\n" %(int(self.use_configs))
            configs += "%s\n" %(int(self.use_arguments))
            configs += "%s\n" %(int(self.use_colors))
            
            try;
                with open(self.file_path,'w') as f:
                    f.write( configs )
                    if supercrap.more_output is True:
                        print("\n{ok}Succesfully written configurations for {bold}CRAP{white}VIEW{default}\n"\
                            .format(**supercrap.text_colors)\
                            %( self.file_path ))
            except:
                # failed to read
                result = False
                print("\n{warn}Warning{white}[{grey}crapview{white}]{red}>{default} failed to write configuration file: {rose}%s{default}"\
                    .format(**supercrap.text_colors)\
                    %( self.file_path ))
                if supercrap.less_output is False:
                    print("                 the error is most-likely caused by a lack of permissions")
                    print("                 please add read/write permissions to the whole crapconf folder and retry")
                print()
        
        if result is True:
            supercrap.viewset_changed = False
    
    
    
    def checkIntegrity(self, supercrap:object, crapview:object ) -> bool :
        """ Check the integrity of the configuration """
        return True
    
    
    
    def run(self, supercrap:object ) ->  tuple :
        """
        Run the configuration process
        """
        def phrase( string:str ) -> list :
            phrase = []
            for word in string.split(' '):
                word = word.strip()
                if word != "":
                    phrase.append( word )
            return phrase
        
        redirect = None
        quit_crapset = False
        loop = True
        while loop is True:
            if supercrap.more_output is False:
                print("{grey}(Enter {white}help{default}{grey} to view a help message)"\
                    .format(**supercrap.text_colors))
            user_input = input("{bold}What to edit about %s? {paradise}:{default} "\
                .format(**supercrap.text_colors)\
                %( supercrap.TXT_crapview )).lower().strip()
            if user_input.startswith('-'):
                supercrap.printWarning("input","dashes {grey}[{default}{bold}-{default}{grey}]{default} are not required"\
                    .format(**supercrap.text_colors))
                if supercrap.more_output is True:
                    print("                honestly, you better totally avoid them here")
                if supercrap.less_output is False:
                    print()
                continue
            elif user_input in ["q","quit","exit","bye"]:
                loop = False
                quit_crapset = True
                continue
            elif user_input in ["b","back","main"]:
                loop = False
                continue
            elif user_input in ["h","help","help me"]:
                space = ""
                if supercrap.less_output is False:
                    print()
                    space = "\n"
                print("""Available choices
  {grey}[{paradise}example{grey}]{default}  {italic}show an example on how to use{default}
  {grey}[{paradise}h{grey}/{white}help{grey}]{default}   {italic}view this help message{default}
  {grey}[{paradise}q{grey}/{white}quit{grey}]{default}   {italic}quit Crapset{default}
  {grey}[{paradise}b{grey}/{white}back{grey}]{default}   {italic}back to the previous menu{default}
  {grey}[{paradise}s{grey}/{white}save{grey}]{default}   {italic}save the changes to the configurations{default}%s
  {grey}[{paradise}show{grey}]{default}  {italic}show the actual configurations{default}%s
  {grey}[{paradise}use{grey}/{white}enable{grey}]{default}         {italic}enable an option{default}
  {grey}[{paradise}don't use{grey}/{white}disable{grey}]{default}  {italic}disable an option{default}\
""".format(**supercrap.text_colors) %( space,space ))
                if supercrap.less_output is False:
                    print()
                print("""Available options
  {grey}[{paradise}configs{grey}]{default}      {italic}allow using the configurations file{default}
  {grey}[{paradise}arguments{grey}]{default}    {italic}allow using command line arguments{default}
  {grey}[{paradise}colors{grey}]{default}       {italic}allow applying colors to the output{default}\
""".format(**supercrap.text_colors))
                if supercrap.less_output is False:
                    print()
                continue
            
            elif user_input.startswith("go"):
                # process a redirection
                if user_input.startswith("go fuck yourself"):
                    # smile, that's a joke ;)
                    msg = ["ok"]*80+["... thanks, you're so nice"]*19+["go fuck YOURself"]
                    msg.shuffle()
                    print("{bold}%s{default}".format(**supercrap.text_colors)%( choice(msg) ))
                    if msg == "go fuck YOURself":
                        exit() # LOL
                    sleep(choice([1,2,3,4,5,6,7,8,9])*choice([1,2]))
                    continue
                phrase = phrase( user_input )
                i = 1
                if phrase[i] in ["to","2"]:
                    i += 1
                if phrase[i] in ["b","back","main"]:
                    loop = False
                    continue
                elif phrase[i] in ["log","craplog"]:
                    loop = False
                    redirect = "log"
                    continue
                elif phrase[i] in ["view","crapview"]:
                    loop = False
                    redirect = "view"
                    continue
                elif phrase[i] in ["set","crapset"]:
                    loop = False
                    redirect = "set"
                    continue
                elif phrase[i] in ["up","crapup"]:
                    loop = False
                    redirect = "up"
                    continue
                else:
                    supercrap.printWarning("redirection","not a valid destination: {rose}%s{default}"\
                        .format(**supercrap.text_colors))
            
            
            elif user_input.startswith("show"):
                # process
                phrase = phrase( user_input )
                i = 1
            
            
            else:
                # leave this normal yellow, it's secondary and doesn't need real attention
                print("\n{yellow}Warning{white}[{grey}choice{white}]{yellow}>{default} not a valid choice: {bold}%s{default}"\
                    .format(**supercrap.text_colors))
                if supercrap.less_output is False:
                    print()
                    sleep(1)
                continue
        
        return (quit_crapset, redirect)
    
