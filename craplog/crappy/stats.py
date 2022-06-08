
import os
from time import perf_counter as timer

from crappy.check import checkFolder, checkFile


def sortStatistics(
    items:  list,
    counts: list
):
    """
    Sort twin arrays (items & items' count) by decrescent order
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
        print("\n{err}Error{white}[{grey}write{white}]{red}>{default} failed to write on file: {grass}%s/{rose}%s{default}"\
            .format(**craplog.text_colors)\
            %( path[:path.rfind('/')], path[path.rfind('/')+1:] ))
        if craplog.more_output is True:
            print("              the error is most-likely caused by a lack of permissions")
            print("              please add read/write permissions to the whole crapstats folder and retry")
        print()
    return successful


def mergeStatistics(
    path: str,
    items: list,
    counts: list,
    craplog: object
) -> bool :
    """
    Read+merge old+new statistics
    """
    successful = True
    try:
        # try read the file
        with open( path, 'r' ) as f:
            # read old statistics from file
            old_stats = f.read().strip().split('\n')
    except:
        # failed to read
        successful = False
        craplog.printJobFailed()
        craplog.undoChanges()
        print("\n{err}Error{white}[{grey}read{white}]{red}>{default} failed to read from file: {grass}%s/{rose}%s{default}"\
            .format(**craplog.text_colors)\
            %( path[:path.rfind('/')], path[:path.rfind('/')+1] ))
        if craplog.more_output is True:
            print("             the error is most-likely caused by a lack of permissions")
            print("             please add read/write permissions to the whole crapstats folder and retry")
        print()
    else:
        # successfully read, now merge
        for stat in old_stats:
            craplog.parsed_size += len(stat)
            stat = stat.lstrip()
            s = stat.find(' ')
            if s < 0:
                successful = False
                craplog.printJobFailed()
                craplog.undoChanges()
                print("\n{err}Error{white}[{grey}statistics{white}]{red}>{default} malformed line found: {rose}%s{default}"\
                    .format(**craplog.text_colors)\
                    %( stat.strip() ))
                if craplog.more_output is True:
                    print("                   this line doesn't respect craplog's standards")
                    print("                   if you manually edited crapstats files, please restore or delete this line")
                    print("                   else, please consider reporting this issue")
                print()
                break
            # retrieve old stuff
            old_count = stat[:s].strip()
            try:
                old_item = stat[s+1:].strip()
            except:
                old_item = ""
            try:
                # assume the item is already in the list
                i = items.index( old_item )
                counts[i] += int(old_count)
            except:
                # add the item as new
                items.append( old_item )
                counts.append( int(old_count) )
        if successful is True:
            # make a copy of the old file
            try:
                bak_path = "%s.bak" %( path )
                os.rename( path, bak_path )
                craplog.undo_paths.append( bak_path )
            except:
                # failed to make a backup copy for safety
                successful = False
                craplog.printJobFailed()
                craplog.undoChanges()
                print("\n{err}Error{white}[{grey}safety_backup{white}]{red}>{default} failed to rename file as backup: {grass}%s/{rose}%s{grey}.bak{default}"\
                    .format(**craplog.text_colors)\
                    %( path[:path.rfind('/')], path[:path.rfind('/')+1] ))
                if craplog.more_output is True:
                    print("""\
                          the error is most-likely caused by a lack of permissions
                          please add read/write permissions to the whole crapstats folder and retry""")
                print()
            if successful is True:
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
    checks_passed = checkFolder(
        craplog, "stats_folder", path, parent_path, item_name,
        True, True, True, True, True )
    if checks_passed is True:
        caret_return = 0
        for log_type, dates in craplog.collection.items():
            # check every log type (access/error)
            parent_path = "%s/sessions" %( craplog.statpath )
            item_name   = log_type
            path        = "%s/%s" %( parent_path, item_name )
            checks_passed = checkFolder(
                craplog, "stats_folder", path, parent_path, item_name,
                True, True, True, True, True )
            if checks_passed is False:
                break
            for date, fields in dates.items():
                # check every date (year,month,day)
                if checks_passed is True:
                    year  = date[:4]
                    month = date[5:7]
                    day   = date[8:]
                    parent_path = "%s/sessions/%s" %( craplog.statpath, log_type )
                    item_name   = year
                    path        = "%s/%s" %( parent_path, item_name )
                    checks_passed = checkFolder(
                        craplog, "stats_folder", path, parent_path, item_name,
                        True, True, True, True, True )
                if checks_passed is True:
                    buildPath( month )
                    checks_passed = checkFolder(
                        craplog, "stats_folder", path, parent_path, item_name,
                        True, True, True, True, True )
                if checks_passed is True:
                    buildPath( day )
                    checks_passed = checkFolder(
                        craplog, "stats_folder", path, parent_path, item_name,
                        True, True, True, True, True )
                if checks_passed is False:
                    break
                for field, data in fields.items():
                    # check every field (IP,UA,REQ,RES/ERR,LEV)
                    parent_path = "%s/sessions/%s/%s/%s/%s" %( craplog.statpath, log_type, year, month, day )
                    item_name   = "%s.crapstat" %(field)
                    path        = "%s/%s" %( parent_path, item_name )
                    checks_passed = checkFile(
                        craplog, "stats_file", path, parent_path, item_name,
                        True, True, True, True, True )
                    if checks_passed is True:
                        # print the field in use if needed
                        craplog.printCaret( field )
                        # get items as twin-arrays
                        counts = []
                        items  = []
                        for key,value in data.items():
                            # do it one-by-one to ensure correct matches
                            items.append( key )
                            counts.append( value )
                        # store statistics
                        if os.path.exists( path ):
                            checks_passed = mergeStatistics( path, items, counts, craplog )
                        else:
                            checks_passed = saveStatistics( path, items, counts, craplog )
                            if checks_passed is True:
                                craplog.undo_paths.append( path )
                        # restore the caret if needed
                        craplog.restoreCaret()
                    
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
        craplog.exitAborted()


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
    checks_passed = checkFolder(
        craplog, "stats_folder", path, parent_path, item_name,
        True, True, True, True, True )
    if checks_passed is True:
        caret_return = 0
        for log_type, dates in craplog.collection.items():
            # check every log type (access/error)
            if checks_passed is True:
                parent_path = "%s/globals" %( craplog.statpath )
                item_name   = log_type
                path        = "%s/%s" %( parent_path, item_name )
                checks_passed = checkFolder(
                    craplog, "stats_folder", path, parent_path, item_name,
                    True, True, True, True, True )
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
            for field, data in global_collection.items():
                # print the field in use if needed
                craplog.printCaret( field )
                # get items as twin-arrays
                counts = []
                items  = []
                for key,value in data.items():
                    # one-by-one to ensure correctness
                    items.append( key )
                    counts.append( value )
                # store statistics
                path = "%s/globals/%s/%s.crapstat" %( craplog.statpath, log_type, field )
                if os.path.exists( path ):
                    checks_passed = mergeStatistics( path, items, counts, craplog )
                else:
                    checks_passed = saveStatistics( path, items, counts, craplog )
                # restore the caret if needed
                craplog.restoreCaret()
                # break if an error occured
                if checks_passed is False:
                    break
            # breaks log types' loop
            if checks_passed is False:
                break
    # exit if an error occured
    if checks_passed is False:
        craplog.exitAborted()

