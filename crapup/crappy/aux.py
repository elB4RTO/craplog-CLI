
def MSG_help( color_set:dict ) -> str :
    return """\
{err}Synopsis{default}

    {grey}craplog{default} update {grey}[{white}OPTION{grey}]{default}


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
                         ¦
                  {bold}--git{default}  ¦  update Craplog with a git-pull
                         ¦
{white}--------------------------------------------------------------------------------{default}\
""".format(**color_set).replace("¦", "{white}¦{default}".format(**color_set))


def MSG_examples( color_set:dict ) -> str :
    return """\
{err}Examples{default}

   - {green}Check for a new version and print the response message.{default}
     
       {italic}craplog{default} {azul}update{default}


   - {green}Fetch every new change from the remote git repository and apply it.
     This is made using system's {bold}{cyan}git{default}{cyan} package.
     If Craplog's local git has not been initialized yet, offers to do so.{default}
     
       {italic}craplog{default} {azul}update{default} {bold}--git{default}\
""".format(**color_set)
