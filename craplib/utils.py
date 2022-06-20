
import os

from time import sleep
from time import perf_counter as timer


def checkPathRecursively(
    path: str,
    colors: dict,
    result: bool=False
):
    """
    Checks a path recursively (existence of every element)
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
    craptool: object
) -> int :
    """
    Choice form
    """
    choice = 0
    MSG_choice = """Available choices:
  - {grey}[{default}{bold}d{grey}]{default}   {bold}delete{default} the conflict accordingly to the settings
  - {grey}[{default}{bold}r{grey}]{default}   {bold}rename{default} the conflict with a trailing '{italic}.copy{default}'
  - {grey}[{default}{bold}h{grey}]{default}   print this {bold}help{default} screen
  - {grey}[{default}{bold}q{grey}]{default}   abort the process and {bold}quit{default} craptool\
  """.format(**craptool.text_colors)
    time_gap = timer()
    while True:
        if craptool.less_output is False:
            print(MSG_choice)
            if craptool.more_output is True:
                print()
        proceed = input("Your choice? {white}[{yellow}d{grey}/{azul}r{grey}/{grass}h{grey}/{red}q{white}] :{default} "\
            .format(**craptool.text_colors)).strip().lower()
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
            if craptool.less_output is True:
                print(MSG_choice)
            else:
                print()
        else:
            # leave this normal yellow, it's secondary and doesn't need real attention
            if craptool.less_output is False:
                print()
            print("{yellow}Warning{white}[{grey}choice{white}]{yellow}>{default} not a valid choice: {bold}%s{default}"\
                .format(**craptool.text_colors)\
                %( proceed ))
            if craptool.less_output is False:
                print()
                sleep(1)
    if craptool.less_output is False:
        print()
    if craptool.name == "craplog":
        if choice > 0:
            craptool.reprintJob()
        # set the time elapsed during user's decision as user-time
        craptool.user_time += timer() - time_gap
    return choice



def conflictFolder(
    craptool: object,
    path: str,
    parent_path: str,
    item_name: str
) -> int :
    """
    Asks the user what to do with the conflict
    """
    if craptool.name == "craplog":
        craptool.printJobHalted()
    if craptool.more_output is True:
        print("\n")
    elif craptool.less_output is False:
        print()
    print("{warn}Warning{white}[{grey}conflict{white}]{warn}>{default} a folder is in conflict with the process: {grass}%s/{yellow}%s{default}"\
        .format(**craptool.text_colors)\
        %( parent_path, item_name ))
    if craptool.more_output is True:
        print("""\
                the entry was supposed to be a file, but it was found to be a folder
                if you haven't made any changes, please report this issue""")
    if craptool.less_output is False:
        print()
    return chooseAction( craptool )



def conflictFile(
    craptool: object,
    path: str,
    parent_path: str,
    item_name: str
) -> int :
    """
    Asks the user what to do with the conflict
    """
    craptool.printJobHalted()
    if craptool.more_output is True:
        print("\n")
    elif craptool.less_output is False:
        print()
    print("{warn}Warning{white}[{grey}conflict{white}]{warn}>{default} a file is in conflict with the process: {grass}%s/{yellow}%s{default}"\
        .format(**craptool.text_colors)\
        %( parent_path, item_name ))
    if craptool.more_output is True:
        print("""\
                the entry was supposed to be a folder, but it was found to be a file
                if you haven't made any changes, please report this issue""")
    if craptool.less_output is False:
        print()
    return chooseAction( craptool )



