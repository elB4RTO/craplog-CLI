#!/bin/bash

printf "\nWelcome to the $(tput setaf 1)C$(tput setaf 3)R$(tput setaf 2)A$(tput setaf 6)P$(tput setaf 7)L$(tput setaf 7)O$(tput setaf 7)G$(tput sgr0) installer\n"
sleep 1 && wait

# actual path
initial_path=$(pwd)

# getting the path of Craplog's directory
crapdir="$(dirname $(realpath $0))"

# getting the home
home=~

# checking the existence of another Craplog executable
if [ -e /usr/bin/craplog ]
then
	while :
	do
		printf "\n$(tput bold)$(tput setaf 3)Warning$(tput setaf 15)[$(tput setaf 8)bin$(tput setaf 15)]$(tput setaf 3)>$(tput sgr0) file $(tput setaf 2)/usr/bin/$(tput setaf 9)craplog$(tput sgr0) already exists\n"
		printf "\nIf you choose to continue, the actual file will be lost forever\n"
		printf "Overwrite file? $(tput setaf 15)[$(tput setaf 2)y$(tput setaf 8)/$(tput setaf 1)n$(tput setaf 15)] :$(tput sgr0) "
		read agree
		case "$agree"
		in
			"y" | "Y" | "yes" | "Yes" | "YES" )
				printf "\n"
				break
			;;
			"n" | "N" | "no" | "No" | "NO" )
				printf "\n$(tput bold)$(tput setaf 1)Installation ABORTED$(tput sgr0)\n\n"
				exit
			;;
			*)
				printf "\n$(tput bold)$(tput setaf 3)Warning$(tput setaf 15)[$(tput setaf 8)choice$(tput setaf 15)]$(tput setaf 15)>$(tput sgr0) not a valid choice: $(tput bold)%s$(tput sgr0)\n"
				sleep 1
			;;
		esac
	done
fi


# start installing
printf "Installing Craplog $(tput setaf 15)...$(tput sgr0) "


