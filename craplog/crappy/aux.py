
def elbarto() -> str :
    return """\
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░██░░░░░░░░░░░░░░░░░░██████████░░░░░░░░░░░░░░░░░░░░
░░░░░███████░██░░░░░░░░░░░░░░░░░░░░░░█░░░░░░░░█░█░█░█░█░█░░░░░░
░░░░░░█░░░░░░██░░░░░███░░░░██░░████░░█░████░░░███████████░░░░░░
░░░░░░████░░░██░░░░░█░░█░░█░█░░░█░░█░█░█░░█░░░███████████░░░░░░
░░░░░░█░░░░░░██░░░░░███░░░█░░█░░███░░█░█░░█░░░███████████░ ░░░░
░░░░░░██████░█░░░░░░█░░█░██████░█░░█░░░████░░░            ░░░░░
░░░░░░░░░░░░░░░░░░░░███░░█░░░░█░█░░█░░░░░░░░░░  ▄       ▄░ ░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░███████████░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░███████████░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░\
"""


def craplogo() -> str :
    return """\
     __    ___     _____    ___     _       _____    _____
    / _|  |   \\   |  _  |  |   \\   | |     |  _  |  |  ___|
   | /    | || |  | |_| |  | || |  | |     | | | |  | |
   | |    |   /   |  _  |  |  _/   | |     | | | |  | | __
   | \\_   |   \\   | | | |  | |     | |__   | |_| |  | |_| |
    \\__|  |_|\\_\\  |_| |_|  |_|     |____|  |_____|  |_____|\
"""


def help( color_set ) -> str :
    return """\
                 {orange}Option{default}  ¦  {orange}Description{default}
{white}-------------------------------------------------------------------------------{default}
                         ¦
                     {bold}-h{default}  ¦  print this screen and exit
                 {bold}--help{default}  ¦
                         ¦
                         ¦
             {bold}--examples{default}  ¦  print usage examples
                         ¦
                         ¦
                     {bold}-l{default}  ¦  less output on screen
                 {bold}--less{default}  ¦
                         ¦
                         ¦
                     {bold}-m{default}  ¦  more output on screen
                 {bold}--more{default}  ¦
                         ¦
                         ¦
                     {bold}-p{default}  ¦  print performance data
          {bold}--performance{default}  ¦
                         ¦
                         ¦
            {bold}--no-colors{default}  ¦  print text without using colors
                         ¦
                         ¦
          {bold}--auto-delete{default}  ¦  auto-delete files/folders when needed
                         ¦
                         ¦
           {bold}--auto-merge{default}  ¦  auto-merge sessions with the same date
                         ¦
                         ¦
      {bold}--max-size{default} {italic}<size>{default}  ¦  emit a warning if a file's size exceeds this limit
                         ¦  the {italic}<size>{default} is in MB, if set to 0 means unlimited
                         ¦
                         ¦
                     {bold}-e{default}  ¦  make statistics of error logs too
               {bold}--errors{default}  ¦
                         ¦
                         ¦
                    {bold}-eO{default}  ¦  use only error logs (don't parse access logs)
          {bold}--only-errors{default}  ¦
                         ¦
                         ¦
                    {bold}-gO{default}  ¦  only update globals (don't store session statistics)
         {bold}--only-globals{default}  ¦
                         ¦
                         ¦
                    {bold}-gA{default}  ¦  do not update global statistics
        {bold}--avoid-globals{default}  ¦
                         ¦
                         ¦
                     {bold}-b{default}  ¦  store a backup of the original logs files
               {bold}--backup{default}  ¦
                         ¦
                         ¦
                    {bold}-bT{default}  ¦  store the backup as a compressed tar.gz archive
           {bold}--backup-tar{default}  ¦
                         ¦
                         ¦
                    {bold}-bZ{default}  ¦  store the backup as a compressed zip archive
           {bold}--backup-zip{default}  ¦
                         ¦
                         ¦
                    {bold}-dO{default}  ¦  delete the original log files when done
     {bold}--delete-originals{default}  ¦
                         ¦
                         ¦
         {bold}--trash{default} {italic}<path>{default}  ¦  move files to Trash instead of remove
                         ¦  {italic}<path>{default} is optional: if omitted, default will be used
                         ¦
                         ¦
                {bold}--shred{default}  ¦  use shred on files instead of remove
                         ¦
                         ¦
              {bold}-P{default} {italic}<path>{default}  ¦  directory where the logs are located
     {bold}--logs-path{default} {italic}<path>{default}  ¦
                         ¦
                         ¦
              {bold}-F{default} {italic}<list>{default}  ¦  list of log files to use (names, NOT paths)
     {bold}--log-files{default} {italic}<list>{default}  ¦  {italic}<list>{default}: whitespace-separated file names
                         ¦
                         ¦
              {bold}-A{default} {italic}<list>{default}  ¦  list of fields to use while parsing access logs
 {bold}--access-fields{default} {italic}<list>{default}  ¦  {italic}<list>{default}: whitespace-separated fields
                         ¦  available fields:
                         ¦    - IP   {italic}IP address of the client{default}
                         ¦    - UA   {italic}User-agent of the client{default}
                         ¦    - REQ  {italic}Request made by the client{default}
                         ¦    - RES  {italic}Response code from the server{default}
                         ¦
                         ¦
              {bold}-W{default} {italic}<list>{default}  ¦  log lines from these IPs won't be considered
  {bold}--ip-whitelist{default} {italic}<list>{default}  ¦  {italic}<list>{default}: whitespace-separated IPs
                         ¦  about the match:
                         ¦    - a whitelisted IP can be a complete address
                         ¦      or a slice of it (like the NET-ID)
                         ¦    - the match is successful when the logged IP
                         ¦      starts with /or/ is equal to a whitelisted IP
                         ¦
{white}-------------------------------------------------------------------------------{default}
""".format(**color_set).replace("¦", "{white}¦{default}".format(**color_set))


