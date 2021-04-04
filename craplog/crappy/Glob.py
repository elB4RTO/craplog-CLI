#!/usr/bin/python3

import os
import os.path
import sys
import time
import collections
from collections import Counter

AccessLogs = int(sys.argv[1])

if AccessLogs == 1:

    print("Updating GLOBAL statistics of ACCESS LOGs ...")
    time.sleep(1)

    # ACTUAL IPs
    file = open("./STATS/IP.crapstats", "r")
    IPlist_tmp = file.read()
    file.close
    IPlist_tmp = IPlist_tmp.strip()
    IPlist_tmp = IPlist_tmp.split("\n")
    IPlist = []
    IPcount = []

    for items in IPlist_tmp:
        items = items.strip()
        if len(items) > 2:
            items_tmp = items.split('>>>')
            count = items_tmp[0]
            count = count.strip('{ }')
            IPcount.append(count)
            item = items_tmp[1]
            item = item.strip('{ }')
            IPlist.append(item)


    # GLOBAL IPs
    file = open("./STATS/GLOBALS/.GLOBAL.IP.crap", "r")
    G_IPlist_tmp = file.read()
    file.close
    G_IPlist_tmp = G_IPlist_tmp.strip()
    G_IPlist_tmp = G_IPlist_tmp.split("\n")
    G_IPlist = []
    G_IPcount = []

    if len(G_IPlist_tmp) > 2:
        F_IPlist = {}
        F_IPcount = {}
        for items in G_IPlist_tmp:
            if len(items) > 2:
                items_tmp = items.split('>>>')
                count = items_tmp[0]
                count = count.strip('{ }')
                G_IPcount.append(count)
                item = items_tmp[1]
                item = item.strip('{ }')
                G_IPlist.append(item)

        for item in G_IPlist:
            i = G_IPlist.index(item)
            item_Gc = G_IPcount[i]
            if item in IPlist:
                count = IPlist.index(item)
                item_i = IPlist[count]
                item_c = IPcount[count]
                item_Fc = int(item_Gc) + int(item_c)
                F_IPcount[item] = item_Fc
                F_IPlist[item] = item
            else:
                F_IPcount[item] = item_Gc
                F_IPlist[item] = item
        F_IParr = ({key: value for key, value in sorted(F_IPcount.items(), key=lambda item: item[1], reverse=True)})
        file = open("./STATS/GLOBALS/GLOBAL.IP.crapstats", "a")
        for items in F_IParr.keys():
            count = F_IPcount[items]
            item = F_IPlist[items]
            file.write("{ " + str(count) + " }   >>>   " + str(item) + "\n-\n")
        file.close

    else:
        F_IPlist = []
        F_IPcount = []
        for item in IPlist:
            if item in F_IPlist:
                continue
            else:
                count = IPlist.index(item)
                F_IPlist.append(IPlist[count])
                F_IPcount.append(IPcount[count])
        file = open("./STATS/GLOBALS/GLOBAL.IP.crapstats", "a")
        for item in F_IPlist:
            count = F_IPlist.index(item)
            file.write("{ " + str(F_IPcount[count]) + " }   >>>   " + str(F_IPlist[count]) + "\n-\n")
        file.close



    # ACTUAL REQs
    file = open("./STATS/REQ.crapstats", "r")
    REQlist_tmp = file.read()
    file.close
    REQlist_tmp = REQlist_tmp.strip()
    REQlist_tmp = REQlist_tmp.split("\n")
    REQlist = []
    REQcount = []

    for items in REQlist_tmp:
        items = items.strip()
        if len(items) > 2:
            items_tmp = items.split('>>>')
            count = items_tmp[0]
            count = count.strip('{ }')
            REQcount.append(count)
            item = items_tmp[1]
            item = item.strip('{ }')
            REQlist.append(item)


    # GLOBAL REQs
    file = open("./STATS/GLOBALS/.GLOBAL.REQ.crap", "r")
    G_REQlist_tmp = file.read()
    file.close
    G_REQlist_tmp = G_REQlist_tmp.strip()
    G_REQlist_tmp = G_REQlist_tmp.split("\n")
    G_REQlist = []
    G_REQcount = []

    if len(G_REQlist_tmp) > 2:
        F_REQlist = {}
        F_REQcount = {}
        for items in G_REQlist_tmp:
            if len(items) > 2:
                items_tmp = items.split('>>>')
                count = items_tmp[0]
                count = count.strip('{ }')
                G_REQcount.append(count)
                item = items_tmp[1]
                item = item.strip('{ }')
                G_REQlist.append(item)

        for item in G_REQlist:
            i = G_REQlist.index(item)
            item_Gc = G_REQcount[i]
            if item in REQlist:
                count = REQlist.index(item)
                item_i = REQlist[count]
                item_c = REQcount[count]
                item_Fc = int(item_Gc) + int(item_c)
                F_REQcount[item] = item_Fc
                F_REQlist[item] = item
            else:
                F_REQcount[item] = item_Gc
                F_REQlist[item] = item
        F_REQarr = ({key: value for key, value in sorted(F_REQcount.items(), key=lambda item: item[1], reverse=True)})
        file = open("./STATS/GLOBALS/GLOBAL.REQ.crapstats", "a")
        for items in F_REQarr.keys():
            count = F_REQcount[items]
            item = F_REQlist[items]
            file.write("{ " + str(count) + " }   >>>   " + str(item) + "\n-\n")
        file.close

    else:
        F_REQlist = []
        F_REQcount = []
        for item in REQlist:
            if item in F_REQlist:
                continue
            else:
                count = REQlist.index(item)
                F_REQlist.append(REQlist[count])
                F_REQcount.append(REQcount[count])
        file = open("./STATS/GLOBALS/GLOBAL.REQ.crapstats", "a")
        for item in F_REQlist:
            count = F_REQlist.index(item)
            file.write("{ " + str(F_REQcount[count]) + " }   >>>   " + str(F_REQlist[count]) + "\n-\n")
        file.close



    # ACTUAL RESs
    file = open("./STATS/RES.crapstats", "r")
    RESlist_tmp = file.read()
    file.close
    RESlist_tmp = RESlist_tmp.strip()
    RESlist_tmp = RESlist_tmp.split("\n")
    RESlist = []
    REScount = []

    for items in RESlist_tmp:
        items = items.strip()
        if len(items) > 2:
            items_tmp = items.split('>>>')
            count = items_tmp[0]
            count = count.strip('{ }')
            REScount.append(count)
            item = items_tmp[1]
            item = item.strip('{ }')
            RESlist.append(item)


    # GLOBAL RESs
    file = open("./STATS/GLOBALS/.GLOBAL.RES.crap", "r")
    G_RESlist_tmp = file.read()
    file.close
    G_RESlist_tmp = G_RESlist_tmp.strip()
    G_RESlist_tmp = G_RESlist_tmp.split("\n")
    G_RESlist = []
    G_REScount = []

    if len(G_RESlist_tmp) > 2:
        F_RESlist = {}
        F_REScount = {}
        for items in G_RESlist_tmp:
            if len(items) > 2:
                items_tmp = items.split('>>>')
                count = items_tmp[0]
                count = count.strip('{ }')
                G_REScount.append(count)
                item = items_tmp[1]
                item = item.strip('{ }')
                G_RESlist.append(item)

        for item in G_RESlist:
            i = G_RESlist.index(item)
            item_Gc = G_REScount[i]
            if item in RESlist:
                count = RESlist.index(item)
                item_i = RESlist[count]
                item_c = REScount[count]
                item_Fc = int(item_Gc) + int(item_c)
                F_REScount[item] = item_Fc
                F_RESlist[item] = item
            else:
                F_REScount[item] = item_Gc
                F_RESlist[item] = item
        F_RESarr = ({key: value for key, value in sorted(F_REScount.items(), key=lambda item: item[1], reverse=True)})
        file = open("./STATS/GLOBALS/GLOBAL.RES.crapstats", "a")
        for items in F_RESarr.keys():
            count = F_REScount[items]
            item = F_RESlist[items]
            file.write("{ " + str(count) + " }   >>>   " + str(item) + "\n-\n")
        file.close

    else:
        F_RESlist = []
        F_REScount = []
        for item in RESlist:
            if item in F_RESlist:
                continue
            else:
                count = RESlist.index(item)
                F_RESlist.append(RESlist[count])
                F_REScount.append(REScount[count])
        file = open("./STATS/GLOBALS/GLOBAL.RES.crapstats", "a")
        for item in F_RESlist:
            count = F_RESlist.index(item)
            file.write("{ " + str(F_REScount[count]) + " }   >>>   " + str(F_RESlist[count]) + "\n-\n")
        file.close



    # ACTUAL UAs
    file = open("./STATS/UA.crapstats", "r")
    UAlist_tmp = file.read()
    file.close
    UAlist_tmp = UAlist_tmp.strip()
    UAlist_tmp = UAlist_tmp.split("\n")
    UAlist = []
    UAcount = []

    for items in UAlist_tmp:
        items = items.strip()
        if len(items) > 2:
            items_tmp = items.split('>>>')
            count = items_tmp[0]
            count = count.strip('{ }')
            UAcount.append(count)
            item = items_tmp[1]
            item = item.strip('{ }')
            UAlist.append(item)


    # GLOBAL UAs
    file = open("./STATS/GLOBALS/.GLOBAL.UA.crap", "r")
    G_UAlist_tmp = file.read()
    file.close
    G_UAlist_tmp = G_UAlist_tmp.strip()
    G_UAlist_tmp = G_UAlist_tmp.split("\n")
    G_UAlist = []
    G_UAcount = []

    if len(G_UAlist_tmp) > 2:
        F_UAlist = {}
        F_UAcount = {}
        for items in G_UAlist_tmp:
            if len(items) > 2:
                items_tmp = items.split('>>>')
                count = items_tmp[0]
                count = count.strip('{ }')
                G_UAcount.append(count)
                item = items_tmp[1]
                item = item.strip('{ }')
                G_UAlist.append(item)

        for item in G_UAlist:
            i = G_UAlist.index(item)
            item_Gc = G_UAcount[i]
            if item in UAlist:
                count = UAlist.index(item)
                item_i = UAlist[count]
                item_c = UAcount[count]
                item_Fc = int(item_Gc) + int(item_c)
                F_UAcount[item] = item_Fc
                F_UAlist[item] = item
            else:
                F_UAcount[item] = item_Gc
                F_UAlist[item] = item
        F_UAarr = ({key: value for key, value in sorted(F_UAcount.items(), key=lambda item: item[1], reverse=True)})
        file = open("./STATS/GLOBALS/GLOBAL.UA.crapstats", "a")
        for items in F_UAarr.keys():
            count = F_UAcount[items]
            item = F_UAlist[items]
            file.write("{ " + str(count) + " }   >>>   " + str(item) + "\n-\n")
        file.close

    else:
        F_UAlist = []
        F_UAcount = []
        for item in UAlist:
            if item in F_UAlist:
                continue
            else:
                count = UAlist.index(item)
                F_UAlist.append(UAlist[count])
                F_UAcount.append(UAcount[count])
        file = open("./STATS/GLOBALS/GLOBAL.UA.crapstats", "a")
        for item in F_UAlist:
            count = F_UAlist.index(item)
            file.write("{ " + str(F_UAcount[count]) + " }   >>>   " + str(F_UAlist[count]) + "\n-\n")
        file.close


