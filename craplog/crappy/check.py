
import os
from time import perf_counter as timer

def checkPathRecursively(
    path: str,
    colors: dict,
    result: bool=False
):
    """
    Check a Path recursively (every element)
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
                if os.exists( test_path ) is True:
                    colored_path += "{green}.{default}".format(**colors)
                else:
                    checks_passed = False
                    colored_path += "{orange}.{default}".format(**colors)
        elif path_slice != "":
            test_path += "/%s" %(path_slice)
            if  checks_passed is True\
            and os.exists( test_path ) is True:
                colored_path += "/{green}%s{default}"
                    %(path_slice)
                    .format(**colors)
            else:
                checks_passed = False
                colored_path += "/{orange}%s{default}"
                    %(path_slice)
                    .format(**colors)
    # return the results
    result_path = colored_path
    if colored is False:
        result_path = test_path
    if result is True:
        return (checks_passed, result_path)
    else:
        return result_path


def checkFolder(
    path:    str,
    err_key: str,
    colors:  dict,
    r: bool=False,
    w: bool=False
) -> bool :
    """
    Do basic usability checks on a folder
    """
    checks_passed = True
    parent_path = path[:path.rfind("/")]
    dir_name = path[path.rfind("/")+1:]
    if os.path.exists( path ) is False:
        checks_passed = False
        print("\n{red}Error{white}[{grey}path{white}]{red}>{default} the given path does not exist: %s\n"
            %( checkPathRecursively( path, colors ) )
            .format(**colors))
    elif os.path.isdir( path ) is False:
        checks_passed = False
        print("\n{red}Error{white}[{grey}%s{white}]{red}>{default} the given path doens't point to a directory: {green}%s/{orange}%s{default}\n"
            %( err_key, parent_path, dir_name )
            .format(**colors))
    else:
        if  r is True\
        and os.access( path, os.R_OK ) is False:
            checks_passed = False
            print("\n{red}Error{white}[{grey}%s{white}]{red}>{default} directory is not readable: {green}%s/{orange}%s{default}"
                %( err_key, parent_path, dir_name )
                .format(**colors))
            if craplog.more_output is True:
                spaces = " "*len(err_key)
                print("%s         craplog doesn't have permissions to read from files inside this folder" %(spaces))
                print("%s         please make the directory readable and retry" %(spaces))
            print()
        if  w is True\
        and os.access( path, os.W_OK ) is False:
            checks_passed = False
            print("\n{red}Error{white}[{grey}%s{white}]{red}>{default} directory is not writable: {green}%s/{orange}%s{default}"
                %( err_key, parent_path, dir_name )
                .format(**colors))
            if craplog.more_output is True:
                print("%s         craplog doesn't have permissions to write on files inside this folder" %(spaces))
                print("%s         please make the directory writable and retry" %(spaces))
            print()
    return checks_passed


def checkFile(
    path:    str,
    err_key: str,
    colors:  dict,
    r: bool=False,
    w: bool=False
) -> bool :
    """
    Do basic usability checks on a file
    """
    checks_passed = True
    parent_path = path[:path.rfind("/")]
    file_name = path[path.rfind("/")+1:]
    if os.path.exists( path ) is False:
        checks_passed = False
        print("\n{red}Error{white}[{grey}path{white}]{red}>{default} the given path %s does not exist\n"
            %( checkPathRecursively( path, colors ) )
            .format(**colors))
    elif os.path.isfile( path ) is False:
        checks_passed = False
        print("\n{red}Error{white}[{grey}%s{white}]{red}>{default} the given path {green}%s/{orange}%s{default} doesn't point to a file\n"
            %( err_key, parent_path, file_name )
            .format(**colors))
    else:
        if  r is True\
        and os.access( path, os.R_OK ) is False:
            checks_passed = False
            print("\n{red}Error{white}[{grey}%s{white}]{red}>{default} file is not readable: {green}%s/{orange}%s{default}"
                %( err_key, parent_path, file_name )
                .format(**colors))
            if craplog.more_output is True:
                print("%s         craplog doesn't have permissions to read from this file" %(spaces))
                print("%s         please make the file readable and retry" %(spaces))
            print()
        if  w is True\
        and os.access( path, os.W_OK ) is False:
            checks_passed = False
            print("\n{red}Error{white}[{grey}%s{white}]{red}>{default} file is not writable: {green}%s/{orange}%s{default}"
                %( err_key, parent_path, file_name )
                .format(**colors))
            if craplog.more_output is True:
                print("%s         craplog doesn't have permissions to write in this file" %(spaces))
                print("%s         please make the file writable and retry" %(spaces))
            print()
    return checks_passed


def makeInitialChecks( craplog ):
    """
    Perform safety checks before to start:
      - check internal variables for correctness/conflicts
      - check files/folders for existence and ability to read/write
    """
    checks_passed = True

    # variables' integrity
    if  craplog.session_stats is False\
    and craplog.global_stats is False:
        checks_passed = False
        print("\n{red}Error{white}[{grey}options_conflict{white}]{red}>{default} you can't use {cyan}--only-globals{default} toghether with {cyan}--avoid-globals{default}\n"
            .format(**craplog.text_colors))
    if  craplog.access_logs is False\
    and craplog.error_logs is False:
        checks_passed = False
        print("\n{red}Error{white}[{grey}variables_conflict{white}]{red}>{default} you can't avoid using both access and error log files, nothing will be done\n"
            .format(**craplog.text_colors))
    if  craplog.access_logs is True\
    and len(craplog.access_fields) == 0:
        checks_passed = False
        print("\n{red}Error{white}[{grey}missing_argument{white}]{red}>{default} you must use at least one field when working on access_logs\n"
            .format(**craplog.text_colors))
    if  craplog.trash is True\
    and craplog.shred is True:
        checks_passed = False
        print("\n{red}Error{white}[{grey}options_conflict{white}]{red}>{default} you can't use {cyan}--trash{default} toghether with {cyan}--shred{default}\n"
            .format(**craplog.text_colors))
    if  craplog.less_output is True\
    and craplog.more_output is True:
        checks_passed = False
        print("\n{red}Error{white}[{grey}options_conflict{white}]{red}>{default} you can't use {cyan}--less{default} toghether with {cyan}--more{default}\n"
            .format(**craplog.text_colors))

    # logs folder
    if craplog.logs_path.endswith("/"):
        craplog.logs_path = craplog.logs_path[:-1]
    if craplog.logs_path == "":
        checks_passed = False
        print("\n{red}Error{white}[{grey}missing_argument{white}]{red}>{default} you must set a path after {cyan}-P{default}/{cyan}--logs_path{default}\n"
            %(craplog.logs_path)
            .format(**craplog.text_colors))
    if checkFolder( craplog.logs_path, "logs_folder", craplog.text_colors, r=True ) is False:
        checks_passed = False

    # log files
    if craplog.file_selection is False:
        if craplog.access_logs is False:
            craplog.log_files.clear()
        if craplog.error_logs is True:
            craplog.log_files.append("error.log.1")
    if len(craplog.file_selection) == 0:
        checks_passed = False
        print("\n{red}Error{white}[{grey}missing_arguments{white}]{red}>{default} you must set at least one file name after {cyan}-F{default}/{cyan}--log-files{default}\n"
            .format(**craplog.text_colors))
    for file_name in craplog.log_files:
        file_path = "%s/%s" %( craplog.logs_path, file_name )
        if checkFile( craplog.file_path, "log_file", craplog.text_colors, r=True ) is False:
            checks_passed = False

    # trash folder
    if  craplog.trash is True\
    and checkFolder( craplog.trash_path, "trash", craplog.text_colors, w=True ) is False:
        checks_passed = False

    # crapstats main folder
    if checks_passed is True:
        if os.path.exists(craplog.statpath) is False:
            os.mkdir( craplog.statpath )
        else:
            if checkFolder( craplog.statpath, "stats_folder", craplog.text_colors, r=True, w=True ) is False:
                checks_passed = False
    # global stats folder
    if  checks_passed is True\
    and craplog.global_stats is True:
        path = "%s/globals" %( craplog.statpath )
        if os.path.exists( path ) is False:
            os.mkdir( path )
        else:
            if checkFolder( path, "stats_folder", craplog.text_colors, r=True, w=True ) is False:
                checks_passed = False
    # sessions stats folder
    if  checks_passed is True\
    and craplog.session_stats is True:
        path = "%s/sessions" %( craplog.statpath )
        if os.path.exists( path ) is False:
            os.mkdir( path )
        else:
            if checkFolder( path, "stats_folder", craplog.text_colors, r=True, w=True ) is False:
                checks_passed = False
    # access stats folder
    if  checks_passed is True\
    and craplog.access_logs is True:
        path = "%s/sessions/access" %( craplog.statpath )
        if os.path.exists( path ) is False:
            os.mkdir( path )
        else:
            if checkFolder( path, "stats_folder", craplog.text_colors, r=True, w=True ) is False:
                checks_passed = False
    # error stats folder
    if  checks_passed is True\
    and craplog.error_logs is True:
        path = "%s/sessions/error" %( craplog.statpath )
        if os.path.exists( path ) is False:
            os.mkdir( path )
        else:
            if checkFolder( path, "stats_folder", craplog.text_colors, r=True, w=True ) is False:
                checks_passed = False

    # access logs fields
    if craplog.access_logs is True:
        for field in craplog.access_fields:
            if field not in ["IP","UA","REQ","RES"]:
                checks_passed = False
                print("\n{red}Error{white}[{grey}invalid_field{white}]{red}>{default} invalid field for access logs: {orange}%s{default}"
                    %( field )
                    .format(**craplog.text_colors))
                if craplog.more_output is True:
                    print("""\
                      available fields:
                        - {bold}IP{default}   {italic}IP address of the client{default}
                        - {bold}UA{default}   {italic}User-agent of the client{default}
                        - {bold}REQ{default}  {italic}Request made by the client{default}
                        - {bold}RES{default}  {italic}Response code from the server{default}"""
                        .format(**craplog.text_colors))
                print()

    # exit if at least one error occured
    if checks_passed is False:
        exit("{bold}%s {red}ABORTED{default}\n"
            %( craplog.TXT_craplog )
            .format(**craplog.text_colors))


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
            while True:
                print("{orange}Warning{white}[{grey}session_date{white}]{red}>{default} the date of one or more parsed lines is already present in the stored sessions"
                    .format(**craplog.text_colors))
                if craplog.more_output is True:
                    # print found conflicts
                    for log_type, dates in conflicts.items():
                        if len(dates) > 0:
                            print("                       dates from {bold}%s{default} logs:"
                                %( log_type )
                                .format(**craplog.text_colors))
                            for date in dates:
                            print("                          - {yellow}%s{default}"
                                %( date )
                                .format(**craplog.text_colors))
                            print()
                if craplog.less_output is False:
                    print("If you choose to proceed, statistics will be {bold}mergerd{default}"
                        .format(**craplog.text_colors))
                    print("Please make sure you're not parsing the same files twice")
                proceed = input("Continue? {white}[{green}y{grey}/{red}n{white}] :{default} "
                    .format(**craplog.text_colors))
                if proceed in ["y","Y","yes","Yes","YES"]:
                    break
                elif proceed in ["n","N","no","No","NO"]:
                    exit("\nCRAPLOG ABORTED\n")
                else:
                    print("\n{orange}Warning{white}[{grey}choice{white}]{red}>{default} not a valid choice: {bold}%s{default}\n"
                        .format(**craplog.text_colors))
            # set the time elapsed during user's decision as user-time
            craplog.user_time += timer() - time_gap()

