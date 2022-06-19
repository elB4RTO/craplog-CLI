

def processDate(
    date_: str
) -> str :
    """
    Process a log date
    """
    date = date_.split('/')
    day = date[0]
    if date[1] == "Jan":
        month = "01"
    elif date[1] == "Feb":
        month = "02"
    elif date[1] == "Mar":
        month = "03"
    elif date[1] == "Apr":
        month = "04"
    elif date[1] == "May":
        month = "05"
    elif date[1] == "Jun":
        month = "06"
    elif date[1] == "Jul":
        month = "07"
    elif date[1] == "Aug":
        month = "08"
    elif date[1] == "Sep":
        month = "09"
    elif date[1] == "Oct":
        month = "10"
    elif date[1] == "Nov":
        month = "11"
    elif date[1] == "Dec":
        month = "12"
    else:
        month = "00"
    year = date[2]
    # return the formatted date
    return "%s-%s-%s" %( year, month, day )



def parseAccess(
    craplog: object,
    lines:   list
):
    """
    Parse access logs lines
    """
    for line in lines:
        # check line standards
        if line[-1] != '"':
            craplog.access_lines -= 1
            continue
        try:
            # initial split
            line_split = line.split('"')
            ip_date    = line_split[0].split(' ')
            ip = ip_date[0].strip()
            # check for matches in the whitelist
            whitelisted = False
            for whitelisted_ip in craplog.ip_whitelist:
                if ip.startswith( whitelisted_ip ):
                    whitelisted = True
                    break
            if whitelisted is True:
                craplog.whitelist_size += len(line)
                craplog.whitelist_lines += 1
                continue
            # retrieve the date
            date = ip_date[3].strip("[ ]").split(':')[0]
            date = processDate( date )
            if date[5:7] == "00":
                craplog.printJobFailed()
                print("\n{err}Error{white}[{grey}log_date{white}]{red}>{default} unknown date found: {rose}%s{default}\n"\
                    .format(**craplog.text_colors)\
                    %( ip_date[3].strip("[ ]") ))
                craplog.exitAborted()
            # retrieve fields
            req = line_split[1].strip()
            res = line_split[2].strip()[:3].strip()
            ua  = line_split[5].strip()
        except:
            # something wrong with this line, skip
            continue
        # update the collection with the current date
        if craplog.collection['access'].get( date ) is None:
            craplog.collection['access'].update({ date : {} })
        # append data to the collection
        for field in craplog.access_fields:
            # get the relative item
            if   field == "IP":  item = ip
            elif field == "UA":  item = ua
            elif field == "REQ": item = req
            elif field == "RES": item = res
            else:
                craplog.printJobFailed()
                print("\n{err}Error{white}[{grey}access_field{white}]{red}>{default} unexpected field found: {rose}%s{default}\n"\
                    .format(**craplog.text_colors)\
                    %( field ))
                craplog.exitAborted()
            # add the field section if not present
            if craplog.collection['access'][date].get( field ) is None:
                craplog.collection['access'][date].update({ field : {} })
            # add the current item to the collection
            if craplog.collection['access'][date][field].get( item ) is None:
                craplog.collection['access'][date][field].update({ item : 1 })
            else:
                craplog.collection['access'][date][field][item] += 1
        # sum data size
        craplog.access_size += len(line)



def parseErrors(
    craplog: object,
    lines:   list
):
    """
    Parse access logs lines
    """
    for line in lines:
        # check line standards
        if line[0] != '[':
            craplog.errors_lines -= 1
            continue
        try:
            # initial split
            line_split = line.split(']')
            # check the presence of a client IP
            ip = line_split[3].strip()
            f  = ip.find("[client ")
            if f >= 0:
                # found, client log
                ip = ip[f+8:].split(':')[0].strip()
                # check for matches in the whitelist
                whitelisted = False
                for whitelisted_ip in craplog.ip_whitelist:
                    if ip.startswith( whitelisted_ip ):
                        whitelisted = True
                        break
                if whitelisted is True:
                    continue
                err = line_split[4].strip()
            else:
                # server log
                err = ip
            # get the date
            date_time  = line_split[0].strip("[ ]").split(' ')
            date = "%s/%s/%s" %( date_time[2], date_time[1], date_time[4] )
            date = processDate( date )
            if date[5:7] == "00":
                craplog.printJobFailed()
                print("\n{err}Error{white}[{grey}log_date{white}]{red}>{default} unknown date found: {rose}%s{default}\n"\
                    .format(**craplog.text_colors)\
                    %( line_split[0].strip("[ ]") ))
                craplog.exitAborted()
            # retrieve fields
            lev = line_split[1].strip("[ ]")
        except:
            continue
        # update the collection with the current date
        if craplog.collection['error'].get( date ) is None:
            craplog.collection['error'].update({ date : {} })
        # append data to the collection
        for field in ["ERR","LEV"]:
            # get the relative item
            if   field == "ERR": item = err
            elif field == "LEV": item = lev
            # add the field section if not present
            if craplog.collection['error'][date].get( field ) is None:
                craplog.collection['error'][date].update({ field : {} })
            # add the current item to the collection
            if craplog.collection['error'][date][field].get( item ) is None:
                craplog.collection['error'][date][field].update({ item : 1 })
            else:
                craplog.collection['error'][date][field][item] += 1
        # sum data size
        craplog.errors_size += len(line)



def parseLogLines(
    craplog: object,
    data:    dict
):
    """
    Parse log lines
    """
    # parse every log type
    for log_type, log_lines in data.items():
        if len(log_lines) > 0:
            craplog.printCaret( log_type )
            # insert the log-type dict if not present yet
            if craplog.collection.get( log_type ) is None:
                craplog.collection.update({ log_type : {} })
            # parse every line
            if log_type == "access":
                craplog.access_lines += len(log_lines)
                parseAccess( craplog, log_lines )
            elif log_type == "error":
                craplog.errors_lines += len(log_lines)
                parseErrors( craplog, log_lines )
            craplog.restoreCaret()
    # sum parsed data
    craplog.parsed_size = craplog.access_size + craplog.errors_size

