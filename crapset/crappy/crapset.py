
from time import sleep

from craplib.utils import checkFile, checkFolder
from crappy.model  import ModelSet


class SetSet(ModelSet):
    """
    Crapset's configurations holder
    """
    def __init__(self, supercrap:object ):
        """ Initialize the configurations holder """
        self.confpath = supercrap.confpath
        self.file_path = "%s/crapset.crapconf" %(self.confpath)
        
        self.sets_map = {
            'configs'   : True,
            'arguments' : True,
            'less output' : False,
            'more output' : False,
            'colors'      : True
        }
        self.sets_list = [k for k in self.sets_map.keys()]
        
        self.unsaved_changes = False
        
        self.settable_choices = []
        self.disabled_choices = ['set','assign']
        
        self.readConfigs( supercrap )
        
        self.space = ""
        self.morespace = ""
        if supercrap.less_output is False:
            self.space = "\n"
            if supercrap.more_output is True:
                self.morespace = "\n"
        self.TXT_crap = supercrap.TXT_crapset
        self.MSG_choices = """%s{cyan}Available choices{default}%s
  {grey}[{paradise}examples{grey}]{default}  {italic}show an example on how to use{default}
    {grey}[{paradise}h{white}/{paradise}help{grey}]{default}  {italic}view this help message{default}
    {grey}[{paradise}q{white}/{paradise}quit{grey}]{default}  {italic}quit Crapset{default}
    {grey}[{paradise}b{white}/{paradise}back{grey}]{default}  {italic}back to the previous menu{default}
    {grey}[{paradise}s{white}/{paradise}save{grey}]{default}  {italic}save the changes to the configurations{default}%s
          {grey}[{paradise}show{white}/{paradise}view{grey}]{default}  {italic}show the actual configurations{default}
         {grey}[{paradise}use{white}/{paradise}enable{grey}]{default}  {italic}enable an option{default}
  {grey}[{paradise}don't use{white}/{paradise}disable{grey}]{default}  {italic}disable an option{default}\
""".format(**supercrap.text_colors)\
   %(self.space,self.morespace,self.space)
        self.MSG_options = """%s{cyan}Available options{default}%s
      {grey}[{paradise}configs{grey}]{default}  {italic}allow using the configurations file{default}
    {grey}[{paradise}arguments{grey}]{default}  {italic}allow using command line arguments{default}
  {grey}[{paradise}less output{grey}]{default}  {italic}reduce the output on screen{default}
  {grey}[{paradise}more output{grey}]{default}  {italic}increase the output on screen{default}
       {grey}[{paradise}colors{grey}]{default}  {italic}allow applying colors to the output{default}%s\
""".format(**supercrap.text_colors)\
   %(self.space,self.morespace,self.space)
        self.MSG_examples = """%s{cyan}Examples{default}%s
  {italic}Enable printing more output on screen{default}%s\n{bold}    : use more output{default}%s
  {italic}Disable using colors and enable using less output at once{default}\n%s{bold}    : don't use colors and use less_output{default}%s\
""".format(**supercrap.text_colors)\
   %(self.space,self.morespace,self.morespace,self.morespace,self.morespace,self.space)
    
    
    
    def readConfigs(self, supercrap:object ):
        """ Read the configuration file """
        if not checkFolder( supercrap, "crapconf", self.confpath ):
            exit()
        if not checkFile( supercrap, "crapset", self.file_path, create=False ):
            exit()
        try:
            with open(self.file_path,'r') as f:
                tmp = f.read().strip().split('\n')
        except:
            # failed to read
            print("\n{err}Error{white}[{grey}crapset{white}]{red}>{default} failed to read configuration file: {rose}%s{default}"\
                .format(**supercrap.text_colors)\
                %( self.file_path ))
            if supercrap.more_output is True:
                print("               the error is most-likely caused by a lack of permissions")
                print("               please add read/write permissions to the whole crapconf folder and retry")
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
        if len(configs) != 5:
            print("\n{err}Error{white}[{grey}crapset.crapconf{white}]{red}>{default} invalid number of lines: {rose}%s{default}"\
                .format(**supercrap.text_colors)\
                %( len(configs) ))
            if supercrap.less_output is False:
                print("""
                         if you have manually edited the configurations file, please un-do the changes
                         else, please report this issue""")
            print("\n{err}CRAPSET ABORTED{default}\n"\
                .format(**supercrap.text_colors))
            exit()
        
        # apply the configs
        self.sets_map['configs'] = bool(int(configs[0]))
        self.sets_map['arguments'] = bool(int(configs[1]))
        self.sets_map['less output'] = bool(int(configs[2]))
        self.sets_map['more output'] = bool(int(configs[3]))
        self.sets_map['colors'] = bool(int(configs[4]))
    
    
    
    def writeConfigs(self, supercrap:object ):
        """ Write the configuration file """
        result = True
        result = self.checkIntegrity( supercrap )
        if result is True:
            result = checkFolder( supercrap, "crapconf", self.confpath )
        if result is True:
            result = checkFile( supercrap, "crapset", self.file_path )
        
        if result is True:
            configs = ""
            configs += "%s\n" %(int(self.sets_map['configs']))
            configs += "%s\n" %(int(self.sets_map['arguments']))
            configs += "%s\n" %(int(self.sets_map['less output']))
            configs += "%s\n" %(int(self.sets_map['more output']))
            configs += "%s\n" %(int(self.sets_map['colors']))
            
            try:
                with open(self.file_path,'w') as f:
                    f.write( configs )
                    if supercrap.more_output is True:
                        print("\n{ok}Succesfully written configurations for {bold}CRAP{white}SET{default}\n"\
                            .format(**supercrap.text_colors)\
                            %( self.file_path ))
            except:
                # failed to write
                result = False
                print("\n{warn}Warning{white}[{grey}crapset{white}]{red}>{default} failed to write configuration file: {rose}%s{default}\n"\
                    .format(**supercrap.text_colors)\
                    %( self.file_path ))
                if supercrap.less_output is False:
                    print("               the error is most-likely caused by a lack of permissions")
                    print("               please add read/write permissions to the whole crapconf folder and retry")
                print()
        
        if result is True:
            self.unsaved_changes = False
    
    
    
    def checkIntegrity(self, supercrap:object ) -> bool :
        """ Check the integrity of the configuration """
        checks_passed = True
        if  self.sets_map['less_output'] is True\
        and self.sets_map['more_output'] is True:
            checks_passed = False
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}crapset{white}]{red}>{default} both {cyan}less{default} and {cyan}more{default} output modes are {rose}enabled{default}"\
                .format(**supercrap.text_colors))
            if supercrap.more_output is True:
                print("                 you can't print less and more output at the same time")
            print()
        return checks_passed
    
