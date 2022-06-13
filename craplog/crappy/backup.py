
import os
import subprocess
from datetime import date

import tarfile
from zipfile import ZipFile, ZIP_DEFLATED

from crappy.check import checkFolder

def newName(
    path:   str,
    suffix: str
) -> str :
    """
    Return the first available name
    """
    number = 1
    found = False
    while found is False:
        new_path = "%s/originals.%s%s" %( path, number, suffix )
        if os.path.exists(new_path):
            number += 1
        else:
            found = True
    return "originals.%s%s" %( number, suffix )


def backupFiles(
    craplog: object,
    path:    str
):
    """
    Backup original log files as they are
    """
    os.mkdir( path )
    path += "/"
    for log_file in craplog.log_files:
        craplog.printCaret( log_file )
        file_path = "%s/%s" %( craplog.logs_path, log_file )
        return_code = subprocess.run(
            ["cp", file_path, path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
            .returncode
        if return_code == 1:
            raise Exception(IOError)
        craplog.restoreCaret()


def backupTarGz(
    craplog: object,
    path:    str
):
    """
    Backup original log files as a tar.gz archive
    """
    with tarfile.open( path, 'w:gz' ) as tz:
        for log_file in craplog.log_files:
            craplog.printCaret(
                "%s {white}->{azul} tar.gz"\
                    .format(**craplog.text_colors)\
                    %(log_file) )
            file_path = "%s/%s" %( craplog.logs_path, log_file )
            tz.add(
                file_path,
                arcname=log_file )
            craplog.restoreCaret()


def backupZip(
    craplog: object,
    path:    str
):
    """
    Backup original log files as a zip archive
    """
    try:
        # try storing with compression
        with ZipFile( path, 'w' ) as z:
            for log_file in craplog.log_files:
                craplog.printCaret(
                    "%s {white}->{azul} zip"\
                        .format(**craplog.text_colors)\
                        %(log_file) )
                file_path = "%s/%s" %( craplog.logs_path, log_file )
                z.write(
                    file_path,
                    arcname=log_file,
                    compress_type=ZIP_DEFLATED,
                    compresslevel=9 )
                craplog.restoreCaret()
    except:
        # try storing normally
        craplog.restoreCaret()
        with ZipFile( path, 'w' ) as z:
            for log_file in craplog.log_files:
                craplog.printCaret( log_file )
                z.write(
                    file_path,
                    arcname=log_file )
                craplog.restoreCaret()


def backupOriginals(
    craplog: object
):
    """
    Main function to call for backups
    """
    checks_passed = True
    backup_date = str( date.today() )
    path = "%s/backups" %( craplog.statpath )
    craplog.proceed = checkFolder(
        craplog, "backups_folder", path,
        r=True, w=True, create=True, resolve=True )
    if craplog.proceed is True:
        path += "/%s" %( backup_date[:4] )
        craplog.proceed = checkFolder(
            craplog, "backups_folder", path,
            r=True, w=True, create=True, resolve=True )
        if craplog.proceed is True:
            path += "/%s" %( backup_date[5:7] )
            craplog.proceed = checkFolder(
                craplog, "backups_folder", path,
                r=True, w=True, create=True, resolve=True )
            if craplog.proceed is True:
                path += "/%s" %( backup_date[8:] )
                craplog.proceed = checkFolder(
                    craplog, "backups_folder", path,
                    r=True, w=True, create=True, resolve=True )
    
    if craplog.proceed is True:
        successful = True
        if craplog.archive_tar is True:
            try:
                # as tar.gz
                path += "/%s" %( newName( path, ".tar.gz" ) )
                backupTarGz( craplog, path )
            except:
                successful = False
                method = "a tar.gz archive"
                craplog.restoreCaret()
        elif craplog.archive_zip is True:
            try:
                # as zip
                path += "/%s" %( newName( path, ".zip" ) )
                backupZip( craplog, path )
            except:
                successful = False
                method = "a zip archive"
                craplog.restoreCaret()
        else:
            try:
                # as files inside a folder
                path += "/%s" %( newName( path, "" ) )
                backupFiles( craplog, path )
            except:
                successful = False
                method = "files copies"
                craplog.restoreCaret()
        if successful is False:
            craplog.printJobFailed()
            print("\n{err}Error{white}[{grey}backup{white}]{red}>{default} failed to backup as %s: {grass}%s/{rose}%s{default}"\
                .format(**craplog.text_colors)\
                %( method, path[:path.rfind('/')], path[path.rfind('/')+1:] ))
            if craplog.more_output is True:
                print("               the error is most-likely caused by a lack of permissions")
                print("               there's no reason to undo everything now")
                print("               please intervene manually and check permissions")
            print()



def backupGlobals(
    craplog: object
):
    """
    Backup global statistics (in case of fire)
    """
    success = True
    undoes = []
    remove = []
    err_msg = ""
    err_msg_more = ""
    globals_path = "%s/globals" %( craplog.statpath )
    backups_path = "%s/.backups" %( globals_path )
    success = checkFolder(
        craplog, "globals_backup", backups_path,
        r=True, w=True, create=True, resolve=True )
    if success is True:
        path = "%s/4" %( backups_path )
        if os.path.exists( path ):
            return_code = subprocess.run(
                ["rm", "-r", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
                .returncode
            if return_code == 1:
                success = False
                err_msg = "unable to remove the directory: {grass}%s/{rose}%s{default}"\
                    .format(**craplog.text_colors)\
                    %( path[:path.rfind('/')], path[path.rfind('/')+1:] )
                err_msg_more = "                       and manually remove this entry"
        if success is True:
            for n in reversed(range(1,4)):
                path = "%s/%s" %( backups_path, n )
                new_path = "%s/%s/" %( backups_path, n+1 )
                if checkFolder( craplog, "globals_backup", path, create=None, resolve=True ):
                    return_code = subprocess.run(
                        ["mv", path, new_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
                        .returncode
                    if return_code == 1:
                        undoes.append(new_path[:-1])
                        success = False
                        err_msg = "unable to rename the directory: {grass}%s/{rose}%s{default}"\
                            .format(**craplog.text_colors)\
                            %( path[:path.rfind('/')], path[path.rfind('/')+1:] )
                        break
    # check the new dir existence, make it if needed
    if success is True:
        try:
            os.mkdir( path )
            remove.append( path )
        except:
            # error creating directory
            success = False
            err_msg = "unable to create the directory: {grass}%s/{rose}%s{default}"\
                .format(**craplog.text_colors)\
                %( path[:path.rfind('/')], path[path.rfind('/')+1:] )
        if success is True:
            new_path = "%s/1/" %( backups_path )
            for log_type in ["access","error"]:
                path = "%s/%s" %( globals_path, log_type )
                if checkFolder( craplog, "globals_backup", path, create=None, resolve=True ):
                    return_code = subprocess.run(
                        ["cp", "-r", path, new_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.STDOUT)
                        .returncode
                    if return_code == 1:
                        undoes.append(new_path)
                        success = False
                        break
    # remove the last dir
    if success is True:
        path = "%s/4" %( backups_path )
        if os.path.exists( path ):
            return_code = subprocess.run(
                ["rm", "-r", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
                .returncode
            if return_code == 1:
                success = False
                err_msg = "unable to remove the directory: {grass}%s/{rose}%s{default}"\
                    .format(**craplog.text_colors)\
                    %( path[:path.rfind('/')], path[path.rfind('/')+1:] )
    # failed
    if success is False:
        craplog.printJobFailed()
        # print the error message
        print("\n{err}Error{white}[{grey}globals_backup{white}]{red}>{default} %s"\
            .format(**craplog.text_colors)\
            %( err_msg ))
        if craplog.more_output is True:
            print("                       the error is most-likely caused by a lack of permissions")
            print("                       please add read/write permissions to the whole crapstats folder")
            if err_msg_more != "":
                print(err_msg_more)
        print()
        # un-do the un-doable
        if len(remove) > 0:
            return_code = subprocess.run(
                ["rm", "-r", remove[0]],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
                .returncode
            if return_code == 1:
                success = False
                print("\n{err}Error{white}[{grey}globals_backup{white}]{red}>{default} unable to remove the directory: {grass}%s/{rose}%s{default}"\
                    .format(**craplog.text_colors)\
                    %( path[:path.rfind('/')], path[path.rfind('/')+1:] ))
                if craplog.more_output is True:
                    print("                       the error is most-likely caused by a lack of permissions")
                    print("                       please add read/write permissions to the whole crapstats folder")
                    print("                       and manually remove this entry")
                print()
        for path in reversed(undoes):
            new_path = "%s%s" %( path[:-1], int(path[-1:])-1 )
            if success is True:
                # skip moving if failed for a previous file
                return_code = subprocess.run(
                    ["mv", path, new_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
                    .returncode
            if return_code == 1:
                success = False
                print("\n{err}Error{white}[{grey}globals_backups{white}]{red}>{default} unable to rename the directory: {grass}%s/{rose}%s{default}"\
                    .format(**craplog.text_colors)\
                    %( path[:path.rfind('/')], path[path.rfind('/')+1:] ))
                print("                       {bold}before{default} to run craplog again, please manually {bold}rename{default} this entry {bold}as{default}: '{bold}%s{default}'"\
                    %( int(path[-1:])-1 )\
                    .format(**craplog.text_colors))
                if craplog.more_output is True:
                    print("                       the error is most-likely caused by a lack of permissions")
                    print("                       please add read/write permissions to the whole crapstats folder")
                print()
                # don't break, keep printing file names to be restored manually
