
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
                     {bold}-e{default}  ¦  make statistics of error logs too
               {bold}--errors{default}  ¦
                         ¦
                         ¦
          {bold}--only-errors{default}  ¦  use only error logs (don't parse access logs)
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

   - {green}use default log files (*.log.1) as input, including errors. store the
     original files as a tar.gz compressed archive and move files to trash if
     needed (instead of complete deletion).
     global statistics will updated by default.{default}
     
       {italic}craplog{default} {bold}-e -bT --trash{default}


   - {green}use defined access and/or error logs files from an alternative logs path.
     automatically merge sessions having the same date if needed.{default}
   
       {italic}craplog{default} {bold}-e -P {default}/your/path {bold}-F {default}file.log.2 file.log.3.gz {bold}--auto-merge{default}


   - {green}use default log files for both access and error logs. use a whitelist for
     ips and select which access fields to parse.{default}
   
       {italic}craplog{default} {bold}-e -W {default}::1 192.168. {bold}-A {default}REQ RES{default}


   - {green}print more informations on screen, including performance details.
     use the default access logs file but only update globals, not sessions.{default}
   
       {italic}craplog{default} {bold}-m -p --only-globals{default}


   - {green}print less informations on screen, without using colors. use the default
     access and error logs files, but do not updatie globals. make a backup
     copy of the original files used and delete them (by shredding) when done.{default}
   
       {italic}craplog{default} {bold}-l --no-colors -e --avoid-globals -b -dO --shred{default}
""".format(**color_set)


def craplog( color_set ) -> str :
    return """{bold}\
   {red} CCCC{default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {blue}L    {default}{bold}  {purple}OOOOO{default}{bold}  {white}GGGGG{default}{bold}
   {red}C    {default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P   P{default}{bold}  {blue}L    {default}{bold}  {purple}O   O{default}{bold}  {white}G    {default}{bold}
   {red}C    {default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {blue}L    {default}{bold}  {purple}O   O{default}{bold}  {white}G  GG{default}{bold}
   {red}C    {default}{bold}  {orange}R  R {default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {blue}L    {default}{bold}  {purple}O   O{default}{bold}  {white}G   G{default}{bold}
   {red} CCCC{default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {blue}LLLLL{default}{bold}  {purple}OOOOO{default}{bold}  {white}GGGGG{default}\
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
             'yellow'  : "\033[93m" }


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
             'yellow'  : "" }