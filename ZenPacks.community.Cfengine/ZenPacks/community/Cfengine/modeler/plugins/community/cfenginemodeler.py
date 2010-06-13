import re, os
from Products.ZenUtils.Utils import zenPath
from Products.DataCollector.plugins.DataMaps import MultiArgs
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin

class cfenginemodeler(PythonPlugin):
    """
    Parse the zCfengineComplianceFile to get the compliance status for devices.
    """

    deviceProperties = PythonPlugin.deviceProperties + ('zCfengineComplianceFile', )

# 62.109.39.157,/Server/Linux,97
# 62.109.39.156,/Server/Linux,96
# 128.39.89.233,/Server/Solaris,73
# 62.109.39.155,/Server/Darwin,95
# 62.109.39.151,/Server/Windows,19
# 62.109.39.152,/Ping,92
# 62.109.39.150,/Ping,80

    def findPath(self):
        path = []
        for p in __file__.split(os.sep):
            if p == 'modeler': break
            path.append(p)
        return os.sep.join(path)

    #get the results we're looking for
    def collect(self, device, log):
        log.info('Parsing cfengine client list for device %s' % device.id)
        compliancefile = device.zCfengineComplianceFile
        log.debug('compliancefile %s' % compliancefile)
        try:
            output = open(compliancefile, 'r')
        except IOError:
            log.error('Can\'t open %s for reading.' % compliancefile)
	    return None
        results = output.read()
        output.close()
	if results is None or output == '':
	    log.info('cfengine zCfengineComplianceFile: Unable to connect or denied access?')
	    return None
	return results

    #push the results into the model
    def process(self, device, results, log):
        log.info('Processing cfengine client list for device %s' % device.id)
	self.modname = 'ZenPacks.community.Cfengine.CfengineClient'
        self.relname = "cfengineclients"
        serverId = device.getId()
        rm = self.relMap()
        rlines = results.split("\n")
        for line in rlines:
            om = self.objectMap()
            if re.search(',', line):
                om.cfcDisplayName, om.cfcDeviceClass, value = line.split(',')
                if om.cfcDeviceClass == "any":
                    om.cfcDeviceClass == "/Discovered"
                om.cfcCompliance = int(value)
                log.debug('Collecting cfengine client list for device %s: Found client = %s' % (device.id,om.cfcDisplayName))
                om.id = self.prepId(om.cfcDisplayName)
                om.setCfengineClient = MultiArgs(om.id, om.cfcDeviceClass, serverId)
                rm.append(om)
        log.debug(rm)

        return rm
        