def checkFolder(
    craptool: object,
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
    Check a folder
    """
    def failed():
        nonlocal checks_passed, craptool
        if checks_passed is True:
            checks_passed = False
            if craptool.name == "craplog":
                craptool.printJobFailed()

    def makeit():
        nonlocal err_key, path, parent_path, entry_name, spaces, craptool
        # make the directory
        try:
            os.mkdir( path )
            if craptool.name == "craplog":
                craptool.undo_paths.append( path )
        except:
            # error creating directory
            failed()
            print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} unable to create the directory: {grass}%s/{rose}%s{default}"\
                .format(**craptool.text_colors)\
                %( err_key, parent_path, entry_name ))
            if craptool.more_output is True:
                print("%s         the error is most-likely caused by a lack of permissions" %(spaces))
                print("%s         please add read/write permissions to the whole craplog folder and retry" %(spaces))
            print()

    if entry_name == ""\
    or parent_path == "":
        parent_path = path[:path.rfind('/')]
        entry_name  = path[len(parent_path)+1:]
    spaces = " "*len(err_key)
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
                    .format(**craptool.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if craptool.more_output is True:
                    print("%s         %s doesn't have permissions to read from files inside this folder" %(spaces,craptool.name))
                    print("%s         please make the directory readable and retry" %(spaces))
                print()
            if w is True\
            and os.access( path, os.W_OK ) is False:
                failed()
                print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} directory is not writable: {grass}%s/{rose}%s{default}"\
                    .format(**craptool.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if craptool.more_output is True:
                    print("%s         %s doesn't have permissions to write on files inside this folder" %(spaces,craptool.name))
                    print("%s         please make the directory writable and retry" %(spaces))
                print()
        else:
            # not a directory
            if os.path.isfile( path ):
                if resolve is True:
                    # resolve the conflict
                    choice = 0
                    try:
                        # only Craplog has auto-delete
                        assert craptool.auto_delete is True
                        choice = 1
                    except:
                        choice = conflictFile( craptool, path, parent_path, entry_name )
                    if choice == 1:
                        # delete the file and make a dir
                        if craptool.name == "craplog":
                            craptool.removeEntry( path )
                            if craptool.proceed is False:
                                checks_passed = False
                        else:
                            checks_passed = removeEntry( craptool, path )
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
                            if craptool.name == "craplog":
                                craptool.renameEntry( path, new_path )
                                if craptool.proceed is False:
                                    checks_passed = False
                            else:
                                checks_passed = renameEntry( craptool, path, new_path )
                            if create is True:
                                makeit()
                        except:
                            failed()
                            print("\n{err}Error{white}[{grey}permissions{white}]{red}>{default} unable to rename file: {grass}%s/{rose}%s{default}"\
                                .format(**craptool.text_colors)\
                                %( parent_path, entry_name ))
                            if craptool.more_output is True:
                                print("                    the error is most-likely caused by a lack of permissions")
                                print("                    please add permissions and retry, or intervene manually")
                            print()
                    else:
                        failed()
                        print("\n{err}Error{white}[{grey}variable{white}]{red}>{default} the choice has an invalid value: {rose}%s{default}"\
                            .format(**craptool.text_colors)\
                            %( choice ))
                        if craptool.more_output is True:
                            print("                 {white}@ {bold}craplib.check.checkFolder(){default}")
                            print("                 please consider reporting this issue")
                        print()
                else:
                    # do not resolve the conflict, print a message
                    failed()
                    print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} the given path doens't point to a directory: {grass}%s/{rose}%s{default}"\
                        .format(**craptool.text_colors)\
                        %( err_key, parent_path, entry_name ))
                    if craptool.more_output is True:
                        print("%s         the entry was supposed to be a folder, but it was found to be a file" %(spaces))
                    print()

            else:
                # unknown type
                failed()
                print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a directory, nor a file: {grass}%s/{rose}%s{default}"\
                    .format(**craptool.text_colors)\
                    %( parent_path, entry_name ))
                if craptool.more_output is True:
                    print("             ok, that was unexpected")
                    print("             please manually check it and consider reporting this issue")
                print()
    else:
        # does not exists
        if create is True:
            try:
                makeit()
            except:
                # error creating directory
                failed()
                print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} unable to create the directory: {grass}%s/{rose}%s{default}"\
                    .format(**craptool.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if craptool.more_output is True:
                    print("%s         the error is most-likely caused by a lack of permissions" %(spaces))
                    print("%s         please add read/write permissions to the whole craplog folder and retry" %(spaces))
                print()
        elif create is False:
            failed()
            print("\n{err}Error{white}[{grey}path{white}]{red}>{default} the given path does not exist: %s\n"\
                .format(**craptool.text_colors)\
                %( checkPathRecursively( path, craptool.text_colors ) ))
        else:
            # when None, return a failure if doesn't exist
            checks_passed = False
    return checks_passed



def checkFile(
    craptool: object,
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
    Checks a file
    """
    def failed():
        nonlocal checks_passed, craptool
        if checks_passed is True:
            checks_passed = False
            if craptool.name == "craplog":
                craptool.printJobFailed()

    if entry_name == ""\
    or parent_path == "":
        parent_path = path[:path.rfind('/')]
        entry_name  = path[len(parent_path)+1:]
    spaces = " "*len(err_key)
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
                    .format(**craptool.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if craptool.more_output is True:
                    print("%s         craptool doesn't have permissions to read from this file" %(spaces))
                    print("%s         please make the file readable and retry" %(spaces))
                print()
            if w is True\
            and os.access( path, os.W_OK ) is False:
                failed()
                print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} file is not writable: {grass}%s/{rose}%s{default}"\
                    .format(**craptool.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if craptool.more_output is True:
                    print("%s         craptool doesn't have permissions to write in this file" %(spaces))
                    print("%s         please make the file writable and retry" %(spaces))
                print()
        else:
            # not a file
            if os.path.isdir( path ):
                if resolve is True:
                    choice = 0
                    try:
                        # only Craplog has auto-delete mode
                        assert craptool.auto_delete is True
                        choice = 1
                    except:
                        choice = conflictFolder( craptool, path, parent_path, entry_name )
                    if choice == 1:
                        # delete the dir
                        if craptool.name == "craplog":
                            craptool.removeEntry( path )
                            if craptool.proceed is False:
                                checks_passed = False
                        else:
                            checks_passed = removeEntry( craptool, path )
                    elif choice == 2:
                        # rename the file and make a dir
                        try:
                            new_path = path
                            while True:
                                new_path += ".copy"
                                if os.path.exists( new_path ) is False:
                                    break
                            if craptool.name == "craplog":
                                craptool.renameEntry( path, new_path )
                                if craptool.proceed is False:
                                    checks_passed = False
                            else:
                                checks_passed = renameEntry( craptool, path, new_path )
                        except:
                            failed()
                            print("\n{err}Error{white}[{grey}permissions{white}]{red}>{default} unable to rename folder: {grass}%s/{rose}%s{default}"\
                                .format(**craptool.text_colors)\
                                %( parent_path, entry_name ))
                            if craptool.more_output is True:
                                print("                    the error is most-likely caused by a lack of permissions")
                                print("                    please add permissions and retry, or intervene manually")
                            print()
                    else:
                        failed()
                        print("\n{err}Error{white}[{grey}variable{white}]{red}>{default} the choice has an invalid value: {rose}%s{default}"\
                            .format(**craptool.text_colors)\
                            %( choice ))
                        if craptool.more_output is True:
                            print("                 {white}@ {bold}craplib.check.checkFile(){default}")
                            print("                 please consider reporting this issue")
                        print()
                else:
                    # do not resolve the conflict, print a message
                    failed()
                    print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} the given path doens't point to a file: {grass}%s/{rose}%s{default}"\
                        .format(**craptool.text_colors)\
                        %( err_key, parent_path, entry_name ))
                    if craptool.more_output is True:
                        print("%s         the entry was supposed to be a file, but it was found to be a folder" %(spaces))
                    print()
            else:
                # unknown type
                failed()
                print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a file, nor a directory: {grass}%s/{rose}%s{default}"\
                    .format(**craptool.text_colors)\
                    %( parent_path, entry_name ))
                if craptool.more_output is True:
                    print("             ok, that was unexpected")
                    print("             please manually check it and consider reporting this issue")
                print()
    else:
        # does not exists
        if create is True:
            # ..yet, will be created later in any case
            pass
        else:
            # ..but should have existed
            if craptool.name != "craptool":
                # print an error message
                failed()
                print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} the given path does not exist: %s\n"\
                    .format(**craptool.text_colors)\
                    %( err_key, checkPathRecursively( path, craptool.text_colors ) ))
            else:
                # print a warning message
                print("\n{warn}Warning{white}[{grey}%s{white}]{red}>{default} configuration file {bold}not found{default}: {rose}%s{default}\n"\
                    .format(**craptool.text_colors)\
                    %( err_key, path[path.rfind('/')+1:] ))
                if craptool.less_output is False:
                    print("%s         the default configuration will be used" %(spaces))
                if craptool.more_output is True:
                    print("%s         if you think you should have it, please exit now and check" %(spaces))
    return checks_passed



