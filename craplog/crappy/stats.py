
import os
from time import perf_counter as timer


def chooseAction(
    craplog: object
) -> int :
    """
    Choice form
    """
    choice = 0
    time_gap = timer()
    while True:
        if craplog.less_output is False:
            print("Available choices:")
            print("  - {grey}[{bold}d{grey}]{default}   {bold}delete{default} the conflict accordingly to the settings"
                .format(**craplog.text_colors))
            print("  - {grey}[{bold}r{grey}]{default}   {bold}rename{default} the conflict with a trailing '{italic}.copy{default}'"
                .format(**craplog.text_colors))
            print("  - {grey}[{bold}q{grey}]{default}   abort the process and {bold}quit{default} craplog"
                .format(**craplog.text_colors))
        proceed = input("Your choice? {white}[{yellow}d{grey}/{azul}r{grey}/{rose}q{white}] :{default} "
            .format(**craplog.text_colors)).strip()
        if proceed in ["q","Q","quit","QUIT"]:
            choice = 0
        elif proceed in ["d","D","del","DEL","delete","DELETE"]:
            choice = 1
        elif proceed in ["r","R","rename","RENAME"]:
            choice = 2
        else:
            print("\n{yellow}Warning{white}[{grey}choice{white}]{red}>{default} not a valid choice: {bold}%s{default}\n"
                .format(**craplog.text_colors))
    # set the time elapsed during user's decision as user-time
    craplog.user_time += timer() - time_gap()
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
    print("{orange}Warning{white}[{grey}conflict{white}]{red}>{default} a folder is in conflict with the process: {green}%s/{orange}%s{default}"
        %( parent_path, item_name )
        .format(**craplog.text_colors))
    if craplog.more_output is True:
        print("""\
                the entry was supposed to be a file, but it was found to be a folder
                if you haven't made any changes, please report this issue""")
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
    print("{orange}Warning{white}[{grey}conflict{white}]{red}>{default} a file is in conflict with the process: {green}%s/{orange}%s{default}"
        %( parent_path, item_name )
        .format(**craplog.text_colors))
    if craplog.more_output is True:
        print("""\
                the entry was supposed to be a folder, but it was found to be a file
                if you haven't made any changes, please report this issue""")
    print()
    return chooseAction( craplog )


def checkFolder(
    craplog: object,
    path:    str,
    parent_path: str,
    item_name:   str
) -> bool :
    """
    Check a crapstats folder
    """
    def failed():
        nonlocal checks_passed, craplog
        if checks_passed is True:
            checks_passed = False
            craplog.printJobFailed()
            craplog.undoChanges()
    # checking
    checks_passed = True
    if os.path.exists( path ):
        # already exists
        if os.path.isdir( path ):
            # is a directory
            if os.access( path, os.R_OK ) is False:
                failed()
                print("\n{red}Error{white}[{grey}permissions{white}]{red}>{default} directory is not readable: {green}%s/{orange}%s{default}"
                    %( parent_path, item_name )
                    .format(**craplog.colors))
                if craplog.more_output is True:
                    print("""\
                    craplog doesn't have permissions to read from files inside this folder
                    please make the directory readable and retry""")
                print()
            if os.access( sessions_path, os.W_OK ) is False:
                failed()
                print("\n{red}Error{white}[{grey}permissions{white}]{red}>{default} directory is not writable: {green}%s/{orange}%s{default}"
                    %( parent_path, item_name )
                    .format(**craplog.colors))
                if craplog.more_output is True:
                    print("""\
                    craplog doesn't have permissions to write on files inside this folder
                    please make the directory writable and retry""")
                print()
        else:
            # not a directory
            if os.path.isfile( path ):
                choice = 0
                if craplog.auto_delete is True:
                    choice = 1
                else:
                    choice = conflictFile()
                if choice == 1:
                    # delete the file and make a dir
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
                        print("\n{red}Error{white}[{grey}file{white}]{red}>{default} unable to rename file: {green}%s/{orange}%s{default}"
                            %( parent_path, item_name )
                            .format(**craplog.colors))
                        if craplog.more_output is True:
                            print("               the error is most-likely caused by a lack of permissions")
                            print("               please proceed manually and retry")
                        print()
                else:
                    failed()
                    exit("{bold}%s {red}ABORTED{default}\n"
                        %( craplog.TXT_craplog )
                        .format(**craplog.text_colors))
            else:
                # unknown type
                failed()
                print("\n{red}Error{white}[{grey}type{white}]{red}>{default} the entry is not a directory, nor a file: {green}%s/{orange}%s{default}"
                    %( parent_path, item_name )
                    .format(**craplog.colors))
                if craplog.more_output is True:
                    print("             ok, that was unexpected")
                    print("             please manually check it and consider reporting this issue")
                print()
    else:
        # does not exists, yet, make it
        os.mkdir( path )
        craplog.undo_paths.append( path )
    return checks_passed


