# craplog
A tool that scrapes Apache2 logs to create both Single-Session and Global statistics

/<br>
<br>
CRAPLOG is a tool that takes Apache2 logs in their default form, scrapes them and creates simple statistics.<br>
It's meant to be ran daily
<br>
<br>
<br>
<b>USAGE</b>:<br>
<br>
./craplog.sh <i>[ARGUMENTS]</i><br>
<br>
<i>NOTE</i>:<br>
In order to run it, please give execution permission to executable files.<br>
From inside craplog's folder, run:<br>
<code>chmod +x ./craplog.sh ./crappy/Clean.py ./crappy/Stats.py ./crappy/Glob.py</code><br>
<br>
<br>
<br>
<b>ARGUMENTS</b>:<br>
<br>
<b>-h</b> / <b>--help</b> <i>---></i> prints help screen and exits<br>
<br>
<b>-c</b> / <b>--clean</b> <i>---></i> creates a CLEAN.access.log file (see below for details)<br>
<br>
<b>-e</b> / <b>--errors</b> <i>---></i> makes statistics of error.log.1 file too<br>
<br>
<b>--only-errors</b> <i>---></i> only makes statistics of error.log.1 file (skips access.log.1)<br>
<br>
<b>--only-globals</b> <i>---></i> only updates GLOBAL statistics<br>
<br>
<b>--avoid-globals</b> <i>---></i> avoid updating GLOBAL statistics with the processed file/s<br>
<br>
<b>--auto-delete</b> <i>---></i> automatically deletes every conflict file found (!CAUTION!)<br>
<br>
<b>--shred</b> <i>---></i> uses 'shred' to delete files instead of 'remove'<br>
<br>
<b>-b</b> / <b>--backup</b> <i>---></i> creates a BACKUP.tar.gz archive of both ACCESS and ERROR log files inside SESSION's stats folder<br>
<br>
<b>--backup+delete</b> <i>---></i> creates a BACKUP.tar.gz archive and delete both access.log.1 and error.log.1 original files (!CAUTION!)<br>
<br>
<br>
<b>IMPORTANT NOTE</b>:<br>
MAKE SURE TO BE INSIDE CRAPLOG'S DIRECTORY WHENEVER YOU RUN IT, or it will use your actual path as base path and will create files and folders in that point.<br>
DON'T DO, for example:<br>
<code>/path/to/craplog/craplog.sh</code><br>
INSTEAD, DO:<br>
<code>cd /path/to/craplog/ && ./craplog.sh</code><br>
<br>
<br><hr><br>
<br>
<b>LOG FILES</b>:<br>
<br>
At the moment, it only supports <b>Apache2</b> log files in their <b>default</b> form and path<br>
If you're using a different path, please open the file named <b>Clean.py</b> (you can find it inside the folder named <i>crappy</i>) and <b>modify</b> these lines:<br>
- <b>19</b> ] for the <i>access.log.1</i> file<br>
- <b>91</b> ] for the <i>error.log.1</i> file<br>
<br>
<br>
<i>DEFAULT PATH:</i><br>
<br>
/var/log/apache2/<br>
<br>
<br>
<i>DEFAULT LOG FORMS:</i><br>
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
Please notice that CRAPLOG is taking <b>*.log.1</b> files as input. This is because these files (by default) are renewed every day at midnight, so they contain the full log stack of the (past) day.<br>
Because of that, when you run it, it will use yesterday's logs and store stat files cosequently.<br>
CRAPLOG is meant to be ran daily.<br>
<br>
<br><hr><br>
<br>
<b>CLEAN.access.log FILE</b>:<br>
<br>
This is nothing special. It just creates a file in which every line from a local connection is removed (this happens with statistics too).<br>
After that, the lines are re-arranged in order to be separeted by one empty line if the connection comes from the same IP address as the previous, or two empty lines if the IP is different from the above one.<br>
This isn't much useful if you usually check logs using <i>cat | grep</i>, but it helps if you read them directly from file.<br>
Not a default feature.<br>
<br>
<br>
<br>
<b>SINGLE-SESSION STATISTIC FILES</b>:<br>
<br>
By default, CRAPLOG takes as input only the <b><i>access.log.1</i></b> file (unless you specify to not use it, calling the <i>--only-errors</i> argument, see below).<br>
<br>
The first time you run it, it will create a folder named <i>STATS</i>.<br>
Stat files will be stored inside that folder and sorted by date.<br>
<br>
Four <i>*.crapstats</i> files will be created inside the folder named STATS:<br>
- <b>IP.crapstats</b> = IPs statistics of the choosen file<br>
- <b>REQ.crapstats</b> = REQUESTs statistics of the choosen file<br>
- <b>RES.crapstats</b> = RESPONSEs statistics of the choosen file<br>
- <b>UA.crapstats</b> = USER AGENTs statistics of the choosen file<br>
<br>
You have the opportunity to also create statistics of the errors (<i>-e</i>) or even of only the errors (<i>--only-errors</i> , avoiding the usage of the access.log.1 file).<br>
This will create 2 additional files inside STATS folder:<br>
- <b>LEV.crapstats</b> = LOG LEVELs statistics of the choosen file<br>
- <b>ERR.crapstats</b> = ERROR REPORTs statistics of the choosen file<br>
<br>
<br>
<br>
<b>GLOBAL STATISTIC FILES</b>:<br>
<br>
Additionally, by default CRAPLOG updates the GLOBAL statistics inside the <i>/STATS/GLOBALS</i> folder every time you run it (unless you specify to not do it, calling <i>--avoid-globals</i>).<br>
<br>
Please notice that if you run it twice for the same log file, GLOBAL statistics will not be reliable (obviously).<br>
<br>
A maximum of 6 GLOBAL files will be created inside craplog/GLOBALS/:<br>
- <b>GLOBAL.IP.crapstats</b> = GLOBAL IPs statistics<br>
- <b>GLOBAL.REQ.crapstats</b> = GLOBAL REQUESTs statistics<br>
- <b>GLOBAL.RES.crapstats</b> = GLOBAL RESPONSEs statistics<br>
- <b>GLOBAL.UA.crapstats</b> = GLOBAL USER AGENTs statistics<br>
[+]<br>
- <b>GLOBAL.LEV.crapstats</b> = GLOBAL LOG LEVELs statistics<br>
- <b>GLOBAL.ERR.crapstats</b> = GLOBAL ERROR REPORTs statistics<br>
<br>
<br><hr><br>
<br>
<b>STATISTICS STRUCTURE</b>:<br>
<br>
Statistics' structure is the same for both SESSION and GLOBALS:<br>
<br>
<b>{ </b><i>COUNT</i><b> } &emsp; >>> &emsp; </b><i>ELEMENT</i><br>
<br>
<br>
<i>example</i>:<br>
<br>
{ 100 } &emsp; >>> &emsp; 200<br>
{ 10 } &emsp; >>> &emsp; 404<br>
<br>
<br><hr><br>
<br>
<b>USAGE EXAMPLES</b>:<br>
<br>
<i>- CRAPLOG's complete functionalities: makes a clean access logs file, creates statisics of both access.log.1 and error.log.1 files, uses them to update globals and creates a backup of the original files</i><br>
<code>./craplog.sh -b -c -e</code><br>
<br>
<i>- Takes both access logs and error logs files as input, but only updates global statistics. Also auto-deletes every conflict file it finds</i><br>
<code>./craplog.sh -e --only-globals --auto-delete</code><br>
<br>
<i>- Also creates statisics of error logs file, but avoids updating globals</i><br>
<code>./craplog.sh -e --avoid-globals</code><br>
<br>
<br>
<b>PS</b>:<br>
Please notice that even usign <i>--only-globals</i>, normal SESSION's statistic files will be created. CRAPLOG needs session files in order to update global ones.<br>
After completing the job, session files will be automatically removed.<br>
<br>
<br><hr><br>
<br>
<b>FINAL CONSIDERATIONS</b>:<br>
<br>
ESTIMATED WORKING SPEED:<br>
1~10 sec / 1 MB<br>
<br>
May be higher or lower depending on the complexity of your SESSION logs, the length of your GLOBALS and the power of your CPU.<br>
If CRAPLOG takes more than 1 minute for a 10 MB file, you've probably been tested in some way (better to check).<br>
<br>
<br>
CRAPLOG automatically makes backups of GLOBAL statistic files, in case of fire.<br>
If something goes wrong and you lose your actual GLOBAL files, you can recover them (at least the last backup).<br>
Move inside CRAPLOG folder, open 'STATS', open 'GLOBALS', show hidden files and open '.BACKUPS'. Here you will find the last 7 backups taken.<br>
Folder named '7' is always the newest and '1' the oldest.<br>
A new BACKUP is made every 7th time you run CRAPLOG. If you run it once a day, it will takes backups once a week, and will keep the older one for 7 weeks.<br>
<br>
CRAPLOG is under development.<br>
If you have suggestions about how to improve it please comment.<br>
<br>
If you're not running Apache, but you like this tool: same as before, comment (bring a sample of a log file).<br>