def removeEntry(
    craptool: object,
    path: str
) -> bool :
    """
    Remove an entry (file/folder)
    """
    result = True
    parent = path[:path.rfind('/')]
    entry  = path[len(parent)+1:]
    # check the type
    return_code = 0
    if os.path.isfile( path ):
        # it's a file
        return_code = run(
            ["rm", path],
            stdout=DEVNULL,
            stderr=STDOUT)\
            .returncode

        if return_code == 1:
            result = False
            print("\n{err}Error{white}[{grey}file{white}]{red}>{default} unable to remove this file: {grass}%s/{rose}%s{default}"\
                .format(**craptool.text_colors)\
                %( parent, entry ))
            if craptool.more_output is True:
                print("               the error is most-likely caused by a lack of permissions")
                print("               please proceed manually")
            print()

    elif os.path.isdir( path ):
        # it's a folder
        return_code = run(
            ["rmdir", path],
            stdout=DEVNULL,
            stderr=STDOUT)\
            .returncode

        if return_code == 1:
            result = False
            print("\n{err}Error{white}[{grey}folder{white}]{red}>{default} unable to this directory: {grass}%s/{rose}%s{default}"\
                .format(**craptool.text_colors)\
                %( parent, entry ))
            if craptool.more_output is True:
                print("               the error is most-likely caused by a non-empty folder")
                print("               or by a lack of permissions")
                print("               please manually remove it and retry")
            print()
    else:
        # unknown type
        result = False
        print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a directory, nor a file: {grass}%s/{rose}%s{default}"\
            .format(**craptool.text_colors)\
            %( parent, entry ))
        if craptool.more_output is True:
            print("             ok, that was unexpected")
            print("             please manually check it and consider reporting this issue")
        print()
    return result



def renameEntry(
    craptool: object,
    path: str,
    new_path: str
) -> bool :
    """
    Rename an entry (file/folder)
    """
    result = True
    try:
        os.rename( path, new_path )
    except:
        parent = path[:path.rfind('/')]
        entry  = path[len(parent)+1:]
        if os.path.isdir( path ):
            entry_type = "folder"
        elif os.path.isfile( path ):
            entry_type = "file"
        else:
            # unknown type
            result = False
            print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a directory, nor a file: {grass}%s/{rose}%s{default}"\
                .format(**craptool.text_colors)\
                %( parent, entry ))
            if craptool.more_output is True:
                print("             ok, that was unexpected")
                print("             please manually check it and consider reporting this issue")
            print()
        # print the error message only if not printed yet
        if result is True:
            result = False
            print("\n{err}Error{white}[{grey}file{white}]{red}>{default} unable to rename this %s: {grass}%s/{rose}%s{default}"\
                .format(**craptool.text_colors)\
                %( parent, entry, entry_type ))
            if craptool.more_output is True:
                print("               the error is most-likely caused by a lack of permissions")
                print("               please proceed manually")
            print()
    return result
