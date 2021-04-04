# craplog
A tool that scrapes Apache2 logs to create both Single-Session and Global statistics


CRAPLOG is a tool that takes Apache2 logs in their default form, scrapes them and creates simple statistics
It's meant to be ran daily



<b>USAGE</b>:

./craplog.sh <i>[ARGUMENTS]</i>


<b>ARGUMENTS</b>:

<b>-h</b> / <b>--help</b> <i>---></i> prints help screen and exit
<b>-c</b> / <b>--clean</b> <i>---></i> creates a cleaned access.log file
<b>-e</b> / <b>--errors</b> <i>---></i> makes statistics of error.log file too
<b>--only-errors</b> <i>---></i> only makes statistics of error.log file (skips access.log)
<b>--only-globals</b> <i>---></i> only updates GLOBAL statistics (remove any other stat file when job is done)
<b>--avoid-globals</b> <i>---></i> avoid updating GLOBAL statistics with the processed file/s
<b>--auto-delete</b> <i>---></i> auto deletes EVERY conflict file found (!CAUTION!)
<b>--shred</b> <i>---></i> use 'shred' to delete files instead of 'remove'


<b>NOTE</b>:
MAKE SURE TO BE INSIDE CRAPLOG'S DIRECTORY WHENEVER YOU RUN IT, or it will use your actual path as base path and will create files and folders in that point.
DON'T DO, for example:
<code>/Path/to/craplog/craplog.sh</code>

INSTEAD, DO:
<code>cd /Path/to/craplog/ && ./craplog.sh</code>



<b>LOG FILES</b>:

At the moment, it only supports <b>Apache2</b> log files in their <b>default</b> form and path
If you're using a different path, please open the file named <b>Clean.py</b> (you can find it inside the folder named <i>Crappy</i>) and <b>modify</b> these lines:
<b>19</b> ] for the <i>access.log</i> file
<b>91</b> ] for the <i>error.log</i> file

<i>DEFAULT PATH:</i>

/var/log/apache2/


<i>DEFAULT LOGS' FORM:</i>

<b>access.log.1</b>
IP - - [DATE:TIME] "REQUEST URI" RESPONSE "FROM URL" "USER AGENT"
123.123.123.123 - - [01/01/2000:00:10:20 +0000] "GET /style.css HTTP/1.1" 200 321 "/index.php" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Firefox/86.0"

<b>error.log.1</b>
[DATE TIME] [LOG LEVEL] [PID] ERROR REPORT
[Mon Jan 01 10:20:30.456789 2000] [headers:trace2] [pid 12345] mod_headers.c(874): AH01502: headers: ap_headers_output_filter()


<i>NOTE</i>:
Please notice that CRAPLOG is taking <b>*.log.1</b> files as input. this is because these files (by default) are renewed every day at midnight, so they contain the full log stack of the (past) day.
Because of that, when you run it, it will use yesterday's logs and store stat files cosequently.
As said before, CRAPLOG is meant to be ran daily. 


<b>CLEAN ACCESS.LOG FILE</b>:
This is nothing special. it just creates a file in which every line from a local connection is removed (this happens with statistics too).
After that the lines are re-arranged in order to be separeted by one empty line if the connection comes from the same IP address as the previous, or two empty lines if the IP is different from the above one.
This isn't much useful if you usually check logs using <i>cat | grep</i>, but it helps if you read them directly from file.
Not a default feature.



<b>STATISTIC FILES</b>:

By default, CRAPLOG takes as input only the <b><i>access.log.1</i></b> file (unless you specify to not use it, calling the <i>--only-err</i> or <i>--only-glob</i> ARGUMENTS, see below).

The first time you run it, it will create a folder named <i>STATS</i>.
Stat files will be stored inside that folder and sorted by date.

four <i>.crapstats</i> files will be created inside the folder named STATS:
<b>IP.crapstats</b> = IPs statistics of the choosen file
<b>REQ.crapstats</b> = REQUESTs statistics of the choosen file
<b>RES.crapstats</b> = RESPONSEs statistics of the choosen file
<b>UA.crapstats</b> = USER AGENTs statistics of the choosen file

You have the opportunity to also create statistics of the errors (<i>-e</i>) or even of only the errors (<i>--only-err</i> , this will skip the usage of the access.log file, if present).
this will create 2 additional files inside STATS folder:
<b>LEV.crapstats</b> = LOG LEVELs statistics of the choosen file
<b>ERR.crapstats</b> = ERROR REPORTs statistics of the choosen file


<b>GLOBAL STATISTIC FILES</b>:

additionally, by default CRAPLOG updates the GLOBAL statistics inside the <i>/STATS/GLOBALS</i> folder every time you run it (unless you specify to not do it, calling <i>--avoid-glob</i>).

Pease notice that if you run it twice for the same log file, GLOBAL statistics will not be reliable (obviously).

amaximum range of 6 GLOBAL files will be created inside craplog/GLOBALS/:
<b>GLOBAL.IP.crapstats</b> = GLOBAL IPs statistics
<b>GLOBAL.REQ.crapstats</b> = GLOBAL REQUESTs statistics
<b>GLOBAL.RES.crapstats</b> = GLOBAL RESPONSEs statistics
<b>GLOBAL.UA.crapstats</b> = GLOBAL USER AGENTs statistics
[+]
<b>GLOBAL.LEV.crapstats</b> = GLOBAL LOG LEVELs statistics
<b>GLOBAL.ERR.crapstats</b> = GLOBAL ERROR REPORTs statistics



<b>EXAMPLES</b>:

<i>CRAPLOG's complete functionalities: makes a clean access logs file, creates statisics of both access.log and error.log files and use them to updates globals</i>
<code>./craplog.sh -c -e</code>

<i>Also creates statisics of error logs file, but avoids updating globals</i>
<code>./craplog.sh -e --avoid-glob</code>

<i>Takes both access.log and error.log files as input, but only updates global statistics. also auto-deletes every conflict file it finds</i>
<code>./craplog.sh -e --only-glob --auto-del</code>


<b>PS</b>:
Please note that even usign <i>--only-glob</i>, normal <i>.crapstat</i> files will be created. CRAPLOG needs session files in order to update global ones. after completing the job, session files will be removed automatically.


<b>FINAL WORDS</b>:

ESTIMATED WORK TIME:
2~10 sec / 1 MB
May be higher or lower depending on the length of your GLOBALS, the power of your CPU and the complexity of your SESSION logs.
If CRAPLOG takes more than 1 minute for a 10 MB file, you've probably been tested in some way (better to check).

As said before, CRAPLOG is under development
If you have suggestions about how to improve it please comment here or PM me

If you're not running Apache, but you like the tool: same as before, comment or PM (bring a sample of a log file)