def examples( color_set ) -> str :
    return """\
  {orange}Examples{default}
{white}-------------------------------------------------------------------------------{default}

   - {green}Use default log files (*.log.1) as input, including errors. Store the
     original files as a tar.gz compressed archive, without deleting them.
     Move files to trash if needed (instead of complete deletion).
     Global statistics will updated by default.{default}
     
       {italic}craplog{default} {bold}-e -bT --trash{default}


   - {green}As the previous but only parse errors, avoiding access logs.
     Store the original files as a zip compressed archive, without deleting them.
     Shred files if needed (instead of normal deletion).
     Global statistics will updated by default.{default}
     
       {italic}craplog{default} {bold}-eO -bZ --shred{default}


   - {green}Use defined access and/or error logs files from an alternative logs path.
     Automatically merge sessions having the same date if needed.{default}
   
       {italic}craplog{default} {bold}-e -P {default}/your/logs/path {bold}-F {default}file.log.2 file.log.3.gz {bold}--auto-merge{default}


   - {green}Use default log files for both access and error logs. Use a whitelist for
     IPs and select which access fields to parse.{default}
   
       {italic}craplog{default} {bold}-e -W {default}::1 192.168. {bold}-A {default}REQ RES{default}


   - {green}Print more informations on screen, including performance details.
     Use the default access logs file but only update globals, not sessions.
     Set the warning level for log files size at 20 MB.{default}
   
       {italic}craplog{default} {bold}-m -p -gO --max-size 20{default}


   - {green}Print less informations on screen, with performances but without using colors.
     Use the default access and error logs files, but do not updatie globals.
     Make a backup copy of the original files used and delete them when done.{default}
   
       {italic}craplog{default} {bold}-l -p --no-colors -e -gA -b -dO{default}
""".format(**color_set)


def craplog( color_set ) -> str :
    return """{bold}\
   {red} CCCC{default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}L    {default}{bold}  {white}OOOOO{default}{bold}  {white}GGGGG{default}{bold}
   {red}C    {default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P   P{default}{bold}  {white}L    {default}{bold}  {white}O   O{default}{bold}  {white}G    {default}{bold}
   {red}C    {default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}L    {default}{bold}  {white}O   O{default}{bold}  {white}G  GG{default}{bold}
   {red}C    {default}{bold}  {orange}R  R {default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white}L    {default}{bold}  {white}O   O{default}{bold}  {white}G   G{default}{bold}
   {red} CCCC{default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white}LLLLL{default}{bold}  {white}OOOOO{default}{bold}  {white}GGGGG{default}\
""".format(**color_set)


def fin( color_set ) -> str :
    return """{bold}\
   {orange}FFFFF{default}{bold}  {grass}II{default}{bold}  {cyan}N   N{default}{bold}
   {orange}F    {default}{bold}  {grass}II{default}{bold}  {cyan}NN  N{default}{bold}
   {orange}FFF  {default}{bold}  {grass}II{default}{bold}  {cyan}N N N{default}{bold}
   {orange}F    {default}{bold}  {grass}II{default}{bold}  {cyan}N  NN{default}{bold}
   {orange}F    {default}{bold}  {grass}II{default}{bold}  {cyan}N   N{default}\
""".format(**color_set)


def colors() -> dict :
    return { 'default' : "\033[0m",
             'bold'    : "\033[1m",
             'italic'  : "\033[3m",
             'black'   : "\033[30m",
             'grey'    : "\033[90m",
             'white'   : "\033[37m",
             'paradise': "\033[97m",
             'purple'  : "\033[35m",
             'pink'    : "\033[95m",
             'blue'    : "\033[34m",
             'azul'    : "\033[94m",
             'cyan'    : "\033[36m",
             'grass'   : "\033[32m",
             'green'   : "\033[92m",
             'red'     : "\033[31m",
             'rose'    : "\033[91m",
             'orange'  : "\033[33m",
             'yellow'  : "\033[93m",
             'err'     : "\033[1;31m",
             'warn'    : "\033[1;33m" }


def no_colors() -> dict :
    return { 'default' : "",
             'bold'    : "",
             'italic'  : "",
             'black'   : "",
             'grey'    : "",
             'white'   : "",
             'paradise': "",
             'purple'  : "",
             'pink'    : "",
             'blue'    : "",
             'azul'    : "",
             'cyan'    : "",
             'grass'   : "",
             'green'   : "",
             'red'     : "",
             'rose'    : "",
             'orange'  : "",
             'yellow'  : "",
             'err'     : "",
             'warn'    : "" }
