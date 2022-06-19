
import os
from time import sleep
from time import perf_counter as timer

from craplib.utils import checkFolder, checkFile


def makeInitialChecks( craplog:object ):
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
    if craplog.warning_size is None:
        failed()
        print("\n{err}Error{white}[{grey}missing_arguments{white}]{red}>{default} you must set the size after {cyan}--max-size{default}\n"\
            .format(**craplog.text_colors))
    else:
        try:
            craplog.warning_size = float(craplog.warning_size)
            if craplog.warning_size < 0:
                failed()
                print("\n{err}Error{white}[{grey}invalid_size{white}]{red}>{default} the max size must be greater or equal to 0\n"\
                    .format(**craplog.text_colors))
            elif craplog.warning_size > 1000000:
                failed()
                print("\n{err}Error{white}[{grey}invalid_size{white}]{red}>{default} the given max size is huge: {yellow}%.2f GB{default}\n"\
                    .format(**craplog.text_colors)
                    %( craplog.warning_size / 1024 ))
                if craplog.less_output is False:
                    print("                     use 0 to have it unlimited")
        except:
            failed()
            print("\n{err}Error{white}[{grey}invalid_argument{white}]{red}>{default} invalid value for {cyan}--max-size{default}: {rose}%s{default}\n"\
                .format(**craplog.text_colors)
                %( craplog.warning_size ))
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
                    # leave this normal yellow, it's secondary and doesn't need a real attention
                    print("\n{yellow}Warning{white}[{grey}choice{white}]{warn}>{default} not a valid choice: {bold}%s{default}"\
                        .format(**craplog.text_colors))
                    if craplog.less_output is False:
                        print()
                        sleep(1)
            # set the time elapsed during user's decision as user-time
            craplog.user_time += timer() - time_gap
    
