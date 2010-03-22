
import pickle
import os
from subprocess import *
import Globals
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

class libvirtPlugin(PythonPlugin):

    modname = 'ZenPacks.community.libvirt.libvirtGuest'
    deviceProperties = ('zLibvirtUsername','zLibvirtConnectType','zLibvirtPassword')

    def collect(self, device, log):
	log.info('libvirt: %s' % device.id)
	filepath = __file__ # There has got to be a better way of finding this one out.... **HACK** perhaps through the device object?
	(pluginpath,tail) = os.path.split(filepath)
	(modelerpath,tail) = os.path.split(pluginpath)
	(libvirtpath,tail) = os.path.split(modelerpath)
	log.info('libvirt: libvirtpath = %s' % libvirtpath)
	pathtocheckscript = os.path.join(libvirtpath,'libexec','check_libvirt.py')
	log.info('libvirt: path to check_libvirt.py script = %s'  % pathtocheckscript)
        username = getattr(device, 'zLibvirtUsername', None)
        password = getattr(device, 'zLibvirtPassword', None)
        connecttype = getattr(device, 'zLibvirtConnectType', None)
	log.info('libvirt: username=' + username + ' connecttype=' + connecttype)
	command = pathtocheckscript
	args = ' -H ' + device.id + ' -c ' + connecttype + ' -u ' + username + ' -l modeler'
	if password != '' and connecttype == 'esx://':
	    args += ' -p ' + password
	#log.info('libvirt: command = "%s"' % command)
	#log.info('libvirt: args = "%s"' % args)
	output = Popen(command + args, stdout=PIPE, shell=True, env={"PATH": "/usr/bin"}).communicate()[0] # have to reset the environment or zenoss overrides python values....
	if output is None or output == '':
	    log.info('libvirt: Unable to connect or denied access?') # unable to connect or denied access --TODO-- need some more error checking
	    return None
	#log.info('libvirt: output = %s' % output)
	results = pickle.loads(output.rstrip('\n'))
	log.info('libvirt: results = '+' '.join(dir(results)))
	return results

    def process(self, device, results, log):
	log.info('libvirt: processing %s for device %s', self.name(), device.id)
	log.info("libvirt: Host results: %r", results)
	# ============ Guests =================
	relname = "libvirtguests" # we redefine this each time we call relMap()
	rmdomains = self.relMap()
	for id in results.keys():
            guest = results[id]
            log.info("libvirt: domain name=%s" % guest['name'])
	    info = dict()
	    info['lvDisplayName']=guest['name']
	    info['lvState']=guest['state']
            log.info("libvirt: lvState=%s" % info['lvState'])
	    info['lvOSType']=guest['ostype']
	    info['lvUUIDString']=guest['uuidstring']
	    info['lvMaxMemory']=guest['maxmemory']
	    info['lvNumberVirtCPUs']=guest['nrvirtcpus']
	    # --TODO - need to extract interfaces and disks for each guest as well...., but we are unable to add dynamic data points in Zenoss ......yet
	    om = self.objectMap(info)
	    om.id = self.prepId(om.lvDisplayName)
	    rmdomains.append(om)
	# ============ Pools =================
	relname = "libvirtpools" # we redefine this each time we call relMap()
	rmpools = self.relMap()
	for poolid in results['pools'].keys():
            log.info("libvirt: pool name=%s" % poolid)
	    pool = results['pools'][poolid]
	    info = dict()
	    info['lvDisplayName']=pool['name']
	    info['lvState']=pool['state']
	    info['lvCapacity']=pool['capacity']
	    info['lvVolumes']=pool['volumes']
	    om = self.objectMap(info)
	    om.id = self.prepId(om.lvDisplayName)
	    rmpools.append(om)
	# ============ Volumes =================
	relname = "libvirtvolumes" # we redefine this each time we call relMap()
	rmvolumes = self.relMap()
	for volid in results['volumes']:
            log.info("libvirt: volume name=%s" % volid)
	    volume = results['volumes'][volid]
	    info = dict()
	    info['lvDisplayName']=volume['name']
	    info['lvPath']=volume['path']
	    info['lvKey']=volume['key']
	    info['lvCapacity']=volume['capacity']
	    info['lvType']=volume['type']
	    info['lvPool']=volume['pool']
	    om = self.objectMap(info)
	    om.id = self.prepId(om.lvDisplayName)
	    rmpools.append(om)
	return [rmdomains,rmpools,rmvolumes]


