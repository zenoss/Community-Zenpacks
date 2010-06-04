import re
from datetime import datetime
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class cfenginemodeler(CommandPlugin):
    """
    Parse the zCfengineComplianceFile to get the compliance status for devices.
    """
    relname = "cfengineclients"
    modname = 'ZenPacks.community.cfengine.CfengineClient'
    command = 'python -c "import os,sys; print os.path.getctime(\'%s\' % sys.argv[1])" $zCfengineComplianceFile; cat $zCfengineComplianceFile'

# 1275602690
# 62.109.39.157,97
# 62.109.39.156,96
# 128.39.89.233,93
# 62.109.39.155,95
# 62.109.39.151,19
# 62.109.39.152,92
# 62.109.39.150,80

    def process(self, device, results, log):
        log.info('Parsing cfengine client list for device %s' % device.id)
        rm = self.relMap()
        rlines = results.split("\n")
        dt = datetime.fromtimestamp(int(rlines[0].strip()))
        filedate = dt.strftime("%Y/%m/%d %H:%M")
        for line in rlines:
            om = self.objectMap()
            if re.search(',', line):
                om.cfcDisplayName, value = line.split(',')
                om.cfcCompliance = int(value)
                om.cfcLastUpdateTime = filedate
                log.info('Collecting cfengine client list for device %s: Found client = %s' % (device.id,om.cfcDisplayName))
                om.id = self.prepId(om.cfcDisplayName)
                rm.append(om)
        return [rm]
