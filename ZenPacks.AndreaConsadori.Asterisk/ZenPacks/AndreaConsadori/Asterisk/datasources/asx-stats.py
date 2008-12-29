#!/usr/bin/env python

# Copyright 2007 ITConnection.ru (Digium Distribution, Asterisk services,
# Russia and the C.I.S.)

# support@itconnection.ru

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# usage ./asx-stats [server [key]]
#   excuting script without any option lists all available keys
#   server - number of server
#   key - display value based on this key

import sys, os, re, socket
from Properties import Properties, IllegalArgumentException

# full path to the configuration file
configfile = "/opt/zenoss/ZenPacks/ZenPacks.AndreaConsadori.Asterisk/ZenPacks/AndreaConsadori/Asterisk/datasources/asx-stats.conf"

# list of IAX2 peers
iaxpeersfile = "/opt/zenoss/ZenPacks/ZenPacks.AndreaConsadori.Asterisk/ZenPacks/AndreaConsadori/Asterisk/datasources/iaxpeers"

# verbose mode (0 - off, 1 - on)
verbose = 0

iaxpeers = []

host = []
port = []
username = []
password = []

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

stats = {}
stats["sip.peers.total"] = 0
stats["sip.peers.online"] = 0
stats["iax.peers.total"] = 0
stats["iax.peers.online"] = 0
stats["sip.users.total"] = 0
stats["iax.users.total"] = 0
stats["sip.channels"] = 0
stats["iax.channels"] = 0
stats["pstn.channels"] = 0
stats["zap.channels"] = 0
stats["agents.loggedin.yes"] = 0
stats["agents.loggedin.no"] = 0
stats["voicemail.all"] = 0
stats["core.threads"] = 0
stats["core.uptime"] = 0

# params:
#   query - query to send
#   response - awaiting response
def query(query, response = ""):
    if verbose:
	print query
    sock.send(query)
    mesg = ""
    s = readline()
    while s != response:
	if verbose:
	    print s
	mesg = mesg + s + "\n"
	s = readline()
    return mesg

def readline():
    mesg = ""
    c = sock.recv(1)
    while c != "\n":
	mesg = mesg + c
	c = sock.recv(1)
    return mesg.strip("\r")

def login(host, port, username, password):
    sock.connect((host, port))
    return query("action: login\r\nusername: " + username + "\r\nsecret: " + password + "\r\nevents: off\r\n\r\n")

def logout():
    mesg = query("action: logoff\r\n")
    sock.close()
    return mesg

