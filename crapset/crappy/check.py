
import os

from time import sleep


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
    crapset: object
) -> int :
    """
    Choice form
    """
    choice = 0
    MSG_choice = """Available choices:
  - {grey}[{default}{bold}d{grey}]{default}   {bold}delete{default} the conflict accordingly to the settings
  - {grey}[{default}{bold}r{grey}]{default}   {bold}rename{default} the conflict with a trailing '{italic}.copy{default}'
  - {grey}[{default}{bold}h{grey}]{default}   print this {bold}help{default} screen
  - {grey}[{default}{bold}q{grey}]{default}   abort the process and {bold}quit{default} crapset\
  """.format(**crapset.text_colors)
    while True:
        if crapset.less_output is False:
            print(MSG_choice)
            if crapset.more_output is True:
                print()
        proceed = input("Your choice? {white}[{yellow}d{grey}/{azul}r{grey}/{green}h/{rose}q{white}] :{default} "\
            .format(**crapset.text_colors)).strip().lower()
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
            if crapset.less_output is True:
                print(MSG_choice)
            else:
                print()
        else:
            # leave this normal yellow, it's secondary and doesn't need real attention
            print("\n{yellow}Warning{white}[{grey}choice{white}]{yellow}>{default} not a valid choice: {bold}%s{default}"\
                .format(**crapset.text_colors))
            if crapset.less_output is False:
                print()
                sleep(1)
    if crapset.less_output is False:
        print()
    return choice


def conflictFolder(
    crapset: object,
    path: str,
    parent_path: str,
    item_name: str
) -> int :
    """
    Ask the user what to do with the conflict
    """
    if crapset.more_output is True:
        print("\n")
    elif crapset.less_output is False:
        print()
    print("{warn}Warning{white}[{grey}conflict{white}]{warn}>{default} a folder is in conflict with the process: {grass}%s/{yellow}%s{default}"\
        .format(**crapset.text_colors)\
        %( parent_path, item_name ))
    if crapset.more_output is True:
        print("""\
                the entry was supposed to be a file, but it was found to be a folder
                if you haven't made any changes, please report this issue""")
    if crapset.less_output is False:
        print()
    return chooseAction( crapset )


def conflictFile(
    crapset: object,
    path: str,
    parent_path: str,
    item_name: str
) -> int :
    """
    Ask the user what to do with the conflict
    """
    if crapset.more_output is True:
        print("\n")
    elif crapset.less_output is False:
        print()
    print("{warn}Warning{white}[{grey}conflict{white}]{warn}>{default} a file is in conflict with the process: {grass}%s/{yellow}%s{default}"\
        .format(**crapset.text_colors)\
        %( parent_path, item_name ))
    if crapset.more_output is True:
        print("""\
                the entry was supposed to be a folder, but it was found to be a file
                if you haven't made any changes, please report this issue""")
    if crapset.less_output is False:
        print()
    return chooseAction( crapset )


