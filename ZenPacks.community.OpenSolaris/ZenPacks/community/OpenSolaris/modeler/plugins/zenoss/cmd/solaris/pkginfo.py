"""
Modeling plugin that parses the contents of pkginfo to gather
information about the software installed on a gentoo linux box.
"""
import re
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class pkginfo(CommandPlugin):
    """
    pkginfo - get software list on solaris machines
    """

    command = "pkginfo -l"
    compname = "os"
    relname = "software"
    modname = "Products.ZenModel.Software"

    pkgPattern = re.compile(r".*PKGINST:\s+(.*)\n")
    verPattern = re.compile(r".*VERSION:\s+(.*)\n")
    versubPattern = re.compile(r"(.*),REV=(.*)")
    descPattern = re.compile(r".*DESC:\s+(.*)\n")

     #PKGINST:  BRCMbnx
     #NAME:  Broadcom NetXtreme II Gigabit Ethernet Adapter Driver
     #CATEGORY:  system
     # ARCH:  i386
     #VERSION:  11.11,REV=2008.10.30.20.37
     #VENDOR:  Broadcom Corporation, Inc.
     # DESC:  Broadcom NetXtreme II Gigabit Ethernet PCI-X/PCIE Adapter Driver
     #HOTLINE:  Please contact your local service provider
     #STATUS:  completely installed


    def process(self, device, results, log):
        log.info('Collecting Software Installed information for device %s' % device.id)
        rm = self.relMap()

        for result in results.split('\n\n'):
            p = self.pkgPattern.search(result)
            v = self.verPattern.search(result)
            d = self.descPattern.search(result)
            if p and v and d:
                om = self.objectMap()
                vs = self.versubPattern.search(v.group(1))
                if vs:
                    om.setProductKey=MultiArgs("%s-%s_%s" % (p.group(1),vs.group(1),vs.group(2)),"OpenSolaris")
                    om.id = self.prepId("%s-%s_%s" % (p.group(1),vs.group(1),vs.group(2)))
                    om.setDescription = d.group(1)
                    rm.append(om)
                    p=v=d=None
        return rm