try:

    p = Properties()
    p.load(file(configfile))
    i = 0
    s = p.getProperty("hosts." + str(i) + ".hostname")
    while s != "":
	host.append(p.getProperty("hosts." + str(i) + ".hostname"))
	port.append(eval(p.getProperty("hosts." + str(i) + ".port")))
	username.append(p.getProperty("hosts." + str(i) + ".username"))
	password.append(p.getProperty("hosts." + str(i) + ".password"))
        i = i + 1
	s = p.getProperty("hosts." + str(i) + ".hostname")

    if len(sys.argv) > 1:
	hi = eval(sys.argv[1])
    else:
	hi = 0

    mesg = login(host[hi], port[hi], username[hi], password[hi])

    if len(sys.argv) < 3:
	print mesg
	
    f = open(iaxpeersfile)
    s = f.readline()
    while s != "":
	iaxpeers.append(s.strip("\r\n"))
	stats["iax.peers." + s.strip("\r\n") + ".status"] = 0
	s = f.readline()
    f.close()

    for p in iaxpeers:
        s = query("action: command\r\ncommand: iax2 show peer " + p + "\r\n\r\n", "--END COMMAND--").split("\n")
	for i in s:
	    if re.compile("Status").search(i) and len(i.split()) == 5:
		stats["iax.peers." + p + ".status"] = eval(i.split()[3][1:])

    s = query("action: command\r\ncommand: sip show peers\r\n\r\n", "--END COMMAND--").split("\n")
    for i in s:
	if re.compile(r"sip peers \[").search(i):
	    stats["sip.peers.total"] = eval(i.split()[0])
	    if len(i.split()) > 8:
		stats["sip.peers.online"] = eval(i.split()[4])
	    else:
		stats["sip.peers.online"] = eval(i.split()[3][1:])

    s = query("action: command\r\ncommand: iax2 show peers\r\n\r\n", "--END COMMAND--").split("\n")
    for i in s:
	if re.compile(r"iax2 peers \[").search(i):
	    stats["iax.peers.total"] = eval(i.split()[0])
	    stats["iax.peers.online"] = eval(i.split()[3][1:])

    s = query("action: command\r\ncommand: sip show users\r\n\r\n", "--END COMMAND--").split("\n")
    x = 0
    for i in s:
	x = x + 1
	if re.compile("-- Remote UNIX connection").search(i):
	    x = x - 1
	if re.compile("Verbosity is").search(i):
	    x = x - 1
	if re.compile("Def.Context").search(i):
	    x = x - 1
	if re.compile("Response:").search(i):
	    x = x - 1
	if re.compile("Privilege:").search(i):
	    x = x - 1
	if i == "":
	    x = x - 1
    stats["sip.users.total"] = x

    s = query("action: command\r\ncommand: iax2 show users\r\n\r\n", "--END COMMAND--").split("\n")
    x = 0
    for i in s:
	x = x + 1
	if re.compile("-- Remote UNIX connection").search(i):
	    x = x - 1
	if re.compile("Verbosity is").search(i):
	    x = x - 1
	if re.compile("Def.Context").search(i):
	    x = x - 1	
	if re.compile("Response:").search(i):
	    x = x - 1
	if re.compile("Privilege:").search(i):
	    x = x - 1
	if i == "":
	    x = x - 1
    stats["iax.users.total"] = x

    s = query("action: command\r\ncommand: sip show channels\r\n\r\n", "--END COMMAND--").split("\n")
    for i in s:
	if re.compile("active SIP channels").search(i):
	    stats["sip.channels"] = eval(i.split()[0])

    s = query("action: command\r\ncommand: iax2 show channels\r\n\r\n", "--END COMMAND--").split("\n")
    for i in s:
	if re.compile("active IAX channel").search(i):
	    stats["iax.channels"] = eval(i.split()[0])

    s = query("action: command\r\ncommand: group show channels\r\n\r\n", "--END COMMAND--").split("\n")
    for i in s:
	if re.compile("active channels").search(i):
	    stats["pstn.channels"] = eval(i.split()[0])

    s = query("action: command\r\ncommand: zap show channels\r\n\r\n", "--END COMMAND--").split("\n")
    x = 0
    for i in s:
	x = x + 1
	if re.compile("-- Remote UNIX connection").search(i):
	    x = x - 1
	if re.compile("Verbosity is").search(i):
	    x = x - 1
	if re.compile("No such command").search(i):
	    x = x - 1
	if re.compile("Chan Extension").search(i):
	    x = x - 1
	if re.compile("pseudo").search(i):
	    x = x - 1
	if re.compile("Response:").search(i):
	    x = x - 1
	if re.compile("Privilege:").search(i):
	    x = x - 1
	if i == "":
	    x = x - 1
    stats["zap.channels"] = x

    #print query("action: command\r\ncommand: transcoder show\r\n\r\n", "--END COMMAND--")
    #print query("action: command\r\ncommand: queue show\r\n\r\n", "--END COMMAND--")
    #print query("action: command\r\ncommand: group show channels\r\n\r\n", "--END COMMAND--")

    s = query("action: command\r\ncommand: agent show\r\n\r\n", "--END COMMAND--").split("\n")
    for i in s:
	if re.compile("available at").search(i):
	    stats["agents.loggedin.yes"] = stats["agents.loggedin.yes"] + 1
	if re.compile("not logged in").search(i):
	    stats["agents.loggedin.no"] = stats["agents.loggedin.no"] + 1

    s = query("action: command\r\ncommand: voicemail show users\r\n\r\n", "--END COMMAND--").split("\n")
    for i in s:
	if re.compile("default").search(i):
	    stats["voicemail.all"] = stats["voicemail.all"] + eval(i.split()[len(i.split()) - 1])

    s = query("action: command\r\ncommand: core show threads\r\n\r\n", "--END COMMAND--").split("\n")
    for i in s:
	if re.compile("threads listed").search(i):
	    stats["core.threads"] = eval(i.split()[0])

    s = query("action: command\r\ncommand: core show uptime seconds\r\n\r\n", "--END COMMAND--").split("\n")
    for i in s:
	if re.compile("System").search(i):
	    stats["core.uptime"] = eval(i.split()[2])

    logout()

    if len(sys.argv) > 2:
	if sys.argv[2] == "sip.peers.total":
	    print stats["sip.peers.total"]
        elif sys.argv[2] == "sip.peers.online":
	    print stats["sip.peers.online"]
	elif sys.argv[2] == "iax.peers.total":
	    print stats["iax.peers.total"]
        elif sys.argv[2] == "iax.peers.online":
	    print stats["iax.peers.online"]
        elif sys.argv[2] == "sip.users.total":
	    print stats["sip.users.total"]
        elif sys.argv[2] == "iax.users.total":
	    print stats["iax.users.total"]
        elif sys.argv[2] == "sip.channels":
	    print stats["sip.channels"]
	elif sys.argv[2] == "iax.channels":
    	    print stats["iax.channels"]
	elif sys.argv[2] == "pstn.channels":
    	    print stats["pstn.channels"]
	elif sys.argv[2] == "zap.channels":
    	    print stats["zap.channels"]
	elif sys.argv[2] =="agents.loggedin.yes":
	    print stats["agents.loggedin.yes"]
	elif sys.argv[2] =="agents.loggedin.no":
	    print stats["agents.loggedin.no"]
	elif sys.argv[2] =="voicemail.all":
	    print stats["voicemail.all"]
	elif sys.argv[2] == "core.threads":
    	    print stats["core.threads"]
	elif sys.argv[2] == "core.uptime":
    	    print stats["core.uptime"]
	else:
	    for p in iaxpeers:
		if sys.argv[2] == "iax.peers." + p + ".status":
		    print stats["iax.peers." + p + ".status"]
    else:
	print "sip.peers.total:" + str(stats["sip.peers.total"])
        print "sip.peers.online:" + str(stats["sip.peers.online"])
	print "iax.peers.total:" + str(stats["iax.peers.total"])
	print "iax.peers.online:" + str(stats["iax.peers.online"])
        print "sip.users.total:" + str(stats["sip.users.total"])
        print "iax.users.total:" + str(stats["iax.users.total"])
        print "sip.channels:" + str(stats["sip.channels"])
	print "iax.channels:" + str(stats["iax.channels"])
        print "pstn.channels:" + str(stats["pstn.channels"])
	print "zap.channels:" + str(stats["zap.channels"])
	print "agents.loggedin.yes:" + str(stats["agents.loggedin.yes"])
	print "agents.loggedin.no:" + str(stats["agents.loggedin.no"])
	print "voicemail.all:" + str(stats["voicemail.all"])
	print "core.threads:" + str(stats["core.threads"])
	print "core.uptime:" + str(stats["core.uptime"])
	for p in iaxpeers:
	    print "iax.peers." + p + ".status:" + str(stats["iax.peers." + p + ".status"])

except Exception, e:
    print e
    sys.exit()
