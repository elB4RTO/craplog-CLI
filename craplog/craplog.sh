#! /bin/bash

CleanAccessLogs=0; AccessLogs=1; ErrorLogs=0; GlobalsOnly=0; GlobalsAvoid=0; AutoDelete=0; Shred=0
for arg in "$@"; do
    case $arg in
        "-h" | "--help" | "-help" | "help")
            printf "\n"
            cat ./.elbarto.txt ./README.txt
            printf "\n"
            exit
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
    esac
done

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
if [[ $AccessLogs -eq 1 ]]
    then
        if [[ ! -e /var/log/apache2/access.log.1 ]]
            then
                printf "\n$(tput setaf 3)Error$(tput sgr0): there is no $(tput setaf 1)access.log.1$(tput sgr0) file inside $(tput setaf 6)/var/log/apache2/$(tput sgr0)\n\n"
                exit
            fi
    fi
if [[ $ErrorLogs -eq 1 ]]
    then
        if [[ ! -e /var/log/apache2/error.log.1 ]]
            then
                printf "\n$(tput setaf 3)Error$(tput sgr0): there is no $(tput setaf 1)error.log.1$(tput sgr0) file inside $(tput setaf 6)/var/log/apache2/$(tput sgr0)\n\n"
                exit
            fi
    fi
if [[ $AccessLogs -eq 0 && $CleanAccessLogs -eq 1 ]]
    then
        printf "\n$(tput setaf 3)Error$(tput sgr0): not possible to make a clean access log file [$(tput setaf 6)-c$(tput sgr0)] without working on a access.log file [$(tput setaf 6)--only-errors$(tput sgr0)]\n\n"
        exit
    fi
if [[ $GlobalsOnly -eq 1 && $GlobalsAvoid -eq 1 ]]
    then
        printf "\n$(tput setaf 3)Error$(tput sgr0): you can't use $(tput setaf 6)--only-globals$(tput sgr0) toghether with $(tput setaf 6)--avoid-globals$(tput sgr0)\n\n"
        exit
    fi

printf "\nWELCOME TO CRAPLOG\nUse $(tput setaf 6)craplog.sh --help$(tput sgr0) to print a help screen\n\n"
sleep 2 && wait
if [[ ! -e ./STATS ]]
    then
        mkdir ./STATS &> /dev/null && wait
        mkdir ./STATS/GLOBALS &> /dev/null && wait
    fi

