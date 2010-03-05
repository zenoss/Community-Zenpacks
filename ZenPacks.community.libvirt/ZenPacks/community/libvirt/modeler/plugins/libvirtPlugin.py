
import pickle
import os
from sets import Set
from subprocess import *
import Globals
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

class libvirtPlugin(PythonPlugin):

    relname = "libvirtguests"
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
	#username = device.zLibvirtUsername # doesn't work
	#connecttype = device.zLibvirtConnectType # doesn't work
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
	    return None # unable to connect or denied access --TODO-- need some more error checking
	#log.info('libvirt: output = %s' % output)
	results = pickle.loads(output.rstrip('\n'))
	log.info('libvirt: results = '+' '.join(dir(results)))
	return results

    def process(self, device, results, log):
	log.info('libvirt: processing %s for device %s', self.name(), device.id)
	log.info("libvirt: Host results: %r", results)
	rm = self.relMap()
#	guestset = Set(device.libvirtguests)
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
	    # --TODO - need to extract interfaces and disks for each guest as well....
	    om = self.objectMap(info)
	    om.id = self.prepId(om.lvDisplayName)
#	    guestset.discard(om.id)
	    rm.append(om)
#	for id in guestset:
#	    om = selfObjectMap()
#	    om.id = id
#	    rm.append(id)
	return [rm]