def checkFile(
    craplog: object,
    path:    str,
    parent_path: str,
    item_name:   str
) -> bool :
    """
    Check a crapstats file
    """
    def failed():
        nonlocal checks_passed, craplog
        if checks_passed is True:
            checks_passed = False
            craplog.printJobFailed()
            craplog.undoChanges()
    # checking
    if os.path.exists( path ):
        # already exists
        if os.path.isfile( path ):
            # is a file
            if os.access( path, os.R_OK ) is False:
                failed()
                print("\n{red}Error{white}[{grey}permissions{white}]{red}>{default} file is not readable: {green}%s/{orange}%s{default}"
                    %( parent_path, item_name )
                    .format(**craplog.colors))
                if craplog.more_output is True:
                    print("""\
                    craplog doesn't have permissions to read from this file
                    please make the file readable and retry""")
                print()
            if os.access( sessions_path, os.W_OK ) is False:
                failed()
                print("\n{red}Error{white}[{grey}permissions{white}]{red}>{default} file is not writable: {green}%s/{orange}%s{default}"
                    %( parent_path, item_name )
                    .format(**craplog.colors))
                if craplog.more_output is True:
                    print("""\
                    craplog doesn't have permissions to write in this file
                    please make the file writable and retry""")
                print()
        else:
            # not a file
            if os.path.isdir( path ):
                choice = 0
                if craplog.auto_delete is True:
                    choice = 1
                else:
                    choice = conflictFolder()
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
                        print("\n{red}Error{white}[{grey}file{white}]{red}>{default} unable to rename file: {green}%s/{orange}%s{default}"
                            %( parent_path, item_name )
                            .format(**craplog.colors))
                        if craplog.more_output is True:
                            print("               the error is most-likely caused by a lack of permissions")
                            print("               please proceed manually and retry")
                        print()
                else:
                    failed()
                    exit("{bold}%s {red}ABORTED{default}\n"
                        %( craplog.TXT_craplog )
                        .format(**craplog.text_colors))
            else:
                # unknown type
                failed()
                print("\n{red}Error{white}[{grey}type{white}]{red}>{default} the entry is not a file, nor a directory: {green}%s/{orange}%s{default}"
                    %( parent_path, item_name )
                    .format(**craplog.colors))
                if craplog.more_output is True:
                    print("             ok, that was unexpected")
                    print("             please manually check it and consider reporting this issue")
                print()
    else:
        # does not exists, yet, it will be created later in any case
        pass
    return checks_passed


def sortStatistics(
    items:  list,
    counts: list
):
    """
    Sort twin arrays by decrescent order
    """
    length = len(counts)
    for i in range(length):
        for j in range(length):
            if counts[i] > counts[j]:
                counts[i],counts[j] = counts[j],counts[i]
                items[i],items[j] = items[j],items[i]


def saveStatistics(
    path: str,
    items: list,
    counts: list,
    craplog: object
) -> bool :
    """
    Save statistics on file
    """
    content = ""
    successful = True
    sortStatistics( items, counts )
    # make a string representing the final file content
    for count,item in zip(counts,items):
        content += "%s %s\n" %( count, item )
    try:
        with open( path, 'w' ) as f:
            # write statistics on file
            f.write( content )
    except:
        successful = False
        craplog.printJobFailed()
        craplog.undoChanges()
        print("\n{red}Error{white}[{grey}write{white}]{red}>{default} failed to write on file: {green}%s/{orange}%s{default}\n"
            %( path[:path.rfind('/')], path[:path.rfind('/')+1] )
            .format(**craplog.colors))
        if craplog.more_output is True:
            print("              craplog doesn't have permissions to write in this file")
            print("              please make it readable and retry")
        print()
    return successful


def mergeStatistics(
    path: str,
    items: list,
    counts: list,
    craplog: object
) -> bool :
    """
    Read merge old and new statistics
    """
    successful = True
    try:
        # try read the file
        with open( path, 'r' ) as f:
            # write statistics on file
            old_stats = f.read().strip().split('\n')
    except:
        # failed to read
        successful = False
        craplog.printJobFailed()
        craplog.undoChanges()
        print("\n{red}Error{white}[{grey}read{white}]{red}>{default} failed to read from file: {green}%s/{orange}%s{default}"
            %( path[:path.rfind('/')], path[:path.rfind('/')+1] )
            .format(**craplog.colors))
        if craplog.more_output is True:
            print("             craplog doesn't have permissions to read from this file")
            print("             please make it readable and retry")
        print()
    else:
        # successfully read, now merge
        for stat in old_stats:
            stat = stat.strip()
            s = stat.find(' ')
            if s < 0:
                successful = False
                craplog.printJobFailed()
                craplog.undoChanges()
                print("\n{red}Error{white}[{grey}statistics{white}]{red}>{default} malformed line found: {orange}%s{default}"
                    %( stat.strip() )
                    .format(**craplog.colors))
                if craplog.more_output is True:
                    print("                   this line doesn't respect craplog's standards")
                    print("                   if you manually edited crapstats files, please restore or delete this line")
                    print("                   else, please consider reporting this issue")
                print()
                break
            # retrieve old stuff
            old_count = stat[:s].strip()
            old_item  = stat[s+1:].strip()
            try:
                i = items.index( old_item )
                counts[i] += old_count
            except:
                items.append( old_item )
                counts.append( old_count )
        # make a copy of the old file
        bak_path = "%s.bak" %( path )
        os.rename( path, bak_path )
        craplog.undo_paths.append( bak_path )
        # save on file
        successful = saveStatistics( path, items, counts, craplog )
    finally:
        # whatever happened, return the result
        return successful


