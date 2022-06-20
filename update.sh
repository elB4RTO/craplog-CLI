#!/bin/bash

inst_stuff="craplib craplog crapset crapup crapview installation_stuff/crapconfs installation_stuff/crapstats LICENSE README.md"

printf "\nWelcome to the \033[1m\033[31mC\033[33mR\033[32mA\033[36mP\033[94mL\033[35mO\033[37mG\033[0m updater\n"
sleep 1
wait

# getting the path of Craplog's directory
crapdir="$(dirname $(realpath $0))"

# default installation path
inst_path=""

# asking for the installation path
while :
do
    printf "\nPlease insert the path in which you installed Craplog\n\033[97m : \033[0m"
    read new_path
    case "$new_path"
    in
        [nN] | [nN][oO] | [cC] | [cC][aA][nN][cC] | [qQ] | [qQ][uU][iI][tT] | [eE][xX][iI][tT] )
            printf "\n\033[1m\033[31mInstallation ABORTED\033[0m\n\n"
            exit
        ;;
        "")
            continue
        ;;
    esac
    new_path=$(realpath "$new_path")
    if [[ "$new_path" != "" ]]
    then
        if [ -d "$new_path" ]
        then
            inst_path="$new_path"
            if [ ! -e "$inst_path/craplog" ] && [ ! -e "$inst_path/craplog.py" ] && [ ! -e "$inst_path/crappy" ]
            then
                while :
                do
                    proceed=0
                    printf "\n\033[93mWarning\033[97m[\033[90mchoice\033[97m]\033[93m>\033[0m the given path doesn't seems to be a Craplog installation folder\n"
                    printf "Are you sure you want to use this path? \033[97m[\033[31my\033[90m/\033[32mn\033[97m] :\033[0m "
                    read agree
                    case "$agree"
                    in
                        [yY] | [yY][eE][sS] )
                            proceed=1
                        ;&
                        [nN] | [nN][oO] )
                            break
                        ;;
                        [qQ] | [qQ][uU][iI][tT] | [eE][xX][iI][tT] )
                            printf "\n\033[1m\033[31mInstallation ABORTED\033[0m\n\n"
                            exit
                        ;;
                        *)
                            printf "\n\033[93mWarning\033[97m[\033[90mchoice\033[97m]\033[93m>\033[0m not a valid choice: \033[1m%$agree\033[0m\n"
                            sleep 1
                        ;;
                    esac
                done
            fi
            if [[ $proceed -eq 0 ]]
            then
                continue
            else
                break
            fi
        else
            printf "\n\033[93mWarning\033[97m[\033[90mchoice\033[97m]\033[93m>\033[0m the given path is not valid\n"
        fi
    else
        printf "\n\033[93mWarning\033[97m[\033[90mchoice\033[97m]\033[93m>\033[0m the given path is not valid\n"
    fi
done


printf "Checking stuff \033[97m...\033[0m\n"


# check that update stuff is present
proceed=1
for entry in $inst_stuff
do
    if [ ! -e "$crapdir/$entry" ]
    then
        proceed=0
        printf "\n\033[1m\033[31mError\033[97m[\033[90minst_stuff\033[97m]\033[31m>\033[0m missing file/folder: \033[91m$entry\033[0m\n"
    fi
done
test $proceed -eq 1 | exit


# start updating
printf "Replacing source code \033[97m...\033[0m\n"

# strip the trailing slash if present
inst_path="${inst_path%/}"
# copy the source to the destination
test -e "$inst_path/craplog.py" && rm "$inst_path/craplog.py"
test -e "$inst_path/crappy" && rm -r "$inst_path/crappy"
for entry in $inst_stuff
do
    test -e "$inst_path/$entry" && rm -r "$inst_path/$entry"
    mv "$crapdir/$entry" "$inst_path/$entry"
done

# done installing
printf "\n\033[32mUpdate completed\033[0m\n"

# remove the download folder
while :
do
    printf "Do you want to remove the source folder? \033[97m[\033[92my\033[90m/\033[91mn\033[97m] :\033[0m "
    read agree
    case "$agree"
    in
        [yY] | [yY][eE][sS] )
            rm -r "$crapdir"
        ;&
        [nN] | [nN][oO] | [qQ] | [qQ][uU][iI][tT] | [eE][xX][iI][tT] )
            break
        ;;
        *)
            printf "\n\033[93mWarning\033[97m[\033[90mchoice\033[97m]\033[93m>\033[0m not a valid choice: \033[1m$agree\033[0m\n"
            sleep 1
        ;;
    esac
done

printf "\n\033[1m\033[33m F\033[32m I\033[36m N\033[0m\n"

