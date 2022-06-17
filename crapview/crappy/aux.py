
def help( color_set:dict ) -> str :
    return """\
{err}Synopsis{default}

    {grey}craplog{default} view {grey}[{white}OPTION{grey}]{default}


{err}Options{default}

                 {yellow}Option{default}  ¦  {yellow}Description{default}
{white}--------------------------------------------------------------------------------{default}
                         ¦
                     {bold}-h{default}  ¦  print this screen and exit
                 {bold}--help{default}  ¦
                         ¦
                         ¦
            {bold}--no-colors{default}  ¦  do not apply colors to the output
                         ¦
{white}--------------------------------------------------------------------------------{default}\
""".format(**color_set).replace("¦", "{white}¦{default}".format(**color_set))


def examples( color_set:dict ) -> str :
    return """\
{err}Examples{default}

   - {green}Use without colors.{default}
     
       {italic}craplog{default} {azul}view{default} {bold}--no-colors{default}\
""".format(**color_set)
