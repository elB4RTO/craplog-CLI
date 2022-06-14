
import os
from time import perf_counter as timer

def checkPathRecursively(
    path: str,
    colors: dict,
    result: bool=False
):
    """
    Check a Path recursively (existence of every element)
    """
    test_path = ""
    colored_path = ""
    checks_passed = True
    if path.endswith("/"):
        path = path.rstrip("/")
    path_slices = path.split('/')
    for path_slice in path_slices:
        if path_slice == ".":
            if len(test_path) == 0:
                test_path += path_slice
                if os.path.exists( test_path ) is True:
                    colored_path += "{grass}.{default}".format(**colors)
                else:
                    checks_passed = False
                    colored_path += "{rose}.{default}".format(**colors)
        elif path_slice != "":
            test_path += "/%s" %(path_slice)
            if  checks_passed is True\
            and os.path.exists( test_path ) is True:
                colored_path += "/{grass}%s{default}"\
                    .format(**colors)\
                    %(path_slice)
            else:
                checks_passed = False
                colored_path += "/{rose}%s{default}"\
                    .format(**colors)\
                    %(path_slice)
    # return the results
    if result is True:
        return (checks_passed, colored_path)
    else:
        return colored_path



def chooseAction(
    craplog: object
) -> int :
    """
    Choice form
    """
    choice = 0
    MSG_choice = """Available choices:
  - {grey}[{default}{bold}d{grey}]{default}   {bold}delete{default} the conflict accordingly to the settings
  - {grey}[{default}{bold}r{grey}]{default}   {bold}rename{default} the conflict with a trailing '{italic}.copy{default}'
  - {grey}[{default}{bold}h{grey}]{default}   print this {bold}help{default} screen
  - {grey}[{default}{bold}q{grey}]{default}   abort the process and {bold}quit{default} craplog\
  """.format(**craplog.text_colors)
    time_gap = timer()
    while True:
        if craplog.less_output is False:
            print(MSG_choice)
            if craplog.more_output is True:
                print()
        proceed = input("Your choice? {white}[{yellow}d{grey}/{azul}r{grey}/{green}h/{rose}q{white}] :{default} "\
            .format(**craplog.text_colors)).strip().lower()
        if proceed in ["q","quit","exit"]:
            choice = 0
            break
        elif proceed in ["d","del","delete"]:
            choice = 1
            break
        elif proceed in ["r","rename"]:
            choice = 2
            break
        elif proceed in ["h","help"]:
            if craplog.less_output is True:
                print(MSG_choice)
            else:
                print()
        else:
            # leave this normal yellow, it's secondary and doesn't need real attention
            print("\n{warn}Warning{white}[{grey}choice{white}]{yellow}>{default} not a valid choice: {bold}%s{default}"\
                .format(**craplog.text_colors))
            if craplog.less_output is False:
                print()
    if craplog.less_output is False:
        print()
    if choice > 0:
        craplog.reprintJob()
    # set the time elapsed during user's decision as user-time
    craplog.user_time += timer() - time_gap
    return choice


def conflictFolder(
    craplog: object,
    path: str,
    parent_path: str,
    item_name: str
) -> int :
    """
    Ask the user what to do with the conflict
    """
    craplog.printJobHalted()
    if craplog.more_output is True:
        print("\n")
    elif craplog.less_output is False:
        print()
    print("{warn}Warning{white}[{grey}conflict{white}]{warn}>{default} a folder is in conflict with the process: {grass}%s/{yellow}%s{default}"\
        .format(**craplog.text_colors)\
        %( parent_path, item_name ))
    if craplog.more_output is True:
        print("""\
                the entry was supposed to be a file, but it was found to be a folder
                if you haven't made any changes, please report this issue""")
    if craplog.less_output is False:
        print()
    return chooseAction( craplog )


def conflictFile(
    craplog: object,
    path: str,
    parent_path: str,
    item_name: str
) -> int :
    """
    Ask the user what to do with the conflict
    """
    craplog.printJobHalted()
    if craplog.more_output is True:
        print("\n")
    elif craplog.less_output is False:
        print()
    print("{warn}Warning{white}[{grey}conflict{white}]{warn}>{default} a file is in conflict with the process: {grass}%s/{yellow}%s{default}"\
        .format(**craplog.text_colors)\
        %( parent_path, item_name ))
    if craplog.more_output is True:
        print("""\
                the entry was supposed to be a folder, but it was found to be a file
                if you haven't made any changes, please report this issue""")
    if craplog.less_output is False:
        print()
    return chooseAction( craplog )


