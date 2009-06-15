"""
Modeling plugin that parses the contents of eix to gather
information about the software installed on a gentoo linux box.
"""
import re
import time
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class suse_rpm(CommandPlugin):
    """
    rpm - get software list
    """

    command = r'rpm -qa --qf "%{NAME}-%{VERSION}-%{RELEASE}|%{INSTALLTIME}|%{SUMMARY}\n" && echo __COMMAND__ && cat /etc/SuSE-brand |head -1'
    compname = "os"
    relname = "software"
    modname = "Products.ZenModel.Software"


    def process(self, device, results, log):
        log.info('Collecting Software Installed information for device %s' % device.id)
        rm = self.relMap()
        rpm, susetype = results.split('\n__COMMAND__\n')
        susetype=susetype.strip('\n')
        for result in rpm.split('\n'):
            om = self.objectMap()
            om.setProductKey, om.setInstallDate, om.setDescription = result.split('|')[:3]
            om.setInstallDate= "%s/%s/%s" % time.gmtime(float(om.setInstallDate))[:3]
            om.setProductKey = MultiArgs(str(om.setProductKey), str(susetype))
            om.id = self.prepId(om.setProductKey)
            rm.append(om)
        return rm
