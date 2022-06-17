
def MSG_help( color_set:dict ) -> str :
    return """\
{err}Synopsis{default}

    {grey}craplog{default} set {grey}[{white}OPTION{grey}]{default}


{err}Options{default}

                 {yellow}Option{default}  ¦  {yellow}Description{default}
{white}--------------------------------------------------------------------------------{default}
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
{white}--------------------------------------------------------------------------------{default}\
""".format(**color_set).replace("¦", "{white}¦{default}".format(**color_set))


def MSG_examples( color_set:dict ) -> str :
    return """\
{err}Examples{default}

   - {green}Use.{default}
     
       {italic}craplog{default} {azul}set{default}


   - {green}UUse with less output on screen and no colors.{default}
     
       {italic}craplog{default} {azul}set{default} {bold}-l --no-colors{default}\
""".format(**color_set)
