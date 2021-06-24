#!/bin/bash

# EDIT THE NEXT LINES TO SETUP CRAPLOG AND RUN IT WITHOUT HAVING TO USE ARGUMENTS
# 1 = YES , 0 = NO
# THESE VARIABLES WILL DETERMINE THE EXECUTION OF THE CODE
# TO HAVE IT WORKING AS EXPECTED, EDIT USING COMMON SENSE AND LOGIC
#
#
# USE COMMAND LINE ARGUMENTS (default 1)
# [  ]
# SETTING THIS VARIABLE TO '0' MEANS THAT EVERY ARGUMENT WILL BE IGNORED
# ONLY THE MANUAL CONFIGURATION OF THESE VARIABLES WILL BE USED
UseArguments=1
#
# REDUCE THE OUTPUT ON SCREEN (default 0)
# [ -l  /  --less ]
LessOutput=0
#
# ALSO MAKE A CLEAN ACCESS LOGS FILE (default 0)
# [ -c  /  --clean ]
# CAN'T BE '1' IF 'AccessLogs' IS '0'
CleanAccessLogs=0
#
# MAKE SESSION STATISTICS FILES FROM ACCESS LOGS (default 1)
# [  ]
# SETTING THIS TO '0' IS LIKE USING [ --only-errors ]
# CAN'T BE '0' IF 'CleanAccessLogs' IS '1'
AccessLogs=1
#
# MAKE SESSION STATISTICS FILES FROM ERROR LOGS (default 0)
# [ -e  /  --errors ]
ErrorLogs=0
#
# ONLY UPDATE GLOBAL STATISTICS, WITHOUT MAKING SESSION FILES (default 0)
# [ --only-globals ]
# CAN'T BE '1' IF 'GlobalsAvoid' IS '1'
GlobalsOnly=0
#
# AVOID UPDATING GLOBAL STATISTICS, BUT MAKE THE SESSION ONES (default 0)
# [ --avoid-globals ]
# CAN'T BE '1' IF 'GlobalsOnly' IS '1'
# CAN'T BE '0' IF 'AccessLogs' IS '0' AND 'ErrorLogs' IS '0'
GlobalsAvoid=0
#
# MAKE A BACKUP ARCHIVE FROM THE ORIGINAL LOG FILES (default 0)
# [ -b  /  --backup ]
Backup=0
#
# MAKE A BACKUP ARCHIVE FROM ORIGINAL LOGS AND THEN DELETE THOSE FILES (default 0)
# [ --backup+delete ]
BackupDelete=0
#
# AUTO-DELETE CONFLICT FILES (default 0)
# [ --auto-delete ]
AutoDelete=0
#
# SHRED FILES INSTEAD OF SIMPLE REMOVE (default 0)
# [ --shred ]
Shred=0
#
# END


if [[ "$UseArguments" -eq "1" ]]
	then
		for arg in "$@"
			do
				case "$arg" in
					"-h" | "--help" | "-help" | "help")
						printf "\n"
						cat ./.elbarto.txt ./README.txt
						printf "\n"
						exit
						;;
					"-l" | "--less")
						LessOutput=1
						;;
					"-c" | "--clean")
						CleanAccessLogs=1
						;;
					"-e" | "--errors")
						ErrorLogs=1
						;;
					"--only-errors")
						AccessLogs=0
						ErrorLogs=1
						;;
					"--only-globals")
						GlobalsOnly=1
						;;
					"--avoid-globals")
						GlobalsAvoid=1
						;;
					"-b" | "--backup")
						Backup=1
						;;
					"--backup+delete")
						BackupDelete=1
						;;
					"--auto-delete")
						AutoDelete=1
						;;
					"--shred")
						Shred=1
						;;
					"-elbarto-")
						printf "\n"
						cat ./.elbarto.txt
						printf "\n"
						exit
						;;
					*)
						printf "\n$(tput setaf 3)Error$(tput sgr0): $(tput setaf 1)$arg$(tput sgr0) is not a valid argument\n\n"
						exit
						;;
				esac
			done
	fi

printf "   $(tput bold)\n"
printf "   $(tput setaf 1) CCCC  $(tput setaf 3)RRRR   $(tput setaf 2)AAAAA  $(tput setaf 6)PPPP   $(tput setaf 4)L      $(tput setaf 5)OOOOO  $(tput setaf 7)GGGGG\n"
printf "   $(tput setaf 1)C      $(tput setaf 3)R   R  $(tput setaf 2)A   A  $(tput setaf 6)P   P  $(tput setaf 4)L      $(tput setaf 5)O   O  $(tput setaf 7)G    \n"
printf "   $(tput setaf 1)C      $(tput setaf 3)RRRR   $(tput setaf 2)AAAAA  $(tput setaf 6)PPPP   $(tput setaf 4)L      $(tput setaf 5)O   O  $(tput setaf 7)G  GG\n"
printf "   $(tput setaf 1)C      $(tput setaf 3)R  R   $(tput setaf 2)A   A  $(tput setaf 6)P      $(tput setaf 4)L      $(tput setaf 5)O   O  $(tput setaf 7)G   G\n"
printf "   $(tput setaf 1) CCCC  $(tput setaf 3)R   R  $(tput setaf 2)A   A  $(tput setaf 6)P      $(tput setaf 4)LLLLL  $(tput setaf 5)OOOOO  $(tput setaf 7)GGGGG\n\n$(tput sgr0)"

