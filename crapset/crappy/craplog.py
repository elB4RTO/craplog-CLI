
from crappy.check import checkFile, checkFolder


class LogSet(object):
    def __init__(self, confpath:str ):
        self.use_configs   = True
        self.use_arguments = True
        
        self.less_output = False
        self.more_output = False
        self.performance = False
        self.use_colors  = True
        
        self.auto_delete   = False
        self.auto_merge    = False
        self.max_file_size = 100.0
        
        self.session_stats = True
        self.global_stats  = True
        self.access_logs   = True
        self.error_logs    = False
        
        self.backup      = False
        self.archive_tar = False
        self.archive_zip = False
        
        self.delete     = False
        self.trash      = False
        self.trash_path = "~/.local/share/Trash/files/"
        self.shred      = False
        
        self.logs_path      = "/var/log/apache2"
        self.log_files      = ["access.log.1"]
        self.file_selection = False
        self.usage_control  = True
        
        self.access_fields = ["IP", "REQ", "RES", "UA"]
        self.ip_whitelist = ["::1"]
        
        self.confpath = confpath
        self.file_path = "%s/craplog.conf" %(confpath)
        
    
    def readConfigs(self, supercrap:object ):
        """ Read the configuration file """
        if not checkFolder( supercrap, "crapconf", self.confpath )
            exit()
        if not checkFile( supercrap, "craplog", self.file_path, create=False ):
            exit()
        try:
            with open(self.confpath,'r') as f:
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
            print("\n{err}Error{white}[{grey}craplog.conf{white}]{red}>{default} invalid number of lines: {rose}%s{default}"\
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
        self.use_configs = bool(int(configs[0]))
        self.use_arguments = bool(int(configs[1]))
        self.less_output = bool(int(configs[2]))
        self.more_output = bool(int(configs[3]))
        self.use_colors = bool(int(configs[4]))
        self.performance = bool(int(configs[5]))
        self.auto_delete = bool(int(configs[6]))
        self.auto_merge = bool(int(configs[7]))
        self.max_file_size = float(configs[8])
        self.session_stats = bool(int(configs[9]))
        self.global_stats = bool(int(configs[10]))
        self.access_logs = bool(int(configs[11]))
        self.error_logs = bool(int(configs[12]))
        self.backup = bool(int(configs[13]))
        self.archive_tar = bool(int(configs[14]))
        self.archive_zip = bool(int(configs[15]))
        self.delete = bool(int(configs[16]))
        self.trash = bool(int(configs[17]))
        self.shred = bool(int(configs[18]))
        self.logs_path = configs[19]
        self.log_files = configs[20].split(' ')
        self.file_selection = bool(int(configs[21]))
        self.usage_control = bool(int(configs[22]))
        self.access_fields = configs[23].split(' ')
        self.ip_whitelist = configs[24].split(' ')
        
        # check log files
        tmp = [f.strip() for f in self.log_files]
        self.log_files = []
        for f in tmp:
            if f != "":
                self.log_files.append( f )
        # check access fields
        tmp = [f.strip() for f in self.access_fields]
        self.access_fields = []
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
            self.access_fields.append( f )
        # check whitelist
        tmp = [f.strip() for f in self.ip_whitelist]
        self.ip_whitelist = []
        for f in tmp:
            if f != "":
                self.ip_whitelist.append( f )
    
    
    
    def writeConfigs(self, supercrap:object ):
        """ Write the configuration file """
        result = True
        result = self.checkIntegrity( supercrap )
        if result is True:
            result = checkFolder( supercrap, "crapconf", self.confpath )
        if result is True:
            result = checkFile( supercrap, "craplog", self.file_path ):
        
        if result is True:
            configs = ""
            configs += "%s\n" %(int(self.use_configs))
            configs += "%s\n" %(int(self.use_arguments))
            configs += "%s\n" %(int(self.less_output))
            configs += "%s\n" %(int(self.more_output))
            configs += "%s\n" %(int(self.use_colors))
            configs += "%s\n" %(int(self.performance))
            configs += "%s\n" %(int(self.auto_delete))
            configs += "%s\n" %(int(self.auto_merge))
            configs += "%s\n" %(self.max_file_size)
            configs += "%s\n" %(int(self.session_stats))
            configs += "%s\n" %(int(self.global_stats))
            configs += "%s\n" %(int(self.access_logs))
            configs += "%s\n" %(int(self.error_logs))
            configs += "%s\n" %(int(self.backup))
            configs += "%s\n" %(int(self.archive_tar))
            configs += "%s\n" %(int(self.archive_zip))
            configs += "%s\n" %(int(self.delete))
            configs += "%s\n" %(int(self.trash))
            configs += "%s\n" %(int(self.shred))
            configs += "%s\n" %(self.logs_path)
            for log_file in self.log_files:
                configs += "%s " %(log_file)
            configs = "%s\n" %( configs.rstrip() )
            configs += "%s\n" %(int(self.file_selection))
            configs += "%s\n" %(int(self.usage_control))
            for field in self.access_fields:
                configs += "%s " %(field)
            configs = "%s\n" %( configs.rstrip() )
            for ip in self.ip_whitelist:
                configs += "%s " %(ip)
            configs = "%s\n" %( configs.rstrip() )
            
            try;
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
            supercrap.logset_changed = False
    
    
    
    def checkIntegrity(self, supercrap:object, craplog:object ) -> bool :
        """ Check the integrity of the configuration """
        def failed():
            nonlocal checks_passed
            if checks_passed is True:
                checks_passed = False
        
        checks_passed = True
        if  craplog.less_output is True\
        and craplog.more_output is True:
            failed()
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} both {cyan}less{default} and {cyan}more{default} output modes are {rose}enabled{default}"\
                .format(**supercrap.text_colors))
            if supercrap.more_output is True:
                print("                  you can't print less and more output at the same time")
        if  craplog.session_stats is False\
        and craplog.global_stats is False:
            failed()
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} both {cyan}globals{default} and {cyan}sessions{default} are {rose}disabled{default}"\
                .format(**supercrap.text_colors))
            if supercrap.more_output is True:
                print("                  you must use at least one of them, or parsing logs will be useless")
        if  craplog.access_logs is False\
        and craplog.error_logs is False:
            failed()
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} both {cyan}access{default} and {cyan}error{default} logs are {rose}disabled{default}"\
                .format(**supercrap.text_colors))
            if supercrap.more_output is True:
                print("                  you can't avoid working on both access and error log files, nothing will be done")
        if len(craplog.access_fields) == 0:
            failed()
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} the list of {cyan}access fields{default} to use is {rose}empty{default}"\
                .format(**supercrap.text_colors))
            if supercrap.more_output is True:
                print("                 you must use at least one field when working on access_logs")
                print("                 if you don't want to work on access logs, rather disable them")
        if  craplog.archive_tar is True\
        and craplog.archive_zip is True:
            failed()
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} both {cyan}tar.gz{default} and {cyan}zip{default} archive modes are {rose}enabled{default}"\
                .format(**supercrap.text_colors))
            if supercrap.more_output is True:
                print("                  you must choose one and disable the other")
        if  craplog.trash is True\
        and craplog.shred is True:
            failed()
            if supercrap.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}craplog{white}]{red}>{default} both {cyan}trash{default} and {cyan}shred{default} deletion modes are {rose}enabled{default}"\
                .format(**supercrap.text_colors))
            if supercrap.more_output is True:
                print("                  you must choose one and disable the other")
        if checks_passed is False:
            print()
        return checks_passed
    
    
    
    def run(self, supercrap:object ):
        """
        Run the configuration process
        """
        quit_crapset = False
        loop = True
        while loop is True:
            if supercrap.less_output is False:
                print("{grey}(Enter {white}help{default}{grey} to view a help message)"\
                    .format(**supercrap.text_colors))
            user_input = input("{bold}What to edit about %s? {paradise}:{default} "\
                .format(**supercrap.text_colors)\
                %( supercrap.TXT_craplog )).lower().strip()
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
            elif user_input in ["b","back"]:
                loop = False
                continue
            elif user_input in ["h","help","help me"]:
                space = ""
                if supercrap.less_output is False:
                    print()
                    space = "\n"
                print("""Available choices
  {grey}[{paradise}h{grey}/{white}help{grey}]{default}  {italic}view this help message{default}
  {grey}[{paradise}q{grey}/{white}quit{grey}]{default}  {italic}quit Crapset{default}
  {grey}[{paradise}b{grey}/{white}back{grey}]{default}  {italic}back to the previous menu{default}
  {grey}[{paradise}s{grey}/{white}save{grey}]{default}  {italic}save the changes to the configurations{default}%s
  {grey}[{paradise}show{grey}]{default}  {italic}show the actual configurations{default}%s
  {grey}[{paradise}set{grey}/{white}assing{grey}]{default}         {italic}assign the given values an option{default}
  {grey}[{paradise}use{grey}/{white}enable{grey}]{default}         {italic}enable an option{default}
  {grey}[{paradise}don't use{grey}/{white}disable{grey}]{default}  {italic}disable an option{default}\
""".format(**supercrap.text_colors) %( space,space ))
                if supercrap.less_output is False:
                    print()
                print("""Available options
  {grey}[{paradise}configs{grey}]{default}         {italic}allow using the configurations file{default}
  {grey}[{paradise}arguments{grey}]{default}       {italic}allow using command line arguments{default}
  {grey}[{paradise}less output{grey}]{default}     {italic}reduce the output on screen{default}
  {grey}[{paradise}more output{grey}]{default}     {italic}increase the output on screen{default}
  {grey}[{paradise}colors{grey}]{default}          {italic}allow applying colors to the output{default}
  {grey}[{paradise}performance{grey}]{default}     {italis}print performance informations{default}
  {grey}[{paradise}auto delete{grey}]{default}     {italis}automatically choose to delete files{default}
  {grey}[{paradise}auto merge{grey}]{default}      {italis}automatically merge sessions having the same date{default}
  {grey}[{paradise}max file size{grey}]{default}   {italis}show a warning message when log files are over this size (MB){default}
  {grey}[{paradise}sessions{grey}]{default}        {italis}whether to store session statistics{default}
  {grey}[{paradise}globals{grey}]{default}         {italis}whether to update global statistics{default}
  {grey}[{paradise}access logs{grey}]{default}     {italis}allow the usage of access logs{default}
  {grey}[{paradise}error logs{grey}]{default}      {italis}allow the usage of error logs{default}
  {grey}[{paradise}backup{grey}]{default}          {italis}whether to make a backup of the original log files{default}
  {grey}[{paradise}archive tar{grey}]{default}     {italis}store the backup as a tar.gz compressed archive{default}
  {grey}[{paradise}archive zip{grey}]{default}     {italis}store the backup as a zip compressed archive{default}
  {grey}[{paradise}delete{grey}]{default}          {italis}whether to delete the original log files when done{default}
  {grey}[{paradise}trash{grey}]{default}           {italis}any occurrence will be moved to the trash instead of removed{default}
  {grey}[{paradise}shred{grey}]{default}           {italis}any occurrence will be shreded instead of simply removed{default}
  {grey}[{paradise}logs path{grey}]{default}       {italis}the path to the logs folder (MUST BE SET){default}
  {grey}[{paradise}log files{grey}]{default}       {italis}the name of the log files to use (MUST BE SET){default}
  {grey}[{paradise}usage control{grey}]{default}   {italis}whether to control which log file has already been used{default}
  {grey}[{paradise}access fields{grey}]{default}   {italis}which field to use when parsing access logs (MUST BE SET){default}
  {grey}[{paradise}ip whitelist{grey}]{default}    {italis}log lines from these IPs will be discarded (MUST BE SET){default}
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
                
                        if log_files != ["access.log.1"]:
                            file_selection = True
            
            
            else:
                # leave this normal yellow, it's secondary and doesn't need real attention
                print("\n{yellow}Warning{white}[{grey}choice{white}]{yellow}>{default} not a valid choice: {bold}%s{default}"\
                    .format(**supercrap.text_colors))
                if supercrap.less_output is False:
                    print()
                    sleep(1)
        
        return quit_crapset
    
