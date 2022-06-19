================================================================================

                 A tool to create statistics from Apache2 logs

================================================================================


Synopsis

    craplog [TOOL] [OPTION] [ARGUMENT]

================================================================================

Tools

                   Tool  ¦  Description
--------------------------------------------------------------------------------
                         ¦
                    log  ¦  Craplog: make statistics from the logs
                         ¦  Implicit, can be omitted
                         ¦
                   view  ¦  Crapview: view your statistics
                         ¦  See the related --help for more details
                         ¦
                  setup  ¦  Crapset: configure these tools
                         ¦  See the related --help for more details
                         ¦
                 update  ¦  Crapup: check for updates
                         ¦  See the related --help for more details
                         ¦

================================================================================


Options

                 Option  ¦  Description
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
          --auto-delete  ¦  auto-choose to delete files/folders
                         ¦
                         ¦
           --auto-merge  ¦  auto-choose to merge sessions having the same date
                         ¦
                         ¦
  --warning-size <size>  ¦  emit a warning if a file's size exceeds this limit
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


Examples

   - Get help about a tool, Crapview in this case.
     To run a tool, replace --help with the options you please.
     
       craplog view --help

   - Use default log files (*.log.1) as input, including errors. Store the
     original files as a tar.gz compressed archive, without deleting them.
     Move files to trash if needed (instead of complete deletion).
     Global statistics will updated by default.
     
       craplog -e -bT --trash


   - As the previous but only parse errors, avoiding access logs. Store the
     original files as a zip compressed archive, without deleting them.
     Shred files if needed (instead of normal deletion).
     Global statistics will updated by default.
     
       craplog -eO -bZ --shred


   - Use defined access and/or error logs files from an alternative logs path.
     Automatically merge sessions having the same date if needed.
   
       craplog -e -P /your/logs/path -F file.log.2 file.log.3.gz --auto-merge


   - Use default log files for both access and error logs. Use a whitelist for
     IPs and select which access fields to parse.
   
       craplog -e -W ::1 192.168. -A REQ RES


   - Print more informations on screen, including performance details.
     Use the default access logs file but only update globals, not sessions.
     Set the warning level for log files size at 20 MB.
   
       craplog -m -p -gO --warning-size 20


   - Print less informations, with performances but without using colors.
     Use the default access and error logs files, but do not updatie globals.
     Make a backup copy of the original files used and delete them when done.
   
       craplog -l -p --no-colors -e -gA -b -dO

================================================================================
