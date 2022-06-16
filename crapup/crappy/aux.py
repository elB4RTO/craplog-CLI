
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
     __    ___     _____    ___     _    _    _____ 
    / _|  |   \\   |  _  |  |   \\   | |  | |  |  _  |
   | /    | || |  | |_| |  | || |  | |  | |  | | | |
   | |    |   /   |  _  |  |  _/   | |  | |  |  ___|
   | \\_   |   \\   | | | |  | |     | |__| |  | |    
    \\__|  |_|\\_\\  |_| |_|  |_|     |______|  |_|    \
"""


def help( color_set ) -> str :
    return """\
{err}Synopsis{default}

    crapup {grey}[{white}OPTION{grey}]{default}


{err}Options{default}

                 {yellow}Option{default}  ¦  {yellow}Description{default}
{white}-------------------------------------------------------------------------------{default}
                         ¦
                     {bold}-h{default}  ¦  print this screen and exit
                 {bold}--help{default}  ¦
                         ¦
                         ¦
             {bold}--examples{default}  ¦  print usage examples and exit
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
            {bold}--no-colors{default}  ¦  do not apply colors to the output
                         ¦
                         ¦
                  {bold}--git{default}  ¦  update Craplog with a git-pull
                         ¦
{white}-------------------------------------------------------------------------------{default}\
""".format(**color_set).replace("¦", "{white}¦{default}".format(**color_set))


def examples( color_set ) -> str :
    return """\
{err}Examples{default}

   - {green}Check for a new version and print the response message.{default}
     
       {italic}crapup{default}


   - {green}Fetch every new change from the remote git repository and apply it.
     This is made using system's {bold}{cyan}git{default}{cyan} package.
     If Craplog's local git has not been initialized yet, offers to do so.{default}
     
       {italic}craplog{default} {bold}--git{default}\
""".format(**color_set)


def crapup( color_set ) -> str :
    return """{bold}\
   {red} CCCC{default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}U   U{default}{bold}  {white}PPPPP{default}{bold}
   {red}C    {default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P   P{default}{bold}  {white}U   U{default}{bold}  {white}P   P{default}{bold}
   {red}C    {default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}U   U{default}{bold}  {white}PPPPP{default}{bold}
   {red}C    {default}{bold}  {orange}R  R {default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white}U   U{default}{bold}  {white}P    {default}{bold}
   {red} CCCC{default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white}UUUUU{default}{bold}  {white}P    {default}\
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
             'ok'      : "\033[1;32m",
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
             'ok'      : "",
             'err'     : "",
             'warn'    : "" }
