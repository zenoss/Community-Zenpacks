#!/usr/bin/env python
import os
import sys
import re
import string
import getopt

##Check for python dependancies. If not found, flail user and quit.
try:
    from pysnmp.entity.rfc3413.oneliner import cmdgen
except Exception, e:
    print "You need to download pysnmp and pyasn1 fool!", e
    sys.exit(1)

##Main Fuction
def main():
    ##Allocate blank table
    SLA_Table = {}
    
    ##Perform walk of common RTT objects 
    rttMonLatestRttOperCompletionTime = walk( device, community, SLATable["rttMonLatestRttOperCompletionTime"])
    rttMonLatestRttOperSense = walk( device, community, SLATable["rttMonLatestRttOperSense"])
    rttMonLatestRttOperApplSpecificSense = walk( device, community, SLATable["rttMonLatestRttOperApplSpecificSense"])
    rttMonLatestRttOperTime = walk( device, community, SLATable["rttMonLatestRttOperTime"])

    ##If SLA is VoIP, perform walk of VoIP objects
    if tType == "V":
            rttMonLatestJitterOperAvgJitter = walk( device, community, vSLATable["rttMonLatestJitterOperAvgJitter"])
            rttMonLatestJitterOperIAJIn = walk( device, community, vSLATable["rttMonLatestJitterOperIAJIn"])
            rttMonLatestJitterOperIAJOut = walk( device, community, vSLATable["rttMonLatestJitterOperIAJOut"])
            rttMonLatestJitterOperICPIF = walk( device, community, vSLATable["rttMonLatestJitterOperICPIF"])
            rttMonLatestJitterOperMOS = walk( device, community, vSLATable["rttMonLatestJitterOperMOS"])

    ##If SLA is HTTP, perform walk of other HTTP objects
    if tType == "W":
            rttMonLatestHTTPOperRTT = walk( device, community, wSLATable["rttMonLatestHTTPOperRTT"])
            rttMonLatestHTTPOperDNSRTT = walk( device, community, wSLATable["rttMonLatestHTTPOperDNSRTT"])
            rttMonLatestHTTPOperTCPConnectRTT = walk( device, community, wSLATable["rttMonLatestHTTPOperTCPConnectRTT"])
            rttMonLatestHTTPOperTransactionRTT = walk( device, community, wSLATable["rttMonLatestHTTPOperTransactionRTT"])
            rttMonLatestHTTPErrorSenseDescription = walk( device, community, wSLATable["rttMonLatestHTTPErrorSenseDescription"])

    ##Take each collected value and store in a table
    for host in rttMonLatestRttOperCompletionTime[1]:
	SLA_Table[str(host[0][0][14])]={}
	SLA_Table[str(host[0][0][14])]["rttMonLatestRttOperCompletionTime"] = host[0][1]
        SLA_Table[str(host[0][0][14])]["item"] = host[0][0][14]

    for host in rttMonLatestRttOperSense[1]:
        SLA_Table[str(host[0][0][14])]["rttMonLatestRttOperSense"] = host[0][1]

    for host in rttMonLatestRttOperApplSpecificSense[1]:
        SLA_Table[str(host[0][0][14])]["rttMonLatestRttOperApplSpecificSense"] = host[0][1]

    for host in rttMonLatestRttOperTime[1]:
        SLA_Table[str(host[0][0][14])]["rttMonLatestRttOperTime"] = host[0][1]

    ##If VoIP, store VoIP objects in same table
    if tType == "V":
                for host in rttMonLatestJitterOperAvgJitter[1]:
                    SLA_Table[str(host[0][0][14])]["rttMonLatestJitterOperAvgJitter"] = host[0][1]

                for host in rttMonLatestJitterOperIAJIn[1]:
                    SLA_Table[str(host[0][0][14])]["rttMonLatestJitterOperIAJIn"] = host[0][1]

                for host in rttMonLatestJitterOperIAJOut[1]:
                    SLA_Table[str(host[0][0][14])]["rttMonLatestJitterOperIAJOut"] = host[0][1]

                for host in rttMonLatestJitterOperICPIF[1]:
                    SLA_Table[str(host[0][0][14])]["rttMonLatestJitterOperICPIF"] = host[0][1]

                for host in rttMonLatestJitterOperMOS[1]:
                    SLA_Table[str(host[0][0][14])]["rttMonLatestJitterOperMOS"] = host[0][1]

    ##If HTTP, store HTTP objects in same table
    if tType == "W":
                for host in rttMonLatestHTTPOperRTT[1]:
                    SLA_Table[str(host[0][0][14])]["rttMonLatestHTTPOperRTT"] = host[0][1]

                for host in rttMonLatestHTTPOperDNSRTT[1]:
                    SLA_Table[str(host[0][0][14])]["rttMonLatestHTTPOperDNSRTT"] = host[0][1]

                for host in rttMonLatestHTTPOperTCPConnectRTT[1]:
                    SLA_Table[str(host[0][0][14])]["rttMonLatestHTTPOperTCPConnectRTT"] = host[0][1]

                for host in rttMonLatestHTTPOperTransactionRTT[1]:
                    SLA_Table[str(host[0][0][14])]["rttMonLatestHTTPOperTransactionRTT"] = host[0][1]

                for host in rttMonLatestHTTPErrorSenseDescription[1]:
                    SLA_Table[str(host[0][0][14])]["rttMonLatestHTTPErrorSenseDescription"] = host[0][1]

    ##If -k / key is not nothing, show the entries using said key, else show all
    if keyS != None:
        sho_specific_result(SLA_Table, keyS)
    else:
	sho_result(SLA_Table)