def checkFolder(
    craplog: object,
    err_key: str,
    path:    str,
    parent_path: str="",
    entry_name:  str="",
    r: bool=False,
    w: bool=False,
    create:  bool=False,
    resolve: bool=False
) -> bool :
    """
    Check a crapstats folder
    """
    def failed():
        nonlocal checks_passed, craplog
        if checks_passed is True:
            checks_passed = False
            craplog.printJobFailed()
    def makeit():
        nonlocal err_key, path, parent_path, entry_name, spaces, craplog
        # make the directory
        try:
            os.mkdir( path )
            craplog.undo_paths.append( path )
        except:
            # error creating directory
            failed()
            print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} unable to create the directory: {grass}%s/{rose}%s{default}"\
                .format(**craplog.text_colors)\
                %( err_key, parent_path, entry_name ))
            if craplog.more_output is True:
                print("%s         the error is most-likely caused by a lack of permissions" %(spaces))
                print("%s         please add read/write permissions to the whole crapstats folder and retry" %(spaces))
            print()
    if entry_name == ""\
    or parent_path == "":
        parent_path = path[:path.rfind('/')]
        entry_name  = path[len(parent_path)+1:]
    # checking
    checks_passed = True
    if os.path.exists( path ):
        # already exists
        if os.path.isdir( path ):
            # is a directory
            if r is True\
            and os.access( path, os.R_OK ) is False:
                failed()
                print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} directory is not readable: {grass}%s/{rose}%s{default}"\
                    .format(**craplog.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if craplog.more_output is True:
                    spaces = " "*len(err_key)
                    print("%s         craplog doesn't have permissions to read from files inside this folder" %(spaces))
                    print("%s         please make the directory readable and retry" %(spaces))
                print()
            if w is True\
            and os.access( path, os.W_OK ) is False:
                failed()
                print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} directory is not writable: {grass}%s/{rose}%s{default}"\
                    .format(**craplog.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if craplog.more_output is True:
                    spaces = " "*len(err_key)
                    print("%s         craplog doesn't have permissions to write on files inside this folder" %(spaces))
                    print("%s         please make the directory writable and retry" %(spaces))
                print()
        else:
            # not a directory
            if os.path.isfile( path ):
                if resolve is True:
                    # resolve the conflict
                    choice = 0
                    if craplog.auto_delete is True:
                        choice = 1
                    else:
                        choice = conflictFile( craplog, path, parent_path, entry_name )
                    if choice == 1:
                        # delete the file and make a dir
                        craplog.removeEntry( path )
                        if create is True:
                            makeit()
                    elif choice == 2:
                        # rename the file and make a dir
                        try:
                            new_path = path
                            while True:
                                new_path += ".copy"
                                if os.path.exists( new_path ) is False:
                                    break
                            os.rename( path, new_path )
                            if create is True:
                                makeit()
                        except:
                            failed()
                            print("\n{err}Error{white}[{grey}permissions{white}]{red}>{default} unable to rename file: {grass}%s/{rose}%s{default}"\
                                .format(**craplog.text_colors)\
                                %( parent_path, entry_name ))
                            if craplog.more_output is True:
                                print("                    the error is most-likely caused by a lack of permissions")
                                print("                    please add permissions and retry, or intervene manually")
                            print()
                    else:
                        failed()
                        print("\n{err}Error{white}[{grey}variable{white}]{red}>{default} the choice has an invalid value: {rose}%s{default}"\
                            .format(**craplog.text_colors)\
                            %( choice ))
                        if craplog.more_output is True:
                            print("                 {white}@ {bold}craplog.crappy.check.checkFolder(){default}")
                            print("                 please consider reporting this issue")
                        print()
                else:
                    # do not resolve the conflict, print a message
                    failed()
                    print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} the given path doens't point to a directory: {grass}%s/{rose}%s{default}"\
                        .format(**craplog.text_colors)\
                        %( err_key, parent_path, entry_name ))
                    if craplog.more_output is True:
                        spaces = " "*len(err_key)
                        print("%s         the entry was supposed to be a folder, but it was found to be a file" %(spaces))
                    print()
                    
            else:
                # unknown type
                failed()
                print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a directory, nor a file: {grass}%s/{rose}%s{default}"\
                    .format(**craplog.text_colors)\
                    %( parent_path, entry_name ))
                if craplog.more_output is True:
                    print("             ok, that was unexpected")
                    print("             please manually check it and consider reporting this issue")
                print()
    else:
        # does not exists
        if create is True:
            try:
                os.mkdir( path )
                craplog.undo_paths.append( path )
            except:
                # error creating directory
                failed()
                print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} unable to create the directory: {grass}%s/{rose}%s{default}"\
                    .format(**craplog.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if craplog.more_output is True:
                    print("%s         the error is most-likely caused by a lack of permissions" %(spaces))
                    print("%s         please add read/write permissions to the whole crapstats folder and retry" %(spaces))
                print()
        elif create is False:
            failed()
            print("\n{err}Error{white}[{grey}path{white}]{red}>{default} the given path does not exist: %s\n"\
                .format(**craplog.text_colors)\
                %( checkPathRecursively( path, craplog.text_colors ) ))
        else:
            # when None, return a failure if doesn't exist
            checks_passed = False
    return checks_passed


