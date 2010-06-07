import re, os
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin

class cfenginemodeler(PythonPlugin):
    """
    Parse the zCfengineComplianceFile to get the compliance status for devices.
    """

    deviceProperties = PythonPlugin.deviceProperties + ('zCfengineComplianceFile',)

# 62.109.39.157,97
# 62.109.39.156,96
# 128.39.89.233,93
# 62.109.39.155,95
# 62.109.39.151,19
# 62.109.39.152,92
# 62.109.39.150,80

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
        rm = self.relMap()
        rlines = results.split("\n")
        for line in rlines:
            om = self.objectMap()
            if re.search(',', line):
                om.cfcDisplayName, value = line.split(',')
                om.cfcCompliance = int(value)
                log.debug('Collecting cfengine client list for device %s: Found client = %s' % (device.id,om.cfcDisplayName))
                om.id = self.prepId(om.cfcDisplayName)
                rm.append(om)
        log.debug(rm)
        return rm
        

