#!/usr/bin/env python
import sys
import httplib, base64 

username = "zenuser" 
password = "zenoss"
http_port=8087
auth = base64.encodestring("%s:%s" % (username, password))

headers = {"Authorization" : "Basic %s" % auth, "Accept": "text/plain"}

deviceName = sys.argv[1]
if deviceName == None:
   deviceName = ''
try:
   hconn = httplib.HTTPConnection(deviceName.lower(), http_port)
   hconn.request('GET','/getStats' + '?isFullMetrics=true', headers=headers)
   r1 = hconn.getresponse()
   if r1.status == 200:
     data1 = r1.read()
   else:
     data1 = ("MQCHECK ERROR| Error from server: %s -- %s" % (r1.status,r1.reason))
   print data1
   hconn.close()
except Exception, ex:
   print "MQCHECK ERROR| General Error accessing MQ server: %s" % str(ex)