def storeSessions(
    craplog: object
):
    """
    Store statistics by date
    """
    def buildPath( new_item ):
        nonlocal path, parent_path, item_name
        parent_path = path
        item_name = new_item
        path = "%s/%s" %( parent_path, item_name )

    checks_passed = True
    parent_path = craplog.statpath
    item_name   = "sessions"
    path        = "%s/%s" %( parent_path, item_name )
    # check sessions main folder
    checks_passed = checkFolder( craplog, path, parent_path, item_name )
    if checks_passed is True:
        for log_type, dates in craplog.collection.items():
            # check every log type (access/error)
            parent_path = "%s/sessions" %( craplog.statpath )
            item_name   = log_type
            path        = "%s/%s" %( parent_path, item_name )
            checks_passed = checkFolder( craplog, path, parent_path, item_name )
            if checks_passed is False:
                break
            for date, fields in dates.items():
                # check every date (year,month,day)
                year  = date[:4]
                month = date[5:7]
                day   = date[8:]
                parent_path = "%s/sessions/%s" %( craplog.statpath, log_type )
                item_name   = year
                path        = "%s/%s" %( parent_path, item_name )
                checks_passed = checkFolder( craplog, path, parent_path, item_name )
                if checks_passed is True:
                    buildPath( month )
                    checks_passed = checkFolder( craplog, path, parent_path, item_name )
                if checks_passed is True:
                    buildPath( day )
                    checks_passed = checkFolder( craplog, path, parent_path, item_name )
                if checks_passed is False:
                    break
                for field, data in fields.items():
                    # check every field (IP,UA,REQ,RES/ERR,LEV)
                    parent_path = "%s/sessions/%s/%s/%s/%s" %( craplog.statpath, log_type, year, month, day )
                    item_name   = "%s.crapstat" %(field)
                    path        = "%s/%s" %( parent_path, item_name )
                    checks_passed = checkFile( craplog, path, parent_path, item_name )
                    if checks_passed is True:
                        counts = []
                        items  = []
                        for key,value in data.items():
                            # do it one-by-one to ensure correctness
                            items.append( key )
                            counts.append( value )
                        if os.path.exists( path ):
                            checks_passed = mergeStatistics( path, items, counts, craplog )
                        else:
                            checks_passed = saveStatistics( path, items, counts, craplog )

                    # breaks fields' loop
                    if checks_passed is False:
                        break
                # breaks dates' loop
                if checks_passed is False:
                    break
            # breaks log-types' loop
            if checks_passed is False:
                break
    # exit if an error occured
    if checks_passed is False:
        exit()


def updateGlobals(
    craplog: object
):
    """
    Update global statistics
    """
    def failed():
        nonlocal checks_passed, craplog
        if checks_passed is True:
            checks_passed = False
            craplog.printJobFailed()
            craplog.undoChanges()

    checks_passed = True
    parent_path = craplog.statpath
    item_name   = "globals"
    path        = "%s/%s" %( parent_path, item_name )
    # check globals main folder
    checks_passed = checkFolder( craplog, path, parent_path, item_name )
    if checks_passed is True:
        for log_type, dates in craplog.collection.items():
            # check every log type (access/error)
            parent_path = "%s/globals" %( craplog.statpath )
            item_name   = log_type
            path        = "%s/%s" %( parent_path, item_name )
            checks_passed = checkFolder( craplog, path, parent_path, item_name )
            if checks_passed is False:
                break
            global_collection = {}
            for date, fields in dates.items():
                # internal statistics: merge all the dates
                for field, data in fields.items():
                    # merge every field (IP,UA,REQ,RES/ERR,LEV)
                    if global_collection.get( field ) is None:
                        global_collection.update({ field : {} })
                    for item,count in data.items():
                        # one-by-one to ensure correctness
                        if global_collection[field].get( item ) is None:
                            global_collection[field].update({ item : count })
                        else:
                            global_collection[field][item] += count

                    # breaks fields' loop
                    if checks_passed is False:
                        break
                # breaks dates' loop
                if checks_passed is False:
                    break
            # breaks log-types' loop
            if checks_passed is False:
                break
            # done merging fields and dates, now save statistics
            for field, data in global_collection[log_type].items():
                # repeat for every field
                counts = []
                items  = []
                for key,value in global_collection[log_type][field].items():
                    # one-by-one to ensure correctness
                    items.append( key )
                    counts.append( value )
                # store
                path = "%s/globals/%s/%s.crapstat" %( craplog.statpath, log_type, field )
                if os.path.exists( path ):
                    checks_passed = mergeStatistics( path, items, counts, craplog )
                else:
                    checks_passed = saveStatistics( path, items, counts, craplog )
                # break if an error occured
                if checks_passed is False:
                    break
            # breaks log types' loop
            if checks_passed is False:
                break
    # exit if an error occured
    if checks_passed is False:
        exit()