if [[ ! -e /var/log/apache2 ]];
	then
		printf "\n$(tput setaf 3)Error$(tput sgr0): directory $(tput setaf 1)/var/log/apache2/$(tput sgr0) does not exist\n\n"
		exit
	fi
if [[ "$AccessLogs" -eq "1" ]]
	then
		if [[ ! -e /var/log/apache2/access.log.1 ]]
			then
				printf "\n$(tput setaf 3)Error$(tput sgr0): there is no $(tput setaf 1)access.log.1$(tput sgr0) file inside $(tput setaf 2)/var/log/apache2/$(tput sgr0)\n\n"
				exit
			fi
	fi
if [[ "$ErrorLogs" -eq "1" ]]
	then
		if [[ ! -e /var/log/apache2/error.log.1 ]]
			then
				printf "\n$(tput setaf 3)Error$(tput sgr0): there is no $(tput setaf 1)error.log.1$(tput sgr0) file inside $(tput setaf 2)/var/log/apache2/$(tput sgr0)\n\n"
				exit
			fi
	fi
if [[ "$AccessLogs" -eq "0" && "$CleanAccessLogs" -eq "1" ]]
	then
		printf "\n$(tput setaf 3)Error$(tput sgr0): not possible to make a clean access log file [$(tput setaf 6)-c$(tput sgr0)] without working on a access.log file [$(tput setaf 6)--only-errors$(tput sgr0)]\n\n"
		exit
	fi
if [[ "$GlobalsOnly" -eq "1" && "$GlobalsAvoid" -eq "1" ]]
	then
		printf "\n$(tput setaf 3)Error$(tput sgr0): you can't use $(tput setaf 6)--only-globals$(tput sgr0) toghether with $(tput setaf 6)--avoid-globals$(tput sgr0)\n\n"
		exit
	fi
if [[ "$GlobalsAvoid" -eq "1" && "$AccessLogs" -eq "0" && "$ErrorLogs" -eq "0" ]]
	then
		printf "\n$(tput setaf 3)Error$(tput sgr0): you can't avoid making both global and session statistics, nothing will be done\n\n"
		exit
	fi

printf "\nWELCOME TO CRAPLOG\nUse $(tput setaf 6)craplog.sh --help$(tput sgr0) to view an help screen\n"
if [[ "$AutoDelete" -eq "1" ]]
	then
		printf "$(tput setaf 3)Auto-Delete$(tput sgr0) is $(tput bold)ON$(tput sgr0)\n"
	fi
printf "\n"
sleep 2 && wait
if [[ ! -e ./STATS ]]
	then
		mkdir ./STATS &> /dev/null && wait
	fi
if [[ ! -e ./STATS/GLOBALS ]]
	then
		mkdir ./STATS/GLOBALS &> /dev/null && wait
	fi
if [[ ! -e ./STATS/GLOBALS/.BACKUPS ]]
	then
		mkdir ./STATS/GLOBALS/.BACKUPS &> /dev/null && wait
		echo "0" > ./STATS/GLOBALS/.BACKUPS/.last_time && wait
	fi
if [[ ! -e ./STATS/GLOBALS/.BACKUPS/.last_time ]]
	then
		touch ./STATS/GLOBALS/.BACKUPS/.last_time && wait
		echo "7" > ./STATS/GLOBALS/.BACKUPS/.last_time && wait
	fi

