# craplog
A tool that scrapes Apache2 logs to create both Single-Session and Global statistics


CRAPLOG is a tool that takes Apache2 logs in their default form, scrapes them and creates simple statistics<br>
it's meant to be ran daily
<br>
<br>
<br>
<b>USAGE</b>:<br>
<br>
./craplog.sh <i>[ARGUMENTS]</i><br>
<br>
<br>
<b>ARGUMENTS</b>:<br>
<br>
<b>-h</b> / <b>--help</b> <i>---></i> prints help screen and exit<br>
<b>-c</b> / <b>--clean</b> <i>---></i> creates a cleaned access.log file<br>
<b>-e</b> / <b>--errors</b> <i>---></i> makes statistics of error.log file too<br>
<b>--only-errors</b> <i>---></i> only makes statistics of error.log file (skips access.log)<br>
<b>--only-globals</b> <i>---></i> only updates GLOBAL statistics (remove any other stat file when job is done)<br>
<b>--avoid-globals</b> <i>---></i> avoid updating GLOBAL statistics with the processed file/s<br>
<b>--auto-delete</b> <i>---></i> auto deletes EVERY conflict file found (!CAUTION!)<br>
<b>--shred</b> <i>---></i> use 'shred' to delete files instead of 'remove'<br>
<br>
<br>
<b>NOTE</b>:<br>
MAKE SURE TO BE INSIDE CRAPLOG'S DIRECTORY WHENEVER YOU RUN IT, or it will use your actual path as base path and will create files and folders in that point.<br>
DON'T DO, for example:<br>
	/Path/to/craplog/craplog.sh<br>
<br>
INSTEAD, DO:<br>
	cd /Path/to/craplog/ && ./craplog.sh<br>
