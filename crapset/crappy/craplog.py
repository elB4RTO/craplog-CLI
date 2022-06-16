
from time import sleep

from crappy.model import ModelSet
from crappy.check import checkFile, checkFolder


class LogSet(ModelSet):
    """
    Craplog's configurations holder
    """
    def __init__(self, supercrap:object ):
        """ Initialize the configurations holder """
        self.confpath = supercrap.confpath
        self.file_path = "%s/craplog.crapconf" %(self.confpath)
        
        self.sets_map = {
            'configs'   : True,
            'arguments' : True,
            
            'less output' : False,
            'more output' : False,
            'performance' : False,
            'colors'      : True,
            
            'auto delete'  : False,
            'auto merge'   : False,
            'warning size' : 100.0,
            
            'sessions'    : True,
            'globals'     : True,
            'access logs' : True,
            'error logs'  : False,
            
            'backup'     : False,
            'backup tar' : False,
            'backup zip' : False,
            
            'delete'     : False,
            'trash'      : False,
            'trash path' : "~/.local/share/Trash/files/",
            'shred'      : False,
            
            'logs path'      : "/var/log/apache2/",
            'log files'      : ["access.log.1"],
            'file selection' : False,
            'usage control'  : True,
            
            'access fields' : ["IP", "REQ", "RES", "UA"],
            'whitelist'     : ["::1"]
        }
        self.sets_list = [k for k in self.sets_map.keys()]
        
        self.unsaved_changes = False
        
        self.settable_choices = ['warning size','trash path','logs path','log files','access fields','whitelist']
        self.disabled_choices = []
        
        self.readConfigs( supercrap )
        
        self.space = ""
        self.morespace = ""
        if supercrap.less_output is False:
            self.space = "\n"
            if supercrap.more_output is True:
                self.morespace = "\n"
        self.TXT_crap = supercrap.TXT_craplog
        self.MSG_choices = """%s{cyan}Available choices{default}%s
  {grey}[{paradise}examples{grey}]{default}  {italic}show an example on how to use{default}
    {grey}[{paradise}h{white}/{paradise}help{grey}]{default}  {italic}view this help message{default}
    {grey}[{paradise}q{white}/{paradise}quit{grey}]{default}  {italic}quit Crapset{default}
    {grey}[{paradise}b{white}/{paradise}back{grey}]{default}  {italic}back to the previous menu{default}
    {grey}[{paradise}s{white}/{paradise}save{grey}]{default}  {italic}save the changes to the configurations{default}%s
          {grey}[{paradise}show{white}/{paradise}view{grey}]{default}  {italic}show the actual configurations{default}
         {grey}[{paradise}set{white}/{paradise}assing{grey}]{default}  {italic}assign the given values an option{default}
         {grey}[{paradise}use{white}/{paradise}enable{grey}]{default}  {italic}enable an option{default}
  {grey}[{paradise}don't use{white}/{paradise}disable{grey}]{default}  {italic}disable an option{default}\
""".format(**supercrap.text_colors)\
   %(self.space,self.morespace,self.space)
        self.MSG_options = """%s{cyan}Available options{default}%s
        {grey}[{paradise}configs{grey}]{default}  {italic}allow using the configurations file{default}
      {grey}[{paradise}arguments{grey}]{default}  {italic}allow using command line arguments{default}
    {grey}[{paradise}less output{grey}]{default}  {italic}reduce the output on screen{default}
    {grey}[{paradise}more output{grey}]{default}  {italic}increase the output on screen{default}
         {grey}[{paradise}colors{grey}]{default}  {italic}allow applying colors to the output{default}
    {grey}[{paradise}performance{grey}]{default}  {italic}print performance informations{default}
    {grey}[{paradise}auto delete{grey}]{default}  {italic}automatically choose to delete files{default}
     {grey}[{paradise}auto merge{grey}]{default}  {italic}automatically merge sessions having the same date{default}
   {grey}[{paradise}warning size{grey}]{default}  {italic}show a warning message when log files are over this size (MB){default}
       {grey}[{paradise}sessions{grey}]{default}  {italic}whether to store session statistics{default}
        {grey}[{paradise}globals{grey}]{default}  {italic}whether to update global statistics{default}
    {grey}[{paradise}access logs{grey}]{default}  {italic}allow the usage of access logs{default}
     {grey}[{paradise}error logs{grey}]{default}  {italic}allow the usage of error logs{default}
         {grey}[{paradise}backup{grey}]{default}  {italic}whether to make a backup of the original log files{default}
     {grey}[{paradise}bachup tar{grey}]{default}  {italic}store the backup as a tar.gz compressed archive{default}
     {grey}[{paradise}backup zip{grey}]{default}  {italic}store the backup as a zip compressed archive{default}
         {grey}[{paradise}delete{grey}]{default}  {italic}whether to delete the original log files when done{default}
          {grey}[{paradise}trash{grey}]{default}  {italic}any occurrence will be moved to the trash instead of removed{default}
     {grey}[{paradise}trash path{grey}]{default}  {italic}the path to the folder used as trash (MUST BE SET){default}
          {grey}[{paradise}shred{grey}]{default}  {italic}any occurrence will be shreded instead of simply removed{default}
      {grey}[{paradise}logs path{grey}]{default}  {italic}the path to the logs folder (MUST BE SET){default}
      {grey}[{paradise}log files{grey}]{default}  {italic}the name of the log files to use (MUST BE SET){default}
  {grey}[{paradise}usage control{grey}]{default}  {italic}whether to control which log file has already been used{default}
  {grey}[{paradise}access fields{grey}]{default}  {italic}which field to use when parsing access logs (MUST BE SET){default}
      {grey}[{paradise}whitelist{grey}]{default}  {italic}log lines from these IPs will be discarded (MUST BE SET){default}%s\
""".format(**supercrap.text_colors)\
   %(self.space,self.morespace,self.space)
        self.MSG_examples = """%s{cyan}Examples{default}%s
  {italic}Enable using error logs{default}%s\n{bold}    use error logs{default}%s
  {italic}Enable making a backup of the original logs as zip archive{default}\n%s{bold}    : use backup zip{default}%s
  {italic}Set a custom warning size for the log files{default}%s\n{bold}    : set warning size 30{default}%s
  {italic}Set a custom path for the logs folder{default}%s\n{bold}    : set logs path /yout/path/to/logs{default}%s
  {italic}Enable using the trash and set the path to it{default}%s\n{bold}    : use trash and set trash path /yout/path/to/trash{default}
  {italic}Set a custom whitelist of IPs{default}%s\n{bold}    : set whitelist ::1 192.168. {default}%s%s\
""".format(**supercrap.text_colors)\
   %(self.space,self.morespace,self.morespace,self.morespace,self.morespace,
     self.morespace,self.morespace,self.morespace,self.morespace,self.morespace,
     self.morespace,self.morespace,self.morespace,self.space)
    
    
    def readConfigs(self, supercrap:object ):
        """ Read the configuration file """
        if not checkFolder( supercrap, "crapconf", self.confpath ):
            exit()
        if not checkFile( supercrap, "craplog", self.file_path, create=False ):
            exit()
        try:
            with open(self.file_path,'r') as f:
                tmp = f.read().strip().split('\n')
        except:
            # failed to read
            print("\n{err}Error{white}[{grey}craplog{white}]{red}>{default} failed to read configuration file: {rose}%s{default}\n"\
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
        if len(configs) != 25:
            print("\n{err}Error{white}[{grey}craplog.crapconf{white}]{red}>{default} invalid number of lines: {rose}%s{default}"\
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
        self.sets_map['performance'] = bool(int(configs[5]))
        self.sets_map['auto delete'] = bool(int(configs[6]))
        self.sets_map['auto merge'] = bool(int(configs[7]))
        self.sets_map['warning size'] = float(configs[8])
        self.sets_map['sessions'] = bool(int(configs[9]))
        self.sets_map['globals'] = bool(int(configs[10]))
        self.sets_map['access logs'] = bool(int(configs[11]))
        self.sets_map['error logs'] = bool(int(configs[12]))
        self.sets_map['backup'] = bool(int(configs[13]))
        self.sets_map['backup tar'] = bool(int(configs[14]))
        self.sets_map['backup zip'] = bool(int(configs[15]))
        self.sets_map['delete'] = bool(int(configs[16]))
        self.sets_map['trash'] = bool(int(configs[17]))
        self.sets_map['shred'] = bool(int(configs[18]))
        self.sets_map['logs path'] = configs[19]
        self.sets_map['log files'] = configs[20].split(' ')
        self.sets_map['file selection'] = bool(int(configs[21]))
        self.sets_map['usage control'] = bool(int(configs[22]))
        self.sets_map['access fields'] = configs[23].split(' ')
        self.sets_map['whitelist'] = configs[24].split(' ')
        
        # check log files
        tmp = [f.strip() for f in self.sets_map['log files']]
        self.sets_map['log files'] = []
        for f in tmp:
            if f != "":
                self.sets_map['log files'].append( f )
        # check access fields
        tmp = [f.strip() for f in self.sets_map['access fields']]
        self.sets_map['access fields'] = []
        for f in tmp:
            if f == "":
                continue
            f = f.upper()
            if tmp.count( f ) > 1:
                if supercrap.less_output is False:
                    print()
                print("{warn}Warning{white}[{grey}configs{white}]{red}>{default} duplicate field removed: {yellow}%s{default}"\
                    .format(**supercrap.text_colors)\
                    %( f ))
                if supercrap.less_output is False:
                    print()
                continue
            elif f not in ["IP","UA","REQ","RES"]:
                if supercrap.less_output is False:
                    print()
                print("\n{warn}Warning{white}[{grey}configs{white}]{red}>{default} invalid field removed: {yellow}%s{default}"\
                    .format(**supercrap.text_colors)\
                    %( f ))
                if supercrap.less_output is False:
                    print()
                continue
            self.sets_map['access fields'].append( f )
        # check whitelist
        tmp = [f.strip() for f in self.sets_map['whitelist']]
        self.sets_map['whitelist'] = []
        for f in tmp:
            if f != "":
                self.sets_map['whitelist'].append( f )
    
    
    
    def writeConfigs(self, supercrap:object ):
        """ Write the configuration file """
        result = True
        result = self.checkIntegrity( supercrap )
        if result is True:
            result = checkFolder( supercrap, "crapconf", self.confpath )
        if result is True:
            result = checkFile( supercrap, "craplog", self.file_path )
        
        if result is True:
            configs = ""
            configs += "%s\n" %(int(self.sets_map['configs']))
            configs += "%s\n" %(int(self.sets_map['arguments']))
            configs += "%s\n" %(int(self.sets_map['less output']))
            configs += "%s\n" %(int(self.sets_map['more output']))
            configs += "%s\n" %(int(self.sets_map['colors']))
            configs += "%s\n" %(int(self.sets_map['performance']))
            configs += "%s\n" %(int(self.sets_map['auto delete']))
            configs += "%s\n" %(int(self.sets_map['auto merge']))
            configs += "%s\n" %(self.sets_map['warning size'])
            configs += "%s\n" %(int(self.sets_map['sessions']))
            configs += "%s\n" %(int(self.sets_map['globals']))
            configs += "%s\n" %(int(self.sets_map['access logs']))
            configs += "%s\n" %(int(self.sets_map['error logs']))
            configs += "%s\n" %(int(self.sets_map['backup']))
            configs += "%s\n" %(int(self.sets_map['backup tar']))
            configs += "%s\n" %(int(self.sets_map['backup zip']))
            configs += "%s\n" %(int(self.sets_map['delete']))
            configs += "%s\n" %(int(self.sets_map['trash']))
            configs += "%s\n" %(int(self.sets_map['shred']))
            configs += "%s\n" %(self.sets_map['logs path'])
            for log_file in self.sets_map['log files']:
                configs += "%s " %(log_file)
            configs = "%s\n" %( configs.rstrip() )
            configs += "%s\n" %(int(self.sets_map['file selection']))
            configs += "%s\n" %(int(self.sets_map['usage control']))
            for field in self.sets_map['access fields']:
                configs += "%s " %(field)
            configs = "%s\n" %( configs.rstrip() )
            for ip in self.sets_map['whitelist']:
                configs += "%s " %(ip)
            configs = "%s\n" %( configs.rstrip() )
            
            try:
                with open(self.file_path,'w') as f:
                    f.write( configs )
                    if supercrap.more_output is True:
                        print("\n{ok}Succesfully written configurations for {bold}CRAP{white}LOG{default}\n"\
                            .format(**supercrap.text_colors)\
                            %( self.file_path ))
            except:
                # failed to read
                result = False
                print("\n{warn}Warning{white}[{grey}craplog{white}]{red}>{default} failed to write configuration file: {rose}%s{default}\n"\
                    .format(**supercrap.text_colors)\
                    %( self.file_path ))
                if supercrap.less_output is False:
                    print("                the error is most-likely caused by a lack of permissions")
                    print("                please add read/write permissions to the whole crapconf folder and retry")
                print()
        
        if result is True:
            self.unsaved_changes = False
    
    
    
    def checkIntegrity(self, supercrap:object ) -> bool :
        """ Check the integrity of the configuration """
        checks_passed = True
        try:
            ws = float(self.sets_map['warning size'])
            if ws < 0.001:
                if supercrap.more_output is True:
                    print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} the {cyan}warning size{default} is {bold}very{small}: {yellow}%s{default} {bold}KB{default}"\
                        .format(**supercrap.text_colors)\
                        %( self.sets_map['warning size'] * 1000 ))
                    print("                  {ok}the configuration will be saved{default}, but keep in mind it is a very small size"\
                        .format(**supercrap.text_colors))
                    print("                  if you're not testing, it is suggested to increase it to at least {bold}10{default} MB"\
                        .format(**supercrap.text_colors))
        except:
            checks_passed = False
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} the {cyan}warning size{default} seems not to be a number: {rose}%s{default}"\
                .format(**supercrap.text_colors)\
                %( self.sets_map['warning size'] ))
            if supercrap.more_output is True:
                print("                  it must be a number (can expressed in floating point notation)")
        if  self.sets_map['less output'] is True\
        and self.sets_map['more output'] is True:
            checks_passed = False
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} both {cyan}less{default} and {cyan}more{default} output modes are {rose}enabled{default}"\
                .format(**supercrap.text_colors))
            if supercrap.more_output is True:
                print("                  you can't print less and more output at the same time")
        if  self.sets_map['sessions'] is False\
        and self.sets_map['globals'] is False:
            checks_passed = False
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} both {cyan}globals{default} and {cyan}sessions{default} are {rose}disabled{default}"\
                .format(**supercrap.text_colors))
            if supercrap.more_output is True:
                print("                  you must use at least one of them, or parsing logs will be useless")
        if  self.sets_map['access logs'] is False\
        and self.sets_map['error logs'] is False:
            checks_passed = False
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} both {cyan}access{default} and {cyan}error{default} logs are {rose}disabled{default}"\
                .format(**supercrap.text_colors))
            if supercrap.more_output is True:
                print("                  you can't avoid working on both access and error log files, nothing will be done")
        if len(self.sets_map['access fields']) == 0:
            checks_passed = False
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} the list of {cyan}access fields{default} to use is {rose}empty{default}"\
                .format(**supercrap.text_colors))
            if supercrap.more_output is True:
                print("                 you must use at least one field when working on access_logs")
                print("                 if you don't want to work on access logs, rather disable them")
        if  self.sets_map['backup tar'] is True\
        and self.sets_map['backup zip'] is True:
            checks_passed = False
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} both {cyan}tar.gz{default} and {cyan}zip{default} archive modes are {rose}enabled{default}"\
                .format(**supercrap.text_colors))
            if supercrap.more_output is True:
                print("                  you must choose one and disable the other")
        if  self.sets_map['trash'] is True\
        and self.sets_map['shred'] is True:
            checks_passed = False
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} both {cyan}trash{default} and {cyan}shred{default} deletion modes are {rose}enabled{default}"\
                .format(**supercrap.text_colors))
            if supercrap.more_output is True:
                print("                  you must choose one and disable the other")
        if checks_passed is False:
            print()
        return checks_passed
    