##Fuction to display table data using a specified key
def sho_specific_result( SLA_Table, keyS ):
    for key in SLA_Table:
	if key == keyS:
                ##Declare vOut and wOut
                vOut = wOut = "" 

                ##If SLA is VoIP, populate vOut with correct table data
                if tType == "V":
                   vOut= " rttMonLatestJitterOperAvgJitter=" + str(SLA_Table[key]["rttMonLatestJitterOperAvgJitter"]) + " rttMonLatestJitterOperIAJIn=" + str(SLA_Table[key]["rttMonLatestJitterOperIAJIn"]) + " rttMonLatestJitterOperIAJOut=" + str(SLA_Table[key]["rttMonLatestJitterOperIAJOut"]) + " rttMonLatestJitterOperICPIF=" + str(SLA_Table[key]["rttMonLatestJitterOperICPIF"]) + " rttMonLatestJitterOperMOS=" + str(SLA_Table[key]["rttMonLatestJitterOperMOS"])

                ##If SLA is HTTP, populate wOut with correct table data
                if tType == "W":
		   wOut= " rttMonLatestHTTPOperRTT=" + str(SLA_Table[key]["rttMonLatestHTTPOperRTT"]) + " rttMonLatestHTTPOperDNSRTT=" + str(SLA_Table[key]["rttMonLatestHTTPOperDNSRTT"]) + " rttMonLatestHTTPOperTCPConnectRTT=" + str(SLA_Table[key]["rttMonLatestHTTPOperTCPConnectRTT"]) + " rttMonLatestHTTPOperTransactionRTT=" + str(SLA_Table[key]["rttMonLatestHTTPOperTransactionRTT"]) + " rttMonLatestHTTPErrorSenseDescription=" + str(SLA_Table[key]["rttMonLatestHTTPErrorSenseDescription"]) 

                ##Populate out with common table data
		out= "OK| key=" + str(SLA_Table[key]["item"]) + " rttMonLatestRttOperCompletionTime=" + str(SLA_Table[key]["rttMonLatestRttOperCompletionTime"]) + " rttMonLatestRttOperSense=" + str(SLA_Table[key]["rttMonLatestRttOperSense"]) + " rttMonLatestRttOperApplSpecificSense=" + str(SLA_Table[key]["rttMonLatestRttOperApplSpecificSense"]) + " rttMonLatestRttOperTime=" + str(SLA_Table[key]["rttMonLatestRttOperTime"])

                ##Print all strings
		print out + vOut + wOut

