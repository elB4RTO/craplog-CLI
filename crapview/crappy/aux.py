
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
     __    ___     _____    ___     _    _    _    _____    _    _
    / _|  |   \   |  _  |  |   \   | |  | |  | |  |  ___|  | |  | |
   | /    | || |  | |_| |  | || |  | |  | |  | |  | |__    | |  | |
   | |    |   /   |  _  |  |  _/   | \  / |  | |  |  __|   | \/\/ |
   | \_   |   \   | | | |  | |      \ \/ /   | |  | |___    \    / 
    \__|  |_|\_\  |_| |_|  |_|       \__/    |_|  |_____|    \/\/  \
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
            {bold}--no-colors{default}  ¦  do not apply colors to the output
                         ¦
{white}-------------------------------------------------------------------------------{default}\
""".format(**color_set).replace("¦", "{white}¦{default}".format(**color_set))


def examples( color_set ) -> str :
    return """\
{err}Examples{default}

   - {green}Use without colors.{default}
     
       {italic}crapview --no-colors{default}
""".format(**color_set)


def crapview( color_set ) -> str :
    return """{bold}\
   {red} CCCC{default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}V   V{default}{bold}  {white}II{default}{bold}  {white}EEEEE{default}{bold}  {white}W   W{default}{bold}
   {red}C    {default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P   P{default}{bold}  {white}V   V{default}{bold}  {white}II{default}{bold}  {white}E    {default}{bold}  {white}W   W{default}{bold}
   {red}C    {default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}V   V{default}{bold}  {white}II{default}{bold}  {white}EEE  {default}{bold}  {white}W W W{default}{bold}
   {red}C    {default}{bold}  {orange}R  R {default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white} V V {default}{bold}  {white}II{default}{bold}  {white}E    {default}{bold}  {white}W W W{default}{bold}
   {red} CCCC{default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white}  V  {default}{bold}  {white}II{default}{bold}  {white}EEEEE{default}{bold}  {white} W W {default}\
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