def checkFile(
    craplog: object,
    err_key: str,
    path:    str,
    parent_path: str="",
    entry_name:  str="",
    r: bool=False,
    w: bool=False,
    create:  bool=False,
    resolve: bool=False
) -> bool :
    """
    Check a crapstats file
    """
    def failed():
        nonlocal checks_passed, craplog
        if checks_passed is True:
            checks_passed = False
            craplog.printJobFailed()
    
    if entry_name == ""\
    or parent_path == "":
        parent_path = path[:path.rfind('/')]
        entry_name  = path[len(parent_path)+1:]
    # checking
    checks_passed = True
    if os.path.exists( path ):
        # already exists
        if os.path.isfile( path ):
            # is a file
            if r is True\
            and os.access( path, os.R_OK ) is False:
                failed()
                print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} file is not readable: {grass}%s/{rose}%s{default}"\
                    .format(**craplog.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if craplog.more_output is True:
                    spaces = " "*len(err_key)
                    print("%s         craplog doesn't have permissions to read from this file" %(spaces))
                    print("%s         please make the file readable and retry" %(spaces))
                print()
            if w is True\
            and os.access( path, os.W_OK ) is False:
                failed()
                print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} file is not writable: {grass}%s/{rose}%s{default}"\
                    .format(**craplog.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if craplog.more_output is True:
                    spaces = " "*len(err_key)
                    print("%s         craplog doesn't have permissions to write in this file" %(spaces))
                    print("%s         please make the file writable and retry" %(spaces))
                print()
        else:
            # not a file
            if os.path.isdir( path ):
                if resolve is True:
                    choice = 0
                    if craplog.auto_delete is True:
                        choice = 1
                    else:
                        choice = conflictFolder( craplog, path, parent_path, entry_name )
                    if choice == 1:
                        # delete the dir
                        craplog.removeEntry( path )
                    elif choice == 2:
                        # rename the file and make a dir
                        try:
                            new_path = path
                            while True:
                                new_path += ".copy"
                                if os.path.exists( new_path ) is False:
                                    break
                            os.rename( path, new_path )
                        except:
                            failed()
                            print("\n{err}Error{white}[{grey}permissions{white}]{red}>{default} unable to rename folder: {grass}%s/{rose}%s{default}"\
                                .format(**craplog.text_colors)\
                                %( parent_path, entry_name ))
                            if craplog.more_output is True:
                                print("                    the error is most-likely caused by a lack of permissions")
                                print("                    please add permissions and retry, or intervene manually")
                            print()
                    else:
                        failed()
                        print("\n{err}Error{white}[{grey}variable{white}]{red}>{default} the choice has an invalid value: {rose}%s{default}"\
                            .format(**craplog.text_colors)\
                            %( choice ))
                        if craplog.more_output is True:
                            print("                 {white}@ {bold}craplog.crappy.check.checkFile(){default}")
                            print("                 please consider reporting this issue")
                        print()
                else:
                    # do not resolve the conflict, print a message
                    failed()
                    print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} the given path doens't point to a file: {grass}%s/{rose}%s{default}"\
                        .format(**craplog.text_colors)\
                        %( err_key, parent_path, entry_name ))
                    if craplog.more_output is True:
                        spaces = " "*len(err_key)
                        print("%s         the entry was supposed to be a file, but it was found to be a folder" %(spaces))
                    print()
            else:
                # unknown type
                failed()
                print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a file, nor a directory: {grass}%s/{rose}%s{default}"\
                    .format(**craplog.text_colors)\
                    %( parent_path, entry_name ))
                if craplog.more_output is True:
                    print("             ok, that was unexpected")
                    print("             please manually check it and consider reporting this issue")
                print()
    else:
        # does not exists
        if create is True:
            # ..yet, will be created later in any case
            pass
        else:
            # ..but should have existed, print an error message
            failed()
            print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} the given path does not exist: %s\n"\
                .format(**craplog.text_colors)\
                %( err_key, checkPathRecursively( path, craplog.text_colors ) ))
    return checks_passed