##Fuction to display all common table data
def sho_result( SLA_Table ):
    for key in SLA_Table:
	print "OK| key=", SLA_Table[key]["item"], "RttOperCompletionTime=", SLA_Table[key]["rttMonLatestRttOperCompletionTime"], "RttOperSense=", SLA_Table[key]["rttMonLatestRttOperSense"], "ApplSpecificSense=", SLA_Table[key]["rttMonLatestRttOperApplSpecificSense"], "RttOperTime=", SLA_Table[key]["rttMonLatestRttOperTime"]

##SNMP walk (essentially)
def walk( dswitch, com, oid ):  
    errorIndication, errorStatus, errorIndex, \
    generic = cmdgen.CommandGenerator().nextCmd(cmdgen.CommunityData('test-agent', com), \
    cmdgen.UdpTransportTarget((dswitch, 161)), oid)
    return ( (errorIndication, generic) )

##Print help menu
def usage():
    print """
    Remember: pysnmp and pyasn1 are requirements to run this script!
    '-d, --device=switch'             This is the device you are connecting to.
    '-c, --community=public'          This is the SNMP community string you are using to connect to the device.
    '-k, --key=unique ID'             This is the unique ID for the entry you wish to return.
    '-h, --help'                      Call this help menu.
    '-t, --type'                      Specify SLA type.
    """
    sys.exit(1)

##Define SLA OID's for specified SLA types
SLATable = { 
            "rttMonLatestRttOperCompletionTime" : (1,3,6,1,4,1,9,9,42,1,2,10,1,1),
            "rttMonLatestRttOperSense" : (1,3,6,1,4,1,9,9,42,1,2,10,1,2),
            "rttMonLatestRttOperApplSpecificSense" : (1,3,6,1,4,1,9,9,42,1,2,10,1,3),
            "rttMonLatestRttOperTime" : (1,3,6,1,4,1,9,9,42,1,2,10,1,5)
            }  

vSLATable = {
             "rttMonLatestJitterOperAvgJitter" : (1,3,6,1,4,1,9,9,42,1,5,2,1,46),
             "rttMonLatestJitterOperIAJIn" : (1,3,6,1,4,1,9,9,42,1,5,2,1,45),
             "rttMonLatestJitterOperIAJOut" : (1,3,6,1,4,1,9,9,42,1,5,2,1,44),
             "rttMonLatestJitterOperICPIF" : (1,3,6,1,4,1,9,9,42,1,5,2,1,43),
             "rttMonLatestJitterOperMOS" : (1,3,6,1,4,1,9,9,42,1,5,2,1,42)
             }

wSLATable = {
            "rttMonLatestHTTPOperRTT" : (1,3,6,1,4,1,9,9,42,1,5,1,1,1),
            "rttMonLatestHTTPOperDNSRTT" : (1,3,6,1,4,1,9,9,42,1,5,1,1,2),
            "rttMonLatestHTTPOperTCPConnectRTT" : (1,3,6,1,4,1,9,9,42,1,5,1,1,3),
            "rttMonLatestHTTPOperTransactionRTT" : (1,3,6,1,4,1,9,9,42,1,5,1,1,4),
            "rttMonLatestHTTPErrorSenseDescription" : (1,3,6,1,4,1,9,9,42,1,5,1,1,6)
            }

##Populate arguments. If Fail, print help menu
try:
    opts, args = getopt.getopt(sys.argv[1:], "c:d:k:t:hv",
          [ 'community=', 'device=', 'key=', 'type=', 'help' ]
          )   
except getopt.error:
    usage()

##Declare strings
help = keyS = tType = community = device = None

##Populate strings with arguments
for opt, val in opts:
    if opt in ('-c', '--community'):
        community = val 
    if opt in ('-d', '--device'):
        device = val 
    if opt in ('-k', '--key'):
        keyS = val
    if opt in ('-t', '--type'):
        tType = val
    if opt in ('-h', '--help'):
        help = usage()

##If minimum arguments are supplied, goto main function, else print help menu
if __name__ == '__main__' and device and community:
    main()
else:
    usage()
