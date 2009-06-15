#!/usr/bin/env python

"""Utility functions for building collectors"""

def build_snmp_command( command, device, oid, snmp_creds="" ):
    """Given a device name, an OID and SNMP credential information build an snmp[walk|get] command.
        The credentials string is supposed to be built up using command line arguments passed to the
       program with the following format:

       zpropname=value[:zpropname=value]*

       For example:
           zSnmpAuthType=:zSnmpCommunity=public:zSnmpVer=1
"""

    cmd= command

    if snmp_creds == "":
        zSnmpVer= "v1"
        zSnmpCommunity= "public"

    if zSnmpVer == "v1":
        cmd= " ".join( [ command, "-v1", "-c", zSnmpCommunity, device, oid ] )
    
    return cmd


if __name__ == "__main__":
    #if len(sys.argv) < 3:
        #print "Need device and SNMP credential arguments!"
        #sys.exit(1)

    #(device, creds )= sys.argv[1:]
    device= "blue"
    creds= ""
    oid= ".1.3.6.4.1"

    print build_snmp_command( "snmpwalk", device, oid, creds )
    import sys
    sys.exit(0)

