#!/usr/bin/python3

import os
import sys
import subprocess

from time import sleep
from time import perf_counter as timer

from crappy import aux
from crappy.check import makeInitialChecks, checkSessionsDates
from crappy.read  import collectLogLines
from crappy.parse import parseLogLines
from crappy.stats import updateGlobals, storeSessions


class Craplog(object):
    """
    Make ststistics from Apache2 logs
    """

    def__init__(self, args: list ):
        """
        Craplog's initializer
        """
        # variables from args
        self.use_arguments:  bool
        self.less_output:    bool
        self.more_output:    bool
        self.use_colors:     bool
        self.performance:    bool
        self.auto_delete:    bool
        self.auto_merge:     bool
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
        self.access_fields:  list
        self.ip_whitelist:   list
        # variables for jobs
        self.collection: dict
        self.undo_paths: list
        self.crappath: str
        self.statpath: str
        # variables for performance
        self.start_time:   float
        self.elapsed_time: float
        self.crap_time: float
        self.user_time: float
        self.total_size:  int
        self.parsed_size: int
        self.access_size: int
        self.errors_size: int
        # variables for messages
        self.text_colors:  dict
        self.MSG_elbarto:  str
        self.MSG_craplogo: str
        self.MSG_help:     str

        # initialize variables
        self.initVariables()
        self.initMessages()
        # parse arguments if not unset
        if self.use_arguments is True:
            self.parseArguments( args )


    def initVariables(self):
        """
        Initialize Craplog's variables
        This section can be manually edited to pre-set Craplog
          and avoid having to pass arguments every time
        """
        ###
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
        # SHOW HOW MUCH TIME DID THE JOB TAKE TO COMPLETE
        # [ -p  /  --performance ]
        self.performance = False
        #
        # USE COLORS WHEN PRINTING TEXT ON SCREEN
        # CAN BE DISABLED PASSING [ --no-colors ]
        self.use_colors = True
        #
        # AUTOMATICALLY DELETE FILES WHEN NEEDED
        # [ --auto-delete ]
        # USE WITH CAUTION
        # THIS APPLIES TO: ORIGINAL LOG FILES, CONFLICT FILES/FOLDERS
        self.auto_delete = False
        #
        # AUTOMATICALLY MERGE SESSIONS STATISTICS WITH THE SAME DATE
        # [ --auto-merge ]
        # IF A SESSION's DATE FROM THE STORED STATISTICS
        # EQUALS A DATE FROM THE PARSED LOGS FILES,
        # THEN MERGE THEM WITHOUT ASKING
        self.auto_merge = False
        #
        # MAKE SESSION STATISTICS
        # CAN BE DISABLED PASSING [ -gO  /  --only-globals ]
        self.session_stats = True
        #
        # UPDATE GLOBAL STATISTICS USING SESSION ONES
        # CAN BE DISABLED PASSING [ -gA  /  --avoid-globals ]
        self.global_stats = True
        #
        # MAKE SESSION STATISTICS FILES FROM ACCESS LOGS
        # [  ]
        # CAN BE DISABLED PASSING [ --only-errors ]
        self.access_logs = True
        #
        # MAKE SESSION STATISTICS FILES FROM ERROR LOGS
        # [ -e  /  --errors ]
        self.error_logs = False
        #
        # MAKE A BACKUP OF THE ORIGINAL LOG FILES
        # [ -b  /  --backup ]
        self.backup = False
        #
        # ARCHIVE THE BACKUP AS tar.gz
        # [ -bT  /  --backup-tar ]
        self.archive_tar = False
        #
        # ARCHIVE THE BACKUP AS zip
        # [ -bZ  /  --backup-zip ]
        self.archive_zip = False
        #
        # DELETE THE ORIGINAL LOG FILES WHEN DONE
        # [ -dO  /  --delete-originals ]
        self.delete = False
        #
        # MOVE FILES TO TRASH INSTEAD OF COMPLETELY REMOVE
        # [ --trash ]
        # DOESN'T APPLY TO CONFLICT FILES, WHICH WILL BE REMOVED (OR SHREDED)
        self.trash = False
        #
        # THE DIRECTORY USED AS TRASH BY YOUR SYSTEM
        # CAN BE PASSED FOLLOWING THE [ --trash ] OPTION
        # DEFAULT TO: ~/.local/share/Trash/files/
        self.trash_path = "~/.local/share/Trash/files/"
        #
        # SHRED FILES INSTEAD OF SIMPLE REMOVE
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
        # TRUE ONLY WHEN USING A CUSTOM LIST OF FILES FROM ARGUMENTS
        # [  ]
        self.file_selection = False
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
        ###


    def initMessages(self):
        """
        Bring message strings
        """
        self.text_colors = aux.colors()
        if self.use_colors is False:
            self.text_colors = aux.no_colors()
        self.MSG_elbarto  = aux.elbarto()
        self.MSG_craplogo = aux.craplogo()
        self.MSG_help     = aux.help( self.text_colors )
        self.MSG_craplog  = aux.craplog( self.text_colors )
        self.TXT_craplog  = "{red}C{orange}R{grass}A{cyan}P{blue}L{purple}O{white}G{default}\n".format(**self.text_colors)


    def parseArguments(self, args: list ):
        """
        Finalize Craplog's variables (if not manually unset)
        """
        n_args = len(sys.argv)-1
        i = 0
        while i < n_args:
            i += 1
            arg = sys.argv[i]
            if arg == "":
                continue
            # elB4RTO
            elif arg == "-elbarto-":
                print("\n%s\n" %( self.MSG_elbarto ))
            # help
            elif arg in ["help", "-h", "--help"]:
                print( "\n%s\n%s\n" %( self.MSG_craplogo, self.MSG_help ))
            # auxiliary arguments
            elif arg in ["-l", "--less"]:
                self.less_output = True
            elif arg in ["-m", "--more"]:
                self.more_output = True
            elif arg in ["-p", "--performance"]:
                self.performance = True
            elif arg in == "--no-colors":
                self.use_colors = False
            # automation arguments
            elif arg == "--auto-delete":
                self.auto_delete = True
            elif arg == "--auto-merge":
                self.auto_merge = True
            # job arguments
            elif arg in ["-e", "--errors"]:
                self.error_logs = True
            elif arg == "--only-errors":
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
                and not sys.argv[i+1].startswith("-"):
                    i += 1
                    self.trash_path = sys.argv[i]
            elif arg in ["-P", "--logs-path"]:
                if i+1 > n_args\
                or sys.argv[i+1].startswith("-"):
                    self.logs_path = ""
                else:
                    i += 1
                    self.logs_path = sys.argv[i]
            elif arg in ["-F", "--log-files"]:
                self.file_selection = True
                self.log_files = []
                while True:
                    if i+1 > n_args\
                    or sys.argv[i+1].startswith("-"):
                        break
                    else:
                        i += 1
                        self.log_files.append( sys.argv[i] )
            elif arg in ["-A", "--access-fields"]:
                self.access_fields = []
                while True:
                    if i+1 > n_args\
                    or sys.argv[i+1].startswith("-"):
                        break
                    else:
                        i += 1
                        self.access_fields.append( sys.argv[i] )
            elif arg in ["-W", "--ip-whitelist"]:
                self.ip_whitelist = []
                while True:
                    if i+1 > n_args\
                    or sys.argv[i+1].startswith("-"):
                        break
                    else:
                        i += 1
                        self.ip_whitelist.append( sys.argv[i] )
            else:
                print("{red}Error{white}[{grey}argument{white}]{red}>{default} not an available option: {orange}%s{default}"
                    %(arg)
                    .format(**self.text_colors))
                if self.more_output is True:
                    print("                 use {cyan}craplog --help{default} to view an help screen"
                        .format(**self.text_colors))
                exit("")


    def welcomeMessage(self):
        """
        Print the welcome message
        """
        print("Use {cyan}craplog --help{default} to view an help screen"
            .format(**self.text_colors))
        if auto_delete is True:
            print("{yellow}Auto-Delete{default} is {bold}ON{default}"
                .format(**self.text_colors))
        self.start_time += 1
        print()
        sleep(1)


    def printJob(self, message: str ):
        """
        Print a job-relative message
        """
        print("%s {white}...{default} "
            %( message )
            .format(**self.text_colors), end="")


    def printJobDone(self):
        """
        Print the job is done
        """
        print("{green}Done{default}"
            .format(**self.text_colors))


    def printJobFailed(self):
        """
        Print the job is done
        """
        print("{rose}Failed{default}"
            .format(**self.text_colors))


    def printElapsedTime(self, time_gap: float ):
        """
        Print the time elapsed since the last gap
        """
        if  self.more_output is True\
        and self.performance is True:
            print("{purple}elapsed time{default}: %.2f s"
                %( timer() - time_gap )
                .format(**self.text_colors)))


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
        item   = path[len(parent)+1:]
        # check the type
        return_code = 0
        if os.path.isfile( path ):
            # is a file
            if self.trash is True:
                return_code = subprocess.run(
                    ["mv", path, self.trash_path],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
            elif self.shred is True:
                return_code = subprocess.run(
                    ["shred", "-uvz", path],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
            else:
                return_code = subprocess.run(
                    ["rm", path],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)

            if return_code == 1:
                print("\n{red}Error{white}[{grey}file{white}]{red}>{default} unable to %s this file%s: {green}%s/{orange}%s{default}"
                    %( parent, item, del_mode, del_mode_aux )
                    .format(**self.text_colors))
                if self.more_output is True:
                    print("               the error is most-likely caused by a lack of permissions")
                    print("               please proceed manually")
                print()

        elif os.path.isdir( path ):
            # is a folder
            if self.trash is True:
                return_code = subprocess.run(
                    ["mv", path, self.trash_path],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
            else:
                if self.shred is True:
                    # recursively rename the folder with zeroes
                    new_name = "0"*(len(item))
                    if len(new_name) < 4:
                        new_name = "0"*4
                    new_path = path
                    while len(new_name) > 1:
                        old_path = new_path
                        new_name = "0"*(len(new_name)-1)
                        new_path = "%s/%s" %( parent, new_name )
                        return_code = subprocess.run(
                            ["mv", path, new_path],
                            check=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)
                        if return_code != 0:
                            break
                    path = new_path
                if return_code == 0:
                    # delete the folder
                    return_code = subprocess.run(
                        ["rmdir", path],
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)

            if return_code == 1:
                print("\n{red}Error{white}[{grey}folder{white}]{red}>{default} unable to %s this directory%s: {green}%s/{orange}%s{default}"
                    %( parent, item, del_mode, del_mode_aux )
                    .format(**self.text_colors))
                if self.more_output is True:
                    print("               the error is most-likely caused by a non-empty folder")
                    print("               or by a lack of permissions")
                    print("               please manually remove it and retry")
                print()
        else:
            # unknown type
            print("\n{red}Error{white}[{grey}type{white}]{red}>{default} the entry is not a directory, nor a file: {green}%s/{orange}%s{default}"
                %( parent, item )
                .format(**self.colors))
            if self.more_output is True:
                print("             ok, that was unexpected")
                print("             please manually check it and consider reporting this issue")
            print()


    def undoChanges(self):
        """
        Un-do changes after a failure
        """
        for path in undo_paths[::-1]:
            if path.endswith(".bak"):
                # delete the new file and restore the backup
            else:
                # delete the newly created entry


    def finalizeChanges(self):
        """
        Finalize changes if exiting successfully
        """
        for path in undo_paths:
            if path.endswith(".bak"):
                # delete the backups


    def main(self):
        """
        Make Craplog do its job
        """
        # CRAPLOG
        if self.less_output is False:
            print("\n%s\n" %( self.MSG_craplog ))
        else:
            print("%s\n" %( self.TXT_craplog ))
        self.start_time = timer()
        # get craplog's path
        self.crappath = os.path.abspath(__file__)
        self.crappath = self.crappath[:self.crappath.rfind('/craplog.py')]
        self.statpath = "%s/crapstats" %(crappath)
        # make initial checkings
        makeInitialChecks( self )
        # welcome message
        if self.less_output is False:
            self.welcomeMessage()

        # read logs files
        if self.more_output is True:
            self.printJob("Reading logs")
            time_gap = timer()
        logs_data = collectLogLines( self )
        if self.more_output is True:
            self.printJobDone()
            self.printElapsedTime( time_gap )

        # parse logs lines
        self.printJob("Parsing logs")
        time_gap = timer()
        parseLogLines( self, logs_data )
        self.printJobDone()
        self.printElapsedTime( time_gap )

        # check for the presence of older session statistics with the same date
        if self.auto_merge is False:
            checkSessionsDates( self )

        self.undo_paths = []
        if self.less_output is True:
            # preventive output
            self.printJob("Updating statistics")

        # store session statistics
        if self.session_stats is True:
            if self.less_output is False:
                self.printJob("Storing session statistics")
            time_gap = timer()
            storeSessions( self )
            self.printJobDone()
            self.printElapsedTime( time_gap )

        # update global statistics
        if self.global_stats is True:
            if self.less_output is False:
                self.printJob("Updating global statistics")
            time_gap = timer()
            updateGlobals( self )
            self.printJobDone()
            self.printElapsedTime( time_gap )

        if self.less_output is True:
            # continuation of the preventive output
            self.printJobDone()




if __name__ == "__main__":
    craplog = Craplog( sys.argv )
    craplog.main()