def makeInitialChecks( craplog ):
    """
    Perform safety checks before to start:
      - check internal variables for correctness/conflicts
      - check files/folders for existence and ability to read/write
    """
    def failed():
        nonlocal checks_passed, craplog
        if checks_passed is True:
            checks_passed = False
            craplog.printJobFailed()
    
    checks_passed = True

    # variables' integrity
    if  craplog.session_stats is False\
    and craplog.global_stats is False:
        failed()
        print("\n{err}Error{white}[{grey}options_conflict{white}]{red}>{default} you can't use {cyan}--only-globals{default} toghether with {cyan}--avoid-globals{default}\n"\
            .format(**craplog.text_colors))
    if  craplog.access_logs is False\
    and craplog.error_logs is False:
        failed()
        print("\n{err}Error{white}[{grey}variables_conflict{white}]{red}>{default} you can't avoid using both access and error log files, nothing will be done\n"\
            .format(**craplog.text_colors))
    if  craplog.access_logs is True\
    and len(craplog.access_fields) == 0:
        failed()
        print("\n{err}Error{white}[{grey}missing_argument{white}]{red}>{default} you must use at least one field when working on access_logs\n"\
            .format(**craplog.text_colors))
    if  craplog.archive_tar is True\
    and craplog.archive_zip is True:
        failed()
        print("\n{err}Error{white}[{grey}options_conflict{white}]{red}>{default} you can't use {cyan}--archive-tar{default} toghether with {cyan}--archive-zip{default}\n"\
            .format(**craplog.text_colors))
    if craplog.backup is False\
    and (craplog.archive_tar is True\
      or craplog.archive_zip is True):
        failed()
        print("\n{err}Error{white}[{grey}options_conflict{white}]{red}>{default} you can't archive a backup if you don't make one\n"\
            .format(**craplog.text_colors))
    if  craplog.trash is True\
    and craplog.shred is True:
        failed()
        print("\n{err}Error{white}[{grey}options_conflict{white}]{red}>{default} you can't use {cyan}--trash{default} toghether with {cyan}--shred{default}\n"\
            .format(**craplog.text_colors))
    if  craplog.less_output is True\
    and craplog.more_output is True:
        failed()
        print("\n{err}Error{white}[{grey}options_conflict{white}]{red}>{default} you can't use {cyan}--less{default} toghether with {cyan}--more{default}\n"\
            .format(**craplog.text_colors))

    # logs folder
    if craplog.logs_path.endswith("/"):
        craplog.logs_path = craplog.logs_path[:-1]
    if craplog.logs_path == "":
        failed()
        print("\n{err}Error{white}[{grey}missing_argument{white}]{red}>{default} you must set a path after {cyan}-P{default}/{cyan}--logs_path{default}\n"\
            .format(**craplog.text_colors)\
            %(craplog.logs_path))
    else:
        if craplog.logs_path.startswith('~/'):
            craplog.logs_path = "%s/%s" %( os.environ['HOME'], craplog.logs_path[2:] )
        craplog.logs_path = os.path.abspath( craplog.logs_path )
    if checkFolder( craplog, "logs_folder", craplog.logs_path, r=True ) is False:
        failed()

    # log files
    if craplog.max_file_size is None:
        failed()
        print("\n{err}Error{white}[{grey}missing_arguments{white}]{red}>{default} you must set the size after {cyan}--max-size{default}\n"\
            .format(**craplog.text_colors))
    else:
        try:
            craplog.max_file_size = float(craplog.max_file_size)
            if craplog.max_file_size < 0:
                failed()
                print("\n{err}Error{white}[{grey}invalid_size{white}]{red}>{default} the max size must be greater or equal to 0\n"\
                    .format(**craplog.text_colors))
            elif craplog.max_file_size > 1000000:
                failed()
                print("\n{err}Error{white}[{grey}invalid_size{white}]{red}>{default} the given max size is huge: {yellow}%.2f GB{default}\n"\
                    .format(**craplog.text_colors)
                    %( craplog.max_file_size / 1024 ))
                if craplog.less_output is False:
                    print("                     use 0 to have it unlimited")
        except:
            failed()
            print("\n{err}Error{white}[{grey}invalid_argument{white}]{red}>{default} invalid value for {cyan}--max-size{default}: {rose}%s{default}\n"\
                .format(**craplog.text_colors)
                %( craplog.max_file_size ))
    if craplog.file_selection is False:
        if craplog.access_logs is False:
            craplog.log_files.clear()
        if craplog.error_logs is True:
            craplog.log_files.append("error.log.1")
    if len(craplog.log_files) == 0:
        failed()
        print("\n{err}Error{white}[{grey}missing_arguments{white}]{red}>{default} you must set at least one file name after {cyan}--log-files{default}\n"\
            .format(**craplog.text_colors))
    for file_name in craplog.log_files:
        if file_name.find(".log.") < 0:
            failed()
            print("\n{err}Error{white}[{grey}invalid_name{white}]{red}>{default} you have inserted an invalid file name: {rose}%s{default}"\
                .format(**craplog.text_colors)\
                %( file_name ))
            if craplog.more_output is True:
                print("                     files not containing '.log.' in their name won't be used")
                print("                     please refer to the README.md for more informations")
            break
        elif craplog.log_files.count( file_name ) > 1:
                failed()
                print("\n{err}Error{white}[{grey}duplicate_argument{white}]{red}>{default} you have inserted the same file name twice: {rose}%s{default}\n"\
                    .format(**craplog.text_colors)\
                    %( file_name ))
                break
        file_path = "%s/%s" %( craplog.logs_path, file_name )
        if checkFile( craplog, "log_file", file_path, r=True ) is False:
            failed()

    # trash folder
    if craplog.trash is True:
        if craplog.trash_path.startswith('~/'):
            craplog.trash_path = "%s/%s" %( os.environ['HOME'], craplog.trash_path[2:] )
        craplog.trash_path = os.path.abspath( craplog.trash_path )
        if checkFolder( craplog, "trash", craplog.trash_path, w=True ) is False:
            failed()

    # crapstats main folder
    if checks_passed is True:
        if checkFolder( craplog, "stats_folder", craplog.statpath, r=True, w=True, create=True ) is False:
            failed()
    # global stats folder
    if  checks_passed is True\
    and craplog.global_stats is True:
        path = "%s/globals" %( craplog.statpath )
        if checkFolder( craplog, "stats_folder", path, r=True, w=True, create=True ) is False:
            failed()
    # sessions stats folder
    if  checks_passed is True\
    and craplog.session_stats is True:
        path = "%s/sessions" %( craplog.statpath )
        if checkFolder( craplog, "stats_folder", path, r=True, w=True, create=True ) is False:
            failed()
    # access stats folder
    if  checks_passed is True\
    and craplog.access_logs is True:
        path = "%s/sessions/access" %( craplog.statpath )
        if checkFolder( craplog, "stats_folder", path, r=True, w=True, create=True ) is False:
            failed()
    # error stats folder
    if  checks_passed is True\
    and craplog.error_logs is True:
        path = "%s/sessions/error" %( craplog.statpath )
        if checkFolder( craplog, "stats_folder", path, r=True, w=True, create=True ) is False:
            failed()

    # access logs fields
    if craplog.access_logs is True:
        for field in craplog.access_fields:
            if craplog.access_fields.count( field ) > 1:
                    failed()
                    print("\n{err}Error{white}[{grey}duplicate_argument{white}]{red}>{default} you have inserted the same field twice: {rose}%s{default}\n"\
                        .format(**craplog.text_colors)\
                        %( field ))
                    break
            elif field not in ["IP","UA","REQ","RES"]:
                failed()
                print("\n{err}Error{white}[{grey}invalid_field{white}]{red}>{default} invalid field for access logs: {rose}%s{default}"\
                    .format(**craplog.text_colors)\
                    %( field ))
                if craplog.more_output is True:
                    print("""\
                      available fields:
                        - {bold}IP{default}   {italic}IP address of the client{default}
                        - {bold}UA{default}   {italic}User-agent of the client{default}
                        - {bold}REQ{default}  {italic}Request made by the client{default}
                        - {bold}RES{default}  {italic}Response code from the server{default}"""\
                        .format(**craplog.text_colors))
                print()
    
    # IPs whitelist
    for ip in craplog.ip_whitelist:
        fc = ip[0]
        if craplog.ip_whitelist.count( ip ) > 1:
                failed()
                print("\n{err}Error{white}[{grey}duplicate_argument{white}]{red}>{default} you have inserted the same IP twice: {rose}%s{default}\n"\
                    .format(**craplog.text_colors)\
                    %( ip ))
                break
        # check the first character, trying to support IPv6 chars
        else:
            try:
                # verify if it is a hexadecimal char
                assert int(fc,16)
            except:
                # verify validity
                if not( fc == ":"\
                     or fc.isdigit() is True):
                    # useless to keep, it will just slow down the process
                    failed()
                    print("\n{err}Error{white}[{grey}invalid_sequence{white}]{red}>{default} you have inserted an invalid IP sequence: {rose}%s{default}"\
                        .format(**craplog.text_colors)\
                        %( ip ))
                    if craplog.more_output is True:
                        print("""\
                                 the sequence is invalid since no IP will ever start like that
                                 keeping this sequence will just slow down the process of parsing lines""")
                    print()
                    break

    # exit if at least one error occured
    if checks_passed is False:
        craplog.exitAborted()