#################################################

# ERRORs
ErrorLogs = int(sys.argv[2])

if ErrorLogs == 1:

    print("Updating GLOBAL statistics of ERROR LOGs ...")
    time.sleep(1)

    # ACTUAL LEVs
    file = open("./STATS/LEV.crapstats", "r")
    LEVlist_tmp = file.read()
    file.close
    LEVlist_tmp = LEVlist_tmp.strip()
    LEVlist_tmp = LEVlist_tmp.split("\n")
    LEVlist = []
    LEVcount = []

    for items in LEVlist_tmp:
        items = items.strip()
        if len(items) > 2:
            items_tmp = items.split('>>>')
            count = items_tmp[0]
            count = count.strip('{ }')
            LEVcount.append(count)
            item = items_tmp[1]
            item = item.strip('{ }')
            LEVlist.append(item)


    # GLOBAL LEVs
    file = open("./STATS/GLOBALS/.GLOBAL.LEV.crap", "r")
    G_LEVlist_tmp = file.read()
    file.close
    G_LEVlist_tmp = G_LEVlist_tmp.strip()
    G_LEVlist_tmp = G_LEVlist_tmp.split("\n")
    G_LEVlist = []
    G_LEVcount = []

    if len(G_LEVlist_tmp) > 2:
        F_LEVlist = {}
        F_LEVcount = {}
        for items in G_LEVlist_tmp:
            if len(items) > 2:
                items_tmp = items.split('>>>')
                count = items_tmp[0]
                count = count.strip('{ }')
                G_LEVcount.append(count)
                item = items_tmp[1]
                item = item.strip('{ }')
                G_LEVlist.append(item)

        for item in G_LEVlist:
            i = G_LEVlist.index(item)
            item_Gc = G_LEVcount[i]
            if item in LEVlist:
                count = LEVlist.index(item)
                item_i = LEVlist[count]
                item_c = LEVcount[count]
                item_Fc = int(item_Gc) + int(item_c)
                F_LEVcount[item] = item_Fc
                F_LEVlist[item] = item
            else:
                F_LEVcount[item] = item_Gc
                F_LEVlist[item] = item
        F_LEVarr = ({key: value for key, value in sorted(F_LEVcount.items(), key=lambda item: item[1], reverse=True)})
        file = open("./STATS/GLOBALS/GLOBAL.LEV.crapstats", "a")
        for items in F_LEVarr.keys():
            count = F_LEVcount[items]
            item = F_LEVlist[items]
            file.write("{ " + str(count) + " }   >>>   " + str(item) + "\n-\n")
        file.close

    else:
        F_LEVlist = []
        F_LEVcount = []
        for item in LEVlist:
            if item in F_LEVlist:
                continue
            else:
                count = LEVlist.index(item)
                F_LEVlist.append(LEVlist[count])
                F_LEVcount.append(LEVcount[count])
        file = open("./STATS/GLOBALS/GLOBAL.LEV.crapstats", "a")
        for item in F_LEVlist:
            count = F_LEVlist.index(item)
            file.write("{ " + str(F_LEVcount[count]) + " }   >>>   " + str(F_LEVlist[count]) + "\n-\n")
        file.close


    # ACTUAL ERRs
    file = open("./STATS/ERR.crapstats", "r")
    ERRlist_tmp = file.read()
    file.close
    ERRlist_tmp = ERRlist_tmp.strip()
    ERRlist_tmp = ERRlist_tmp.split("\n")
    ERRlist = []
    ERRcount = []

    for items in ERRlist_tmp:
        items = items.strip()
        if len(items) > 2:
            items_tmp = items.split('>>>')
            count = items_tmp[0]
            count = count.strip('{ }')
            ERRcount.append(count)
            item = items_tmp[1]
            item = item.strip('{ }')
            ERRlist.append(item)


    # GLOBAL ERRs
    file = open("./STATS/GLOBALS/.GLOBAL.ERR.crap", "r")
    G_ERRlist_tmp = file.read()
    file.close
    G_ERRlist_tmp = G_ERRlist_tmp.strip()
    G_ERRlist_tmp = G_ERRlist_tmp.split("\n")
    G_ERRlist = []
    G_ERRcount = []

    if len(G_ERRlist_tmp) > 2:
        F_ERRlist = {}
        F_ERRcount = {}
        for items in G_ERRlist_tmp:
            if len(items) > 2:
                items_tmp = items.split('>>>')
                count = items_tmp[0]
                count = count.strip('{ }')
                G_ERRcount.append(count)
                item = items_tmp[1]
                item = item.strip('{ }')
                G_ERRlist.append(item)

        for item in G_ERRlist:
            i = G_ERRlist.index(item)
            item_Gc = G_ERRcount[i]
            if item in ERRlist:
                count = ERRlist.index(item)
                item_i = ERRlist[count]
                item_c = ERRcount[count]
                item_Fc = int(item_Gc) + int(item_c)
                F_ERRcount[item] = item_Fc
                F_ERRlist[item] = item
            else:
                F_ERRcount[item] = item_Gc
                F_ERRlist[item] = item
        F_ERRarr = ({key: value for key, value in sorted(F_ERRcount.items(), key=lambda item: item[1], reverse=True)})
        file = open("./STATS/GLOBALS/GLOBAL.ERR.crapstats", "a")
        for items in F_ERRarr.keys():
            count = F_ERRcount[items]
            item = F_ERRlist[items]
            file.write("{ " + str(count) + " }   >>>   " + str(item) + "\n-\n")
        file.close

    else:
        F_ERRlist = []
        F_ERRcount = []
        for item in ERRlist:
            if item in F_ERRlist:
                continue
            else:
                count = ERRlist.index(item)
                F_ERRlist.append(ERRlist[count])
                F_ERRcount.append(ERRcount[count])
        file = open("./STATS/GLOBALS/GLOBAL.ERR.crapstats", "a")
        for item in F_ERRlist:
            count = F_ERRlist.index(item)
            file.write("{ " + str(F_ERRcount[count]) + " }   >>>   " + str(F_ERRlist[count]) + "\n-\n")
        file.close