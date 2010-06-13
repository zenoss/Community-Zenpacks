#!/usr/bin/env python
import Globals
import sys
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from transaction import commit

dmd = ZenScriptBase(connect=True).dmd

cfile = sys.argv[1]

#parse file again

echo "Performing reindex"
echo 'reindex()' | zendmd

print cfile

        #build up a list of devices
        #if client == None:
        #if newdevices[om.cfcDeviceClass]:
        #newdevices[om.cfcDeviceClass] = (newdevices[om.cfcDeviceClass],om.cfcDisplayName)
        #else:
        #newdevices[om.cfcDeviceClass] = (om.cfcDisplayName)
        #${here/ZenPackManager/packs/ZenPacks.community.VMwareEsx/path}/libexec/vmware-esx.sh  ${dev/manageIp} ${dev/zSnmpCommunity} ${here/mount}
        #log.debug(newdevices)
        #client = self.dmd.getDmdRoot("Devices").findDevice(om.cfcDisplayName)
        #make sure the cfengine template is bound

