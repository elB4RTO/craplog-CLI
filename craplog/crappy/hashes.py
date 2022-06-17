
from os.path import exists
from hashlib import sha256

from crappy.check import checkFile


def digestFile(
    craplog: object,
    path: str
) -> str :
    """
    Digest a file's hash
    """
    try:
        file_hash = sha256()
        with open(path,'rb') as f:
            # read data in blocks and update the hash
            while True:
                data_block = f.read( 8192 )
                if bool(data_block) is False:
                    break
                file_hash.update( data_block )
        file_hash = file_hash.hexdigest()
        return file_hash
    except:
        craplog.printJobFailed()
        print("\n{err}Error{white}[{grey}file_hash{white}]{red}>{default} unable to digest file: {grass}%s/{rose}.hashes{default}"\
            .format(**craplog.text_colors)\
            %( path, path[path.rfind('/')+1:] ))
        if craplog.more_output is True:
            print("                  craplog needs the hash to avoid parsing the same file twice")
            print("                  please check this file manually and retry")
        print()
        craplog.exitAborted()



def bringHashes( craplog: object ):
    """
    Get the previous hashes for usage-track of log files
    """
    path = "%s/.hashes" %( craplog.statpath )
    checks_passed = checkFile(
        craplog, "usage_hashes", path, craplog.statpath, ".hashes",
        r=True, w=True, create=True, resolve=True )
    if checks_passed is True:
        if exists( path ):
            try:
                # read the content
                with open(path,'r') as f:
                    hash_list = f.read().strip().split('\n')
                # discard possible invalid values
                halted = False
                for h in hash_list:
                    if len(h) != 64:
                        if craplog.more_output is True:
                            if halted is False:
                                craplog.printJobHalted()
                                halted = True
                            print("\n{warn}Warning{white}[{grey}hash_size{white}]{warn}>{default} hash discarded: {bold}%s{default}\n"\
                                .format(**craplog.text_colors))
                        continue
                    craplog.hashes.append(h)
                if halted is True\
                and craplog.more_output is True:
                    craplog.reprintJob()
                # rename the (now) old file as a backup copy
                new_path = "%s.bak" %( path )
                craplog.renameEntry( path, new_path )
                if craplog.proceed is True:
                    craplog.undo_paths.append( new_path )
                else:
                    craplog.exitAborted()
            except:
                craplog.printJobFailed()
                print("\n{err}Error{white}[{grey}hashes_file{white}]{red}>{default} unable to read from file: {grass}%s/{rose}.hashes{default}"\
                    .format(**craplog.text_colors)\
                    %( craplog.statpath ))
                if craplog.more_output is True:
                    print("                    the error is most-likely caused by a lack of permissions")
                    print("                    please make the file readable and retry")
                print()
                craplog.exitAborted()



def storeHashes( craplog: object ):
    """
    Save the actual list of hashes for usage-track of log files
    """
    path = "%s/.hashes" %( craplog.statpath )
    checks_passed = checkFile(
        craplog, "usage_hashes", path, craplog.statpath, ".hashes",
        w=True, create=True, resolve=True )
    if checks_passed is False:
        craplog.exitAborted()
    # try to write on file
    try:
        hash_list = ""
        for h in craplog.hashes:
            hash_list += "%s\n" %( h )
        hash_list = hash_list.strip()
        # write the new content
        with open(path,'w') as f:
            f.write( hash_list )
        # check if the path is already in the undoes
        if "%s.bak"%(path) not in craplog.undo_paths:
            # if the .bak is in the list, there is no need to append
            craplog.undo_paths.append( path )
    except:
        craplog.printJobFailed()
        print("\n{err}Error{white}[{grey}hashes_file{white}]{red}>{default} unable to write on file: {grass}%s/{rose}.hashes{default}"\
            .format(**craplog.text_colors)\
            %( craplog.statpath ))
        if craplog.more_output is True:
            print("                    the error is most-likely caused by a lack of permissions")
            print("                    please make the file readable and retry")
        print()
        craplog.exitAborted()
    
