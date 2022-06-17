
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


def LOGO_craplog() -> str :
    return """\
     __    ___     _____    ___     _       _____    _____
    / _|  |   \\   |  _  |  |   \\   | |     |  _  |  |  ___|
   | /    | || |  | |_| |  | || |  | |     | | | |  | |
   | |    |   /   |  _  |  |  _/   | |     | | | |  | | __
   | \\_   |   \\   | | | |  | |     | |__   | |_| |  | |_| |
    \\__|  |_|\\_\\  |_| |_|  |_|     |____|  |_____|  |_____|\
"""

def MSG_craplog( color_set ) -> str :
    return """{bold}\
   {red} CCCC{default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}L    {default}{bold}  {white}OOOOO{default}{bold}  {white}GGGGG{default}{bold}
   {red}C    {default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P   P{default}{bold}  {white}L    {default}{bold}  {white}O   O{default}{bold}  {white}G    {default}{bold}
   {red}C    {default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}L    {default}{bold}  {white}O   O{default}{bold}  {white}G  GG{default}{bold}
   {red}C    {default}{bold}  {orange}R  R {default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white}L    {default}{bold}  {white}O   O{default}{bold}  {white}G   G{default}{bold}
   {red} CCCC{default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white}LLLLL{default}{bold}  {white}OOOOO{default}{bold}  {white}GGGGG{default}\
""".format(**color_set)

def TXT_craplog( color_set ) -> str :
    return "{red}c{orange}r{grass}a{cyan}p{white}LOG{default}".format(**color_set)


def LOGO_crapview() -> str :
    return """\
     __    ___     _____    ___     _    _    _    _____    _    _
    / _|  |   \\   |  _  |  |   \\   | |  | |  | |  |  ___|  | |  | |
   | /    | || |  | |_| |  | || |  | |  | |  | |  | |__    | |  | |
   | |    |   /   |  _  |  |  _/   | \\  / |  | |  |  __|   | \\/\\/ |
   | \\_   |   \\   | | | |  | |      \\ \\/ /   | |  | |___    \\    / 
    \\__|  |_|\\_\\  |_| |_|  |_|       \\__/    |_|  |_____|    \\/\\/  \
"""

def MSG_crapview( color_set ) -> str :
    return """{bold}\
   {red} CCCC{default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}V   V{default}{bold}  {white}II{default}{bold}  {white}EEEEE{default}{bold}  {white}W   W{default}{bold}
   {red}C    {default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P   P{default}{bold}  {white}V   V{default}{bold}  {white}II{default}{bold}  {white}E    {default}{bold}  {white}W   W{default}{bold}
   {red}C    {default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}V   V{default}{bold}  {white}II{default}{bold}  {white}EEE  {default}{bold}  {white}W W W{default}{bold}
   {red}C    {default}{bold}  {orange}R  R {default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white} V V {default}{bold}  {white}II{default}{bold}  {white}E    {default}{bold}  {white}W W W{default}{bold}
   {red} CCCC{default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white}  V  {default}{bold}  {white}II{default}{bold}  {white}EEEEE{default}{bold}  {white} W W {default}\
""".format(**color_set)

def TXT_crapview( color_set ) -> str :
    return "{red}c{orange}r{grass}a{cyan}p{white}VIEW{default}".format(**color_set)


def LOGO_crapset() -> str :
    return """\
     __    ___     _____    ___     ____    ____    _____
    / _|  |   \\   |  _  |  |   \\   |  __|  |  __|  |_   _|
   | /    | || |  | |_| |  | || |  | |__   | |_      | |   
   | |    |   /   |  _  |  |  _/   |____|  |  _|     | |   
   | \\_   |   \\   | | | |  | |      __| |  | |__     | |   
    \\__|  |_|\\_\\  |_| |_|  |_|     |____|  |____|    |_|   \
"""

def MSG_crapset( color_set ) -> str :
    return """{bold}\
   {red} CCCC{default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}SSSSS{default}{bold}  {white}EEEEE{default}{bold}  {white}TTTTT{default}{bold}
   {red}C    {default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P   P{default}{bold}  {white}S    {default}{bold}  {white}E    {default}{bold}  {white}  T  {default}{bold}
   {red}C    {default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}SSSSS{default}{bold}  {white}EEE  {default}{bold}  {white}  T  {default}{bold}
   {red}C    {default}{bold}  {orange}R  R {default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white}    S{default}{bold}  {white}E    {default}{bold}  {white}  T  {default}{bold}
   {red} CCCC{default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white}SSSSU{default}{bold}  {white}EEEEE{default}{bold}  {white}  T  {default}\
""".format(**color_set)

def TXT_crapset( color_set ) -> str :
    return "{red}c{orange}r{grass}a{cyan}p{white}SET{default}".format(**color_set)


def LOGO_crapup() -> str :
    return """\
     __    ___     _____    ___     _    _    _____ 
    / _|  |   \\   |  _  |  |   \\   | |  | |  |  _  |
   | /    | || |  | |_| |  | || |  | |  | |  | | | |
   | |    |   /   |  _  |  |  _/   | |  | |  |  ___|
   | \\_   |   \\   | | | |  | |     | |__| |  | |    
    \\__|  |_|\\_\\  |_| |_|  |_|     |______|  |_|    \
"""

def MSG_crapup( color_set ) -> str :
    return """{bold}\
   {red} CCCC{default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}U   U{default}{bold}  {white}PPPPP{default}{bold}
   {red}C    {default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P   P{default}{bold}  {white}U   U{default}{bold}  {white}P   P{default}{bold}
   {red}C    {default}{bold}  {orange}RRRR {default}{bold}  {grass}AAAAA{default}{bold}  {cyan}PPPP {default}{bold}  {white}U   U{default}{bold}  {white}PPPPP{default}{bold}
   {red}C    {default}{bold}  {orange}R  R {default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white}U   U{default}{bold}  {white}P    {default}{bold}
   {red} CCCC{default}{bold}  {orange}R   R{default}{bold}  {grass}A   A{default}{bold}  {cyan}P    {default}{bold}  {white}UUUUU{default}{bold}  {white}P    {default}\
""".format(**color_set)

def TXT_crapup( color_set ) -> str :
    return "{red}c{orange}r{grass}a{cyan}p{white}UP{default}".format(**color_set)


def MSG_fin( color_set ) -> str :
    return """{bold}\
   {orange}FFFFF{default}{bold}  {grass}II{default}{bold}  {cyan}N   N{default}{bold}
   {orange}F    {default}{bold}  {grass}II{default}{bold}  {cyan}NN  N{default}{bold}
   {orange}FFF  {default}{bold}  {grass}II{default}{bold}  {cyan}N N N{default}{bold}
   {orange}F    {default}{bold}  {grass}II{default}{bold}  {cyan}N  NN{default}{bold}
   {orange}F    {default}{bold}  {grass}II{default}{bold}  {cyan}N   N{default}\
""".format(**color_set)

def TXT_fin( color_set ) -> str :
    return "{orange}F{grass}I{cyan}N{default}".format(**color_set)


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
             'sky'     : "\033[94m",
             'cyan'    : "\033[36m",
             'azul'    : "\033[96m",
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
