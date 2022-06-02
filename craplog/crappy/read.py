
import gzip
from random import choice, randint


def defineLogType(
    name:  str,
    lines: list,
    craplog: object
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
        print("\n{red}Error{white}[{grey}logs{white}]{red}>{default} something is wrong with the logs in: {orange}%s{default}"
             %( name )
             .format(craplog.text_colors))
        if craplog.more_output is True:
            print("""\
             number of randomly examined lines : %s
             number of lines identified as {bold}access{default} logs  : {bold}%s{default}
             number of lines identified as {bold}error{default} logs   : {bold}%s{default}
             number of lines identified as {bold}{italic}unknown{default} type : {bold}%s{default}"""
                %( n, a, e, u )
                .format(craplog.text_colors))
        exit("\n")
    return logs_type


def collectLogLines( craplog ) -> dict :
    """
    Read every given input-file and collect all the lines
    """
    data = {
        'access' : [],
        'error'  : []
    }
    for file_name in craplog.log_files:
        path = "%s/%s" %( craplog.logs_path, file_name )
        log_lines = []
        try:
            # try reading as gzipped file
            with gzip.open(path,'r') as log_file:
                log_lines = log_file.read().strip().split('\n')
        except:
            # try reading as text file
            with open(path,'r') as log_file:
                log_lines = log_file.read().strip().split('\n')
        # check random lines to define the logs type
        log_type = defineLogType( file_name, log_lines )
        if (log_type == "access" and craplog.access_logs is False)\
        or (log_type == "error" and craplog.error_logs is False):
            continue
        # append non-empty lines to the collection
        for line in log_lines:
            line = line.strip()
            if len(line) > 0:
                data[log_type].append(line)
                # sum data size
                craplog.total_size += len(line)
    return data

