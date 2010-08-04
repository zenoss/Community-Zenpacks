#!/bin/env python

version="%prog 0.02"

import re
import sys
import subprocess

from socket   import gethostbyname
from optparse import OptionParser

def parseOptions():

  usage = "usage: %prog [-d][-h] -H <HOST> [-V <SNMPVERSION>] [-C <COMMUNITY>] [-l <DATATYPE>] [-t <TIMEOUT>] [-f <FSINDEX>]"

  parser = OptionParser(version=version,usage=usage)
  parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Turn on output of any debugging information")
  parser.add_option("-H", "--host", help="Hostname or IP address of server you wish to query", metavar="<HOST>")
  parser.add_option("-V", "--snmpversion", help="Set the SNMP version (default is 2c)", metavar="<SNMPVERSION>", default="v2c")
  parser.add_option("-C", "--community", help="Set the community string for SNMPv1/v2c transactions (default is public)", metavar="<COMMUNITY>", default="public")
  parser.add_option("-l", help="[power,cpu,fan,temp,filesystemlist,filesystem,nfscache,enclosure,product] - Data to fetch (default is cpu)", metavar="<DATATYPE>", default="cpu")
  parser.add_option("-f", "--fsindex", help="index to the snmp data (used in combination with -l filesystem)", metavar="<FSINDEX>")
  parser.add_option("-t", "--timeout", help="timeout in seconds for SNMP data request", metavar="<TIMEOUT>")
  parser.add_option("-u", "--user", help="user for ssh df command", metavar="<USER>", default="supervisor")

  (options, args) = parser.parse_args()

  if (options.host == None) or (options.l == "filesystem" and options.fsindex == None): parser.print_help()

  if options.l not in ("cpu", "enclosure", "fan", "filesystem", "filesystemlist", "nfscache", "power", "product", "temp"):
    print "Unknown option: ", options.l
    parser.print_help()

  return options

def snmpGetTable(host, version, community, tablename, table, columns):

  snmpValues = subprocess.Popen(["snmpwalk", "-On", "-" + version, "-c", community, host, table], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].split("\n")[:-1]

  snmpPairs={}
  for line in snmpValues:
    oid, value = line.split()[0], line.split()[-1].replace("\"", "")

    snmpPairs[oid] = value

  snmpTableIndexValues={}
  for oid in snmpPairs.keys():
    snmpTableIndexValues[oid.split(table,1)[1][1:].split(".",1)[1]] = 1

  snmpTable={}
  for snmpTableIndexValue in snmpTableIndexValues.keys():
    rowEntries={}
    for column in columns:
      rowEntries[columns[column]]=snmpPairs[table+column+"."+snmpTableIndexValue]
    snmpTable[snmpTableIndexValue]=rowEntries
    
  return { tablename: snmpTable }

def sshHost(host, user, command, re):

  sshValues = subprocess.Popen(["ssh", user + "@" + host, command], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

  return re.findall(sshValues)


options=parseOptions()

volumeTable=".1.3.6.1.4.1.11096.6.1.1.1.3.5.2.1"
volumeTableColumns = {
  '.1': 'volumeSysDriveIndex',
  '.2': 'volumePartitionID',
  '.3': 'volumeLabel',
  '.4': 'volumeStatus',
  '.5': 'volumeCapacity',
  '.6': 'volumeFreeCapacity',
  '.7': 'volumeEnterpriseVirtualServer',
}

fsStatsTable = ".1.3.6.1.4.1.11096.6.1.1.1.3.5.3.1"
fsStatsTableColumns = {
  '.2': 'fsLabel',
  '.3': 'opsPerSecAverage'
}

if options.l == "filesystemlist":

  filesystems=[]
  volumes=snmpGetTable(options.host, options.snmpversion, options.community, "volumeTable", volumeTable, volumeTableColumns)

  ipaddy=gethostbyname(options.host)
  
  print "|",
  for volume in volumes.get('volumeTable').values():
    sys.stdout.softspace=False
    print volume['volumeSysDriveIndex']+"=\""+volume['volumeLabel']+"\" ",
  sys.exit(0)

if options.l == "filesystem":

  volumes = snmpGetTable(options.host, options.snmpversion, options.community, "volumeTable", volumeTable, volumeTableColumns)
  fsLabel = ''
  output  = '|'
  for volume in volumes.get('volumeTable').values():
    if volume['volumeSysDriveIndex'] == options.fsindex:

      fsLabel = volume['volumeLabel']

      output += "volumeSysDriveIndex=" + volume['volumeSysDriveIndex'] + \
                " volumeLabel=\"" + fsLabel + "\"" + \
                " volumeStatus=" + volume['volumeStatus'] + \
                " totalBlocks=" + str(int(volume['volumeCapacity'])/1024) + \
                " availBlocks=" + str(int(volume['volumeFreeCapacity'])/1024) + \
                " usedBlocks=" + str((int(volume['volumeCapacity'])-int(volume['volumeFreeCapacity']))/1024) + \
                " volumeEnterpriseVirtualServer=" + volume['volumeEnterpriseVirtualServer']

  snapList = sshHost(options.host, options.user, "df -k", re.compile('(\d+)\s+\S+\s+\d+\s+\d+\s+KB\s+\d+\s+KB\s+\d+\s+KB\s+\S+\s+(\d+)\s+KB',re.DOTALL) )
  for filesystemSnapUsage in snapList:
    if filesystemSnapUsage[0]==options.fsindex:
      output += " snapshots=" + str(filesystemSnapUsage[1]).strip()

  # Get the fsStats
  fsStats = snmpGetTable(options.host, options.snmpversion, options.community, "fsStatsTable", fsStatsTable, fsStatsTableColumns)
  for fsStat in fsStats.get('fsStatsTable').values():
    if fsStat['fsLabel'] == fsLabel:
      output += " opsPerSecAverage=" + fsStat['opsPerSecAverage']

  print output

  sys.exit(0)

print options.l, " not implementend yet"
