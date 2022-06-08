# craplog-fullCLI
Parse Apache2 logs to create statistics

<br>

## Table of contents

- [Overview](#overview)
- [Installation and execution](#installation-and-execution)
  - [Dependencies](#dependencies)
  - [Run without installation](#run-without-installation)
  - [Run with installation](#run-with-installation)
- [Usage](#usage)
  - [Arguments](#arguments)
  - [Examples](#examples)
  - [Output control](#output-control)
- [Log files](#log-files)
  - [Default logs files](#default-logs-files)
  - [Default logs path](#default-logs-path)
  - [Default logs structure](#default-logs-structure)
- [Statistics](#statistics)
  - [Storage](#storage)
  - [Examined fields](#examined-fields)
  - [Sessions statistics](#sessions-statistics)
  - [Global statistics](#global-statistics)
  - [Whitelist](#whitelist)
- [Extra features](#extra-features)
  - [Statistics viewer](#statistics-viewer)
  - [Check updates](#check-updates)
- [Final considerations](#final-considerations)
  - [Estimated working speed](#estimated-working-speed)
  - [Backups](#backups)
- [Contributions](#contributions)

<br><br>

## Overview

Craplog is a tool that takes Apache2 logs in their default form, parses them and creates simple statistics.

<br>

Welcome to the command line version

![screenshot](https://github.com/elB4RTO/CRAPLOG/blob/main/crapshots/fullCLI/craplog.png)

<br>

Searching for something different? Try the [other versions of CRAPLOG](https://github.com/elB4RTO/CRAPLOG).

<br><br>

## Installation and execution

### Dependencies
*None*

<br>

### Run without installation

- Download and unzip this repo
  <br>*or*<br>
  `git clone https://github.com/elB4RTO/craplog-fullCLI`<br><br>
- Open a terminal inside "*craplog-fullCLI-main/craplog*"
  <br>*or*<br>
  `cd craplog-fullCLI/craplog/`<br><br>
- Run craplog using python's environment (you must be in the *craplog/craplog* folder):
  <br>`python3 craplog.py --help`<br><br>

<br>

### Run with installation

- Download and unzip this repo
  <br>*or*<br>
  `git clone https://github.com/elB4RTO/craplog-fullCLI`<br><br>
- Open a terminal inside "*craplog-fullCLI-main*"
  <br>*or*<br>
  `cd craplog-fullCLI/`<br><br>
- Run the installation script:
  <br>`chmod +x ./install.sh && exec ./install.sh`<br><br>
- You can now run craplog from terminal, as any other application (you don't need to be in craplog's folder):
  <br>`craplog --help`<br><br>

<br><br>

## Usage

### Arguments

| Abbr. |           Option | Additional     | Description |
| :-: | -----------------: | :------------- | :-- |
| -h  |             --help |                | prints an help screen |
|     |         --examples |                | prints usage examples |
| -l  |             --less |                | less output on screen |
| -m  |             --more |                | more output on screen |
| -p  |      --performance |                | prints performances data |
|     |        --no-colors |                | prints text without using colors |
|     |      --auto-delete |                | auto-deletes files/folders when needed |
|     |       --auto-merge |                | auto-merges sessions with the same date |
| -e  |           --errors |                | make sstatistics of error logs too |
| -eO |      --only-errors |                | only uses error logs (doesn't parse access logs) |
| -gO |     --only-globals |                | only updates globals (doesn't store sessions) |
| -gA |    --avoid-globals |                | does not update global statistics |
| -b  |           --backup |                | stores a backup copy of the original logs file |
| -bT |       --backup-tar |                | stores the backup as a compressed tar.gz archive |
| -bZ |       --backup-zip |                | stores the backup as a compressed zip archive |
| -dO | --delete-originals |                | deletes the original log files when done |
|     |            --trash | *&lt;path&gt;* | moves files to Trash instead of remove<br>*&lt;path&gt;* is optional: if omitted, default will be used |
|     |            --shred |                | uses shred on files instead of remove |
| -P  |        --logs-path | *&lt;path&gt;* | path of the directory where the logs are located |
| -F  |        --log-files | *&lt;list&gt;* | list of log files to use (names, NOT paths)<br>*&lt;list&gt;*: whitespace-separated file names |
| -A  |    --access-fields | *&lt;list&gt;* | list of fields to use while parsing access logs<br>*&lt;list&gt;*: whitespace-separated fields |
| -W  |     --ip-whitelist | *&lt;list&gt;* | doesn't parse log lines from these IPs<br>*&lt;list&gt;*: whitespace-separated IPs |

<br>

### Examples

- Uses default log files as input, including errors (access logs are used by default). Stores a backup copy the original files as a *tar.gz* compressed archive, without deleting them. Moves files to trash if needed (instead of complete deletion). Global statistics will be updated by default.

    `craplog -e -bT --trash`<br><br>

- As the above one, but only parses errors (not access logs). Stores a backup copy the original files as a *zip* compressed archive, without deleting them. Shreds files if needed (instead of normal deletion). Global statistics will be updated by default.

    `craplog -eO -bZ --shred`<br><br>


- Uses user-defined access and/or error logs files from an alternative logs path. Automatically merges sessions having the same date if needed.

    `craplog -e -P /your/logs/path -F file.log.2 file.log.3.gz --auto-merge`<br><br>


- Uses default log files for both access and error logs. Uses a whitelist for IPs and a selection of which access fields to parse.

    `craplog -e -W ::1 192.168. -A REQ RES`<br><br>


- Print more informations on screen, including performance details. Use the default access logs file but only update globals, not sessions.

    `craplog -m -p -gO`<br><br>


- Print less informations on screen, including performance details but without using colors. Use the default access and error logs files, but do not update globals. Make a backup copy of the original files used and delete them when done.

    `craplog -l -p --no-colors -e -gA -b -dO`<br><br>

<br>

### Output control

You can control the output on screen, like: quantity of informations printed, performance details and the use of colors.<br><br>

![output diffs](https://github.com/elB4RTO/CRAPLOG/blob/main/crapshots/fullCLI/output_diff.png)
*Normal output vs Less output*

<br><br>

## Log files

At the moment, it still only supports **Apache2** log files in their **default** form<br>
Be aware that log-files usage is not tracked, be careful of not parsing the same logs twice, which will lead to altered statistics<br><br>
Archived (**gzipped**) log files can be used as well as normal files

<br>

### Default logs files

If not specified, the files to be used will be **access.log.1** *and/or* **error.log.1**<br>

Different file/s can be used by passing their names with `-F <names>` / `--log-files <names>`<br>
Please note that only names have to be specified, not full paths<br>

<br>

### Default logs path

If not specified, the default path will be **/var/log/apache2/**<br>

A different path can be used by passing it with `-P <path>` / `--logs-path <path>`

<br>

### Default logs structure

**access.log.1**<br>
IP - - [DATE:TIME] "REQUEST URI" RESPONSE "FROM URI" "USER AGENT"<br>
*123.123.123.123 - - [01/01/2000:00:10:20 +0000] "GET /style.css HTTP/1.1" 200 321 "/index.php" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Firefox/86.0"*


**error.log.1**<br>
[DATE TIME] [LOG LEVEL] [PID] ERROR REPORT<br>
*[Mon Jan 01 10:20:30.456789 2000] [headers:trace2] [pid 12345] mod_headers.c(874): AH01502: headers: ap_headers_output_filter()*

<br><br>

## Statistics

### Storage

Statistics will be stored in Craplog's main folder: **craplog/crapstats**<br>
Please refer to the [statistics viewer tool](#statistics-viewer) to view your crapstats

<br>

### Examined fields

#### Access logs

Four fields can be examined while parsing **access** logs:

- IP address of the client
- User-agent of the client
- Requested page/URL
- Response code from the server

<br>You can select which fields to use by passing them with `-A <fields>` / `--access-fields <fields>`<br>
Available fields choices are: **IP**, **UA**, **REQ**, **RES**<br>

You can avoid parsing access logs by passing `-eO` / `--only-errors`<br>

<br>

#### Error logs

While parsing **error** logs, only two fields will be used:

- Log level
- Error report

<br>By default error logs won't be used, but you can parse them by passing `-e` / `--error-logs`<br>

<br>

### Sessions statistics

**Sessions** are made by grouping statistics depending on the **date** of the single lines and will be stored consequently: new content will be made if that date is not present in the *crapstats* yet, or it will be merged if the date already exists.<br><br>
Olny '**\*.log.\***' files will be considered valid as input. This is because these files (usually) contain the full logs stack of an entire (*past*) day.<br>
Running it against a *today*'s file (which is not complete yet) may lead to re-running it in the future on the same file, parsing the same lines twice<br>

You can avoid storing sessions by passing `-gO` / `--only-globals`<br>

<br>

### Global statistics

Additionally, **global statistics** will be created and/or updated *consequently*.<br>
These statistics are identical to the session ones, in fact they're just merged sessions, for a larger view.<br>

You can avoid updating globals by passing `-gA` / `--avoid-globals`<br>

<br>

### Whitelist

You can add IP addresses to this list (may them be full *IPs*, only the *net-ID* part or just a portion of your choice), in order to skip the relative lines by whitelisting (or blacklisting..?) them, in both **access** and **error** logs.<br><br>
Please notice that the given sequence must be the **starting part**: it's not possible (at the moment, and more likely also in future versions) to skip IPs ending or just containing that sequence.<br><br>
As an example, if you insert "123", then only IP addresses starting with that sequence will be skipped.<br>
If you insert ".1", then nothing will be skipped, since no IP will ever start with a dot.<br>
But the shortcut "::1" is used by Apache2 for internal connections and will therefore be valid to skip those lines.<br>

The **default** is to only skip logs from **::1**, but different sequences can be passed with `-W <IPs>` / `--ip-whitelist <IPs>`


<br><br>

## Extra features

### Statistics viewer


*COMING SOON*

<br>

### Check updates

*COMING SOON*

<br><br>

## Final considerations

### Estimated working speed

1~10 MB/s

May be higher or lower depending on the complexity of the logs, the complexity of the stored statistics (in case of merge), your hardware and the workload of your system during the execution.<br>
Usually, if Craplog is taking more than 10 seconds to parse 10 MB of data, it means you've probably been tested in some way (better to check).<br><br>

![performance diffs](https://github.com/elB4RTO/CRAPLOG/blob/main/crapshots/fullCLI/perf_diff.png)<br>
*The above image shows the difference in performances for two log files having the same number of lines and very similar dimensions.<br>
On the left side, the parsed logs resulted from a normal webserver activity.<br>
On the right side, the parsed logs resulted from a webserver scan (with tools like **sqlmap** and **nikto**, not nmap)*

<br>

### Backups

Craplog will automatically make backups of **global statistics** files (in case of fire).<br>
If something goes wrong and you lose your actual globals, you can recover them (at least the last backup taken).<br><br>
Move inside the folder you choose to store statistics in, open the "**globals**" folder, show hidden files and open the folder named "**.backups**'.<br>
The complete path should look like **/&lt;your_path&gt;/craplog/crapstats/globals/.backups/**<br>
Here you will find the last 3 backups taken. Folder named '3' is always the oldest and '1' the newest.<br><br>
A new backup is made every time you run Craplog *successfully* over globals.<br><br>
Please notice that SESSION statistics will **not** be backed-up

<br><br>

## Contributions

CRAPLOG is under development

If you have suggestions about how to improve it please open an ![issue](https://github.com/elB4RTO/craplog-fullCLI/issues) or make a ![pull request](https://github.com/elB4RTO/craplog-fullCLI/pulls)

If you're not running Apache, but you like this tool: same as the above (bring a sample of a log file)
