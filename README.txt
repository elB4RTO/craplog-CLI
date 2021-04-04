  ----------------------------------------------------------- 
 ¦                                                           ¦
 ¦     A tool that scrapes Apache2 default log files and     ¦
 ¦     creates both SINGLE-SESSION and GLOBAL statistics     ¦
 ¦                                                           ¦
 ¦===========================================================¦
 ¦                                                           ¦
 ¦  USAGE:                                                   ¦
 ¦                                                           ¦
 ¦  ./craplog.sh [ARGUMENTS]                                 ¦
 ¦                                                           ¦
 ¦===========================================================¦
 ¦                                                           ¦
 ¦  ARGUMENTS:                                               ¦
 ¦                                                           ¦
 ¦       -h        ¦ print this screen and exit              ¦
 ¦     --help      ¦                                         ¦
 ¦-----------------------------------------------------------¦
 ¦       -c        ¦ create a cleaned access.log.1 file      ¦
 ¦     --clean     ¦                                         ¦
 ¦-----------------------------------------------------------¦
 ¦       -e        ¦ make statistics of error.log.1 file too ¦
 ¦    --errors     ¦                                         ¦
 ¦-----------------------------------------------------------¦
 ¦  --only-errors  ¦ use only error logs (skip access logs)  ¦
 ¦-----------------------------------------------------------¦
 ¦ --only-globals  ¦ use only error logs (skip access logs)  ¦
 ¦-----------------------------------------------------------¦
 ¦ --avoid-globals ¦ use only error logs (skip access logs)  ¦
 ¦-----------------------------------------------------------¦
 ¦  --auto-delete  ¦ auto-delete conflict files              ¦
 ¦-----------------------------------------------------------¦
 ¦    --shred      ¦ shred files instead of remove           ¦
  -----------------------------------------------------------
