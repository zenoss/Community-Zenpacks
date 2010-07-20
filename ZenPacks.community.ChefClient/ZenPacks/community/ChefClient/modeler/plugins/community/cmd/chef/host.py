import json
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class host(CommandPlugin):
    maptype = "DeviceMap"
    compname = ""
    command = "ohai fqdn kernel"

    def process(self, device, results, log):
        """Collect command-line information from this device"""
        log.info("Processing the ohai host info for device %s" % device.id)
        om = self.objectMap()
        #results are JSON-formatted output
        #get a JSON parser and pull out values
        #first [] set is snmpSysName
        fqdnresults = results[0:results.index(']')+1]
        fqdnjson = json.loads(fqdnresults)
        om.snmpSysName = fqdnjson[0]
        #seond [] set is kernel info
        kernelresults = results[results.index(']')+1:]
        kerneljson = json.loads(kernelresults)
        kerneljson.sort()
        # "name" 
        om.uname = kerneljson[2][1]
        # "machine"
        machine = kerneljson[0][1]
        # "os"
        os = kerneljson[3][1]
        # "release"
        release = kerneljson[4][1]
        # "version"
        version = kerneljson[5][1]
        om.setOSProductKey = MultiArgs(version, os)
        # "name fqdn version release machine"
        om.snmpDescr = om.uname+' '+om.snmpSysName+' '+version+' '+release+' '+machine

        log.debug(om)
        return om
