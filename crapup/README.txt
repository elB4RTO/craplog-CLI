================================================================================

                           A tool to update the tools

================================================================================

Synopsis

    craplog update [OPTION]

================================================================================

Options

                 Option  ¦  Description
--------------------------------------------------------------------------------
                         ¦
                     -h  ¦  print this screen and exit
                 --help  ¦
                         ¦
                         ¦
             --examples  ¦  print usage examples and exit
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
            --no-colors  ¦  do not apply colors to the output
                         ¦
                         ¦
                  --git  ¦  update Craplog with a git-pull
                         ¦

================================================================================

Examples

   - Check for a new version and print the response message.
     
       craplog update


   - Fetch every new change from the remote git repository and apply it.
     This is made using system's git package.
     If Craplog's local git has not been initialized yet, offers to do so.
     
       craplog update --git

================================================================================
