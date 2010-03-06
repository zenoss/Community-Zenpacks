#!/usr/bin/env python
###########################################################################
#
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import os
import socket
import sys
import time
import xml.dom.minidom

# Get our options
try:
	ghost = socket.gethostbyname(sys.argv[1])
	gport = int(sys.argv[2])
	devip = sys.argv[3]
	cache = int(sys.argv[4])
except:
	sys.stderr.write("Usage: %s <ganglia_host> <ganglia_port> <cluster_host>\n" % os.path.basename(sys.argv[0]))
	sys.exit(1)

# Setup some global stuff
TEMPDIR = "/tmp"
TEMPDIR = os.path.join(TEMPDIR, "gangliadata")
CACHEFILE = os.path.join(TEMPDIR, "%s:%d.cache" % (ghost, gport))

# Make sure we have the tempdir
if not os.path.isdir(TEMPDIR):
  os.mkdir(TEMPDIR)

# If we have no cache or the cache is stale, repopulate
curtime = time.time()
if not os.path.exists(CACHEFILE) or curtime - os.path.getmtime(CACHEFILE) > cache:
	tmpfile = CACHEFILE + ".%d" % os.getpid()

	# Connect to socket and save data to tempfile
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((ghost, gport))
		xmldata = ""
		while True:
			chunk = s.recv(1024)
			if not chunk: break
			xmldata += chunk
		s.close()
	except:
		s.close()
		print "Unable to connect to ganglia server!"
		sys.exit(1)

	try:
		dom = xml.dom.minidom.parseString(xmldata)
	except:
		print "Ganglia server returned malformed XML!"
		sys.exit(1)

	# Save our cache
	f = open(tmpfile, "w")
	for cluster in dom.getElementsByTagName("GANGLIA_XML")[0].getElementsByTagName("CLUSTER"):
		data = {}
		for host in cluster.getElementsByTagName("HOST"):
			data = {}
			for metric in host.getElementsByTagName("METRIC"):
				data[metric.getAttribute("NAME")] = metric.getAttribute("VAL")
			data["lastUpdate"] =  str(int(curtime) - int(host.getAttribute("REPORTED")))
			f.write("%s\t%s\n" % (host.getAttribute("IP"), " ".join(["%s=%s" % (k, v) for k,v in data.items()])))
	f.close()

	# Try to rename the data into place
	for i in range(10): # Handle up to 10 errors, then fail
		if os.path.exists(CACHEFILE):
			try:
				os.remove(CACHEFILE)
			except OSError:
				pass
		try:
			os.rename(tmpfile, CACHEFILE)
			break
		except OSError:
			pass
	if os.path.exists(tmpfile):
		os.remove(tmpfile)

# Check to make sure we have cache and it is updated
if not os.path.exists(CACHEFILE):
	print "Unable to find ganglia cache!"
	sys.exit(1)
if curtime - os.path.getmtime(CACHEFILE) > cache:
	print "Unable to update stale ganglia cache!"
	sys.exit(1)

# OK, now we actually try to read the data from the cache
for line in open(CACHEFILE):
	if line.startswith(devip + "\t"):
		print "OK|" + line.split("\t", 1)[1]
		break
