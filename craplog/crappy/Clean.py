#!/usr/bin/python3

import sys
import time

AccessLogs = int(sys.argv[1])
CleanAccessLogs = int(sys.argv[2])


if AccessLogs == 1:

	if CleanAccessLogs == 1:
		print ("Cleaning & Scraping ACCESS LOGs ...")
	else:
		print ("Scraping ACCESS LOGs ...")
	time.sleep(1)

	# MODIFY THE NEXT LINE IF YOUR LOG PATH IS DIFFERENT
	file = open("/var/log/apache2/access.log.1", "r")
	LOGlist = file.read()
	file.close
	LOGlist = LOGlist.split('\n')
	LOGlist_tmp = []

	for log in LOGlist:
		if log.startswith('192.168.') or log.startswith(str('::1')) or log == '':
			continue
		else:
			LOGlist_tmp.append(log)

	LOGlist = LOGlist_tmp
	LOGcheck_tmp = []
	LOGcheck = ""
	
	if CleanAccessLogs == 1:
		file = open("./STATS/CLEAN.access.log", "a")
		for log in LOGlist:
			log_tmp = log.split(' ')
			log_ = log_tmp[0]
			if log_ == LOGcheck:
				file.write("\n%s\n" %( log ))
			else:
				if len(LOGcheck_tmp) == 0:
					file.write("%s\n" %( log ))
					LOGcheck_tmp.append(log)
				else:
					file.write("\n\n%s\n" %( log ))
				LOGcheck = log_
		file.close

	file = open("./STATS/.IP.crap", "a")
	for log in LOGlist:
		log_tmp = log.split(' ')
		log_ = log_tmp[0]
		file.write("%s\n" %( log_ ))
	file.close

	file = open("./STATS/.REQ.crap", "a")
	for log in LOGlist:
		log_tmp = log.split('"')
		log_ = log_tmp[1]
		file.write("%s\n" %( log_ ))
	file.close

	file = open("./STATS/.RES.crap", "a")
	for log in LOGlist:
		log_tmp = log.split('"')
		log_ = log_tmp[2]
		log_ = log_.strip()
		log_ = str(log_[:3])
		file.write("%s\n" %( log_ ))
	file.close

	file = open("./STATS/.UA.crap", "a")
	for log in LOGlist:
		log_tmp = log.split('"')
		log_ = log_tmp[5]
		file.write("%s\n" %( log_ ))
	file.close


################################

ErrorLogs = int(sys.argv[3])

if ErrorLogs == 1:
	print("Scraping ERROR LOGs ...")
	time.sleep(1)
	
	# MODIFY THE NEXT LINE IF YOUR LOG PATH IS DIFFERENT
	file = open("/var/log/apache2/error.log.1", "r")
	ERRLOGlist = file.read()
	file.close
	ERRLOGlist = ERRLOGlist.strip()
	ERRLOGlist = ERRLOGlist.split('\n')
	LEVlist = []
	ERRlist = []

	for log in ERRLOGlist:
		if log != '':
			log = log.split('[')
			LEVlist.append(log[2].strip(' ]'))
			if log[3].startswith('pid') and log[3].endswith('] '):
				ERRlog = log[4]
				ERRlog = ERRlog.split(']')
				ERRlist.append(ERRlog[1].strip())
			else:
				ERRlog = log[3]
				ERRlog = ERRlog.split(']')
				ERRlist.append(ERRlog[1].strip())

	file = open("./STATS/.LEV.crap", "a")
	for log in LEVlist:
		file.write("%s\n" %( log ))
	file.close

	file = open("./STATS/.ERR.crap", "a")
	for log in ERRlist:
		file.write("%s\n" %( log ))
	file.close
