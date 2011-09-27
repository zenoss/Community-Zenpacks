========================================================================================================================
Zenpack: IBM System x Integrated Management Module...
========================================================================================================================
------------------------------------------------------------------------------------------------------------------------
Developed by:
------------------------------------------------------------------------------------------------------------------------
IBM Linux Technology Center

------------------------------------------------------------------------------------------------------------------------
Description:
------------------------------------------------------------------------------------------------------------------------
The IBMSystemxIMM Zenpack supports out-of-band management (that is, independent of the running OS) for IBM System x servers with Integrated Management Module (IMM).  IMM is an onboard Management Processor that provides monitoring, alerting, remote management and remote control of IBM servers.  IMM supports IPMI 2.0, Serial over LAN (SOL), SNMP v1 and v3, telnet, ssh, SMASH CLP, SLP, CIM, SMTP and Web Access via HTTP/HTTPS.

The primary interface to IMM for the IBMSystemxIMM Zenpack is via SNMP.  (as of v0.3.1 it has been tested with SNMP v1 only)  The Zenpack currently supports the following features:

Configuration data (Modeler Plugins):
- Device-level Vital Product Data (VPD): Machine Type Model (MTM), Serial Number, UUID, etc.
- Firmware VPD
- CPU VPD (not supported on all IBM servers)
- Memory VPD
- Chassis Component VPD
- Chassis Component Log
- System Fan Monitors
- System Voltage Monitors

Performance data (Monitoring Templates):
- Ambient Temperature (device level)
- Fan Speeds  (component level)
- System Voltages (component level)

Device Classes:
 - /Server/IMM

Event Classes:
 - /Events/IMM


------------------------------------------------------------------------------------------------------------------------
Components:
------------------------------------------------------------------------------------------------------------------------
The Zenpack automatically installs the following:

Device Class: /Server/IMM

Modeler Plugins:
 - community.snmp.IBMIMMDeviceMap
 - community.snmp.IBMIMMFwVpdMap
 - community.snmp.IBMIMMCpuVpdMap
 - community.snmp.IBMIMMMemVpdMap
 - community.snmp.IBMIMMComponentVpdMap
 - community.snmp.IBMIMMComponentLogMap
 - community.snmp.IBMIMMFanMonMap
 - community.snmp.IBMIMMVoltMonMap

Monitoring Templates (only IMMAmbientTemp will be bound the the device (green checkmark); the other two are component-level collectors):

 - Devices
   `- Server
      `- IMM
         |- IMMAmbientTemp (Locally defined)
         |- IMMFanMon (Locally defined)
         `- IMMVoltMon (Locally defined)

Event Class: /Events/IMM

Event Mappings: for all traps defined in IMMALERT-MIB, mapped to /Events/IMM, severity mapped to Zenoss severity levels.


------------------------------------------------------------------------------------------------------------------------
Requirements:
------------------------------------------------------------------------------------------------------------------------
 - Zenoss Versions Supported: >= 3.0
 - External Dependencies: IBM System x server with Integrated Management Module, SNMP enabled.
 - ZenPack Dependencies: None
 - Installation Notes: See above
 - Configuration: No config required other than SNMP community string, etc.


------------------------------------------------------------------------------------------------------------------------
Installation:
------------------------------------------------------------------------------------------------------------------------
 1. Enable SNMP protocol on the IMM via the IMM's web UI.  Specifically you need to configure: IMM Control > Network Protocols, and optionally IMM Control > Alert.  Follow your server admin guide or the online help (in the web UI).

 2. Install the IMM-MIB and IMMALERT-MIB in Zenoss per the standard procedure, i.e. Advanced > MIBs > Add MIB.  The IMM mibs are included with any IMM firmware download (http://www.ibm.com/support/).  Look for the .mib files in zip file containing the firmware.

    Alternately, to install MIBs from the command line, copy the files to: /opt/zenoss/share/mibs/site/ and:

    $ su - zenoss
    $ zenmib run $ZENHOME/share/mibs/site/imm.mib
    $ zenmib run $ZENHOME/share/mibs/site/immalert.mib

 3. Install the IBMSystemxIMM Zenpack from .egg per the standard procedure, i.e. Advanced > Zenpacks > Install Zenpack.  'zopectl restart' after installing.

    Alternately, to install from command line:
    $ zenpack --install ZenPacks.community.IBMSystemxIMM-0.3.0-py2.6.egg

 4. Discover the server via the IP address of the IMM (not the IP of the running OS instance) per the standard procedure, i.e. Infrastructure > Devices > Add Device.  Use device class: /Server/IMM.  Follow the discovery output or wait a few mins for modeling to complete.

    Alternately, to discover from command line (device cannot exist first):
    $ zendisc run --now -d myserverIMM.mydomain.com --monitor localhost --deviceclass /Server/IMM

5. After it's discovered (and modeled) navigate to the device and you should see the following entries under Components:

  - Components
    |- IMM Chassis Component Log
    |- IMM Chassis Component VPD
    |- IMM CPU VPD                   # if applicable; not supported on M2/M3
    |- IMM Fan Monitors
    |- IMM Firmware VPD
    |- IMM Memory VPD
    `- IMM Voltage Monitors

    The Fan and Voltage Monitors should have Graphs.  The Device level Graphs should include AmbientTemp.

    It should model it on discovery but just fyi, to run the modeler from cli:

    $ zenmodeler run -d myserverIMM.mydomain.com

6. Troubleshooting:

     If you have missing entries under Components list try restarting zopeclt & zenhub.  Navigate AWAY from the device in the UI then navigate back.  If all else fails try deleting and rediscovering the device.

     If it's not collecting performance data (graphs) you can try this, or the steps below. (IMMAmbientTemp and IMMVoltMon are SNMP Datasources; IMMFanMon is a COMMAND Datasource):

     $ zenperfsnmp restart
     $ zencommand restart


================================================================================
TROUBLESHOOTING PERF COLLECTION PROBLEMS:
================================================================================
## -- look for errors here...
tail -F /opt/zenoss/log/zenperfsnmp.log

## -- Check timestamp of RRD files... this is a reliable indicator of when they were last updated...
find /opt/zenoss/perf/Devices/mydevice.mydomain.com/ -name \*.rrd -exec ls -la {} \;
find /opt/zenoss/perf/Devices/mydevice.mydomain.com/IMM* -name \*.rrd -exec ls -la {} \;

## -- Run the poller daemons manually...
##    If everything is good this will force collection and therefore update of RRD files.  But that's NO GUARANTEE automatic collection is working!
zenperfsnmp run -v10 -d mydevice.mydomain.com
zencommand run -v10 -d mydevice.mydomain.com

## -- Restart the thing, if nothing else works...
zenperfsnmp restart
zencommand restart
