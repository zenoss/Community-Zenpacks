################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################
from ZenPacks.community.WMIDataSource.WMIPlugin import WMIPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class Hyperv(WMIPlugin):

    maptype = "hypervVMMap"
    relname = "HypervVM"
    modname = "ZenPacks.Hyper.virtualMachines.HypervVM"
   
    tables = {
            "MSVM_ComputerSystem":
                (
		"MSVM_ComputerSystem",
                None,
                "root/Virtualization",
                    {
                    'ElementName':'vmDisplayName',
                    'Name':'vmVMID',
		    'EnabledState':'vmState',
                    },
		),
            "MSVM_Memory":
                (
		"select NumberOfBlocks,SystemName from MSVM_Memory",
                None,
                "root/Virtualization",
                    {
 		    'NumberOfBlocks':'vmMemory',
		    'SystemName':'InstanceId',
                    },
		),
             }


    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
	rm = self.relMap()
	cs = results['MSVM_ComputerSystem']
	if cs:
	   for instance in cs:
	      try:
		 om = self.objectMap(instance)
		 if om.vmDisplayName != om.vmVMID:
		    om.id = self.prepId(om.vmDisplayName)
		    om.snmpindex = om.vmVMID
		    if om.vmState == 0: om.vmState='unknown'
		    if om.vmState == 2: om.vmState='Enabled'
		    if om.vmState == 3: om.vmState='Disabled'
		    if om.vmState == 32768: om.vmState='Paused'
		    if om.vmState == 32769: om.vmState='Suspended'
		    if om.vmState == 32770: om.vmState='Starting'
		    if om.vmState == 32771: om.vmState='Snapshotting'
		    if om.vmState == 32773: om.vmState='Saving'
		    if om.vmState == 32774: om.vmState='Stopping'
		    if om.vmState == 32776: om.vmState='Pausing'
		    if om.vmState == 32777: om.vmState='Resuming'
		    rm.append(om)
		    mem = results['MSVM_Memory']
		    if not mem: return
		    for resultat in mem:
		       try:
			  log.info('Result of MSVM_Memory : %s',resultat) 
		          memoire = self.objectMap(resultat)
	                  if om.vmVMID == memoire.InstanceId:
			     om.vmMemory = memoire.vmMemory
		       except: continue
              except: continue
	   log.info('End of Processing rm Values %s',rm)
	   return [rm]
