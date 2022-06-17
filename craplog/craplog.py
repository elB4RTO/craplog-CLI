
import os

from sys import argv
from sys.path import append as libpath
libpath("../")

from time import sleep
from time import perf_counter as timer

from subprocess import run, STDOUT, DEVNULL

from craplib import aux
from crappy.aux    import MSG_help, MSG_examples
from crappy.check  import makeInitialChecks, checkSessionsDates
from crappy.hashes import bringHashes, storeHashes
from crappy.read   import collectLogLines
from crappy.parse  import parseLogLines
from crappy.stats  import updateGlobals, storeSessions
from crappy.backup import backupOriginals, backupGlobals


class Craplog(object):
    """
    Make statistics from Apache2 logs
    """
    def __init__(self, args: list ):
        """
        Craplog's initializer
        """
        # variables from args
        self.use_configs:    bool
        self.use_arguments:  bool
        self.less_output:    bool
        self.more_output:    bool
        self.use_colors:     bool
        self.performance:    bool
        self.auto_delete:    bool
        self.auto_merge:     bool
        self.warning_size:   float
        self.session_stats:  bool
        self.global_stats:   bool
        self.access_logs:    bool
        self.error_logs:     bool
        self.backup:         bool
        self.archive_tar:    bool
        self.archive_zip:    bool
        self.delete:         bool
        self.trash:          bool
        self.shred:          bool
        self.logs_path:      str
        self.log_files:      list
        self.file_selection: bool
        self.usage_control:  bool
        self.access_fields:  list
        self.ip_whitelist:   list
        # variables for jobs
        self.aborted: bool
        self.proceed: bool
        self.collection: dict
        self.undo_paths: list
        self.undo_fails: dict
        self.crappath: str
        self.statpath: str
        # variables for performance
        self.start_time:   float
        self.elapsed_time: float
        self.crap_time: float
        self.user_time: float
        self.parsed_size: int
        self.logs_size:   int
        self.access_size: int
        self.errors_size: int
        self.whitelist_size: int
        self.total_lines:  int
        self.access_lines: int
        self.errors_lines: int
        self.whitelist_lines: int
        # text messages
        self.last_job:     str
        self.caret_return: int
        self.text_colors:  dict
        self.MSG_elbarto:  str
        self.MSG_craplogo: str
        self.MSG_help:     str
        self.MSG_examples: str
        self.MSG_craplog:  str
        self.MSG_fin:      str
        self.TXT_craplog:  str
        self.TXT_fin:      str
        
        # get craplog's path
        self.crappath = os.path.abspath(__file__)
        self.crappath = self.crappath[:self.crappath.rfind('/')]
        self.statpath = "%s/crapstats" %(self.crappath[:self.crappath.rfind('/')])
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
        Initialize Craplog's variables
        This section can be manually edited to pre-set Craplog
          and avoid having to pass arguments every time
        """
        ################################################################
        #                 START OF THE EDITABLE SECTION
        #
        # HIERARCHY FOR APPLYING SETTINGS:
        #  - HARDCODED VARIABLES (THESE ONES)
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
        # SETTING THIS VARIABLE TO 'False' MEANS THAT EVERY ARGUMENT WILL BE IGNORED
        # ONLY THE MANUAL CONFIGURATION OF THESE VARIABLES WILL BE USED
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
        # SHOW INFORMATIONS ABOUT THE PERFORMANCE
        # [ -p  /  --performance ]
        self.performance = False
        #
        # USE COLORS WHEN PRINTING TEXT ON SCREEN
        # CAN BE DISABLED PASSING [ --no-colors ]
        self.use_colors = True
        #
        # AUTOMATICALLY DELETE FILES WHEN NEEDED
        # [ --auto-delete ]
        # USE WITH CAUTION, THIS APPLIES IN EVERY CIRCUMSTANCE
        # INCLUDES: ORIGINAL LOG FILES, CONFLICT FILES/FOLDERS
        self.auto_delete = False
        #
        # AUTOMATICALLY MERGE SESSIONS STATISTICS WITH THE SAME DATE
        # [ --auto-merge ]
        # IF SOME OF THE NEWELY PARSED LOGS HAVE THE SAME DATE OF AN
        # ALREADY STORED SESSION, MERGE THE RELATIVE LINES
        self.auto_merge = False
        #
        # A WARNING IS EMITTED IF THE SIZE AN INPUT FILE OVERTAKES THIS LIMIT
        # [ --max-size ]
        # IN MB (MegaBytes)
        self.warning_size = 100.0
        #
        # STORE SESSION STATISTICS OF THE PARSED DATA
        # CAN BE DISABLED PASSING [ -gO  /  --only-globals ]
        self.session_stats = True
        #
        # UPDATE GLOBAL STATISTICS WITH THE PARSED DATA
        # CAN BE DISABLED PASSING [ -gA  /  --avoid-globals ]
        self.global_stats = True
        #
        # MAKE STATISTICS FROM ACCESS LOGS
        # [  ]
        # CAN BE DISABLED PASSING [ --only-errors ]
        self.access_logs = True
        #
        # MAKE STATISTICS FROM ERROR LOGS
        # [ -e  /  --errors ]
        self.error_logs = False
        #
        # MAKE A BACKUP COPY OF THE ORIGINAL LOG FILES (AS THEY ARE)
        # [ -b  /  --backup ]
        # MUST BE SET TO True IF AN ARCHIVE CHOICE IS True
        self.backup = False
        #
        # ARCHIVE THE BACKUP AS tar.gz
        # [ -bT  /  --backup-tar ]
        # gzip COMPRESSED tar ARCHIVE
        self.archive_tar = False
        #
        # ARCHIVE THE BACKUP AS zip
        # [ -bZ  /  --backup-zip ]
        # TRIES TO COMPRESS THE ARCHIVE WITH THE MAX COMPRESSION LEVEL
        # STORES AS NORMAL zip IF THE PREVIOUS FAILS
        self.archive_zip = False
        #
        # DELETE THE ORIGINAL LOG FILES WHEN DONE
        # [ -dO  /  --delete-originals ]
        # IF THE PROCESS FAILS BEFORE THE DELETE STEP, DELETION WILL BE SKIPPED
        # AFTER THE DELETE STEP, THE PROCESS WILL NO MORE BE REVERSIBLE
        self.delete = False
        #
        # MOVE FILES TO TRASH INSTEAD OF COMPLETELY REMOVING THEM
        # [ --trash ]
        # DOESN'T APPLY TO CONFLICT FILES, WHICH WILL BE REMOVED (OR SHREDED)
        self.trash = False
        #
        # THE DIRECTORY USED AS TRASH BY YOUR SYSTEM
        # CAN BE PASSED FOLLOWING THE [ --trash <path> ] OPTION
        # DEFAULT TO: ~/.local/share/Trash/files/
        self.trash_path = "~/.local/share/Trash/files/"
        #
        # SHRED FILES INSTEAD OF SIMPLY REMOVING THEM
        # [ --shred ]
        self.shred = False
        #
        # THE DIRECTORY CONTAINING THE LOGS FILES
        # [ -P  /  --logs-path ]
        # WHEN PASSING ARGUMENTS, THE OPTION MUST BE FOLLOWED BY THE PATH
        self.logs_path = "/var/log/apache2"
        #
        # THE LIST OF LOGS FILES TO USE
        # [ -F  /  --log-files ]
        # WHEN PASSING ARGUMENTS:
        # - THE OPTION MUST BE FOLLOWED BY THE LIST OF FILES
        # - FILES MUST BE PASSED AS NAMES ONLY, NOT PATHS
        # - ' ' (WITHESPACE) HAVE TO BE USED AS SEPARATOR BETWEEN NAMES
        self.log_files = ["access.log.1"]
        #
        # True ONLY WHEN USING A CUSTOM LIST OF FILES !-> FROM ARGUMENTS <-!
        # [  ]
        self.file_selection = False
        #
        # STORE A HASH OF EVERY PARSED FILE TO AVOID PARSING THEM TWICE
        # [  ]
        # THE HASH ALGORITHM IS sha256
        # PLEASE NOTICE THAT THIS CANNOT BE USED TO TRACK YOU OR YOUR FILES,
        # THE HASH IS IRREVERSIBLE AND CAN'T THEREFORE BE USED TO HARM YOUR PRIVACY
        self.usage_control = True
        #
        # LIST OF FIELDS TO BE USED WHILE PARSING ACCESS LOGS' LINES
        # [ -A  /  --access-fields ]
        # WHEN PASSING ARGUMENTS:
        # - THE OPTION MUST BE FOLLOWED BY THE LIST OF FIELDS
        # - FIELDS MUST BE PASSED AS ABBREVIATIONS
        # - ' ' (WITHESPACE) HAVE TO BE USED AS SEPARATOR
        self.access_fields = ["IP", "REQ", "RES", "UA"]
        #
        # LOG LINES FROM THESE IPs WILL BE SKIPPED
        # [ -W  /  --ip-whitelist ]
        # VIEW 'README.md' FOR MORE INFORMATIONS
        # WHEN PASSING ARGUMENTS:
        # - THE OPTION MUST BE FOLLOWED BY THE LIST OF IPs
        # - ' ' (WITHESPACE) HAVE TO BE USED AS SEPARATOR
        self.ip_whitelist = ["::1"]
        #
        #                 END OF THE EDITABLE SECTION
        ################################################################
        #
        #
        # DO NOT MODIFY THE FOLLOWING VARIABLES
        self.collection = {}
        self.undo_paths = []
        self.undo_fails = []
        self.hashes     = []
        self.aborted = False
        self.proceed = True
        self.elapsed_time = 0.
        self.crap_time    = 0.
        self.user_time    = 0.
        self.parsed_size = 0
        self.logs_size   = 0
        self.access_size = 0
        self.errors_size = 0
        self.whitelist_size = 0
        self.total_lines  = 0
        self.access_lines = 0
        self.errors_lines = 0
        self.whitelist_lines = 0
    
    
    
    def readConfigs(self):
        """
        Read the saved configuration
        """
        path = "%s/crapconfs/craplog.crapconf" %(self.crappath[:self.crappath.rfind('/')])
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
        if len(configs) != 25:
            self.printJobFailed()
            print("\n{err}Error{white}[{grey}configs{white}]{red}>{default} invalid number of lines: {rose}%s{default}"\
                .format(**self.text_colors)\
                %( len(configs) ))
            if self.less_output is False:
                print("                if you have manually edited the configurations file, please un-do the changes")
                print("                else, please report this issue")
            print()
            self.exitAborted()
        
        # apply the configs
        self.use_configs = bool(int(configs[0]))
        if self.use_configs is True:
            self.use_arguments = bool(int(configs[1]))
            self.less_output = bool(int(configs[2]))
            self.more_output = bool(int(configs[3]))
            self.use_colors  = bool(int(configs[4]))
            self.performance = bool(int(configs[5]))
            self.auto_delete = bool(int(configs[6]))
            self.auto_merge  = bool(int(configs[7]))
            self.warning_size = float(configs[8])
            self.session_stats = bool(int(configs[9]))
            self.global_stats  = bool(int(configs[10]))
            self.access_logs = bool(int(configs[11]))
            self.error_logs  = bool(int(configs[12]))
            self.backup      = bool(int(configs[13]))
            self.archive_tar = bool(int(configs[14]))
            self.archive_zip = bool(int(configs[15]))
            self.delete = bool(int(configs[16]))
            self.trash  = bool(int(configs[17]))
            self.shred  = bool(int(configs[18]))
            self.logs_path = configs[19]
            self.log_files = configs[20].split(' ')
            self.file_selection = bool(int(configs[21]))
            self.usage_control  = bool(int(configs[22]))
            self.access_fields = configs[23].split(' ')
            self.ip_whitelist  = configs[24].split(' ')
            self.initMessages()
            
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
                    self.printJobFailed()
                    print("\n{err}Error{white}[{grey}configs{white}]{red}>{default} you have inserted the same field twice: {rose}%s{default}\n"\
                        .format(**self.text_colors)\
                        %( f ))
                    self.exitAborted()
                elif f not in ["IP","UA","REQ","RES"]:
                    self.printJobFailed()
                    print("\n{err}Error{white}[{grey}configs{white}]{red}>{default} invalid field for access logs: {rose}%s{default}\n"\
                        .format(**self.text_colors)\
                        %( f ))
                    self.exitAborted()
                self.access_fields.append( f )
            # check whitelist
            tmp = [f.strip() for f in self.ip_whitelist]
            self.ip_whitelist = []
            for f in tmp:
                if f != "":
                    self.ip_whitelist.append( f )
    
    
    
    def initMessages(self):
        """
        Bring message strings
        """
        self.last_job     = ""
        self.caret_return = 0
        if self.use_colors is True:
            self.text_colors = aux.colors()
        else:
            self.text_colors = aux.no_colors()
        self.MSG_elbarto  = aux.elbarto()
        self.MSG_craplogo = aux.LOGO_craplog()
        self.MSG_help     = MSG_help( self.text_colors )
        self.MSG_examples = MSG_examples( self.text_colors )
        self.MSG_craplog  = aux.MSG_craplog( self.text_colors )
        self.MSG_fin      = aux.MSG_fin( self.text_colors )
        self.TXT_craplog  = aux.TXT_craplog( self.text_colors )
        self.TXT_fin      = aux.TXT_fin( self.text_colors )
    
    
    
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
                print("\n%s\n\n%s\n\n%s\n" %( self.LOGO_craplog, self.MSG_help, self.MSG_examples ))
                exit()
            elif arg == "--examples":
                print("\n%s\n\n%s\n" %( self.LOGO_craplog, self.MSG_examples ))
                exit()
            # auxiliary arguments
            elif arg in ["-l", "--less"]:
                self.less_output = True
            elif arg in ["-m", "--more"]:
                self.more_output = True
            elif arg in ["-p", "--performance"]:
                self.performance = True
            elif arg == "--no-colors":
                self.use_colors = False
                self.initMessages()
            # automation arguments
            elif arg == "--auto-delete":
                self.auto_delete = True
            elif arg == "--auto-merge":
                self.auto_merge = True
            # file size limit
            elif arg == "--warning-size":
                if i+1 > n_args\
                or ( args[i+1].startswith("--")\
                  or (args[i+1].startswith("-") and not args[i+1][1].isdigit())):
                    self.warning_size = None
                else:
                    i += 1
                    self.warning_size = args[i]
            # job arguments
            elif arg in ["-e", "--errors"]:
                self.error_logs = True
            elif arg in ["-eO", "--only-errors"]:
                self.access_logs = False
                self.error_logs  = True
            elif arg in ["-gO", "--only-globals"]:
                self.session_stats = False
            elif arg in ["-gA", "--avoid-globals"]:
                self.global_stats = False
            elif arg in ["-b", "--backup"]:
                self.backup = True
            elif arg in ["-bT", "--backup-tar"]:
                self.backup = True
                self.archive_tar = True
            elif arg in ["-bZ", "--backup-zip"]:
                self.backup = True
                self.archive_zip = True
            elif arg in ["-dO", "--delete-originals"]:
                self.delete = True
            elif arg == "--shred":
                self.shred = True
            # user defined arguments
            elif arg == "--trash":
                self.trash = True
                if  i+1 <= n_args\
                and not args[i+1].startswith("-"):
                    i += 1
                    self.trash_path = args[i]
            elif arg in ["-P", "--logs-path"]:
                if i+1 > n_args\
                or args[i+1].startswith("-"):
                    self.logs_path = ""
                else:
                    i += 1
                    self.logs_path = args[i]
            elif arg in ["-F", "--log-files"]:
                self.file_selection = True
                self.log_files = []
                while True:
                    if i+1 > n_args\
                    or args[i+1].startswith("-"):
                        break
                    else:
                        i += 1
                        self.log_files.append( args[i] )
            elif arg in ["-A", "--access-fields"]:
                self.access_fields = []
                while True:
                    if i+1 > n_args\
                    or args[i+1].startswith("-"):
                        break
                    else:
                        i += 1
                        self.access_fields.append( args[i] )
            elif arg in ["-W", "--ip-whitelist"]:
                self.ip_whitelist = []
                while True:
                    if i+1 > n_args\
                    or args[i+1].startswith("-"):
                        break
                    else:
                        i += 1
                        self.ip_whitelist.append( args[i] )
            else:
                print("{err}Error{white}[{grey}argument{white}]{red}>{default} not an available option: {rose}%s{default}"\
                    .format(**self.text_colors)\
                    %(arg))
                if self.more_output is True:
                    print("                 use {cyan}craplog --help{default} to view an help screen"\
                        .format(**self.text_colors))
                exit("")
    
    
    
    def welcomeMessage(self):
        """
        Print the welcome message
        """
        if self.less_output is False:
            print("\n%s\n" %( self.MSG_craplog ))
            if self.more_output is True:
                print("Use {cyan}craplog --help{default} to view an help screen"\
                .format(**self.text_colors))
            if self.auto_delete is self.auto_merge is True:
                print("{yellow}Auto-Delete{default} and {yellow}Auto-Merge{default} are {bold}ON{default}"\
                    .format(**self.text_colors))
            else:
                if self.auto_delete is True:
                    print("{yellow}Auto-Delete{default} is {bold}ON{default}"\
                        .format(**self.text_colors))
                if self.auto_merge is True:
                    print("{yellow}Auto-Merge{default} is {bold}ON{default}"\
                        .format(**self.text_colors))
            print()
            sleep(1)
        else:
            print("{bold}%s"\
                .format(**self.text_colors)\
                %( self.TXT_craplog ))
    
    
    
    def exitMessage(self):
        """
        Print the exit message
        """
        if self.performance is True:
            self.printOverallPerformance()
        if self.less_output is False:
            print("\n%s\n" %( self.MSG_fin ))
        else:
            print("{bold}%s"\
                .format(**self.text_colors)\
                %( self.TXT_fin ))
    
    
    
    def printJob(self, message: str ):
        """
        Print a job-relative message
        """
        self.last_job = "{bold}%s {default}{paradise}...{default} "\
            .format(**self.text_colors)\
            %( message )
        print(self.last_job, end="", flush=True)
    
    
    def reprintJob(self):
        """
        Print a job-relative message
        """
        self.caret_return = 0
        print(self.last_job, end="", flush=True)
    
    
    
    def printJobHalted(self):
        """
        Print the job has been halted
        """
        if self.last_job != "":
            self.restoreCaret()
            print("{orange}Halted{default}"\
                .format(**self.text_colors),
                end="", flush=True )
    
    
    def printJobDone(self):
        """
        Print the job is done
        """
        print("{grass}Done{default}"\
            .format(**self.text_colors))
        self.last_job = ""
    
    
    def printJobFailed(self):
        """
        Print the job failed
        """
        if self.proceed is True:
            self.proceed = False
            if self.caret_return != 0:
                self.restoreCaret()
                print("{rose}Failed{default}"\
                    .format(**self.text_colors))
                self.printElapsedTime()
                self.timer_gap = timer()
                self.last_job = ""
            if len(self.undo_paths) > 0:
                self.undoChanges()
        
    
    
    def printCaret(self, message: str ):
        """
        Print the message and update the caret for a restore
        """
        if self.more_output is True:
            print("{yellow}%s{default}"\
                .format(**self.text_colors)\
                %( message ),
                end="", flush=True )
            self.caret_return = len(message)
    
    
    def restoreCaret(self):
        """
        Restore the caret to the previous position
        """
        if self.more_output is True:
            print("%s%s%s"\
                %( "\b"*self.caret_return, " "*self.caret_return, "\b"*self.caret_return ),
                end="", flush=True )
        self.caret_return = 0
    
    
    
    def printAborted(self):
        """
        Print the abortion message
        """
        self.aborted = True
        if self.less_output is False:
            print()
        print("{err}CRAPLOG ABORTED{default}"\
            .format(**self.text_colors))
        if self.less_output is False:
            print()
    
    
    
    def exitAborted(self):
        """
        Print the abortion message and exit
        """
        self.aborted = True
        self.finalCleanUp()
        if self.less_output is False:
            print()
        print("{err}CRAPLOG ABORTED{default}"\
            .format(**self.text_colors))
        if self.less_output is False:
            print()
        exit()
    
    
    
    def printElapsedTime(self):
        """
        Print the time elapsed since the last gap
        """
        if  self.more_output is True\
        and self.performance is True:
            elapsed = timer() - self.time_gap
            if elapsed <= 60:
                msg = "%.2f {white}s"\
                    .format(**self.text_colors)\
                    %( elapsed )
            else:
                msg = "%d {white}m{pink} %d {white}s"\
                    .format(**self.text_colors)\
                    %( int(elapsed/60), (elapsed%60) )
                
            print("{grey}┖┄{purple}elapsed time{paradise}:{pink} %s{default}"\
                .format(**self.text_colors)\
                %( msg ))
    
    
    
    def printOverallPerformance(self):
        """
        Print overall performance details
        """
        self.elapsed_time = timer() - self.start_time
        self.crap_time = self.elapsed_time - self.user_time
        if self.less_output is False:
            print("{pink}Total size parsed{white}:{paradise} %.2f {white}MB{default}"\
                .format(**self.text_colors)\
                %( self.parsed_size / 1048576 ))
            if self.more_output is True:
                print("{grey}┠┄{pink}total logs size{white}:{paradise} %.2f {white}MB{default}"\
                    .format(**self.text_colors)\
                    %( self.logs_size / 1048576 ))
                print("{grey}┃ └┄{pink}total number of lines{white}:{paradise} %d {default}"\
                    .format(**self.text_colors)\
                    %( self.total_lines ))
            if self.less_output is False:
                print("{grey}┖┄{pink}total used logs size{white}:{paradise} %.2f {white}MB{default}"\
                    .format(**self.text_colors)\
                    %( (self.access_size+self.errors_size) / 1048576 ))
            if self.more_output is True:
                print("{grey}  ┠┄{pink}total number of used lines{white}:{paradise} %d {default}"\
                    .format(**self.text_colors)\
                    %( (self.access_lines+self.errors_lines) ))
                if self.access_logs is True:
                    tree = "  ├" # for errors
                    print("{grey}  ┖─┬┄{pink}used access logs size{white}:{paradise} %.2f {white}MB{default}"\
                        .format(**self.text_colors)\
                        %( self.access_size / 1048576 ))
                    print("{grey}    │ └┄{pink}number of access lines{white}:{paradise} %d {default}"\
                        .format(**self.text_colors)\
                        %( self.access_lines ))
                else:
                    tree = "┖─┬"
                if self.error_logs is True:
                    print("{grey}  %s┄{pink}used error logs size{white}:{paradise} %.2f {white}MB{default}"\
                        .format(**self.text_colors)\
                        %( tree, (self.errors_size / 1048576) ))
                    print("{grey}    │ └┄{pink}number of error lines{white}:{paradise} %d {default}"\
                        .format(**self.text_colors)\
                        %( self.errors_lines ))
                if len(self.ip_whitelist) > 1\
                or (len(self.ip_whitelist) == 1
                and self.ip_whitelist[0] != "::1"):
                    print("{grey}    ├┄{pink}whitelisted logs size{white}:{paradise} %.2f {white}MB{default}"\
                        .format(**self.text_colors)\
                        %( self.whitelist_size / 1048576 ))
                    print("{grey}    │ └┄{pink}number of whitelisted lines{white}:{paradise} %d {default}"\
                        .format(**self.text_colors)\
                        %( self.whitelist_lines ))
                self.ip_whitelist.clear()
                print("{grey}    └┄{pink}discarded logs size{white}:{paradise} %.2f {white}MB{default}"\
                    .format(**self.text_colors)\
                    %( (self.logs_size - (self.access_size+self.errors_size)) / 1048576 ))
                print("{grey}      └┄{pink}number of discarded lines{white}:{paradise} %d {default}"\
                    .format(**self.text_colors)\
                    %( self.total_lines - (self.access_lines+self.errors_lines) ))
            
            print("{pink}Total time elapsed{white}:{paradise} %d {white}m{paradise} %d {white}s{default}"\
                .format(**self.text_colors)\
                %( int(self.elapsed_time/60), (self.elapsed_time%60) ))
            if self.more_output is True:
                print("{grey}┠┄{pink}time used by craplog{white}:{paradise} %d {white}m{paradise} %d {white}s{default}"\
                    .format(**self.text_colors)\
                    %( int(self.crap_time/60), (self.crap_time%60) ))
                print("{grey}┖┄{pink}time used by you{white}:{paradise} %d {white}m{paradise} %d {white}s{default}"\
                    .format(**self.text_colors)\
                    %( int(self.user_time/60), (self.user_time%60) ))
        
        print("{pink}Overall performance{white}:{paradise} %.2f {white}KB/s{default}"\
            .format(**self.text_colors)\
            %( (self.parsed_size / 1024) / self.crap_time ))
        if self.more_output is True:
            real_lines = (self.access_lines+self.errors_lines)
            if (real_lines / self.crap_time) < real_lines:
                print("{grey}┖┄{pink}over lines{white}:{paradise} %.2f {white}lines/sec{default}"\
                    .format(**self.text_colors)\
                    %( real_lines / self.crap_time ))
        if (self.crap_time/60) > 1:
            print("{grey}{pink}Alternative overall{white}:{paradise} %.2f {white}MB/m{default}"\
                .format(**self.text_colors)\
                %( (self.parsed_size / 1048576) / (self.crap_time/60) ))
            if self.more_output is True:
                if (real_lines / (self.crap_time/60)) < real_lines:
                    print("{grey}┖┄{pink}over lines{white}:{paradise} %.2f {white}lines/min{default}"\
                        .format(**self.text_colors)\
                            %( real_lines / (self.crap_time/60) ))
    
    
    
    def removeEntry(self, path: str ):
        """
        Remove an entry (file/folder) accordingly to settings
        """
        del_mode = "remove"
        del_mode_aux = ""
        if self.trash is True:
            del_mode = "move"
            del_mode_aux = " to trash"
        elif self.shred is True:
            del_mode = "shred"
        parent = path[:path.rfind('/')]
        entry  = path[len(parent)+1:]
        if os.path.isdir( path ):
            entry_type = "folder"
        elif os.path.isfile( path ):
            entry_type = "file"
        else:
            # unknown type
            self.printJobFailed()
            print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a directory, nor a file: {grass}%s/{rose}%s{default}"\
                .format(**self.text_colors)\
                %( parent, entry ))
            if self.more_output is True:
                print("             ok, that was unexpected")
                print("             please manually check it and consider reporting this issue")
            print()
        # check the type
        return_code = 0
        if os.path.isfile( path ):
            # is a file
            if self.trash is True:
                return_code = run(
                    ["mv", path, self.trash_path],
                    stdout=DEVNULL,
                    stderr=STDOUT)\
                    .returncode
            elif self.shred is True:
                return_code = run(
                    ["shred", "-uvz", path],
                    stdout=DEVNULL,
                    stderr=STDOUT)\
                    .returncode
            else:
                return_code = run(
                    ["rm", path],
                    stdout=DEVNULL,
                    stderr=STDOUT)\
                    .returncode

            if return_code == 1:
                self.printJobFailed()
                print("\n{err}Error{white}[{grey}file{white}]{red}>{default} unable to %s this %s%s: {grass}%s/{rose}%s{default}"\
                    .format(**self.text_colors)\
                    %( del_mode, entry_type, del_mode_aux, parent, entry ))
                if self.more_output is True:
                    print("               the error is most-likely caused by a lack of permissions")
                    print("               please proceed manually")
                print()

        elif os.path.isdir( path ):
            # is a folder
            if self.trash is True:
                return_code = run(
                    ["mv", path, self.trash_path],
                    stdout=DEVNULL,
                    stderr=STDOUT)\
                    .returncode
            else:
                if self.shred is True:
                    # recursively rename the folder with zeroes
                    new_name = "0"*(len(entry))
                    if len(new_name) < 4:
                        new_name = "0"*4
                    new_path = path
                    while len(new_name) > 1:
                        old_path = new_path
                        new_name = "0"*(len(new_name)-1)
                        new_path = "%s/%s" %( parent, new_name )
                        return_code = run(
                            ["mv", path, new_path],
                            stdout=DEVNULL,
                            stderr=STDOUT)\
                            .returncode
                        if return_code != 0:
                            break
                    path = new_path
                if return_code == 0:
                    # delete the folder
                    return_code = run(
                        ["rmdir", path],
                        stdout=DEVNULL,
                        stderr=STDOUT)\
                        .returncode

            if return_code == 1:
                self.printJobFailed()
                print("\n{err}Error{white}[{grey}folder{white}]{red}>{default} unable to %s this %s%s: {grass}%s/{rose}%s{default}"\
                    .format(**self.text_colors)\
                    %(  del_mode, entry_type, del_mode_aux, parent, entry ))
                if self.more_output is True:
                    print("               the error is most-likely caused by a non-empty folder")
                    print("               or by a lack of permissions")
                    print("               please manually remove it and retry")
                print()
        else:
            # unknown type
            self.printJobFailed()
            print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a directory, nor a file: {grass}%s/{rose}%s{default}"\
                .format(**self.text_colors)\
                %( parent, entry ))
            if self.more_output is True:
                print("             ok, that was unexpected")
                print("             please manually check it and consider reporting this issue")
            print()
    
    
    
    def renameEntry(self, path: str, new_path: str):
        """
        Rename an entry (file/folder)
        """
        try:
            os.rename( path, new_path )
        except:
            parent = path[:path.rfind('/')]
            entry  = path[len(parent)+1:]
            if os.path.isdir( path ):
                entry_type = "folder"
            elif os.path.isfile( path ):
                entry_type = "file"
            else:
                # unknown type
                self.printJobFailed()
                print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a directory, nor a file: {grass}%s/{rose}%s{default}"\
                    .format(**self.text_colors)\
                    %( parent, entry ))
                if self.more_output is True:
                    print("             ok, that was unexpected")
                    print("             please manually check it and consider reporting this issue")
                print()
            # print the error message only if not printed yet
            if self.proceed is True:
                self.printJobFailed()
                print("\n{err}Error{white}[{grey}rename{white}]{red}>{default} unable to rename this %s: {grass}%s/{rose}%s{default}"\
                    .format(**self.text_colors)\
                    %( entry_type, parent, entry ))
                if self.more_output is True:
                    print("                 the error is most-likely caused by a lack of permissions")
                    print("                 please proceed manually")
                print()
    
    
    
    def removeOriginals(self):
        """
        Remove the original log files used
        """
        for original_file in self.log_files:
            self.removeEntry( "%s/%s" %( self.logs_path, original_file ))
    
    
    
    def undoChanges(self):
        """
        Un-do changes after a failure
        """
        if self.less_output is False:
            self.last_job = "Un-doing changes"
            self.caret_return = 0
            print("{bold}{rose}Un-doing changes {default}{paradise}...{default} "\
                .format(**self.text_colors), end="", flush=True)
            self.time_gap = timer()
        self.proceed = True
        self.undo_fails = {'remove':[],'restore':[]}
        for path in reversed(self.undo_paths):
            if path.endswith(".bak"):
                # delete the new file
                old_path = path[:-4]
                if os.path.exists( old_path ):
                    self.removeEntry( old_path )
                if self.proceed is False:
                    self.undo_fails['remove'].append( old_path )
                    self.undo_fails['restore'].append( path )
                    self.proceed = True
                    continue
                # and restore the backup
                self.renameEntry( path, old_path )
                if self.proceed is False:
                    self.undo_fails['restore'].append( old_path )
                    self.proceed = True
            else:
                # delete the newly created entry
                self.removeEntry( path )
                if self.proceed is False:
                    self.undo_fails['remove'].append( path )
                    self.proceed = True
        if len(self.undo_fails['remove']) > 0\
        or len(self.undo_fails['restore']) > 0:
            # print failures
            for action, paths in self.undo_fails.items():
                if len(paths) == 0:
                    break
                col1 = "\033[91m"
                col2 = "\033[1;31m"
                if action == "restore":
                    col1 = "\033[93m"
                    col2 = "\033[1;33m"
                if self.use_colors is False:
                    col1 = ""
                    col2 = ""
                print("\n{bold}Failed to %s%s{default}:"\
                    .format(**self.text_colors)\
                    %( col1, action ))
                for path in paths:
                    print("  - {green}%s/%s%s{default}"\
                        .format(**self.text_colors)\
                        %( path[:path.rfind('/')], col2, path[path.rfind('/')+1:] ))
            print()
            if self.stage == 1:
                # only during the crapstats stage
                print("{bold}{rose}Changes to the crapstats has been discarded{default}"\
                    .format(**self.text_colors))
            if len(self.undo_fails['remove']) > 0:
                print("Please manually remove the files in the remove list before to run craplog again")
                if self.more_output is True:
                    print("  These files are the result of the process (which failed) and must be deleted")
            if len(self.undo_fails['restore']) > 0:
                print("Please manually restore the files in the restore list before to run craplog again")
                if self.more_output is True:
                    print("  These files are copies of the previous files and thus must be restored")
                if self.less_output is False:
                    print("  You can restore a file by deleting the trailing '{bold}.bak{default}' extension")
        else:
            # "successfully" failed
            if self.less_output is False:
                self.printJobDone()
                self.printElapsedTime()
        # in any case, clear the lists
        self.undo_paths.clear()
        self.undo_fails.clear()
    
    
    
    def finalizeChanges(self):
        """
        Finalize changes if exiting successfully
        """
        self.undo_fails = {'remove':[],'restore':[]}
        for path in self.undo_paths:
            if path.endswith(".bak"):
                # delete the backups
                self.removeEntry( path )
                if self.proceed is False:
                    self.undo_fails['remove'].append( path )
                    self.proceed = True
        if  len(self.undo_fails['remove']) > 0:
            printJobFailed()
            # print failures
            for action, paths in self.undo_fails.items():
                if len(paths) == 0:
                    break
                print("\n{bold}Failed to {rose}remove{default} {italic}(safety backups){default}:"\
                    .format(**self.text_colors)\
                    %( action ))
                for path in paths:
                    print("  - {green}%s/{warn}%s{default}"\
                        .format(**self.text_colors)\
                        %( path[:path.rfind('/')], path[path.rfind('/')+1:] ))
            print()
            if self.more_output is True:
                print("There is no reason to undo everything now")
            print("{bold}{blue}Changes to the crapstats will be kept{default}".format(**self.text_colors))
            if self.more_output is True:
                print("These files are just copies of previous stats and thus can be safely deleted")
            if self.less_output is False:
                print("It is suggested to manually remove these files before to run craplog again")
        else:
            # successfully finalized
            self.undo_paths.clear()
    
    
    
    def finalCleanUp(self):
        """
        Clean-up variables
        """
        self.collection.clear()
        self.undo_paths.clear()
        self.undo_fails.clear()
        self.log_files.clear()
        self.logs_path = ""
        self.statpath = ""
        self.crappath = ""
    
    
    
    def main(self):
        """
        Make Craplog do its job
        """
        # welcome message
        self.welcomeMessage()
        # CRAPLOG
        self.stage = 0
        self.start_time = timer()
        
        if self.more_output is True:
            self.printJob("Initializing craplog")
        self.time_gap = timer()
        # make initial checkings
        makeInitialChecks( self )
        # retrieve usage-control hashes
        bringHashes( self )
        if self.more_output is True:
            self.printJobDone()
            self.printElapsedTime()
            print()
        
        if self.less_output is True:
            # preventive output
            self.printJob("Parsing logs")

        # read logs files
        if self.more_output is True:
            self.printJob("Reading logs")
        self.time_gap = timer()
        logs_data = collectLogLines( self )
        if self.more_output is True:
            self.printJobDone()
            self.printElapsedTime()
        
        # store usage hashes of log files
        self.proceed = True
        if self.more_output is True:
            self.printJob("Saving usage-hashes")
        self.time_gap = timer()
        storeHashes( self )
        if self.proceed is True\
        and self.more_output is True:
            self.printJobDone()
            self.printElapsedTime()

        # parse logs lines
        if self.less_output is False:
            self.printJob("Parsing logs")
            self.time_gap = timer()
        parseLogLines( self, logs_data )
        if self.less_output is False:
            self.printJobDone()
            self.printElapsedTime()
        
        if self.less_output is True:
            # continuation of the preventive output
            self.printJobDone()
        
        # check for the presence of older session statistics with the same date
        if self.auto_merge is False:
            checkSessionsDates( self )

        # from now on a failure will un-do any modification to the crapstats
        self.stage = 1
        
        if self.less_output is True:
            # next preventive output
            self.printJob("Updating statistics")
        else:
            print()

        # store session statistics
        if self.session_stats is True:
            if self.less_output is False:
                self.printJob("Storing session statistics")
            self.time_gap = timer()
            storeSessions( self )
            if self.less_output is False:
                self.printJobDone()
                self.printElapsedTime()

        # update global statistics
        if self.global_stats is True:
            if self.less_output is False:
                self.printJob("Updating global statistics")
            self.time_gap = timer()
            updateGlobals( self )
            if self.less_output is False:
                self.printJobDone()
                self.printElapsedTime()
        
        # finalize changes
        self.proceed = True
        if self.more_output is True:
            self.printJob("Finalizing changes")
        self.time_gap = timer()
        self.finalizeChanges()
        if self.proceed is True\
        and self.more_output is True:
            self.printJobDone()
            self.printElapsedTime()

        if self.less_output is True:
            # continuation of the preventive output
            self.printJobDone()
            # next preventive output
            if self.backup is True\
            or self.delete is True:
                self.printJob("Managing original log files")
        else:
            print()
        
        # 'proceed' will be used from now on
        # failures will only un-do further modifications
        self.undo_paths.clear()
        self.stage = 2
        
        # make a backup copy of the original logs used
        if self.backup is True:
            if self.less_output is False:
                self.printJob("Backing-up original log files")
            self.time_gap = timer()
            backupOriginals( self )
            if self.proceed is True\
            and self.less_output is False:
                self.printJobDone()
                self.printElapsedTime()
        
        # delete original logs used
        if self.delete is True:
            if self.proceed is False:
                print("{bold}{rose}Backup failed, skipping deletion{default}"
                    .format(**self.text_colors))
                if self.less_output is False:
                    print()
            else:
                if self.less_output is False:
                    self.printJob("Deleting original log files")
                self.time_gap = timer()
                self.removeOriginals()
                if self.proceed is True\
                and self.less_output is False:
                    self.printJobDone()
                    self.printElapsedTime()
        
        if self.less_output is True:
            # continuation of the preventive output
            if self.proceed is True\
            and (self.backup is True\
             or  self.delete is True):
                self.printJobDone()
            # next preventive output
            self.printJob("Finalizing")
        elif self.backup is True\
          or self.delete is True:
            print()
        
        # make a backup of the globals
        if self.global_stats is True:
            if self.more_output is True:
                self.printJob("Backing-up global statistics")
            self.time_gap = timer()
            backupGlobals( self )
            if self.proceed is True\
            and self.more_output is True:
                self.printJobDone()
                self.printElapsedTime()
        
        # final clean up
        if self.less_output is False:
            self.printJob("Cleaning up")
        self.time_gap = timer()
        # not a real need, I know
        self.finalCleanUp()
        if self.less_output is False:
            self.printJobDone()
            self.printElapsedTime()
        
        if self.proceed is True\
        and self.less_output is True:
            # continuation of the preventive output
            self.printJobDone()
        else:
            print()
        
        # fin
        self.exitMessage()
    


if __name__ == "__main__":
    failed = False
    craplog = Craplog( argv )
    try:
        # run craplog
        craplog.main()
    except (KeyboardInterrupt):
        failed = True
        if craplog.aborted is False:
            print()
            if craplog.more_output is True:
                print()
    except:
        failed = True
    finally:
        if failed is True:
            if craplog.aborted is False:
                try:
                    # failing succesfully
                    if len(craplog.undo_paths) > 0:
                        craplog.undoChanges()
                except:
                    # complete failure
                    pass
                finally:
                    craplog.exitAborted()
        # successful
        del craplog
    
