
import gzip

from os.path import getsize
from random import choice, randint
from time import perf_counter as timer

from crappy.hashes import digestFile


def choiceDialog(
    craplog: object,
    question: str
) -> bool :
    """
    Dialog for a binary choice to make
    """
    time_gap = timer()
    choice = False
    while True:
        proceed = input("%s? {white}[{grass}y{grey}/{red}n{white}] :{default} "\
            .format(**craplog.text_colors)
            %(question)
            ).strip().lower()
        if proceed in ["y","yes"]:
            choice = True
            break
        elif proceed in ["n","no"]:
            choice = False
            break
        else:
            # leave this normal yellow, it's secondary and doesn't need real attention
            print("\n{warn}Warning{white}[{grey}choice{white}]{yellow}>{default} not a valid choice: {bold}%s{default}\n"\
                .format(**craplog.text_colors)
                %( proceed ))
    # set the time elapsed during user's decision as user-time
    craplog.user_time += timer() - time_gap
    return choice


def checkUsage(
    craplog: object,
    path: str,
    file_name: str
) -> bool :
    """
    Hash a file with sha1 to check a possible previous usage
    """
    file_hash = digestFile( craplog, path )
    # check the present of the hash
    if file_hash in craplog.hashes:
        # file hash found, emit a warning
        craplog.printJobHalted()
        if craplog.more_output is True:
            print("\n")
        elif craplog.less_output is True:
            print()
        print("{warn}Warning{white}[{grey}file_usage{white}]{warn}>{default} this file has probably been used already: {grass}%s/{yellow}%s{default}"\
            .format(**craplog.text_colors)\
            %( path[:-len(file_name)-1], file_name ))
        if craplog.more_output is True:
            print("""\
                    file hash (sha256): {yellow}%s{default}
                    craplog keeps track of files usage by storing their unique checksum
                    it's close to impossible for two files to have the same hash
                    please continue only if you're REALLY sure"""\
                .format(**craplog.text_colors)\
                %( file_hash ))
        if craplog.less_output is False:
            print()
        choice = choiceDialog( craplog, "Do you really want to use this file" )
        # reprint the last job if needed
        if craplog.less_output is False:
            print()
        if choice is True:
            craplog.hashes.append( file_hash )
            if craplog.less_output is True\
            or craplog.more_output is True:
                craplog.reprintJob()
        return choice
    else:
        # hash not found, append and continue
        craplog.hashes.append( file_hash )
        return True
            


def checkSize(
    craplog: object,
    path: str,
    file_name: str
) -> bool :
    """
    Check the size of a file before to read and warn in case of big files
    """
    if craplog.warning_size > 0\
    and (getsize( path ) / 1048576) > craplog.warning_size:
        # file over max allowed dimensions, emit a warning
        craplog.printJobHalted()
        if craplog.more_output is True:
            print("\n")
        elif craplog.less_output is True:
            print()
        print("{warn}Warning{white}[{grey}file_size{white}]{warn}>{default} a file's size exceeds the max allowed size: {grass}%s/{yellow}%s{default}"\
            .format(**craplog.text_colors)\
            %( path[:-len(file_name)-1], file_name ))
        if craplog.more_output is True:
            print("""\
                    the size of the file is: {yellow}%.2f MB{default}
                    the warning limit is actually set at: {green}%.2f MB{default}
                    you can temporary change it using {cyan}--max-size {italic}<size>{default}"""\
                .format(**craplog.text_colors)\
                %( (getsize( path ) / 1048576), craplog.warning_size ))
        if craplog.less_output is False:
            print()
        choice = choiceDialog( craplog, "Do you really want to use this file" )
        # reprint the last job if needed
        if craplog.less_output is False:
            print()
        if choice is True:
            craplog.reprintJob()
        return choice
    else:
        return True


def defineLogType(
    craplog: object,
    name:  str,
    lines: list
) -> str :
    """
    Define the type of the logs in a file
    """
    logs_type = ""
    a = e = u = 0
    i = 0
    n = randint(15,30)
    while i < n:
        line = choice( lines ).strip()
        if line == "":
            continue
        elif line.startswith('['):
            # error logs line
            e += 1
        elif line.endswith('"'):
            # access logs line
            a += 1
        else:
            u += 1
        i += 1
    if e == 0:
        logs_type = "access"
    elif a == 0:
        logs_type = "error"
    else:
        craplog.printJobFailed()
        print("\n{err}Error{white}[{grey}logs{white}]{red}>{default} something is wrong with the logs in: {rose}%s{default}"\
             .format(craplog.text_colors)\
             %( name ))
        if craplog.more_output is True:
            print("""\
             number of randomly examined lines : %s
             number of lines identified as {bold}access{default} logs  : {bold}%s{default}
             number of lines identified as {bold}error{default} logs   : {bold}%s{default}
             number of lines identified as {bold}{italic}unknown{default} type : {bold}%s{default}"""\
                .format(craplog.text_colors)\
                %( n, a, e, u ))
        print()
        craplog.exitAborted()
    return logs_type


def collectLogLines(
    craplog: object
) -> dict :
    """
    Read every given input-file and collect all the lines
    """
    data = {
        'access' : [],
        'error'  : []
    }
    remove_list = []
    for file_name in craplog.log_files:
        craplog.printCaret( file_name )
        path = "%s/%s" %( craplog.logs_path, file_name )
        if craplog.usage_control is True:
            if checkUsage( craplog, path, file_name ) is False:
                # file already used, don't remove now or the loop will be damaged
                remove_list.append( file_name )
        if checkSize( craplog, path, file_name ) is False:
            # file too big
            craplog.exitAborted()
        log_lines = ""
        try:
            # try reading as gzipped file
            with gzip.open(path,'rt') as log_file:
                log_lines = log_file.read().strip().split('\n')
        except:
            try:
                # try reading as text file
                with open(path,'r') as log_file:
                    log_lines = log_file.read().strip().split('\n')
            except:
                # failed to read
                craplog.printJobFailed()
                print("\n{err}Error{white}[{grey}input_file{white}]{red}>{default} unable to open/read file: {grass}%s/{rose}%s{default}"\
                     .format(craplog.text_colors)\
                     %( craplog.logs_path, file_name ))
                if craplog.more_output is True:
                    print("                   failed as both text file and gzipped file")
                print()
                craplog.exitAborted()
        
        # check random lines to define the logs type
        log_type = defineLogType( craplog, file_name, log_lines )
        if (log_type == "access" and craplog.access_logs is False)\
        or (log_type == "error" and craplog.error_logs is False):
            continue
        # append non-empty lines to the collection
        for line in log_lines:
            line = line.strip()
            if len(line) > 0:
                data[log_type].append(line)
                craplog.logs_size += len(line)
            else:
                craplog.logs_size += 1
        craplog.total_lines += len(log_lines)
        craplog.restoreCaret()
    if len(remove_list) > 0:
        for file_name in remove_list:
            craplog.log_files.remove( file_name )
        if len(craplog.log_files) == 0:
            print("{rose}Nothing to do".format(**craplog.text_colors))
            craplog.exitMessage(True)
            exit()
    return data

