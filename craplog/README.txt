================================================================================

                 A tool to create statistics from Apache2 logs

================================================================================

  USAGE:

    INSTALLED:
      craplog <arguments>

    FROM LOCATION:
      python3 craplog.py <arguments>

================================================================================
 
  ARGUMENTS:
 
                 OPTION  ¦  DESCRIPTION
--------------------------------------------------------------------------------
                         ¦
                     -h  ¦  print this screen and exit
                 --help  ¦
                         ¦
                         ¦
             --examples  ¦  print usage examples
                         ¦
                         ¦
                     -l  ¦  less output on screen
                 --less  ¦
                         ¦
                         ¦
                     -m  ¦  more output on screen
                 --more  ¦
                         ¦
                         ¦
                     -p  ¦  print performance data
          --performance  ¦
                         ¦
                         ¦
            --no-colors  ¦  print text without using colors
                         ¦
                         ¦
          --auto-delete  ¦  auto-delete files/folders when needed
                         ¦
                         ¦
           --auto-merge  ¦  auto-merge sessions with the same date
                         ¦
                         ¦
      --max-size <size>  ¦  emit a warning if a file's size exceeds this limit
                         ¦  the <size> is in MB, if set to 0 means unlimited
                         ¦
                         ¦
                     -e  ¦  make statistics of error logs too
               --errors  ¦
                         ¦
                         ¦
                    -eO  ¦  use only error logs (don't parse access logs)
          --only-errors  ¦
                         ¦
                         ¦
                    -gO  ¦  only update globals (don't store session statistics)
         --only-globals  ¦
                         ¦
                         ¦
                    -gA  ¦  do not update global statistics
        --avoid-globals  ¦
                         ¦
                         ¦
                     -b  ¦  store a backup of the original logs files
               --backup  ¦
                         ¦
                         ¦
                    -bT  ¦  store the backup as a compressed tar.gz archive
           --backup-tar  ¦
                         ¦
                         ¦
                    -bZ  ¦  store the backup as a compressed zip archive
           --backup-zip  ¦
                         ¦
                         ¦
                    -dO  ¦  delete the original log files when done
     --delete-originals  ¦
                         ¦
                         ¦
         --trash <path>  ¦  move files to Trash instead of remove
                         ¦  <path> is optional: if omitted, default will be used
                         ¦
                         ¦
                --shred  ¦  use shred on files instead of remove
                         ¦
                         ¦
              -P <path>  ¦  directory where the logs are located
     --logs-path <path>  ¦
                         ¦
                         ¦
              -F <list>  ¦  list of log files to use (names, NOT paths)
     --log-files <list>  ¦  <list>: whitespace-separated file names
                         ¦
                         ¦
              -A <list>  ¦  list of fields to use while parsing access logs
 --access-fields <list>  ¦  <list>: whitespace-separated fields
                         ¦  available fields:
                         ¦    - IP   IP address of the client
                         ¦    - UA   User-agent of the client
                         ¦    - REQ  Request made by the client
                         ¦    - RES  Response code from the server
                         ¦
                         ¦
              -W <list>  ¦  log lines from these IPs won't be considered
  --ip-whitelist <list>  ¦  <list>: whitespace-separated IPs
                         ¦  about the match:
                         ¦    - a whitelisted IP can be a complete address
                         ¦      or a slice of it (like the NET-ID)
                         ¦    - the match is successful when the logged IP
                         ¦      starts with /or/ is equal to a whitelisted IP
                         ¦

================================================================================
 
  EXAMPLES:
  
   - USE DEFAULT LOG FILES (*.log.1) AS INPUT, INCLUDING ERRORS. STORE THE
     ORIGINAL FILES AS A tar.gz COMPRESSED ARCHIVE AND MOVE FILES TO TRASH IF
     NEEDED (INSTEAD OF COMPLETE DELETION).
     GLOBAL STATISTICS WILL UPDATED BY DEFAULT.
     
       craplog -e -bT --trash

   - AS THE PREVIOUS BUT ONLY PARSE ERRORS, AVOIDING ACCESS LOGS.
     STORE THE ORIGINAL FILES AS A zip COMPRESSED ARCHIVE, WITHOUT DELETING THEM.
     SHRED FILES IF NEEDED (INSTEAD OF NORMAL DELETION).
     GLOBAL STATISTICS WILL UPDATED BY DEFAULT.
     
       craplog -eO -bZ --shred


   - USE DEFINED ACCESS AND/OR ERROR LOGS FILES FROM AN ALTERNATIVE LOGS PATH.
     AUTOMATICALLY MERGE SESSIONS HAVING THE SAME DATE IF NEEDED.
   
       craplog -e -P /your/logs/path -F file.log.2 file.log.3.gz --auto-merge


   - USE DEFAULT LOG FILES FOR BOTH ACCESS AND ERROR LOGS. USE A WHITELIST FOR
     IPs AND SELECT WHICH ACCESS FIELDS TO PARSE.
   
       craplog -e -W ::1 192.168. -A REQ RES


   - PRINT MORE INFORMATIONS ON SCREEN, INCLUDING PERFORMANCE DETAILS.
     USE THE DEFAULT ACCESS LOGS FILE BUT ONLY UPDATE GLOBALS, NOT SESSIONS.
     SET THE WARNING LEVEL FOR LOG FILES SIZE AT 20 MB.
   
       craplog -m -p -gO --max-size 20


   - PRINT LESS INFORMATIONS ON SCREEN, WITH PERFORMANCES BUT WITHOUT USING COLORS.
     USE THE DEFAULT ACCESS AND ERROR LOGS FILES, BUT DO NOT UPDATIE GLOBALS.
     MAKE A BACKUP COPY OF THE ORIGINAL FILES USED AND DELETE THEM WHEN DONE.
   
       craplog -l --no-colors -e -gA -b -dO
  
  
--------------------------------------------------------------------------------
 
