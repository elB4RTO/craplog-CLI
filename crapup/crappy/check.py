
import os


def chooseAction(
    crapup: object
) -> int :
    """
    Choice form
    """
    choice = 0
    MSG_choice = """Available choices:
  - {grey}[{default}{bold}d{grey}]{default}   {bold}delete{default} the conflict accordingly to the settings
  - {grey}[{default}{bold}r{grey}]{default}   {bold}rename{default} the conflict with a trailing '{italic}.copy{default}'
  - {grey}[{default}{bold}h{grey}]{default}   print this {bold}help{default} screen
  - {grey}[{default}{bold}q{grey}]{default}   abort the process and {bold}quit{default} crapup\
  """.format(**crapup.text_colors)
    while True:
        if crapup.less_output is False:
            print(MSG_choice)
            if crapup.more_output is True:
                print()
        proceed = input("Your choice? {white}[{yellow}d{grey}/{azul}r{grey}/{green}h/{rose}q{white}] :{default} "\
            .format(**crapup.text_colors)).strip().lower()
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
            if crapup.less_output is True:
                print(MSG_choice)
            else:
                print()
        else:
            # leave this normal yellow, it's secondary and doesn't need real attention
            print("\n{warn}Warning{white}[{grey}choice{white}]{yellow}>{default} not a valid choice: {bold}%s{default}"\
                .format(**crapup.text_colors))
            if crapup.less_output is False:
                print()
    if crapup.less_output is False:
        print()
    if choice > 0:
        crapup.reprintJob()
    return choice


def conflictFolder(
    crapup: object,
    path: str,
    parent_path: str,
    item_name: str
) -> int :
    """
    Ask the user what to do with the conflict
    """
    crapup.printJobHalted()
    if crapup.more_output is True:
        print("\n")
    elif crapup.less_output is False:
        print()
    print("{warn}Warning{white}[{grey}conflict{white}]{warn}>{default} a folder is in conflict with the process: {grass}%s/{yellow}%s{default}"\
        .format(**crapup.text_colors)\
        %( parent_path, item_name ))
    if crapup.more_output is True:
        print("""\
                the entry was supposed to be a file, but it was found to be a folder
                if you haven't made any changes, please report this issue""")
    if crapup.less_output is False:
        print()
    return chooseAction( crapup )


def checkFile(
    crapup:  object,
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
    Check a crapstats file
    """
    def failed():
        nonlocal checks_passed, crapup
        if checks_passed is True:
            checks_passed = False
            crapup.printJobFailed()
    
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
                    .format(**crapup.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if crapup.more_output is True:
                    spaces = " "*len(err_key)
                    print("%s         crapup doesn't have permissions to read from this file" %(spaces))
                    print("%s         please make the file readable and retry" %(spaces))
                print()
            if w is True\
            and os.access( path, os.W_OK ) is False:
                failed()
                print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} file is not writable: {grass}%s/{rose}%s{default}"\
                    .format(**crapup.text_colors)\
                    %( err_key, parent_path, entry_name ))
                if crapup.more_output is True:
                    spaces = " "*len(err_key)
                    print("%s         crapup doesn't have permissions to write in this file" %(spaces))
                    print("%s         please make the file writable and retry" %(spaces))
                print()
        else:
            # not a file
            if os.path.isdir( path ):
                if resolve is True:
                    choice = 0
                    if crapup.auto_delete is True:
                        choice = 1
                    else:
                        choice = conflictFolder( crapup, path, parent_path, entry_name )
                    if choice == 1:
                        # delete the dir
                        crapup.removeEntry( path )
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
                            print("\n{err}Error{white}[{grey}permissions{white}]{red}>{default} unable to rename folder: {grass}%s/{rose}%s{default}"\
                                .format(**crapup.text_colors)\
                                %( parent_path, entry_name ))
                            if crapup.more_output is True:
                                print("                    the error is most-likely caused by a lack of permissions")
                                print("                    please add permissions and retry, or intervene manually")
                            print()
                    else:
                        failed()
                        print("\n{err}Error{white}[{grey}variable{white}]{red}>{default} the choice has an invalid value: {rose}%s{default}"\
                            .format(**crapup.text_colors)\
                            %( choice ))
                        if crapup.more_output is True:
                            print("                 {white}@ {bold}crapup.crappy.check.checkFile(){default}")
                            print("                 please consider reporting this issue")
                        print()
                else:
                    # do not resolve the conflict, print a message
                    failed()
                    print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} the given path doens't point to a file: {grass}%s/{rose}%s{default}"\
                        .format(**crapup.text_colors)\
                        %( err_key, parent_path, entry_name ))
                    if crapup.more_output is True:
                        spaces = " "*len(err_key)
                        print("%s         the entry was supposed to be a file, but it was found to be a folder" %(spaces))
                    print()
            else:
                # unknown type
                failed()
                print("\n{err}Error{white}[{grey}type{white}]{red}>{default} the entry is not a file, nor a directory: {grass}%s/{rose}%s{default}"\
                    .format(**crapup.text_colors)\
                    %( parent_path, entry_name ))
                if crapup.more_output is True:
                    print("             ok, that was unexpected")
                    print("             please manually check it and consider reporting this issue")
                print()
    else:
        # does not exists
        if create is True:
            # ..yet, will be created later in any case
            pass
        else:
            # ..but should have existed, print an error message
            failed()
            print("\n{err}Error{white}[{grey}%s{white}]{red}>{default} the given path does not exist: %s\n"\
                .format(**crapup.text_colors)\
                %( err_key, checkPathRecursively( path, crapup.text_colors ) ))
    return checks_passed
