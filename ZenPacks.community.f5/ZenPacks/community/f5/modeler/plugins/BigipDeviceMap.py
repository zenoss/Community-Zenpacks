"""
Gather F5 BIG-IP hardware model + serial number and other hardware information

@author: David Petzel
@contact: david.petzel@disney.com
@date: 05/06/2011

"""

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class BigipDeviceMap(SnmpPlugin):
    """
    Collects the basic hardware information about the Bigip
    """
    
    modname = "ZenPacks.community.f5.BigipLtm"
    
    snmpGetMap = GetMap({ 
        #'.1.3.6.1.4.1.674.10892.1.300.10.1.8' : 'manufacturer',
        '.1.3.6.1.4.1.3375.2.1.3.3.1.0' : 'sysGeneralHwName',
        '.1.3.6.1.4.1.3375.2.1.3.3.2.0' : 'setHWProductKey',
        '.1.3.6.1.4.1.3375.2.1.3.3.3.0' : 'setHWSerialNumber',
        #'.1.3.6.1.4.1.674.10892.1.400.10.1.6.1': 'setOSProductKey',
        # Collect some info to build the setOSProductKey string later
        '.1.3.6.1.4.1.3375.2.1.4.1.0': 'sysProductName',
        '.1.3.6.1.4.1.3375.2.1.4.2.0': 'sysProductVersion',
        '.1.3.6.1.4.1.3375.2.1.4.3.0': 'sysProductBuild',
        '.1.3.6.1.4.1.3375.2.1.4.4.0': 'sysProductEdition',
         })
      
    def process(self, device, results, log):
        """collect snmp information from this device"""
        manufacturer_name = "F5 Labs, Inc."
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        #if getdata['setHWProductKey'] is None: return None
        om = self.objectMap(getdata)
        # Build a product build and version string to populate the OSModel field
        # Also set the manufacturer_name
        os_model = " ".join([om.sysProductName, om.sysProductVersion, om.sysProductBuild, om.sysProductEdition])
        om.setOSProductKey = MultiArgs(os_model, manufacturer_name)
        
        #To make things more fun, there is an issue on Viprions.
        #http://support.f5.com/kb/en-us/solutions/public/10000/600/sol10635.html
        #http://support.f5.com/kb/en-us/solutions/public/11000/400/sol11441.html
        # This results in om.sysProductName coming back as unknown....
        # Lets try to work around that
        if om.setHWProductKey == "unknown":
            viprion_marketing_names = ['A100', 'A107']
            if om.sysGeneralHwName in viprion_marketing_names:
                hw_model = "VIPRION"
            pass
        else:
        # By default the HWProductKey is very generic, ie '3400'. Lets prepend an identifier
        # so it aligns with the table in sol10635
            hw_model = " ".join([om.sysProductName, om.setHWProductKey])
            
        # Now set it. I'm not entirely up to speed on this method, 
        # But in testing the multiargs stuff will populate two fields in the GUI
        om.setHWProductKey = MultiArgs(hw_model, manufacturer_name)
        return om