<br>
<br>
<br>
<b>LOG FILES</b>:<br>
<br>
at the moment, it only supports <b>Apache2</b> log files in their <b>default</b> form and path<br>
if you're using a different path, please open the file named <b>Clean.py</b> (you can find it inside the folder named <i>Crappy</i>) and <b>modify</b> these lines:<br>
- <b>19</b> ] for the <i>access.log</i> file<br>
- <b>91</b> ] for the <i>error.log</i> file<br>
<br>
<i>default path:</i><br>
<br>
/var/log/apache2/<br>
<br>
<br>
<i>default log examples:</i><br>
<br>
<b>access.log.1</b><br>
IP - - [DATE:TIME] "REQUEST URI" RESPONSE "FROM URL" "USER AGENT"<br>
123.123.123.123 - - [01/01/2000:00:10:20 +0000] "GET /style.css HTTP/1.1" 200 321 "/index.php" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Firefox/86.0"<br>
<br>
<b>error.log.1</b><br>
[DATE TIME] [LOG LEVEL] [PID] ERROR REPORT<br>
[Mon Jan 01 10:20:30.456789 2000] [headers:trace2] [pid 12345] mod_headers.c(874): AH01502: headers: ap_headers_output_filter()<br>
<br>
<br>
<i>NOTE</i>:<br>
please notice that CRAPLOG is taking <b>*.log.1</b> files as input. this is because these files (by default) are renewed every day at midnight, so they contain the full log stack of the (past) day.<br>
because of that, when you run it, it will use yesterday's logs and store stat files cosequently.<br>
as said before, CRAPLOG is meant to be ran daily. <br>
<br>
<br>
<b>CLEAN ACCESS.LOG FILE</b>:<br>
this is nothing special. it just creates a file in which every line from a local connection is removed (this happens with statistics too).<br>
after that the lines are re-arranged in order to be separeted by one empty line if the connection comes from the same IP address as the previous, or two empty lines if the IP is different from the above one.<br>
this isn't much useful if you usually check logs using <i>cat | grep</i>, but it helps if you read them directly from file.<br>
not a default feature.<br>
<br>
<br>
<br>
<b>STATISTIC FILES</b>:<br>
<br>
by default, CRAPLOG takes as input only the <b><i>access.log.1</i></b> file (unless you specify to not use it, calling the <i>--only-err</i> or <i>--only-glob</i> ARGUMENTS, see below).<br>
<br>
the first time you run it, it will create a folder named <i>STATS</i>.<br>
stat files will be stored inside that folder and sorted by date.<br>
<br>
four <i>.crapstats</i> files will be created inside the folder named STATS:<br>
- <b>IP.crapstats</b> = IPs statistics of the choosen file<br>
- <b>REQ.crapstats</b> = REQUESTs statistics of the choosen file<br>
- <b>RES.crapstats</b> = RESPONSEs statistics of the choosen file<br>
- <b>UA.crapstats</b> = USER AGENTs statistics of the choosen file<br>
<br>
you have the opportunity to also create statistics of the errors (<i>-e</i>) or even of only the errors (<i>--only-err</i> , this will skip the usage of the access.log file, if present).<br>
as the above, please move the <b><i>error.log</i></b> file you want to use inside craplog's folder and run the tool calling the ARGUMENT you choose.<br>
this will create 2 additional files inside STATS folder:<br>
- <b>LEV.crapstats</b> = LOG LEVELs statistics of the choosen file<br>
- <b>ERR.crapstats</b> = ERROR REPORTs statistics of the choosen file<br>
<br>
<br>
<b>GLOBAL STATISTIC FILES</b>:<br>
<br>
additionally, by default CRAPLOG updates the GLOBAL statistics inside the <i>/STATS/GLOBALS</i> folder every time you run it (unless you specify to not do it, calling <i>--avoid-glob</i>).<br>
<br>
please notice that if you run it twice for the same log file, GLOBAL statistics will not be reliable (obviously).<br>
<br>
a maximum range of 6 GLOBAL files will be created inside craplog/GLOBALS/:<br>
- <b>GLOBAL.IP.crapstats</b> = GLOBAL IPs statistics<br>
- <b>GLOBAL.REQ.crapstats</b> = GLOBAL REQUESTs statistics<br>
- <b>GLOBAL.RES.crapstats</b> = GLOBAL RESPONSEs statistics<br>
- <b>GLOBAL.UA.crapstats</b> = GLOBAL USER AGENTs statistics<br>
[+]<br>
- <b>GLOBAL.LEV.crapstats</b> = GLOBAL LOG LEVELs statistics<br>
- <b>GLOBAL.ERR.crapstats</b> = GLOBAL ERROR REPORTs statistics<br>
<br>
<br>
<br>
<b>EXAMPLES</b>:<br>
<br>
<i>- CRAPLOG's complete functionalities: makes a clean access logs file, creates statisics of both access.log and error.log files and use them to updates globals</i><br>
<code>./craplog.sh -c -e</code><br>
<br>
<i>- also creates statisics of error logs file, but avoids updating globals</i><br>
<code>./craplog.sh -e --avoid-glob</code><br>
<br>
<i>- takes both access.log and error.log files as input, but only updates global statistics. also auto-deletes every conflict file it finds</i><br>
<code>./craplog.sh -e --only-glob --auto-del</code><br>
<br>
<br>
<b>PS</b>:<br>
please note that even usign <i>--only-glob</i>, normal <i>.crapstat</i> files will be created. CRAPLOG needs session files in order to update global ones. after completing the job, session files will be removed automatically.<br>
<br>
<br>
<b>FINAL WORDS</b>:<br>
<br>
ESTIMATED WORK TIME:<br>
2~10 sec / 1 MB<br>
may be higher or lower depending on the length of your GLOBALS, the power of your CPU and the complexity of your SESSION logs.<br>
if CRAPLOG takes more than 1 minute for a 10 MB file, you've probably been tested in some way (better to check).<br>
<br>
as said before, CRAPLOG is under development<br>
if you have suggestions about how to improve it please comment here or PM me<br>
<br>
if you're not running Apache, but you like the tool: same as before, comment or PM (bring a sample of a log file)<br>
