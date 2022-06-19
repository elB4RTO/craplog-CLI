
def MSG_help( color_set:dict ) -> str :
    return """\
{err}Synopsis{default}

    craplog {grey}[{white}TOOL{grey}]{default} {grey}[{white}OPTION{grey}]{default} {grey}[{italic}{white}ARGUMENT{default}{grey}]{default}


{err}Tools{default}

                   {yellow}Tool{default}  ¦  {yellow}Description{default}
{white}--------------------------------------------------------------------------------{default}
                         ¦
                    {italic}log{default}  ¦  Craplog: make statistics from the logs
                         ¦  {italic}Implicit, can be omitted{default}
                         ¦
                   {bold}view{default}  ¦  Crapview: view your statistics
                         ¦  {italic}See the related {default}--help{italic} for more details{default}
                         ¦
                  {bold}setup{default}  ¦  Crapset: configure these tools
                         ¦  {italic}See the related {default}--help{italic} for more details{default}
                         ¦
                 {bold}update{default}  ¦  Crapup: check for updates
                         ¦  {italic}See the related {default}--help{italic} for more details{default}
                         ¦
{white}--------------------------------------------------------------------------------{default}


{err}Options{default}

                 {yellow}Option{default}  ¦  {yellow}Description{default}
{white}--------------------------------------------------------------------------------{default}
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
          {bold}--auto-delete{default}  ¦  auto-choose to delete files/folders
                         ¦
                         ¦
           {bold}--auto-merge{default}  ¦  auto-choose to merge sessions having the same date
                         ¦
                         ¦
  {bold}--warning-size{default} {italic}<size>{default}  ¦  emit a warning if a file's size exceeds this limit
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
{white}--------------------------------------------------------------------------------{default}\
""".format(**color_set).replace("¦", "{white}¦{default}".format(**color_set))


def MSG_examples( color_set:dict ) -> str :
    return """\
{err}Examples{default}

   - {green}Get help about a tool, {azul}Crapview{default}{green} in this case.
     To run a tool, replace {cyan}--help{green} with the options you please.{default}
     
       {italic}craplog{default} {azul}view{default} {bold}--help{default}

   - {green}Use default log files (*.log.1) as input, including errors. Store the
     original files as a tar.gz compressed archive, without deleting them.
     Move files to trash if needed (instead of complete deletion).
     Global statistics will updated by default.{default}
     
       {italic}craplog{default} {bold}-e -bT --trash{default}


   - {green}As the previous but only parse errors, avoiding access logs. Store the
     original files as a zip compressed archive, without deleting them.
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
   
       {italic}craplog{default} {bold}-m -p -gO --warning-size 20{default}


   - {green}Print less informations, with performances but without using colors.
     Use the default access and error logs files, but do not updatie globals.
     Make a backup copy of the original files used and delete them when done.{default}
   
       {italic}craplog{default} {bold}-l -p --no-colors -e -gA -b -dO{default}\
""".format(**color_set)
