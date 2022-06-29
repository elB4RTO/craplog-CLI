
from os import chdir
from os.path import abspath, exists
from subprocess import run, PIPE, DEVNULL

from craplib.utils import checkFolder, checkFile


def gitPull( crapup:object ):
    """
    Manages the git-pull
    """
    def gitConfig( field:str, value:str ):
        nonlocal crapup
        command = run(
            ["git","config",field,value],
            stdout=DEVNULL,
            stderr=PIPE )
        if command.returncode != 0:
            crapup.printError(
                "git_config",
                "failed to configure the local git")
            if crapup.less_output is False:
                print("""\
                   please consider reporting this issue
                   {italic}field:{default} {bold}%s{default}
                   {italic}value:{default} {bold}%s{default}"""\
                    .format(**crapup.text_colors)\
                    %( field, value ))
            if crapup.more_output is True:
                print("\n{rose}%s{default}\n"\
                    .format(**crapup.text_colors)\
                    %( command.stderr.decode.strip('\n') ))
            print()
            crapup.exitAborted()
    
    # remote git's address
    git_remote = "%s.git" %( crapup.repo )
    # fallback dir
    command = run(
        ["pwd"],
        stdout=PIPE,
        stderr=DEVNULL )
    if command.returncode != 0:
        crapup.printError(
            "pwd", 
            "failed to get the actual path"\
                .format(**crapup.text_colors))
        print()
        crapup.exitAborted()
    fallback_dir = abspath( command.stdout.decode().strip() )
    # change dir to be in craplog's main folder
    try:
        chdir( crapup.crappath )
    except:
        crapup.printError(
            "chdir", 
            "failed to step into Craplog's directory: {rose}%s{default}"\
                .format(**crapup.text_colors)\
                %( crapup.crappath ))
        print()
        crapup.exitAborted()
    
    # check if git is installed in the system
    command = run(
        ["which", "git"],
        stdout=DEVNULL,
        stderr=PIPE )
    if command.returncode != 0:
        crapup.printError(
            "git_package", 
            "it seems you don't have {bold}git{default} installed"\
                .format(**crapup.text_colors))
        crapup.exitAborted()
    
    # check if Craplog's git has been initialized
    command = run(
        ["git", "status"],
        stdout=DEVNULL,
        stderr=PIPE )
    if command.returncode != 0:
        while True:
            if crapup.less_output is False:
                print()
            print("{warn}Warning{white}[{grey}local_git{white}]{red}>{default} it seems you don't have a local {bold}Craplog's git{default} initialized"\
                .format(**crapup.text_colors))
            if crapup.less_output is False:
                print()
            choice = input("Do you want to initialize it? {white}[{green}y{grey}/{rose}n{white}] :{default} "\
                .format(**crapup.text_colors)).strip().lower()
            if choice in ["y","yes"]:
                break
            elif choice in ["n","no"]:
                crapup.exitAborted()
            else:
                if crapup.less_output is False:
                    print()
                print("{warn}Warning{white}[{grey}choice{white}]{warn}>{default} not a valid choice: {bold}%s{default}"\
                    .format(**crapup.text_colors))
        
        # initialize the local git
        command = run(
            ["git", "init","-b","main"],
            stdout=DEVNULL,
            stderr=PIPE )
        if command.returncode != 0:
            crapup.printError(
                "git_config",
                "failed to configure")
            crapup.exitAborted()
        
        # configure the local git
        gitConfig( "core.filemode","false" ) # basically tells git to remove the "executable bit" from the fetched files
        gitConfig(
            "remote.origin.url",
            git_remote )
        gitConfig(
            "remote.origin.fetch",
            "+refs/heads/*:refs/remotes/origin/*" )
        gitConfig( "remote.origin.prune","true" ) # update the local commit refs to follow the remote ones
        gitConfig( "branch.main.remote","origin" )
        gitConfig( "branch.main.merge","refs/heads/main" )
        gitConfig( "pull.rebase","false" ) # don't touch local files not related to the git index
        
        # add Craplog's files
        command = run(
            ["git", "add","craplib/","craplog/","crapset/","crapup/","crapview/","README.md", "LICENSE"],
            stdout=DEVNULL,
            stderr=PIPE )
        if command.returncode != 0:
            crapup.printError(
                "git_config",
                "failed to configure")
            crapup.exitAborted()
        
    # explicitly specify to ignore user's data folders [crapstats,configs]
    file_mode = 'w'
    found_stat  = False
    found_stats = False
    found_conf    = False
    found_configs = False
    trailing_newline = False
    path_ignore = "%s/.gitignore"%(crapup.crappath)
    if exists( path_ignore ):
        checkFile(
            crapup, "git_ignore", path_ignore,
            r=True, w=True, create=True, resolve=True )
        try:
            with open(".gitignore", 'r') as f:
                git_ignoreds = f.read()
        except:
            crapup.printError(
                "git_ignored", 
                "failed to read from file: {grass}%s/{rose}.gitignore{default}"\
                    .format(**crapup.text_colors)\
                    %( crapup.crappath ))
            crapup.exitAborted()
        file_mode = 'a'
        if git_ignoreds.endswith('\n'):
            trailing_newline = True
        git_ignoreds = git_ignoreds.strip().split()
        for path in git_ignoreds:
            path_ = path.rstrip('/')
            if path_ == "/crapstats"\
            or path_ == "crapstats":
                found_stats = True
            if path_ == "*.crapstat":
                found_stat = True
            elif path_ == "/crapconfs"\
              or path_ == "crapconfs":
                found_configs = True
            elif path_ == "*.crapconf":
                found_conf = True
    if found_stat is False or found_stats is False\
    or found_conf is False or found_configs is False:
        new_line = ""
        if trailing_newline is False:
            new_line += "\n"
        if found_stats is False:
            new_line += "/crapstats\n"
        if found_stat is False:
            new_line += "*.crapstat\n"
        if found_configs is False:
            new_line += "/crapconf\n"
        if found_configs is False:
            new_line += "*.crapconf\n"
        try:
            with open(path_ignore, file_mode) as f:
                f.write( new_line )
        except:
            crapup.printError(
                "git_ignore",
                "failed to write on file: {grass}%s/{rose}.gitignore{default}"\
                    .format(**crapup.text_colors)\
                    %( crapup.crappath ))
    
    # copy the .gitignore to restore later an keep personal changes
    if exists( path_ignore ):
        command = run(
            ["mv", ".gitignore", ".gitignore.copy"],
            stdout=DEVNULL,
            stderr=PIPE )
        if command.returncode != 0:
            crapup.printError(
                "git_ignore",
                "failed to backup file: {bold}.gitignore{default}"\
                    .format(**crapup.text_colors))
            print()
            crapup.exitAborted()
    # pull the remote git
    command = run(
        ["git", "pull", "origin", "main"],
        stdout=DEVNULL,
        stderr=PIPE )
    if command.returncode != 0:
        crapup.printError(
            "git_pull",
            "failed to pull the remote git")
        if crapup.less_output is False:
            print("                 remote url: {bold}%s{default}"\
                .format(**crapup.text_colors)\
                %( git_remote ))
        if crapup.more_output is True:
            print("\n{rose}%s{default}"\
                .format(**crapup.text_colors)\
                %( command.stderr.decode().strip('\n') ))
        print()
        crapup.exitAborted()
    # restore the personal gitignore file
    if exists( "%s.copy" %(path_ignore) ):
        command = run(
            ["mv", ".gitignore.copy", ".gitignore"],
            stdout=DEVNULL,
            stderr=PIPE )
        if command.returncode != 0:
            print("{warn}Warning{white}[{grey}git_ignore{white}]{red}>{default} failed to restore file: {bold}.gitignore.copy{default}"\
                .format(**crapup.text_colors))
            if crapup.less_output is False:
                print("                     that was you personal file before the update")
                print("                     if you need it, please restore it manually")
            print()
    # remove un-needed stuff
    command = run(
        ["rm", "-r", "install.sh", "update.sh", "installation_stuff", ".github"],
        stdout=DEVNULL,
        stderr=PIPE )
    if command.returncode != 0:
        print("{yellow}Warning{white}[{grey}clean_up{white}]{red}>{default} failed to remove some un-needed files"\
            .format(**crapup.text_colors))
        if crapup.less_output is False:
            print("                   nothing to worry about, just Craplog's repo stuff")
        print()
    
    # succesfully updated
    print("{bold}%s{ok} is up-to-date{default}"\
        .format(**crapup.text_colors)\
        %( crapup.TXT_craplog ))
