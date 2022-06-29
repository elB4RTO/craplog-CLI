#!/bin/bash

inst_stuff="craplib craplog crapset crapup crapview installation_stuff/crapconfs installation_stuff/crapstats LICENSE README.md"

printf "\nWelcome to the \033[1m\033[31mC\033[33m R\033[32m A\033[36m P\033[94m L\033[35m O\033[37m G\033[0m installer\n"
sleep 1
wait

# getting the path of Craplog's directory
crapdir=$(dirname "$(realpath $0)")

# default installation path
inst_path=$(dirname "$crapdir")"/Craplog-CLI"

# asking for the installation path
while :
do
    printf "\nThe current \033[1minstallation path\033[0m is: \033[96m$inst_path\033[0m\n"
    printf "Do you want to change it? \033[97m[\033[95my\033[90m/\033[94mn\033[97m] :\033[0m "
    read agree
    case "$agree"
    in
        [yY] | [yY][eE][sS] )
            printf "\nPlease insert the new path\n\033[97m : \033[0m"
            read new_path
            case "$new_path"
            in
                [nN] | [nN][oO] | [cC] | [cC][aA][nN][cC] )
                    new_path=""
                    break
                ;;
                [qQ] | [qQ][uU][iI][tT] | [eE][xX][iI][tT] )
                    printf "\n\033[1m\033[31mInstallation ABORTED\033[0m\n\n"
                    exit
                ;;
            esac
            new_path=$(realpath "$new_path")
            if [[ "$new_path" != "" ]]
            then
                inst_path="$new_path"
            else
                printf "\n\033[93mWarning\033[97m[\033[90mchoice\033[97m]\033[93m>\033[0m the given path is not valid\n"
            fi
        ;;
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


printf "\n\033[1mChecking stuff \033[97m...\033[0m\n"


# checking the existence of the given path
if [ -e "$inst_path" ]
then
    while :
    do
        printf "\n\033[1m\033[33mWarning\033[97m[\033[90mbin\033[97m]\033[33m>\033[0m the installation folder already exists\n"
        printf "\nIf you choose to continue, the actual content will be lost forever\n"
        printf "Erase the directory? \033[97m[\033[92my\033[90m/\033[91mn\033[97m] :\033[0m "
        read agree
        case "$agree"
        in
            [yY] | [yY][eE][sS] )
                break
            ;;
            [nN] | [nN][oO] | [qQ] | [qQ][uU][iI][tT] | [eE][xX][iI][tT] )
                printf "\n\033[1m\033[31mInstallation ABORTED\033[0m\n\n"
                exit
            ;;
            *)
                printf "\n\033[93mWarning\033[97m[\033[90mchoice\033[97m]\033[93m>\033[0m not a valid choice: \033[1m$agree\033[0m\n"
                sleep 1
            ;;
        esac
    done
fi


# checking the existence of another Craplog executable
if [ -e /usr/bin/craplog ]
then
    while :
    do
        printf "\n\033[1m\033[33mWarning\033[97m[\033[90mbin\033[97m]\033[33m>\033[0m file \033[32m/usr/bin/\033[91mcraplog\033[0m already exists\n"
        printf "\nIf you choose to continue, the actual file will be lost forever\n"
        printf "Overwrite the file? \033[97m[\033[92my\033[90m/\033[91mn\033[97m] :\033[0m "
        read agree
        case "$agree"
        in
            [yY] | [yY][eE][sS] )
                printf "\n"
                break
            ;;
            [nN] | [nN][oO] | [qQ] | [qQ][uU][iI][tT] | [eE][xX][iI][tT] )
                printf "\n\033[1m\033[31mInstallation ABORTED\033[0m\n\n"
                exit
            ;;
            *)
                printf "\n\033[93mWarning\033[97m[\033[90mchoice\033[97m]\033[93m>\033[0m not a valid choice: \033[1m$agree\033[0m\n"
                sleep 1
            ;;
        esac
    done
fi


# check that installation stuff is present
proceed=1
for entry in $inst_stuff
do
    if [ ! -e "$crapdir/$entry" ]
    then
        proceed=0
        printf "\033[1m\033[31mError\033[97m[\033[90minst_stuff\033[97m]\033[31m>\033[0m missing file/folder: \033[91m$entry\033[0m\n\n"
    fi
done
if [ ! -e "$crapdir/installation_stuff/craplog" ]
then
    proceed=0
    printf "\n\033[1m\033[31mError\033[97m[\033[90minst_stuff\033[97m]\033[31m>\033[0m missing file/folder: \033[91minstallation_stuff/craplog\n"
fi
if [[ $proceed -eq 0 ]]
then
    exit
fi


# start installing
printf "\033[1mMoving source code \033[97m...\033[0m\n"

# strip the trailing slash if present
if [[ "$inst_path" =~ /$  ]]
then
    inst_path="${inst_path%/}"
fi
# remove the un-needed
test -e "$crapdir/installation_stuff/crapstats/DELETEME"\
&& rm "$crapdir/installation_stuff/crapstats/DELETEME"
wait
# make the installation directory if needed
mkdir -p "$inst_path"
# copy the source to the destination
for src in $inst_stuff
do
    dst="$src"
    if [[ "$dst" =~ ^installation ]]
    then
        dst="$(echo $dst | cut -d/ -f2)/"
    fi
    cp "$crapdir/$src" "$inst_path/$dst"
    wait
done

# copy the executable
printf "\033[1mMaking the executable \033[97m...\033[0m\n"
cp "$crapdir/installation_stuff/craplog" "$crapdir/installation_stuff/craplog.copy"
# append the content in the file for the bins
printf "\
crapexe=\"$inst_path/\$crapexe\"
# start
python3 \"\$crapexe\" \$@
\n" >> "$crapdir/installation_stuff/craplog.copy"
wait
chmod +x "$crapdir/installation_stuff/craplog.copy"
# ask for priviledges
printf "\n\033[1m\033[33mWarning\033[97m[\033[90mbin\033[97m]\033[33m>\033[0m SuperUser priviledges required to copy the executable in the \033[1mbins\033[0m\n"
sudo mv "$crapdir/installation_stuff/craplog.copy" "/usr/bin/craplog"
wait

# done installing
printf "\n\033[32mInstallation complete\033[0m\n"

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

