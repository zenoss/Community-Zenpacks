#! /usr/bin/env python
import commands
import sys
import getopt
import re
import BaseHTTPServer, cgi
from base64 import b64decode
import socket
import logging
import logging.config


class MQHTTPServer(BaseHTTPServer.HTTPServer):
    def __init__(self, addr, handler):
       self.stop = False
       BaseHTTPServer.HTTPServer.__init__(self, addr, handler)


    def run_forever(self):
        """Handle one request at a time until doomsday."""
        while not self.stop:
            try:
                self.handle_request()
            except (IOError, socket.error), ex:
                if 'Bad file descriptor' in str(ex):
                    logger.error( "Skipping bad file error" )
                    pass
                else:
                    logger.error( str(ex) )
                    raise

    def handle_error(self, request, client_address):
        """Handle an error gracefully.  Overridden from SocketServer."""

        logger.exception("handle_error caught error")


class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    config_props = dict()
    parent = None

    def do_GET(self):
        authorization = self.headers.get('authorization')
	if (authorization == None):
	    self.send_response(401)
	    self.send_header('WWW-Authenticate', 'Basic realm="MQ Monitor"')
	    self.end_headers()
	    logger.error( "Missing auth header" )
	    self.wfile.write('Authentication failure')
	    return
	else:
	    (kind, data) = authorization.split(' ')
	    if (kind == 'Basic'):
	       b64data = b64decode(data)
	       namepass = b64data.split(":")
	       username = namepass[0]
	       password = namepass[1]
	       #(username, _, password) = b64data.partition(':')
               if (username != config_props["web.username"] or password != config_props["web.password"]):
	          self.send_response(403)
	          self.send_header('WWW-Authenticate', 'Basic realm="MQ Monitor"')
	          self.end_headers()
	          logger.error( "Invalid auth header: %s -- %s" % (username,password) )
	          self.wfile.write('Authentication failure - Wrong user/password')
	          return

        if self.path.find('?') != -1:
            self.urlPath, self.query_string = self.path.split('?', 1)
        else:
            self.urlPath = self.path

	mq_qmgr = config_props["mq.qmgr"]
        mq_channels = config_props["mq.channels"]
	logger.debug( "Channels data %s" % (mq_channels))
        allchans=mq_channels.split(",")
        
        logger.info ("For path: %s the url is: %s; qmgr is: %s  and allchans is: %s" % (self.path,self.urlPath,mq_qmgr,allchans))
        
        if self.urlPath == config_props["web.path"]:
            qsl = dict(cgi.parse_qsl(self.query_string))
            logger.debug(qsl)
            
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            logger.info("About to collect statistics for MQ")
            stats = getStatistics(mq_qmgr, allchans)
            self.wfile.write(stats)
        else:
            self.send_error(404, "Requested resource not found")

    def log_message(self, format, *args):
        """Overridden from BaseHTTPRequestHandler because this method occasionally throws error when send_response(200) is called."""
        
        if logger.isEnabledFor(logging.DEBUG):
           logger.debug(args[0])

