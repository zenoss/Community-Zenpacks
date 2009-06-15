__doc__="""Maps the system name to OS version etc"""

import re

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class AIXBase(SnmpPlugin):
    maptype = "AIXBase"
    relname = "aixbase"
    modname = "ZenPacks.community.AIX.AIXBase"

    columns = {
             '.1.3.6.1.4.1.2.6.191.1.3.6.0' : 'setHWProductKey', # aixSeMachineType
             '.1.3.6.1.4.1.2.6.191.1.3.7.0' : 'setHWSerialNumber', # aixSeSerialNumber
             '.1.3.6.1.2.1.1.1.0' : 'snmpDescr',
             }

    snmpGetMap = GetMap(columns)

    osregex = (
        # Regular AIX
        # IBM PowerPC CHRP Computer Machine Type: 0x0800004c Processor id: 000DA981D900 Base Operating System Runtime AIX version: 05.03.0000.0060 TCP/IP Client Support version: 05.03.0000.0063
        re.compile(r'(AIX version: .*) TCP'),

        # AIX Virtual IO (VIO) Server
        # IBM PowerPC CHRP Computer Machine Type: 0x0800004c Processor id: 000DA981D900 Base Operating System Runtime VIOS version: 05.03.0007.0000 TCP/IP Client Support  version: 05.03.0007.0000
        re.compile(r'(VIOS version: .*) TCP'),
    )


    def process(self, device, results, log):
        """Gather data from the standard AIX snmpd + friends"""

        log.info( 'processing %s for AIX device %s', self.name(), device.id)

        getdata, tabledata = results

        if not self.checkColumns(getdata, self.columns, log):
           log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
           log.warn( "Data= %s", getdata )
           log.warn( "Columns= %s", self.columns )
           return

        om = self.objectMap(getdata)
        if not om:
           log.warn( 'Unable to map getdata into something sane using response from %s for the %s plugin', device.id, self.name() )
           return

        om.setHWProductKey= om.setHWProductKey.replace( "IBM,", "" )
        log.debug( "setHWProductKey=%s", om.setHWProductKey)
        om.setHWProductKey=MultiArgs(om.setHWProductKey,"IBM")
        om.setHWSerialNumber= om.setHWSerialNumber.replace( "IBM,", "" )
        log.debug( "setHWSerialNumber=%s", om.setHWSerialNumber)

        log.debug( "snmpDescr=%s", om.snmpDescr)

        #
        # Map the AIX info to match AIX or VIO strings
        #
        om.setOSProductKey= "AIX"
        if om.snmpDescr:
            descr = re.sub( "\s", " ", om.snmpDescr)
            for regex in self.osregex:
                m = regex.search(descr)
                if m: 
                    om.setOSProductKey = " ".join(m.groups())
                    break
        log.debug( "setOSProductKey=%s", om.setOSProductKey)

        om.setOSProductKey=MultiArgs(om.setOSProductKey,"IBM")
        return om