if [[ "$AutoDelete" -eq "1" ]]
	then
		if [ -e ./STATS/CLEAN.access.log ] || [ -e ./STATS/IP.crapstats ] || [ -e ./STATS/REQ.crapstats ] || [ -e ./STATS/RES.crapstats ] || [ -e ./STATS/UA.crapstats ] || [ -e ./STATS/LEV.crapstats ] || [ -e ./STATS/ERR.crapstats ] || [ -e ./STATS/.IP.crap ] || [ -e ./STATS/.REQ.crap ] || [ -e ./STATS/.RES.crap ] || [ -e ./STATS/.UA.crap ] || [ -e ./STATS/.LEV.crap ] || [ -e ./STATS/.ERR.crap ]
			then
				if [[ "$LessOutput" -eq "0" ]]
					then
						printf "Removing conflict files automatically ...\n\n"
						sleep 1 && wait
					fi
			fi
		if [ -e ./STATS/CLEAN.access.log ]
			then
				if [[ "$Shred" -eq "1" ]]
					then
						shred -uvz ./STATS/CLEAN.access.log &> /dev/null && wait
					else
						rm ./STATS/CLEAN.access.log &> /dev/null && wait
					fi
			fi
		ls -1 ./STATS/*.crapstats &> /dev/null 2>&1
		if [ "$?" = "0" ]
			then
				if [[ "$Shred" -eq "1" ]]
					then
						shred -uvz ./STATS/*.crapstats &> /dev/null && wait
					else
						rm ./STATS/*.crapstats &> /dev/null && wait
					fi
			fi
		ls -1 ./STATS/.*.crap &> /dev/null 2>&1
		if [ "$?" = "0" ]
			then
				if [[ "$Shred" -eq "1" ]]
					then
						shred -uvz ./STATS/.*.crap &> /dev/null && wait
					else
						rm ./STATS/.*.crap &> /dev/null && wait
					fi
			fi
		ls -1 ./STATS/GLOBALS/.*.crap &> /dev/null 2>&1
		if [ "$?" = "0" ]
			then
				if [[ "$Shred" -eq "1" ]]
					then
						shred -uvz ./STATS/GLOBALS/.*.crap &> /dev/null && wait
					else
						rm ./STATS/GLOBALS/.*.crap &> /dev/null && wait
					fi
			fi
	else
		while [ -e ./STATS/CLEAN.access.log ] || [ -e ./STATS/IP.crapstats ] || [ -e ./STATS/REQ.crapstats ] || [ -e ./STATS/RES.crapstats ] || [ -e ./STATS/UA.crapstats ] || [ -e ./STATS/LEV.crapstats ] || [ -e ./STATS/ERR.crapstats ] || [ -e ./STATS/.IP.crap ] || [ -e ./STATS/.REQ.crap ] || [ -e ./STATS/.RES.crap ] || [ -e ./STATS/.UA.crap ] || [ -e ./STATS/.LEV.crap ] || [ -e ./STATS/.ERR.crap ]
			do
				crapstat=0 && craptemp=0
				printf "!!! $(tput setaf 3)WARNING$(tput sgr0) !!!\n"
				printf "Conflict files detected:\n"
				if [ -e ./STATS/CLEAN.access.log ]
					then
						crapstat=1
						echo "- $(tput setaf 3)./STATS/CLEAN.access.log$(tput sgr0)"
					fi
				if [ -e ./STATS/IP.crapstats ] || [ -e ./STATS/REQ.crapstats ] || [ -e ./STATS/RES.crapstats ] || [ -e ./STATS/UA.crapstats ] || [ -e ./STATS/LEV.crapstats ] || [ -e ./STATS/ERR.crapstats ]
					then
						for stat in ./STATS/*.crapstats
							do
								crapstat=1
								echo "- $(tput setaf 3)$stat$(tput sgr0)"
							done
					fi
				ls -1 ./STATS/.*.crap &> /dev/null 2>&1
				if [ "$?" = "0" ]
					then
						craptemp=1
					fi
				ls -1 ./STATS/GLOBALS/.*.crap &> /dev/null 2>&1
				if [ "$?" = "0" ]
					then
						craptemp=1
					fi
				if [[ "$craptemp" -eq 1 ]]
					then
						echo "- $(tput setaf 242)Craplog's temporary files$(tput sgr0)"
					fi
				if [[ "$LessOutput" -eq "0" ]]
					then
						printf "\nThese files must be removed to have CRAPLOG working as expected\n"
						if [[ "$crapstat" -eq 1 ]]
							then
								printf "Files in $(tput setaf 3)YELLOW$(tput sgr0) are the result of your last invocation of CRAPLOG, aborted before the end\nBecause of that, you should consider to delete them\nPlease check these files and make sure you don't need them before to procede\n"
							fi
					fi
				printf "\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!\nDelete listed files? [Y/n] : "
				read delete
				case "$delete" in
					Y)
						printf "\nRemoving conflict files ..."
						if [ -e ./STATS/CLEAN.access.log ]
							then
								if [[ "$Shred" -eq "1" ]]
									then
										shred -uvz ./STATS/CLEAN.access.log &> /dev/null && wait
									else
										rm ./STATS/CLEAN.access.log &> /dev/null && wait
									fi
							fi
						ls -1 ./STATS/*.crapstats &> /dev/null 2>&1
						if [ "$?" = "0" ]
							then
								if [[ "$Shred" -eq "1" ]]
									then
										shred -uvz ./STATS/*.crapstats &> /dev/null && wait
									else
										rm ./STATS/*.crapstats &> /dev/null && wait
									fi
							fi
						ls -1 ./STATS/.*.crap &> /dev/null 2>&1
						if [ "$?" = "0" ]
							then
								if [[ "$Shred" -eq "1" ]]
									then
										shred -uvz ./STATS/.*.crap &> /dev/null && wait
									else
										rm ./STATS/.*.crap &> /dev/null && wait
									fi
							fi
						ls -1 ./STATS/GLOBALS/.*.crap &> /dev/null 2>&1
						if [ "$?" = "0" ]
							then
								if [[ "$Shred" -eq "1" ]]
									then
										shred -uvz ./STATS/GLOBALS/.*.crap &> /dev/null && wait
									else
										rm ./STATS/GLOBALS/.*.crap &> /dev/null && wait
									fi
							fi
						printf "\nDone\n"
						sleep 1
						printf "\nSTARTING $(tput setaf 1)C$(tput setaf 3)R$(tput setaf 2)A$(tput setaf 6)P$(tput setaf 4)L$(tput setaf 5)O$(tput setaf 7)G$(tput sgr0)\n\n"
						sleep 2 && wait
						;;
					*)
						printf "\nCRAPLOG ABORTED\n\n"
						exit
						;;
				esac
			done;
	fi;

python3 ./crappy/Clean.py "$AccessLogs" "$CleanAccessLogs" "$ErrorLogs"
printf "Done\n\n"
if [[ "$LessOutput" -eq "0" ]]
	then
		if [[ "$CleanAccessLogs" -eq "1" ]]
			then
				printf "New file created:\n- $(tput setaf 10)CLEAN.access.log$(tput sgr0)\n\n"
				sleep 2 && wait
			fi
	else
		sleep 1 && wait
	fi

python3 ./crappy/Stats.py "$AccessLogs" "$ErrorLogs"
printf "Done\n\n"
if [[ "$LessOutput" -eq "0" ]]
	then
		if [[ "$GlobalsOnly" -eq "0" ]]
			then
				printf "New SESSION files created:\n"
				if [[ "$AccessLogs" -eq "1" ]]
					then
						printf "$(tput sgr0)- $(tput setaf 10)IP.crapstats$(tput sgr0)\n- $(tput setaf 10)REQ.crapstats$(tput sgr0)\n- $(tput setaf 10)RES.crapstats$(tput sgr0)\n- $(tput setaf 10)UA.crapstats$(tput sgr0)\n"
					fi
				if [[ "$ErrorLogs" -eq "1" ]]
					then
						printf "$(tput sgr0)- $(tput setaf 10)LEV.crapstats$(tput sgr0)\n- $(tput setaf 10)ERR.crapstats$(tput sgr0)\n"
					fi
				if [[ "$AccessLogs" -eq "1" || "$ErrorLogs" -eq "1" ]]
					then
						printf "\n"
						sleep 2 && wait
					fi
			fi
	else
		sleep 1 && wait
	fi

if [[ "$GlobalsAvoid" -eq "0" ]]
	then
		if [[ "$AccessLogs" -eq "1" ]]
			then
				if [ -e ./STATS/GLOBALS/GLOBAL.IP.crapstats ]
					then
						mv ./STATS/GLOBALS/GLOBAL.IP.crapstats ./STATS/GLOBALS/.GLOBAL.IP.crap && wait
					else
						touch ./STATS/GLOBALS/.GLOBAL.IP.crap && wait
					fi
				if [ -e ./STATS/GLOBALS/GLOBAL.REQ.crapstats ]
					then
						mv ./STATS/GLOBALS/GLOBAL.REQ.crapstats ./STATS/GLOBALS/.GLOBAL.REQ.crap && wait
					else
						touch ./STATS/GLOBALS/.GLOBAL.REQ.crap && wait
					fi
				if [ -e ./STATS/GLOBALS/GLOBAL.RES.crapstats ]
					then
						mv ./STATS/GLOBALS/GLOBAL.RES.crapstats ./STATS/GLOBALS/.GLOBAL.RES.crap && wait
					else
						touch ./STATS/GLOBALS/.GLOBAL.RES.crap && wait
					fi
				if [ -e ./STATS/GLOBALS/GLOBAL.UA.crapstats ]
					then
						mv ./STATS/GLOBALS/GLOBAL.UA.crapstats ./STATS/GLOBALS/.GLOBAL.UA.crap && wait
					else
						touch ./STATS/GLOBALS/.GLOBAL.UA.crap && wait
					fi
			fi

		if [[ "$ErrorLogs" -eq "1" ]]
			then
				if [ -e ./STATS/GLOBALS/GLOBAL.LEV.crapstats ]
					then
						mv ./STATS/GLOBALS/GLOBAL.LEV.crapstats ./STATS/GLOBALS/.GLOBAL.LEV.crap && wait
					else
						touch ./STATS/GLOBALS/.GLOBAL.LEV.crap && wait
					fi
				if [ -e ./STATS/GLOBALS/GLOBAL.ERR.crapstats ]
					then
						mv ./STATS/GLOBALS/GLOBAL.ERR.crapstats ./STATS/GLOBALS/.GLOBAL.ERR.crap && wait
					else
						touch ./STATS/GLOBALS/.GLOBAL.ERR.crap && wait
					fi
			fi

		python3 ./crappy/Glob.py "$AccessLogs" "$ErrorLogs"
		printf "Done\n\n"
		if [[ "$LessOutput" -eq "0" ]]
			then
				printf "GLOBAL statistics updated:\n"
				if [[ "$AccessLogs" -eq "1" ]]
					then
						printf "$(tput sgr0)- $(tput setaf 10)GLOBAL.IP.crapstats$(tput sgr0)\n- $(tput setaf 10)GLOBAL.REQ.crapstats$(tput sgr0)\n- $(tput setaf 10)GLOBAL.RES.crapstats$(tput sgr0)\n- $(tput setaf 10)GLOBAL.UA.crapstats$(tput sgr0)\n"
					fi
				if [[ "$ErrorLogs" -eq "1" ]]
					then
						printf "$(tput sgr0)- $(tput setaf 10)GLOBAL.LEV.crapstats$(tput sgr0)\n- $(tput setaf 10)GLOBAL.ERR.crapstats$(tput sgr0)\n"
					fi
				if [[ "$AccessLogs" -eq "1" || "$ErrorLogs" -eq "1" ]]
					then
						printf "\n"
						sleep 2 && wait
					fi
			else
				sleep 1 && wait
			fi
	fi

if [[ "$GlobalsOnly" -eq "0" ]]
	then
		day=$(date --date="${dataset_date} - 1 day" +%d)
		if [[ $(date +%d) -eq 1 ]]
			then
				month=$(date --date="${dataset_date} - 1 month" +%m)
				if [[ $(date +%m) -eq 1 ]]
					then
						year=$(date --date="${dataset_date} - 1 year" +%Y)
					else
						year=$(date +%Y)
					fi
			else
				month=$(date +%m)
				year=$(date +%Y)
			fi
		dir="./STATS/$year/$month/$day"
		printf "Preparing to move files inside $(tput setaf 14)$dir/$(tput sgr0)\n"
		sleep 2 && wait
		if [[ -e "$dir" ]]
			then
				printf "DIRECTORY ALREADY EXIST!"
				if [[ "$AutoDelete" -eq "1" ]] && [[ "$LessOutput" -eq "0" ]]
					then
						printf "\n\nRemoving conflict files automatically ..."
						sleep 1
					fi
				printf "\n"
				sleep 1 && wait
				if [[ "$CleanAccessLogs" -eq "1" ]]
					then
						if [[ "$AutoDelete" -eq "1" ]]
							then
								printf "\nMoving CLEAN ACCESS LOGs file ..."
								sleep 1 && wait
								if [ -e $dir/CLEAN.access.log ]
									then
										if [[ "$Shred" -eq "1" ]]
											then
												shred -uvz $dir/CLEAN.access.log &> /dev/null && wait
											else
												rm $dir/CLEAN.access.log &> /dev/null && wait
											fi
									fi
							else
								if [ -e $dir/CLEAN.access.log ]
									then
										printf "\nTrying to move CLEAN ACCESS LOGs file ..."
										sleep 1 && wait
										while [ -e $dir/CLEAN.access.log ]
											do
												printf "\n\n!!! $(tput setaf 1)WARNING$(tput sgr0) !!!\n"
												printf "Conflict file detected:\n"
												echo "- $(tput setaf 1)CLEAN.access.log$(tput sgr0)"
												if [[ "$LessOutput" -eq "0" ]]
													then
														printf "\nThis file is the result of your last invocation of CRAPLOG\nIf CRAPLOG succesfully completed the last job, you may need it\nPlease check this file and make sure you don't need it before to procede\n"
													fi
												printf "\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!\nDelete listed files? [Y/n] : "
												read delete
												case "$delete" in
													Y)
														printf "\nRemoving conflict file ..."
														sleep 1 && wait
														if [[ "$Shred" -eq "1" ]]
															then
																shred -uvz $dir/CLEAN.access.log &> /dev/null && wait
															else
																rm $dir/CLEAN.access.log &> /dev/null && wait
															fi
														printf "\nMoving CLEAN ACCESS LOGs file ..."
														sleep 1 && wait
														;;
													*)
														printf "\nCRAPLOG ABORTED\n\n"
														exit
														;;
												esac
											done
									else
										printf "\nMoving CLEAN ACCESS LOGs file ..."
										sleep 1 && wait
									fi
							fi
						mv ./STATS/CLEAN.access.log $dir/ && wait
						printf "\nDone\n"
						sleep 1 && wait
					fi
				if [[ "$AccessLogs" -eq "1" ]]
					then
						if [[ -e $dir/ACCESS ]]
							then
								if [[ "$AutoDelete" -eq "1" ]]
									then
										printf "\nMoving ACCESS LOGs files ..."
										sleep 1 && wait
										ls -1 $dir/ACCESS/*.crapstats &> /dev/null 2>&1
										if [ "$?" = "0" ]
											then
												if [[ "$Shred" -eq "1" ]]
													then
														shred -uvz $dir/ACCESS/*.crapstats &> /dev/null && wait
													else
														rm $dir/ACCESS/*.crapstats &> /dev/null && wait
													fi
											fi
									else
										printf "\nTrying to move ACCESS LOGs files ..."
										sleep 1 && wait
										while [ -e $dir/ACCESS/IP.crapstats ] || [ -e $dir/ACCESS/REQ.crapstats ] || [ -e $dir/ACCESS/RES.crapstats ] || [ -e $dir/ACCESS/UA.crapstats ]
										do
											printf "\n\n!!! $(tput setaf 1)WARNING$(tput sgr0) !!!\n"
											printf "Conflict files detected:\n"
											for stat in $dir/ACCESS/*.crapstats
												do
													echo "- $(tput setaf 1)$stat$(tput sgr0)"
												done
											if [[ "$LessOutput" -eq "0" ]]
												then
													printf "\nThese files are the result of your last invocation of CRAPLOG\nIf CRAPLOG succesfully completed the last job, you may need them\nPlease check these files and make sure you don't need them before to procede\n"
												fi
											printf "\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!\nDelete listed files? [Y/n] : "
											read delete
											case "$delete" in
												Y)
													printf "\nRemoving conflict files ..."
													sleep 1 && wait
													if [[ "$Shred" -eq "1" ]]
														then
															shred -uvz $dir/ACCESS/*.crapstats &> /dev/null && wait
														else
															rm $dir/ACCESS/*.crapstats &> /dev/null && wait
														fi
													printf "\nMoving ACCESS LOGs files ..."
													sleep 1 && wait
													;;
												*)
													printf "\nCRAPLOG ABORTED\n\n"
													exit
													;;
											esac
										done
									fi
							else
								printf "\nMoving ACCESS LOGs files ..."
								sleep 1 && wait
								mkdir $dir/ACCESS
							fi
						mv ./STATS/IP.crapstats $dir/ACCESS/ && wait
						mv ./STATS/REQ.crapstats $dir/ACCESS/ && wait
						mv ./STATS/RES.crapstats $dir/ACCESS/ && wait
						mv ./STATS/UA.crapstats $dir/ACCESS/ && wait
						printf "\nDone\n"
						sleep 1 && wait
					fi
				if [[ "$ErrorLogs" -eq "1" ]]
					then
						if [[ -e $dir/ERROR ]]
							then
								if [[ "$AutoDelete" -eq "1" ]]
									then
										printf "\nMoving ERROR LOGs files ..."
										sleep 1 && wait
										ls -1 $dir/ERROR/*.crapstats &> /dev/null 2>&1
										if [ "$?" = "0" ]
											then
												if [[ "$Shred" -eq "1" ]]
													then
														shred -uvz $dir/ERROR/*.crapstats &> /dev/null && wait
													else
														rm $dir/ERROR/*.crapstats &> /dev/null && wait
													fi
											fi
									else
										printf "\nTrying to move ERROR LOGs files ..."
										sleep 1 && wait
										while [ -e $dir/ERROR/LEV.crapstats ] || [ -e $dir/ERROR/ERR.crapstats ]
											do
												printf "\n\n!!! $(tput setaf 1)WARNING$(tput sgr0) !!!\n"
												printf "Conflict files detected:\n"
												for stat in $dir/ERROR/*.crapstats
													do
														echo "- $(tput setaf 1)$stat$(tput sgr0)"
													done
												if [[ "$LessOutput" -eq "0" ]]
													then
														printf "\nThese files are the result of your last invocation of CRAPLOG\nIf CRAPLOG succesfully completed the last job, you may need them\nPlease check these files and make sure you don't need them before to procede\n"
													fi
												printf "\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!\nDelete listed files? [Y/n] : "
												read delete
												case "$delete" in
													Y)
														printf "\nRemoving conflict files ..."
														sleep 1 && wait
														if [[ "$Shred" -eq "1" ]]
															then
																shred -uvz $dir/ERROR/*.crapstats &> /dev/null && wait
															else
																rm $dir/ERROR/*.crapstats &> /dev/null && wait
															fi
														printf "\nMoving ERROR LOGs files ..."
														sleep 1 && wait
														;;
													*)
														printf "\nCRAPLOG ABORTED\n\n"
														exit
														;;
												esac
											done
									fi
							else
								printf "\nMoving ERROR LOGs files ..."
								mkdir $dir/ERROR && wait
								sleep 1 && wait
							fi
						mv ./STATS/LEV.crapstats $dir/ERROR/ && wait
						mv ./STATS/ERR.crapstats $dir/ERROR/ && wait
						printf "\nDone\n"
						sleep 1 && wait
					fi
				printf "\n"
			else
				printf "Creating directory ..."
				sleep 1 && wait
				if [[ ! -e ./STATS/$year ]]
					then
						mkdir ./STATS/$year && wait
					fi
				if [[ ! -e ./STATS/$year/$month ]]
					then
						mkdir ./STATS/$year/$month && wait
					fi
				mkdir "$dir"
				printf "\nMoving SESSION files ..."
				sleep 1 && wait
				if [[ "$CleanAccessLogs" -eq "1" ]]
					then
						mv ./STATS/CLEAN.access.log $dir/ && wait
					fi
				if [[ "$AccessLogs" -eq "1" ]]
					then
						mkdir "$dir/ACCESS"
						mv ./STATS/IP.crapstats $dir/ACCESS/ && wait
						mv ./STATS/REQ.crapstats $dir/ACCESS/ && wait
						mv ./STATS/RES.crapstats $dir/ACCESS/ && wait
						mv ./STATS/UA.crapstats $dir/ACCESS/ && wait
					fi
				if [[ "$ErrorLogs" -eq "1" ]]
					then
						mkdir "$dir/ERROR"
						mv ./STATS/LEV.crapstats $dir/ERROR/ && wait
						mv ./STATS/ERR.crapstats $dir/ERROR/ && wait
					fi
				printf "\nDone\n\n"
				sleep 1 && wait
			fi;
	fi

if [[ "$Backup" -eq 1 ]]
	then
		if [[ "$AutoDelete" -eq "1" ]]
			then
				printf "Creating BACKUP archive ..."
				sleep 1 && wait
				while [ -e $dir/BACKUP.tar.gz ]
					do
						if [[ "$Shred" -eq "1" ]]
							then
								shred -uvz $dir/BACKUP.tar.gz &> /dev/null && wait
							else
								rm $dir/BACKUP.tar.gz &> /dev/null && wait
							fi
					done
				if [ -e $dir/access.log ]
					then
						if [[ "$Shred" -eq "1" ]]
							then
								shred -uvz $dir/access.log &> /dev/null && wait
							else
								rm $dir/access.log &> /dev/null && wait
							fi
					fi
				if [ -e $dir/error.log ]
					then
						if [[ "$Shred" -eq "1" ]]
							then
								shred -uvz $dir/error.log &> /dev/null && wait
							else
								rm $dir/error.log &> /dev/null && wait
							fi
					fi
			else
				printf "Trying to create BACKUP archive ..."
				sleep 1 && wait
				while [ -e $dir/BACKUP.tar.gz ] || [ -e $dir/access.log ] || [ -e $dir/error.log ]
					do
						printf "\n\n!!! $(tput setaf 1)WARNING$(tput sgr0) !!!\n"
						printf "Conflict files detected:\n"
						if [ -e $dir/BACKUP.tar.gz ]
							then
								echo "- $(tput setaf 1)BACKUP.tar.gz$(tput sgr0)"
							fi
						if [ -e $dir/access.log ]
							then
								echo "- $(tput setaf 3)access.log$(tput sgr0)"
							fi
						if [ -e $dir/error.log ]
							then
								echo "- $(tput setaf 3)error.log$(tput sgr0)"
							fi
						if [[ "$LessOutput" -eq "0" ]]
							then
								if [ -e $dir/access.log ] || [ -e $dir/error.log ]
									then
										printf "\nFiles in $(tput setaf 3)YELLOW$(tput sgr0) are the result of your last invocation of CRAPLOG, aborted before the end\nBecause of that, you should consider to delete them\n"
										printf "Please check these files and make sure you don't need them before to procede\n"
									else
										printf "\nPlease check these files and make sure you don't need them before to procede\n"
									fi
							fi
						printf "\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!\nDelete conflict file? [Y/n] : "
						read delete
						case "$delete" in
							Y)
								printf "\nRemoving conflict files ..."
								sleep 1 && wait
								if [[ "$Shred" -eq "1" ]]
									then
										shred -uvz $dir/BACKUP.tar.gz $dir/access.log $dir/error.log &> /dev/null && wait
									else
										rm $dir/BACKUP.tar.gz $dir/access.log $dir/error.log &> /dev/null && wait
									fi
								printf "\nCreating BACKUP archive ..."
								sleep 1 && wait
								;;
							*)
								printf "\nCRAPLOG ABORTED\n\n"
								exit
								;;
						esac
					done
			fi
		cd "$dir"
		cp /var/log/apache2/access.log.1 access.log && wait
		cp /var/log/apache2/error.log.1 error.log && wait
		tar -czf BACKUP.tar.gz access.log error.log &> /dev/null && wait
		if [[ "$Shred" -eq "1" ]]
			then
				shred -uvz ./access.log ./error.log &> /dev/null && wait
			else
				rm ./access.log ./error.log &> /dev/null && wait
			fi
		cd ../../../.. && wait
		printf "\nDone\n\n"
		sleep 1 && wait
		if [[ "$BackupDelete" -eq 1 ]]
			then
				if [[ "$AutoDelete" -eq "1" ]]
					then
						printf "Removing ORIGINAL files ..."
						sleep 1 && wait
						if [[ "$Shred" -eq "1" ]]
							then
								shred -uvz /var/log/apache2/access.log.1 /var/log/apache2/error.log.1 &> /dev/null && wait
							else
								rm /var/log/apache2/access.log.1 /var/log/apache2/error.log.1 &> /dev/null && wait
							fi
					else
						printf "Preparing to remove ORIGINAL files ..."
						sleep 1 && wait
						if [[ "$LessOutput" -eq "0" ]]
							then
								printf "\nPlease ensure the archive has been created correctly before to proceed\n"
							fi
						printf "EVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!\nDelete ORIGINAL files? [Y/n] : "
						read delete
						case "$delete" in
							Y)
								printf "\nRemoving original files ..."
								sleep 1 && wait
								if [[ "$Shred" -eq "1" ]]
									then
										shred -uvz /var/log/apache2/access.log.1 /var/log/apache2/error.log.1 &> /dev/null && wait
									else
										rm /var/log/apache2/access.log.1 /var/log/apache2/error.log.1 &> /dev/null && wait
									fi
								;;
							*)
								printf "\nCRAPLOG ABORTED\n\n"
								exit
								;;
						esac;
					fi
				
				printf "\nDone\n\n"
				sleep 1 && wait
			fi;
	fi

printf "Removing temporary files ..."
if [[ "$Shred" -eq "1" ]]
	then
		shred -uvz ./STATS/.*.crap ./STATS/GLOBALS/.*.crap &> /dev/null && wait
	else
		rm ./STATS/.*.crap ./STATS/GLOBALS/.*.crap &> /dev/null && wait
	fi
if [[ "$GlobalsOnly" -eq 1 ]]
	then
		if [[ "$Shred" -eq "1" ]]
			then
				shred -uvz ./STATS/*.crapstats &> /dev/null && wait
			else
				rm ./STATS/*.crapstats &> /dev/null && wait
			fi
	fi

LastGlobalsBackup=$(cat ./STATS/GLOBALS/.BACKUPS/.last_time)
if [[ "$LastGlobalsBackup" -lt "7" ]]
	then
		echo "$(($LastGlobalsBackup + 1))" > ./STATS/GLOBALS/.BACKUPS/.last_time && wait
	else
		if [[ "$( ls ./STATS/GLOBALS/.BACKUPS/ | wc -l )" -ge "7" ]]
			then
				mkdir ./STATS/GLOBALS/.BACKUPS/TMP &> /dev/null && wait
				cp ./STATS/GLOBALS/*.crapstats ./STATS/GLOBALS/.BACKUPS/TMP/ &> /dev/null && wait
				rm -r ./STATS/GLOBALS/.BACKUPS/1 &> /dev/null && wait
				mv ./STATS/GLOBALS/.BACKUPS/2 ./STATS/GLOBALS/.BACKUPS/1 &> /dev/null && wait
				mv ./STATS/GLOBALS/.BACKUPS/3 ./STATS/GLOBALS/.BACKUPS/2 &> /dev/null && wait
				mv ./STATS/GLOBALS/.BACKUPS/4 ./STATS/GLOBALS/.BACKUPS/3 &> /dev/null && wait
				mv ./STATS/GLOBALS/.BACKUPS/5 ./STATS/GLOBALS/.BACKUPS/4 &> /dev/null && wait
				mv ./STATS/GLOBALS/.BACKUPS/6 ./STATS/GLOBALS/.BACKUPS/5 &> /dev/null && wait
				mv ./STATS/GLOBALS/.BACKUPS/7 ./STATS/GLOBALS/.BACKUPS/6 &> /dev/null && wait
				mv ./STATS/GLOBALS/.BACKUPS/TMP ./STATS/GLOBALS/.BACKUPS/7 &> /dev/null && wait
			else
				dir=$(( $( ls ./STATS/GLOBALS/.BACKUPS/ | wc -l ) + 1 ))
				mkdir ./STATS/GLOBALS/.BACKUPS/$dir &> /dev/null && wait
				cp ./STATS/GLOBALS/*.crapstats ./STATS/GLOBALS/.BACKUPS/$dir/ &> /dev/null && wait
			fi
		echo "0" > ./STATS/GLOBALS/.BACKUPS/.last_time && wait
	fi

printf "\nDone\n\n\n"
printf "$(tput setaf 3)F$(tput setaf 2)I$(tput setaf 6)N$(tput sgr0)\n\n"