def getStatistics(qmgr, allchans):
    failedChanCount=0
    successChanCount=0
    errchans = ""
    statMetrcs = ""
    for i in range(len(allchans)):
        if allchans[i] == "":
           'print "Skipping blank line"'
           continue
        else:
    
           cmdstr='echo \"DIS CHS(' + allchans[i] + ') BYTSSENT,BYTSRCVD,MSGS\" | runmqsc ' + qmgr
           logger.debug("Command string is: %s" % (cmdstr))
    
           chanstatoutput=commands.getstatusoutput(cmdstr)
    
           if chanstatoutput[0] != 0:
               print ("MQCHECK ERROR: runmqsc call returned error: %s" % chanstatoutput[1])
               sys.exit(1)
    
           chanstatstr = chanstatoutput[1].replace ('\n', '')
           #print "Exec Result is: %s" % (chanstatstr)
    
           matched=re.search('(?<=STATUS\()\w+', chanstatstr)
           if matched == None:
               statusstr="ERROR"
           else:
               statusstr=matched.group(0)
           #print "Channel status for %s is: %s" % (allchans[i],statusstr)
    
           if statusstr != "RUNNING":
               errchans = errchans + statusstr + ", "
               failedChanCount = failedChanCount+1
           else:
               successChanCount = successChanCount+1
    
           matched=re.search('(?<=BYTSSENT\()\w+', chanstatstr)
           if matched != None:
               thisMetrcs = " " + allchans[i] + "_BYTSSENT=" + matched.group(0)
               #print "A metrics: %s" % thisMetrcs
               statMetrcs = statMetrcs + thisMetrcs
    
           matched=re.search('(?<=BYTSRCVD\()\w+', chanstatstr)
           if matched != None:
               statMetrcs = statMetrcs + " " + allchans[i] + "_BYTSRCVD=" + matched.group(0)
    
           matched=re.search('(?<=MSGS\()\w+', chanstatstr)
           if matched != None:
               statMetrcs = statMetrcs + " " + allchans[i] + "_MSGS=" + matched.group(0)
    
    'print "ErrChan result is %s" % errchans'
    if failedChanCount > 0:
        return 'MQCHECK ERROR|ChanStatus=%d %s errorMessage=%s' % (failedChanCount, statMetrcs, errchans[:-2])
    else:
        return 'MQCHECK OK|ChanStatus=0 %s successChannels=Total channels checked is %d' % (statMetrcs, successChanCount)

def readProperties(prop_filename):
    propFile= file( prop_filename, "r" )
    
    propDict= dict()
    for propLine in propFile:
        propDef= propLine.strip()
        if len(propDef) == 0:
            continue
        if propDef[0] in ( '!', '#' ):
            continue
        punctuation= [ propDef.find(c) for c in ':= ' ] + [ len(propDef) ]
        found= min( [ pos for pos in punctuation if pos != -1 ] )
        name= propDef[:found].rstrip()
        value= propDef[found:].lstrip(":= ").rstrip()
        propDict[name]= value
    propFile.close()
    return propDict

def startServer():
    req_handler = WebRequestHandler
    req_handler.config_props = config_props
    server = MQHTTPServer((http_address,http_port), req_handler)
    server.run_forever()

def usage():
   print ("%s\n\t-h|--help\t\tTo print this help\n\t-s|--standalone\t\tTo run monitor service in command-line\n\t-c|--config_file\tProperties file to configure the webservice\n\t-q|--queue_file\t\t(-s only)File containing queue channel names\n\t-q|--qmgr\t\t(-s only)Queue Manager to access in standalone" % (sys.argv[0]))

nosvc = False
queue_file="/opt/support/queue_channels.txt"
qmgr="B001"
prop_filename="/opt/support/mq_monitor_web_service.properties"
argrest=sys.argv[1:]
opts, args = getopt.getopt(argrest, "hsc:q:m:", ["help", "standalone", "config_file=", "queue_file=", "qmgr="]) 
for opt, arg in opts:
   if opt in ("-h", "--help"):
      usage()
      sys.exit()
   elif opt in ("-s", "--standalone"):
      nosvc = True
      print "Running the monitor one-time"
   elif opt in ("-c", "--config_file"):
      prop_filename = arg
      print "Using config_file: %s" % prop_filename
   elif opt in ("-q", "--queue__file"):
      queue_file = arg
      print "Using queue_file: %s" % queue_file
   elif opt in ("-m", "--qmgr"):
      qmgr = arg
      print "Using qmgr: %s" % qmgr

config_props=readProperties(prop_filename)
http_address = config_props.get("web.address", "")
http_port_str = config_props.get("web.port", "7890")
http_port = int(http_port_str)

log_filename=config_props.get("svc.log.config", "/opt/support/zenoss_mq_svc_logging.conf")

logging.config.fileConfig(log_filename)

logger = logging.getLogger('main_logger')

logger.debug( config_props )

if nosvc:
   print ("Launching program at commandline")
   f = open(queue_file)
   lines=""
   try:
       for line in f:
           lines=lines + line
   finally:
       f.close()
   allchans=lines.split("\n")
   stats = getStatistics(qmgr, allchans)
   print stats
else:
   startServer()
