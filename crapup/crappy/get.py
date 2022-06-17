
from requests import get as GET


def versionCheck( crapup:object ):
    """
    Manages the request
    """
    # version check url
    url = "https://github.com/elB4RTO/craplog-CLI/blob/main/version_check"
    # additional headers
    headers = { 'Connection':'close' }
    # timeout for the connection to be established (in seconds)
    timeout = 120
    # mark to find
    version_mark = ".:!¦version¦!:.";
    # make the request
    try:
        request = GET( url, headers=headers, timeout=timeout )
        # pick the page content
        html = request.text
    except:
        crapup.printError(
            "request",
            "failed to establish a connection with: {rose}%s{default}"\
                .format(**crapup.text_colors)\
                %( url ))
        if crapup.more_output is True:
            print("                 please check your connection or retry again later")
            print("                 if this situation persists, please report this issue")
        print()
        crapup.exitAborted()
    # pick the actual version
    pos = html.find( version_mark )
    if pos >= 0:
        new_version = None
        try:
            # get the new version string and convert it to number
            new_version = html[
                (pos+len(version_mark)+1)
                :
                html.find(version_mark,(pos+len(version_mark)+1)) ]
            new_version = float( new_version )
        except:
            crapup.printError(
                "version_format",
                "unable to format the new version: {rose}%s{default}"\
                    .format(**crapup.text_colors)\
                    %( url ))
            if crapup.more_output is True:
                print("                       please report this issue")
            print()
            crapup.exitAborted()
    # compare to the actual version
    if new_version < crapup.version:
        # this version is newer then official one :O
        print("{err}Er{purple}R{blue}n{grass}1{warn}ng{white}[{grey}version{white}]{red}>{default} you have a version from the future! {rose}%s{default}\n"\
            .format(**crapup.text_colors)\
            %( new_version ))
        if crapup.more_output is True:
            print("                  seriously, if you haven't edited the {yellow}version_check{default} file, please report this issue"\
                .format(**crapup.text_colors))
        print()
        crapup.exitAborted()
    elif new_version == crapup.version:
        # same version
        print("{bold}%s{ok} is up-to-date{default}"\
            .format(**crapup.text_colors)\
            %( crapup.TXT_crapup ))
        if crapup.less_output is False:
            print()
        exit()
    else:
        # older version
        print("{bold}New version available{default}{paradise}:{default} {warn}%s{default}"\
            .format(**crapup.text_colors)\
            %( new_version ))
        if crapup.more_output is True:
            print("{grey}Repository link{white}:{default}\n\t%s"\
                .format(**crapup.text_colors)\
                %( crapup.repo ))
        print()
        exit()