if [[ $AutoDelete -eq 1 ]]
    then
        if [ -e ./STATS/CLEAN.access.log ]
            then
                if [[ $Shred -eq 1 ]]
                    then
                        shred -zuvn 6 ./STATS/CLEAN.access.log &> /dev/null && wait
                    else
                        rm ./STATS/CLEAN.access.log &> /dev/null && wait
                    fi
            fi
        ls -1 ./STATS/*.crapstats &> /dev/null 2>&1
        if [ "$?" = "0" ]
            then
                if [[ $Shred -eq 1 ]]
                    then
                        shred -zuvn 6 ./STATS/*.crapstats &> /dev/null && wait
                    else
                        rm ./STATS/*.crapstats &> /dev/null && wait
                    fi
            fi
        ls -1 ./STATS/.*.crap &> /dev/null 2>&1
        if [ "$?" = "0" ]
            then
                if [[ $Shred -eq 1 ]]
                    then
                        shred -zuvn 6 ./STATS/.*.crap &> /dev/null && wait
                    else
                        rm ./STATS/.*.crap &> /dev/null && wait
                    fi
            fi
        ls -1 ./STATS/GLOBALS/.*.crap &> /dev/null 2>&1
        if [ "$?" = "0" ]
            then
                if [[ $Shred -eq 1 ]]
                    then
                        shred -zuvn 6 ./STATS/GLOBALS/.*.crap &> /dev/null && wait
                    else
                        rm ./STATS/GLOBALS/.*.crap &> /dev/null && wait
                    fi
            fi
    else
        while [ -e ./STATS/CLEAN.access.log ] || [ -e ./STATS/IP.crapstats ] || [ -e ./STATS/REQ.crapstats ] || [ -e ./STATS/RES.crapstats ] || [ -e ./STATS/UA.crapstats ] || [ -e ./STATS/LEV.crapstats ] || [ -e ./STATS/ERR.crapstats ] || [ -e ./STATS/.IP.crap ] || [ -e ./STATS/.REQ.crap ] || [ -e ./STATS/.RES.crap ] || [ -e ./STATS/.UA.crap ] || [ -e ./STATS/.LEV.crap ] || [ -e ./STATS/.ERR.crap ]
            do
                crapstat=0 && craptemp=0
                printf "\n!!! $(tput setaf 3)WARNING$(tput sgr0) !!!\n\n"
                printf "Conflict files detected:\n"
                if [ -e ./STATS/CLEAN.access.log ]
                    then
                        crapstat=1
                        echo "- $(tput setaf 3)./STATS/CLEAN.access.log$(tput sgr0)"
                    fi
                for stat in ./STATS/*.crapstats
                    do
                        crapstat=1
                        echo "- $(tput setaf 3)$stat$(tput sgr0)"
                    done
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
                if [[ $craptemp -eq 1 ]]
                    then
                        echo "- $(tput setaf 7)Craplog's temporary files$(tput sgr0)"
                    fi
                printf "\nThese files must be removed in order to have CRAPLOG working as expected\n\n"
                if [[ $crapstat -eq 1 ]]
                    then
                        printf "Files in $(tput setaf 3)YELLOW$(tput sgr0) are the result of your last invocation of CRAPLOG, interrupted before the end of the script\nBecause of that, you should consider to delete them\nPlease check these files and make sure you don't need them before to procede\n"
                    fi
                printf "\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!\nDelete listed files? [Y/n] : "
                read delete
                case $delete in
                    Y)
                        printf "\nRemoving conflict files ..."
                        if [ -e ./STATS/CLEAN.access.log ]
                            then
                                if [[ $Shred -eq 1 ]]
                                    then
                                        shred -zuvn 6 ./STATS/CLEAN.access.log &> /dev/null && wait
                                    else
                                        rm ./STATS/CLEAN.access.log &> /dev/null && wait
                                    fi
                            fi
                        ls -1 ./STATS/*.crapstats &> /dev/null 2>&1
                        if [ "$?" = "0" ]
                            then
                                if [[ $Shred -eq 1 ]]
                                    then
                                        shred -zuvn 6 ./STATS/*.crapstats &> /dev/null && wait
                                    else
                                        rm ./STATS/*.crapstats &> /dev/null && wait
                                    fi
                            fi
                        ls -1 ./STATS/.*.crap &> /dev/null 2>&1
                        if [ "$?" = "0" ]
                            then
                                if [[ $Shred -eq 1 ]]
                                    then
                                        shred -zuvn 6 ./STATS/.*.crap &> /dev/null && wait
                                    else
                                        rm ./STATS/.*.crap &> /dev/null && wait
                                    fi
                            fi
                        ls -1 ./STATS/GLOBALS/.*.crap &> /dev/null 2>&1
                        if [ "$?" = "0" ]
                            then
                                if [[ $Shred -eq 1 ]]
                                    then
                                        shred -zuvn 6 ./STATS/GLOBALS/.*.crap &> /dev/null && wait
                                    else
                                        rm ./STATS/GLOBALS/.*.crap &> /dev/null && wait
                                    fi
                            fi
                        printf "\nDone\nAll conflict files has been removed\n"
                        sleep 1
                        printf "\n\nSTARTING $(tput setaf 1)C$(tput setaf 3)R$(tput setaf 2)A$(tput setaf 6)P$(tput setaf 4)L$(tput setaf 5)O$(tput setaf 7)G$(tput sgr0)\n\n"
                        sleep 2 && wait
                        ;;
                    *)
                        printf "\nCRAPLOG ABORTED\n\n"
                        exit
                        ;;
                esac
            done
    fi

./crappy/Clean.py $AccessLogs $CleanAccessLogs $ErrorLogs
printf "Done\n\n"
if [[ $CleanAccessLogs -eq 1 ]]
    then
        printf "New file created:\n- $(tput setaf 1)CLEAN.access.log$(tput sgr0)\n\n"
    fi
sleep 2 && wait

./crappy/Stats.py $AccessLogs $ErrorLogs
printf "Done\n\n"

if [[ $GlobalsAvoid -eq 0 ]]
    then
        if [[ $AccessLogs -eq 1 ]]
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

        if [[ $ErrorLogs -eq 1 ]]
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

        ./crappy/Glob.py $AccessLogs $ErrorLogs
        printf "Done\n\n"
        printf "GLOBAL statistics updated:\n"
        if [[ $AccessLogs -eq 1 ]]
            then
                printf "$(tput sgr0)- $(tput setaf 1)GLOBAL.IP.crapstats$(tput sgr0)\n- $(tput setaf 1)GLOBAL.REQ.crapstats$(tput sgr0)\n- $(tput setaf 1)GLOBAL.RES.crapstats$(tput sgr0)\n- $(tput setaf 1)GLOBAL.UA.crapstats$(tput sgr0)\n"
            fi
        if [[ $ErrorLogs -eq 1 ]]
            then
                printf "$(tput sgr0)- $(tput setaf 1)GLOBAL.LEV.crapstats$(tput sgr0)\n- $(tput setaf 1)GLOBAL.ERR.crapstats$(tput sgr0)\n"
            fi
        if [[ $AccessLogs -eq 1 || $ErrorLogs -eq 1 ]]
            then
                printf "\n" && sleep 3 && wait
            else
                sleep 1 && wait
            fi
    fi

if [[ $GlobalsOnly -eq 0 ]]
    then
        printf "New files created:\n"
        if [[ $AccessLogs -eq 1 ]]
            then
                printf "$(tput sgr0)- $(tput setaf 1)IP.crapstats$(tput sgr0)\n- $(tput setaf 1)REQ.crapstats$(tput sgr0)\n- $(tput setaf 1)RES.crapstats$(tput sgr0)\n- $(tput setaf 1)UA.crapstats$(tput sgr0)\n"
            fi
        if [[ $ErrorLogs -eq 1 ]]
            then
                printf "$(tput sgr0)- $(tput setaf 1)LEV.crapstats$(tput sgr0)\n- $(tput setaf 1)ERR.crapstats$(tput sgr0)\n"
            fi
        if [[ $AccessLogs -eq 1 || $ErrorLogs -eq 1 ]]
            then
                printf "\n" && sleep 3 && wait
            else
                sleep 1 && wait
            fi

        day=$(date --date="${dataset_date} - 1 day" +%d)
        if [[ $(date +%d) -eq 1 ]]
            then
                if [[ $(date +%m) -eq 1 ]]
                    then
                        month=$(date --date="${dataset_date} - 1 month" +%m)
                        year=$(date --date="${dataset_date} - 1 year" +%Y)
                    else
                        month=$(date --date="${dataset_date} - 1 month" +%m)
                        year=$(date +%Y)
                    fi
            else
                month=$(date +%m)
                year=$(date +%Y)
            fi
        dir="./STATS/$year/$month/$day"
        printf "\nPreparing to move files inside $(tput setaf 6)$dir/$(tput sgr0)\n\n"
        sleep 2 && wait
        if [[ -e $dir ]]
            then
                printf "DIRECTORY ALREADY EXIST!\n"
                if [[ $AutoDelete -eq 1 ]]
                    then
                        printf "$(tput setaf 3)Auto-Delete$(tput sgr0) is $(tput bold)ON$(tput sgr0). Removing conflict files automatically...\n"
                        sleep 2 && wait
                    else
                        printf "Checking for conflict files...\n"
                        sleep 1 && wait
                    fi
                if [[ $CleanAccessLogs -eq 1 ]]
                    then
                        printf "\nTrying to move CLEAN ACCESS LOGs file to $(tput setaf 6)$dir/$(tput sgr0)\n"
                        sleep 2 && wait
                        if [[ $AutoDelete -eq 1 ]]
                            then
                                if [ -e $dir/CLEAN.access.log ]
                                    then
                                        if [[ $Shred -eq 1 ]]
                                            then
                                                shred -zuvn 6 $dir/CLEAN.access.log &> /dev/null && wait
                                            else
                                                rm $dir/CLEAN.access.log &> /dev/null && wait
                                            fi
                                    fi
                            else
                                while [ -e $dir/CLEAN.access.log ]
                                    do
                                        printf "\n!!! $(tput setaf 1)WARNING$(tput sgr0) !!!\n\n"
                                        printf "Conflict file detected:\n"
                                        echo "- $(tput setaf 1)CLEAN.access.log$(tput sgr0)"
                                        printf "\nThis file is the result of your last invocation of CRAPLOG\nIf CRAPLOG succesfully completed the last job, you may need it\nPlease check this file and make sure you don't need it before to procede\n"
                                        printf "\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!\nDelete listed files? [Y/n] : "
                                        read delete
                                        case $delete in
                                            Y)
                                                printf "\nRemoving conflict file ..."
                                                if [[ $Shred -eq 1 ]]
                                                    then
                                                        shred -zuvn 6 $dir/CLEAN.access.log &> /dev/null && wait
                                                    else
                                                        rm $dir/CLEAN.access.log &> /dev/null && wait
                                                    fi
                                                printf "\nDone\nConflict file has been removed\n\n"
                                                sleep 1 && wait
                                                printf "Moving CLEAN ACCESS LOGs file\n"
                                                sleep 1 && wait
                                                ;;
                                            *)
                                                printf "\nCRAPLOG ABORTED\n\n"
                                                exit
                                                ;;
                                        esac
                                    done
                            fi
                        mv ./STATS/CLEAN.access.log $dir/ && wait
                        printf "Done\nFile has been moved\n\n\n"
                        sleep 1 && wait
                    fi
                if [[ $AccessLogs -eq 1 ]]
                    then
                        printf "Trying to move ACCESS LOGs files to $(tput setaf 6)$dir/ACCESS/$(tput sgr0)\n"
                        sleep 2 && wait
                        if [[ -e $dir/ACCESS ]]
                            then
                                if [[ $AutoDelete -eq 1 ]]
                                    then
                                        ls -1 $dir/ACCESS/*.crapstats &> /dev/null 2>&1
                                        if [ "$?" = "0" ]
                                            then
                                                if [[ $Shred -eq 1 ]]
                                                    then
                                                        shred -zuvn 6 $dir/ACCESS/*.crapstats &> /dev/null && wait
                                                    else
                                                        rm $dir/ACCESS/*.crapstats &> /dev/null && wait
                                                    fi
                                            fi
                                    else
                                        while [ -e $dir/ACCESS/IP.crapstats ] || [ -e $dir/ACCESS/REQ.crapstats ] || [ -e $dir/ACCESS/RES.crapstats ] || [ -e $dir/ACCESS/UA.crapstats ]
                                        do
                                            crapstat=0
                                            printf "\n!!! $(tput setaf 1)WARNING$(tput sgr0) !!!\n\n"
                                            printf "Conflict files detected:\n"
                                            for stat in $dir/ACCESS/*.crapstats
                                                do
                                                    echo "- $(tput setaf 1)$stat$(tput sgr0)"
                                                done
                                            printf "\nThese files are the result of your last invocation of CRAPLOG\nIf CRAPLOG succesfully completed the last job, you may need them\nPlease check these files and make sure you don't need them before to procede\n"
                                            printf "\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!\nDelete listed files? [Y/n] : "
                                            read delete
                                            case $delete in
                                                Y)
                                                    printf "\nRemoving conflict files ..."
                                                    if [[ $Shred -eq 1 ]]
                                                        then
                                                            shred -zuvn 6 $dir/ACCESS/*.crapstats &> /dev/null && wait
                                                        else
                                                            rm $dir/ACCESS/*.crapstats &> /dev/null && wait
                                                        fi
                                                    printf "\nDone\nAll conflict files have been removed\n\n"
                                                    sleep 1 && wait
                                                    printf "Moving ACCESS LOGs files\n"
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
                                mkdir $dir/ACCESS
                            fi
                        mv ./STATS/IP.crapstats $dir/ACCESS/ && wait
                        mv ./STATS/REQ.crapstats $dir/ACCESS/ && wait
                        mv ./STATS/RES.crapstats $dir/ACCESS/ && wait
                        mv ./STATS/UA.crapstats $dir/ACCESS/ && wait
                        printf "Done\nAll files have been moved\n\n\n"
                        sleep 1 && wait
                    fi
                if [[ $ErrorLogs -eq 1 ]]
                    then
                        printf "Trying to move ERROR LOGs files to $(tput setaf 6)$dir/ERROR$(tput sgr0)\n"
                        sleep 2 && wait
                        if [[ -e $dir/ERROR ]]
                            then
                                if [[ $AutoDelete -eq 1 ]]
                                    then
                                        ls -1 $dir/ERROR/*.crapstats &> /dev/null 2>&1
                                        if [ "$?" = "0" ]
                                            then
                                                if [[ $Shred -eq 1 ]]
                                                    then
                                                        shred -zuvn 6 $dir/ERROR/*.crapstats &> /dev/null && wait
                                                    else
                                                        rm $dir/ERROR/*.crapstats &> /dev/null && wait
                                                    fi
                                            fi
                                    else
                                        while [ -e $dir/ERROR/LEV.crapstats ] || [ -e $dir/ERROR/ERR.crapstats ]
                                            do
                                                printf "\n!!! $(tput setaf 1)WARNING$(tput sgr0) !!!\n\n"
                                                printf "Conflict files detected:\n"
                                                for stat in $dir/ERROR/*.crapstats
                                                    do
                                                        crapstat=1
                                                        echo "- $(tput setaf 1)$stat$(tput sgr0)"
                                                    done
                                                printf "\nThese files are the result of your last invocation of CRAPLOG\nIf CRAPLOG succesfully completed the last job, you may need them\nPlease check these files and make sure you don't need them before to procede\n"
                                                printf "\nEVERY DELETED FILE WILL BE LOST FOREVER AND NOT RECOVERABLE!\nDelete listed files? [Y/n] : "
                                                read delete
                                                case $delete in
                                                    Y)
                                                        printf "\nRemoving conflict files ..."
                                                        if [[ $Shred -eq 1 ]]
                                                            then
                                                                shred -zuvn 6 $dir/ERROR/*.crapstats &> /dev/null && wait
                                                            else
                                                                rm $dir/ERROR/*.crapstats &> /dev/null && wait
                                                            fi
                                                        printf "\nDone\nAll conflict files have been removed\n\n"
                                                        sleep 1 && wait
                                                        printf "Moving ERROR LOGs files\n"
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
                                mkdir $dir/ERROR && wait
                            fi
                        mv ./STATS/LEV.crapstats $dir/ERROR/ && wait
                        mv ./STATS/ERR.crapstats $dir/ERROR/ && wait
                        printf "Done\nAll files have been moved\n\n\n"
                        sleep 1 && wait
                    fi
                printf "\n"
            else
                printf "Creating directory\n"
                sleep 1 && wait
                if [[ ! -e ./STATS/$year ]]
                    then
                        mkdir ./STATS/$year && wait
                    fi
                if [[ ! -e ./STATS/$year/$month ]]
                    then
                        mkdir ./STATS/$year/$month && wait
                    fi
                mkdir $dir
                printf "Done\n\n"
                printf "Moving previously created files to $(tput setaf 6)$dir/$(tput sgr0)\n"
                if [[ $CleanAccessLogs -eq 1 ]]
                    then
                        mv ./STATS/CLEAN.access.log $dir/ && wait
                    fi
                if [[ $AccessLogs -eq 1 ]]
                    then
                        mkdir $dir/ACCESS
                        mv ./STATS/IP.crapstats $dir/ACCESS/ && wait
                        mv ./STATS/REQ.crapstats $dir/ACCESS/ && wait
                        mv ./STATS/RES.crapstats $dir/ACCESS/ && wait
                        mv ./STATS/UA.crapstats $dir/ACCESS/ && wait
                    fi
                if [[ $ErrorLogs -eq 1 ]]
                    then
                        mkdir $dir/ERROR
                        mv ./STATS/LEV.crapstats $dir/ERROR/ && wait
                        mv ./STATS/ERR.crapstats $dir/ERROR/ && wait
                    fi
                printf "\nDone\nAll files have been moved\n\n"
                sleep 2 && wait
            fi
    fi

printf "Removing temporary files ...\n\n\n"
if [[ $Shred -eq 1 ]]
    then
        shred -zuvn 6 ./STATS/.*.crap ./STATS/GLOBALS/.*.crap &> /dev/null && wait
    else
        ./STATS/.*.crap ./STATS/GLOBALS/.*.crap &> /dev/null && wait
    fi
if [[ $GlobalsOnly -eq 1 ]]
    then
        if [[ $Shred -eq 1 ]]
            then
                shred -zuvn 6 ./STATS/*.crapstats &> /dev/null && wait
            else
                rm ./STATS/*.crapstats &> /dev/null && wait
            fi
    fi
printf "$(tput setaf 3)F$(tput setaf 2)I$(tput setaf 6)N$(tput sgr0)\n\n"