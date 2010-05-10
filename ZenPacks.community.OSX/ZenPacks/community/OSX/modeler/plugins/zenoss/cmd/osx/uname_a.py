_doc__ = """uname -a
Determine snmpSysName and setOSProductKey from the result of the uname -a command.
"""

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

def parse_serial(command):
    "Parse the output of system_profiler SPHardwareDataType | grep 'Serial Number (system)'"
    serial = command.split(':')[1].strip()
    return serial

def parse_hwmodel(command):
    "Parse the output of system_profiler -detailLevel mini | grep 'Model Identifier'"
    hwmodel = command.split(':')[1].strip()
    return hwmodel

def parse_osversion(command):
    "Parse the output of system_profiler -detailLevel mini SPSoftwareDataType | grep 'System Version'"
    osversion = command.split(':')[1].strip()
    return osversion

class uname_a(CommandPlugin):
    maptype = "DeviceMap"
    compname = ""
    command = "uname -a && system_profiler SPHardwareDataType | grep 'Serial Number (system)' && system_profiler -detailLevel mini | grep 'Model Identifier' && system_profiler -detailLevel mini SPSoftwareDataType | grep 'System Version'"

    def process(self, device, results, log):
        """Collect command-line information from this device"""
        log.info("Processing the uname -a info for device %s" % device.id)
        om = self.objectMap()
        command_output = results.split('\n')
        om.snmpDescr = command_output[0].strip()
        om.uname = om.snmpDescr.split()[0]
        om.snmpSysName = om.snmpDescr.split()[1]
        om.setHWSerialNumber = parse_serial(command_output[1])
        hwmodel = parse_hwmodel(command_output[2])
        #using "Apple" instead of "Darwin" for clarity
        om.setHWProductKey = MultiArgs(hwmodel, "Apple")
        osversion = parse_osversion(command_output[3])
        #using "Apple" instead of "Darwin" for clarity
        om.setOSProductKey = MultiArgs(osversion,"Apple")

        log.debug(om)
        return om