def checkFolder(
    crapset: object,
    err_key: str,
    path:    str,
    parent_path: str="",
    entry_name:  str="",
    r: bool=True,
    w: bool=True,
    create:  bool=True,
    resolve: bool=True
) -> bool :
    """
    Check a crapstats folder
    """
    def failed():
        nonlocal checks_passed
        if checks_passed is True:
            checks_passed = False
    def makeit():
        nonlocal err_key, path, parent_path, entry_name, spaces, crapset
        # make the directory
        try:
            os.mkdir( path )
        except:
            # error creating directory
            failed()
            print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} unable to create the directory: {grass}%s/{rose}%s{default}"\
                .format(**crapset.text_colors)\
                %( err_key, parent_path, entry_name ))
            if crapset.more_output is True:
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
                    .format(**crapset.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if crapset.more_output is True:
                    spaces = " "*len(err_key)
                    print("%s         crapset doesn't have permissions to read from files inside this folder" %(spaces))
                    print("%s         please make the directory readable and retry" %(spaces))
                print()
            if w is True\
            and os.access( path, os.W_OK ) is False:
                failed()
                print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} directory is not writable: {grass}%s/{rose}%s{default}"\
                    .format(**crapset.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if crapset.more_output is True:
                    spaces = " "*len(err_key)
                    print("%s         crapset doesn't have permissions to write on files inside this folder" %(spaces))
                    print("%s         please make the directory writable and retry" %(spaces))
                print()
        else:
            # not a directory
            if os.path.isfile( path ):
                if resolve is True:
                    # resolve the conflict
                    choice = conflictFile( crapset, path, parent_path, entry_name )
                    if choice == 1:
                        # delete the file and make a dir
                        removeEntry( path )
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
                            renameEntry( path, new_path )
                            if create is True:
                                makeit()
                        except:
                            failed()
                            print("\n{err}Error{white}[{grey}permissions{white}]{red}>{default} unable to rename file: {grass}%s/{rose}%s{default}"\
                                .format(**crapset.text_colors)\
                                %( parent_path, entry_name ))
                            if crapset.more_output is True:
                                print("                    the error is most-likely caused by a lack of permissions")
                                print("                    please add permissions and retry, or intervene manually")
                            print()
                    else:
                        failed()
                        print("\n{err}Error{white}[{grey}variable{white}]{red}>{default} the choice has an invalid value: {rose}%s{default}"\
                            .format(**crapset.text_colors)\
                            %( choice ))
                        if crapset.more_output is True:
                            print("                 {white}@ {bold}crapset.crappy.check.checkFolder(){default}")
                            print("                 please consider reporting this issue")
                        print()
                else:
                    # do not resolve the conflict, print a message
                    failed()
                    print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} the given path doens't point to a directory: {grass}%s/{rose}%s{default}"\
                        .format(**crapset.text_colors)\
                        %( err_key, parent_path, entry_name ))
                    if crapset.more_output is True:
                        spaces = " "*len(err_key)
                        print("%s         the entry was supposed to be a folder, but it was found to be a file" %(spaces))
                    print()
                    
            else:
                # unknown type
                failed()
                print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a directory, nor a file: {grass}%s/{rose}%s{default}"\
                    .format(**crapset.text_colors)\
                    %( parent_path, entry_name ))
                if crapset.more_output is True:
                    print("             ok, that was unexpected")
                    print("             please manually check it and consider reporting this issue")
                print()
    else:
        # does not exists
        if create is True:
            try:
                os.mkdir( path )
            except:
                # error creating directory
                failed()
                print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} unable to create the directory: {grass}%s/{rose}%s{default}"\
                    .format(**crapset.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if crapset.more_output is True:
                    print("%s         the error is most-likely caused by a lack of permissions" %(spaces))
                    print("%s         please add read/write permissions to the whole crapstats folder and retry" %(spaces))
                print()
        elif create is False:
            failed()
            print("\n{err}Error{white}[{grey}path{white}]{red}>{default} the given path does not exist: %s\n"\
                .format(**crapset.text_colors)\
                %( checkPathRecursively( path, crapset.text_colors ) ))
        else:
            # when None, return a failure if doesn't exist
            checks_passed = False
    return checks_passed


