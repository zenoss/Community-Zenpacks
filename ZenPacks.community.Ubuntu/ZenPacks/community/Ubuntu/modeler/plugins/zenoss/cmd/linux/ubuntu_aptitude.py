"""
Modeling plugin that parses the contents of eix to gather
information about the software installed on a gentoo linux box.
"""
import re
import time
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class ubuntu_aptitude(CommandPlugin):
    """
    rpm - get software list
    """

    command = r'aptitude -v search ~i -F "%40p %40v" && echo __COMMAND__ && cat /etc/lsb-release'
    compname = "os"
    relname = "software"
    modname = "Products.ZenModel.Software"

    def process(self, device, results, log):
        log.info('Collecting Software Installed information for device %s' % device.id)
        rm = self.relMap()
        rpm, ubuntutype = results.split('\n__COMMAND__\n')
        descPattern = re.compile(r"DISTRIB_DESCRIPTION=\"(.*)\"")
        codenamePattern = re.compile(r"DISTRIB_CODENAME=(.*)")
        semicolonPattern = re.compile(r".*:(.*)")

        for line in ubuntutype.split('\n'):
            p = descPattern.search(line)
            if p:
                desc=p.group(1)
            p = codenamePattern.search(line)
            if p:
                codename=p.group(1)
        ubuntutype="%s (%s)" % (desc,codename)

        for result in rpm.split('\n'):
            om = self.objectMap()
            om.setProductKey, om.setDescription = result.split()[:2]

            # second field based on semi colon
            p = semicolonPattern.search(om.setDescription)
            if p:
                om.setDescription=p.group(1)

            om.setProductKey="%s %s" % (om.setProductKey,om.setDescription)
            om.setDescription=om.setProductKey
            #om.setInstallDate= "%s/%s/%s" % time.gmtime(float(om.setInstallDate))[:3]
            om.setProductKey = MultiArgs(str(om.setProductKey), str(ubuntutype))
            om.id = self.prepId(om.setProductKey)
            rm.append(om)
        return rm
