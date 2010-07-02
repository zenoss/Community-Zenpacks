#!/usr/bin/env python
# Author: Nick Anderson <nick.anderson@motorola.com>
# Rack PDU AMP Load Aggregation
# Designed for use with APC 7840
# Scinario: You have 2 legs of power A and B, each rack has 1 PDU on each leg
#           and you need to monitor the aggregate and individual AMP Load

import sys
import subprocess
from optparse import *

def display(aggregate, results):
    '''Output load results in zenoss parsable format'''
    print "PDU: OK | Aggregate=%s" %aggregate,
    count = 0
    for device in results:
        if count == 0:
            print "A=%s" %(results[device]),
        else:
            print "B=%s" %(results[device]),
        count += 1

def collect_data(options, devices, oid):
    '''Fetch data at given OID from specified devices'''
    results = {}
    for device in devices:
        cmd = "snmpget -v1 -c %s %s %s" %(options.community_string,device, oid)
        # Get the numeric value from snmp
        p = subprocess.Popen(cmd,
                    shell=True,
                    stdout=subprocess.PIPE)
        value = p.communicate()[0]
        # Check for error running snmpget
        if not p.returncode == 0:
            # Return critical if unable to communicate
            print "PDU: Failed to communicate with %s" %device
            sys.exit(2)
        else:
            value = value.split()[-1]
        results[device] = value
    return results
    
def convert_values(results):
    '''Likely specific to the OID data but for APC 7840 this converts
    the string into a float and converts it to AMP Decimal'''
    for device in results:
        results[device] = round(float(results[device])/10,2)
    return results
    
if __name__ == "__main__":

    op = OptionParser("Usage: %prog [-c communitystring] OID PDUA PDUB")
    op.add_option('-c',
            dest='community_string',
            help='snmp v1 community string (default: %default)')

    op.set_defaults(community_string='public')

    (options, args) = op.parse_args()

    if not len(args) == 3:
        op.error("PDUA PDUB and OID are required")

    # Add PDUA and PDUB to device list
    oid = args[0]
    devices = [ args[1], args[2] ]

    # Collect and convert results
    try:
        results = collect_data(options, devices, oid)
    except:
        # Exit critical if something bad happens during collection
        sys.exit(2)
    results = convert_values(results)

    # Tabulate aggrigate value for devices
    aggregate = 0
    for device in results:
       aggregate += results[device]

    # Display output
    display(aggregate,results)