def checkSessionsDates( craplog ):
    """
    Check every collected date for a match in older sessions dates
    """
    if os.path.exists( "%s/sessions" %(craplog.statpath) ):
        conflicts = { 'access':[], 'error':[] }
        for log_type, dates in craplog.collection.items():
            if os.path.exists( "%s/sessions/%s" %(craplog.statpath, log_type) ) is False:
                continue
            for date in dates.keys():
                year, month, day = date.split('-')
                path = "%s/sessions/%s/%s/%s/%s" %(craplog.statpath, log_type, year, month, day)
                if os.path.exists(path):
                    conflicts[log_type].append(date)
        if len(conflicts['access']) > 0\
        or len(conflicts['error']) > 0:
            time_gap = timer()
            if craplog.less_output is False:
                print()
            while True:
                print("{warn}Warning{white}[{grey}merge{white}]{warn}>{default} one or more logs' dates match with the already stored sessions"\
                    .format(**craplog.text_colors))
                if craplog.more_output is True:
                    # print found conflicts
                    for log_type, dates in conflicts.items():
                        if len(dates) > 0:
                            print("                dates from {bold}%s{default} logs:"\
                                .format(**craplog.text_colors)\
                                %( log_type ))
                            for date in dates:
                                print("                   - {yellow}%s{default}"\
                                    .format(**craplog.text_colors)\
                                    %( date ))
                if craplog.less_output is False:
                    print("\nIf you choose to proceed, statistics will be {bold}mergerd{default}"\
                        .format(**craplog.text_colors))
                    if craplog.more_output is True:
                        print("Please make sure you're not parsing the same files twice\n")
                proceed = input("Continue? {white}[{grass}y{grey}/{red}n{white}] :{default} "\
                    .format(**craplog.text_colors)).strip().lower()
                if proceed in ["y","yes"]:
                    break
                elif proceed in ["n","no"]:
                    if len(craplog.undo_paths) > 0:
                        craplog.undoChanges()
                    craplog.exitAborted()
                else:
                    print("\n{warn}Warning{white}[{grey}choice{white}]{warn}>{default} not a valid choice: {bold}%s{default}"\
                        .format(**craplog.text_colors))
                    if craplog.less_output is False:
                        print()
            # set the time elapsed during user's decision as user-time
            craplog.user_time += timer() - time_gap

