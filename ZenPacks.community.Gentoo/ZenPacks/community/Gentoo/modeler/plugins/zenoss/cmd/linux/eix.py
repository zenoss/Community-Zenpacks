"""
Modeling plugin that parses the contents of eix to gather
information about the software installed on a gentoo linux box.
"""
import re
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class eix(CommandPlugin):
    """
    eix - get software list on gentoo machines
    """

    command = "/usr/bin/eix -c -I -n"
    compname = "os"
    relname = "software"
    modname = "Products.ZenModel.Software"

    #[I] xfce-extra/xfce4-mixer (4.4.3@03/31/09): Volume control application using gstreamer
    linePattern = re.compile(r"\[I\] (.*) \((.*)@([0-9]+)/([0-9]+)/([0-9]+)\): (.*)")

    def process(self, device, results, log):
        log.info('Collecting Software Installed information for device %s' % device.id)
        rm = self.relMap()

        for result in results.split('\n'):
            m = self.linePattern.match(result)
            if m:
                om = self.objectMap()
                om.setProductKey = MultiArgs("%s-%s" % (m.group(1),m.group(2)),"Gentoo")
                om.id = self.prepId(om.setProductKey)
                om.setInstallDate = "%s/%s/%s" % (str(2000+int(m.group(5))),m.group(3),m.group(4))
                om.setDescription = m.group(6)
                rm.append(om)
        return rm
        #[I] xfce-extra/xfce4-mixer (4.4.3@03/31/09): Volume control application using gstreamer