def checkFile(
    crapset: object,
    err_key: str,
    path:    str,
    parent_path: str="",
    entry_name:  str="",
    r: bool=True,
    w: bool=True,
    create:  bool=True,
    resolve: bool=True
) -> bool :
    """
    Check a crapstats file
    """
    def failed():
        nonlocal checks_passed
        if checks_passed is True:
            checks_passed = False
    
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
                    .format(**crapset.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if crapset.more_output is True:
                    spaces = " "*len(err_key)
                    print("%s         crapset doesn't have permissions to read from this file" %(spaces))
                    print("%s         please make the file readable and retry" %(spaces))
                print()
            if w is True\
            and os.access( path, os.W_OK ) is False:
                failed()
                print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} file is not writable: {grass}%s/{rose}%s{default}"\
                    .format(**crapset.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if crapset.more_output is True:
                    spaces = " "*len(err_key)
                    print("%s         crapset doesn't have permissions to write in this file" %(spaces))
                    print("%s         please make the file writable and retry" %(spaces))
                print()
        else:
            # not a file
            if os.path.isdir( path ):
                if resolve is True:
                    choice = conflictFolder( crapset, path, parent_path, entry_name )
                    if choice == 1:
                        # delete the dir
                        removeEntry( path )
                    elif choice == 2:
                        # rename the file and make a dir
                        try:
                            new_path = path
                            while True:
                                new_path += ".copy"
                                if os.path.exists( new_path ) is False:
                                    break
                            renameEntry( path, new_path )
                        except:
                            failed()
                            print("\n{err}Error{white}[{grey}permissions{white}]{red}>{default} unable to rename folder: {grass}%s/{rose}%s{default}"\
                                .format(**crapset.text_colors)\
                                %( parent_path, entry_name ))
                            if crapset.more_output is True:
                                print("                    the error is most-likely caused by a lack of permissions")
                                print("                    please add permissions and retry, or intervene manually")
                            print()
                    else:
                        failed()
                        print("\n{err}Error{white}[{grey}variable{white}]{red}>{default} the choice has an invalid value: {rose}%s{default}"\
                            .format(**crapset.text_colors)\
                            %( choice ))
                        if crapset.more_output is True:
                            print("                 {white}@ {bold}crapset.crappy.check.checkFile(){default}")
                            print("                 please consider reporting this issue")
                        print()
                else:
                    # do not resolve the conflict, print a message
                    failed()
                    print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} the given path doens't point to a file: {grass}%s/{rose}%s{default}"\
                        .format(**crapset.text_colors)\
                        %( err_key, parent_path, entry_name ))
                    if crapset.more_output is True:
                        spaces = " "*len(err_key)
                        print("%s         the entry was supposed to be a file, but it was found to be a folder" %(spaces))
                    print()
            else:
                # unknown type
                failed()
                print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a file, nor a directory: {grass}%s/{rose}%s{default}"\
                    .format(**crapset.text_colors)\
                    %( parent_path, entry_name ))
                if crapset.more_output is True:
                    print("             ok, that was unexpected")
                    print("             please manually check it and consider reporting this issue")
                print()
    else:
        # does not exists
        if create is True:
            # ..yet, will be created later in any case
            pass
        else:
            # ..but should have existed, print a warning message
            print("\n{warn}Warning{white}[{grey}%s{white}]{red}>{default} configuration file {bold}not found{default}: {rose}%s{default}\n"\
                .format(**crapset.text_colors)\
                %( err_key, path[path.rfind('/')+1:] ))
            spaces = " "*len(err_key)
            if crapset.less_output is False:
                print("%s         the default configuration will be used" %(spaces))
            if crapset.more_output is True:
                print("%s         if you think you should have it, please exit now and check" %(spaces))
    return checks_passed




def removeEntry(self, path: str ):
    """
    Remove an entry (file/folder)
    """
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
            print("\n{err}Error{white}[{grey}file{white}]{red}>{default} unable to %s this file%s: {grass}%s/{rose}%s{default}"\
                .format(**crapset.text_colors)\
                %( parent, entry, del_mode, del_mode_aux ))
            if crapset.more_output is True:
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
            print("\n{err}Error{white}[{grey}folder{white}]{red}>{default} unable to %s this directory%s: {grass}%s/{rose}%s{default}"\
                .format(**crapset.text_colors)\
                %( parent, entry, del_mode, del_mode_aux ))
            if crapset.more_output is True:
                print("               the error is most-likely caused by a non-empty folder")
                print("               or by a lack of permissions")
                print("               please manually remove it and retry")
            print()
    else:
        # unknown type
        print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a directory, nor a file: {grass}%s/{rose}%s{default}"\
            .format(**crapset.text_colors)\
            %( parent, entry ))
        if crapset.more_output is True:
            print("             ok, that was unexpected")
            print("             please manually check it and consider reporting this issue")
        print()


def renameEntry(self, path: str, new_path: str):
    """
    Rename an entry (file/folder)
    """
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
            print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a directory, nor a file: {grass}%s/{rose}%s{default}"\
                .format(**crapset.text_colors)\
                %( parent, entry ))
            if crapset.more_output is True:
                print("             ok, that was unexpected")
                print("             please manually check it and consider reporting this issue")
            print()
        # print the error message only if not printed yet
        if crapset.proceed is True:
            print("\n{err}Error{white}[{grey}file{white}]{red}>{default} unable to rename this %s: {grass}%s/{rose}%s{default}"\
                .format(**crapset.text_colors)\
                %( parent, entry, entry_type ))
            if crapset.more_output is True:
                print("               the error is most-likely caused by a lack of permissions")
                print("               please proceed manually")
            print()
