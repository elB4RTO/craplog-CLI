#!usr/bin/python3

import os
import os.path
import sys
import time
import collections
from collections import Counter

AccessLogs = int(sys.argv[1])

if AccessLogs == 1:

    print("Creating statistics from ACCESS LOGs ...")
    time.sleep(1)

    # IPs
    file = open("./STATS/.IP.crap", "r")
    IPlist = file.read()
    file.close

    CheckList = []
    IPlist = IPlist.split()
    count = collections.Counter(IPlist)
    IPlist = (sorted(IPlist, key=lambda x: (count[x], x), reverse=True))

    file = open("./STATS/IP.crapstats", "a")
    for ip in IPlist:
        if ip in CheckList or ip == "::1":
            continue
        else:
            CheckList.append(ip)
            file.write("{ " + str(IPlist.count(ip)) + " }   >>>   " + ip + "\n-\n")
    file.close


    # REQUESTS
    file = open("./STATS/.REQ.crap", "r")
    REQlist = file.read()
    file.close

    CheckList = []
    REQlist = REQlist.split("\n")
    count = collections.Counter(REQlist)
    REQlist = (sorted(REQlist, key=lambda x: (count[x], x), reverse=True))

    file = open("./STATS/REQ.crapstats", "a")
    for req in REQlist:
        if req in CheckList:
            continue
        else:
            CheckList.append(req)
            if req.startswith('OPTIONS'):
                req_t = req.split(" ")
                rq_t = ""
                for rq in req_t:
                    if rq.startswith('OPTIONS'):
                        rq_t += rq + " * "
                    elif rq.startswith('HTTP/'):
                        rq_t += rq
                file.write("{ " + str(REQlist.count(req)) + " }   >>>   " + rq_t + "\n-\n")
            else:
                file.write("{ " + str(REQlist.count(req)) + " }   >>>   " + req + "\n-\n")
    file.close


    # RESPONSES
    file = open("./STATS/.RES.crap", "r")
    RESlist = file.read()
    file.close

    CheckList = []
    RESlist_tmp = []
    RESlist = RESlist.split("\n")
    RESlist = (sorted(RESlist, key=lambda x: (count[x], x), reverse=True))

    for res in RESlist:
        res = res.strip()
        res = str(res[:3])
        RESlist_tmp.append(res)

    count = collections.Counter(RESlist_tmp)
    RESlist = sorted(RESlist_tmp, key=count.get, reverse=True)
    res = ""

    file = open("./STATS/RES.crapstats", "a")
    for res in RESlist:
        if res in CheckList:
            continue
        else:
            CheckList.append(res)
            file.write("{ " + str(RESlist.count(res)) + " }   >>>   " + res + "\n-\n")
    file.close


    # USER AGENTS
    file = open("./STATS/.UA.crap", "r")
    UAlist = file.read()
    file.close

    CheckList = []
    UAlist = UAlist.split("\n")

    count = collections.Counter(UAlist)
    UAlist = (sorted(UAlist, key=lambda x: (count[x], x), reverse=True))

    file = open("./STATS/UA.crapstats", "a")
    for ua in UAlist:
        if ua in CheckList:
            continue
        else:
            CheckList.append(ua)
            file.write("{ " + str(UAlist.count(ua)) + " }   >>>   " + ua + "\n-\n")
    file.close


#################################################

# ERRORs
ErrorLogs = int(sys.argv[2])

if ErrorLogs == 1:
    print("Creating statistics from ERROR LOGS ...\n(This can take a while, depending on your LOG LEVEL configuration)")
    time.sleep(1)

    # LEVs
    file = open("./STATS/.LEV.crap", "r")
    LEVlist = file.read()
    file.close

    CheckList = []
    LEVlist = LEVlist.split('\n')
    count = collections.Counter(LEVlist)
    LEVlist = (sorted(LEVlist, key=lambda x: (count[x], x), reverse=True))

    file = open("./STATS/LEV.crapstats", "a")
    for lev in LEVlist:
        if lev in CheckList or lev == "::1":
            continue
        else:
            CheckList.append(lev)
            file.write("{ " + str(LEVlist.count(lev)) + " }   >>>   " + lev + "\n-\n")
    file.close

    # ERRs
    file = open("./STATS/.ERR.crap", "r")
    ERRlist = file.read()
    file.close

    CheckList = []
    ERRlist = ERRlist.split('\n')

    count = collections.Counter(ERRlist)
    ERRlist = (sorted(ERRlist, key=lambda x: (count[x], x), reverse=True))

    file = open("./STATS/ERR.crapstats", "a")
    for err in ERRlist:
        if err in CheckList or err == "::1":
            continue
        else:
            CheckList.append(err)
            file.write("{ " + str(ERRlist.count(err)) + " }   >>>   " + err + "\n-\n")
    file.close
