
import gzip
from random import choice, randint


def defineLogType(
    craplog: object,
    name:  str,
    lines: list
) -> str :
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
        print("\n{red}Error{white}[{grey}logs{white}]{red}>{default} something is wrong with the logs in: {orange}%s{default}"\
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
    for file_name in craplog.log_files:
        craplog.printCaret( file_name )
        path = "%s/%s" %( craplog.logs_path, file_name )
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
                print("\n{red}Error{white}[{grey}input_file{white}]{red}>{default} unable to open/read file: {green}%s/{orange}%s{default}"\
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
    return data

