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
		printf "\n$(tput bold)$(tput setaf 3)Warning$(tput setaf 15)[$(tput setaf 8)bin$(tput setaf 15)]$(tput setaf 15)>$(tput sgr0) file $(tput setaf 2)/usr/bin/$(tput setaf 9)craplog$(tput sgr0) already exists\n"
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
# checking the existence of another Crapview executable
if [ -e /usr/bin/crapview ]
then
	while :
	do
		printf "\n$(tput bold)$(tput setaf 3)Warning$(tput setaf 15)[$(tput setaf 8)bin$(tput setaf 15)]$(tput setaf 15)>$(tput sgr0) file $(tput setaf 2)/usr/bin/$(tput setaf 9)crapview$(tput sgr0) already exists\n"
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
# checking the existence of another Crapup executable
if [ -e /usr/bin/crapup ]
then
	while :
	do
		printf "\n$(tput bold)$(tput setaf 3)Warning$(tput setaf 15)[$(tput setaf 8)bin$(tput setaf 15)]$(tput setaf 15)>$(tput sgr0) file $(tput setaf 2)/usr/bin/$(tput setaf 9)crapup$(tput sgr0) already exists\n"
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
# checking the existence of another Crapset executable
if [ -e /usr/bin/crapset ]
then
	while :
	do
		printf "\n$(tput bold)$(tput setaf 3)Warning$(tput setaf 15)[$(tput setaf 8)bin$(tput setaf 15)]$(tput setaf 15)>$(tput sgr0) file $(tput setaf 2)/usr/bin/$(tput setaf 9)crapset$(tput sgr0) already exists\n"
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

# checking the existence of another Craplog folder in the home
if [ -e "$home/.craplog" ]
then
	if [ -d "$home/.craplog" ]
	then
		while :
		do
			printf "\n$(tput bold)$(tput setaf 3)Warning$(tput setaf 15)[$(tput setaf 8)directory$(tput setaf 15)]$(tput setaf 15)>$(tput sgr0) directory $(tput setaf 2)$home/$(tput setaf 9).craplog$(tput sgr0) already exists\n"
			printf "\nException made for the $(tput bold)crapstats$(tput sgr0), yf you choose to continue the actual content will be lost forever\n"
			printf "Overwrite content? $(tput setaf 15)[$(tput setaf 2)y$(tput setaf 8)/$(tput setaf 1)n$(tput setaf 15)] :$(tput sgr0) "
			read agree
			case "$agree"
			in
				"y" | "Y" | "yes" | "Yes" | "YES" )
					printf "\n"
					cd "$home/.craplog/"
					for entry in *
					do
						if [[ "$entry" != "crapstats" ]]
						then
							if [ -d "$entry" ]
							then
								rm -r "$entry" &> /dev/null && wait
							else
								rm "$entry" &> /dev/null && wait
							fi
						fi
					done
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
	else
		while :
		do
			printf "\n$(tput bold)$(tput setaf 3)Warning$(tput setaf 15)[$(tput setaf 8)conflict$(tput setaf 15)]$(tput setaf 15)>$(tput sgr0) an entry for $(tput setaf 2)$home/$(tput setaf 9).craplog$(tput sgr0) already exists\n"
			printf "\nIf you choose to continue, the actual entry will be lost forever\n"
			printf "Delete entry? $(tput setaf 15)[$(tput setaf 2)y$(tput setaf 8)/$(tput setaf 1)n$(tput setaf 15)] :$(tput sgr0) "
			read agree
			case "$agree"
			in
				"y" | "Y" | "yes" | "Yes" | "YES" )
					printf "\n"
					rm "$home/.craplog" &> /dev/null && wait
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
fi


# start installing
printf "Installing Craplog $(tput setaf 15)...$(tput sgr0)"

