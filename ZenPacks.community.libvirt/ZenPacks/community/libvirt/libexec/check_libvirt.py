#!/usr/bin/python -E
# have to unset PYTHONHOME and PYTHONPATH to avoid getting the zenoss python tree....

"""libvirt based statistics fetcher

This script is used for obtaining information from libvirt based virtualization
servers and exporting them in a NAGIOS/Zenoss compatible style format.

"""

__version__ = "0.2"


import libvirt
import getopt
import sys
import pickle
# --TODO-- work around for cross python version differences in elementtree
try:
    from xml.etree import ElementTree
    mypythonversion = '2.6'
except ImportError:
    from elementtree.ElementTree import ElementTree
    from elementtree.ElementTree import fromstring
    mypythonversion = '2.4'


args = sys.argv[1:]
shortopt='c:l:u:p:H:d:i:n:g:s:hvr'
longopts=['help']
connecttype = 'qemu+ssh://'
socket = '/var/run/libvirt/libvirt-sock-ro'
username = 'zenoss'
password = ''
hostname = 'localhost'
datatype = 'list'
domain = -1
domainname = ''
poolname = ''
volumepath = ''
disk = ''
interface = ''
verbose = 0
humanreadable = 0
version = 0
remoteversion = 0


def help(status=0):
    print "check_libvirt.py [-u username] [-c connecttype] [-H hostname] [-l datatype] [-h] [-v]"
    print "-c connecttype   (see the libvirt docs for more info about connecturi format)"
    print "-r		    print in human readable format instead of default NAGIOS format"
    print "-l dataorcmdtype type of data to lookup or command to run"
    print "                   data = (list, domain, interface, interfacelist, disk, disklist, memory, cpu, all, modeler)"
    print "                   commands = (save, resume, destroy, create, undefine, startup, shutdown, autostart)"
    print "-n nameofdp      The value of the datapoint we need to lookup (this could be the domain, volumepath, pool ,etc.)"
    print "-s socket        path to the readonly libvirt socket on the remote host"
    print "-g domain ID#    the ID number of the domain to query" # can be used in place of -n
    print "-d disk-device   the device name of the disk to gets stats for (e.g. vda, hda, .etc.)"
    print "-i net-interface the interface name to get stats for (e.g. vnet1, vnet2, etc.)"
    print "-u username	    username to connect as to the remote libvirt host (or to ESX)"
    print "-p password      password to use to connect to remote host (used for ESX)"
    print "-H hostname	    hostname of the remote libvirt host"
    print "-v		    enable verbose mode"
    sys.exit(status)

"""
Print data in either humanly readable or NAGIOS format (the default)
"""
def print_data(data):
    if humanreadable:
	print "\n".join([str(x)+'='+str(data[x]) for x in data.keys()])
    else:
	print '|'+' '.join([str(x)+'='+str(data[x]) for x in data.keys()])

def get_disk_devices(dom):
    if mypythonversion == '2.6':
        etree=ElementTree.fromstring(dom.XMLDesc(0))
    else:
        etree=fromstring(dom.XMLDesc(0))
    devs=[]
    for target in etree.findall("devices/disk/target"):
	dev=target.get("dev")
	if not dev in devs:
	    devs.append(dev)
    return devs

def get_interface_devices(dom):
    if mypythonversion == '2.6':
        etree=ElementTree.fromstring(dom.XMLDesc(0))
    else:
        etree=fromstring(dom.XMLDesc(0))
    devs=[]
    for target in etree.findall("devices/interface/target"):
	dev=target.get("dev")
	if not dev in devs:
	    devs.append(dev)
    return devs

def get_data_domain(conn,domain,domainname):
    """Get data specific to this domain
       --TODO-- I am totaling up the interface and disk totals since I don't have dynamic datapoint support in the zenoss modeler plugin yet....
    """
    data = dict()
    dom = get_dom_handle(conn,domain,domainname)
    if dom is None:
	print_data(data)
	return
    info = dom.info()
    data['ostype']=dom.OSType()
    data['uuidstring']=dom.UUIDString()
    data['state']=info[0]
    data['maxmemory']=info[1]
    data['memory']=info[2]
    data['nrvirtcpu']=info[3]
    data['cputime']=info[4]
    if connecttype != 'esx://': # not supported for disk stats yet
	data['autostart']=dom.autostart()
    if version >= 7005 and remoteversion >= 7005 and connecttype != 'esx://':
	mem_stats=dom.memoryStats()
	if mem_stats is not None:
	    for stat in mem_stats.keys():
		data['mem_' + stat] = mem_stats[stat]
    ifdevs = get_interface_devices(dom)
    dps = ('rxbytes','rxpackets','rxerrs','rxdrops','txbytes','txpackets','txerrs','txdrops')
    for dp in dps:
	data['if_total_' + dp] = 0
    for ifdev in ifdevs:
	if data['state'] == 1:
	    if_stats=dom.interfaceStats(ifdev)
	i = 0
	for dp in dps:
	    if data['state'] == 1:
		data['if_' + ifdev + '_' + dp] = if_stats[i]
		data['if_total_' + dp] += if_stats[i]
	    else:
		data['if_' + ifdev + '_' + dp] = 0
	    i += 1
    diskdevs = get_disk_devices(dom)
    dps = ('readrequests','readbytes','writerequests','writebytes')
    for dp in dps:
	data['disk_total_' + dp]=0
    for disk in diskdevs:
	if connecttype != 'esx://': # block stats is not supported for esx yet
	    if data['state'] == 1:
		    disk_stats=dom.blockStats(disk)
	    i = 0
	    for dp in dps:
		if data['state'] == 1:
		    data['disk_' + disk + '_' + dp]=disk_stats[i]
		    data['disk_total_' + dp]+=disk_stats[i]
		else:
		    data['disk_' + disk + '_' + dp]=0
		i += 1
    print_data(data)

def get_dom_handle(conn,domain,domainname):
    dom = None
    try:
	if domain > 0:
	    dom=conn.lookupByID(domain)
	else:
	    dom=conn.lookupByName(domainname)
    except:
	return None
    return dom


def set_destroy(conn,domain,domainname):
    """Set the domain to destroy"""
    dom = get_dom_handle(conn,domain,domainname)
    dom.autostart()

def set_autostart(conn,domain,domainname):
    """Set the domain to autostart"""
    dom = get_dom_handle(conn,domain,domainname)
    dom.autostart()

def set_save(conn,domain,domainname):
    """Set the domain to save"""
    dom = get_dom_handle(conn,domain,domainname)
    dom.save()

def set_resume(conn,domain,domainname):
    """Set the domain to resume"""
    dom = get_dom_handle(conn,domain,domainname)
    dom.resume()

def set_reboot(conn,domain,domainname):
    """Set the domain to reboot"""
    dom = get_dom_handle(conn,domain,domainname)
    dom.reboot()

def set_shutdown(conn,domain,domainname):
    """Set the domain to shutdown"""
    dom = get_dom_handle(conn,domain,domainname)
    dom.shutdown()

def set_suspend(conn,domain,domainname):
    """Set the domain to suspend"""
    dom = get_dom_handle(conn,domain,domainname)
    dom.suspend()

def set_undefine(conn,domain,domainname):
    """Set the domain to undefine"""
    dom = get_dom_handle(conn,domain,domainname)
    dom.undefine()

def set_create(conn,domain,domainname):
    """Set the domain to create"""
    dom = get_dom_handle(conn,domain,domainname)
    dom.create()

def get_data_disklist(conn,domain,domainname):
    """Get a list of disks for this domain"""
    data = dict()
    dom = get_dom_handle(conn,domain,domainname)
    if dom is None:
	print_data(data)
	return
    for dev in get_disk_devices(dom):
	data[dev] = dev
    print_data(data)
	

def get_data_disk(conn,domain,domainname,disk):
    """
     Get disk stats about an individual disk
      domain will be a number returned by get_data_list
      disk will be something like vda, hda, etc...
    """
    data = dict()
    dom = get_dom_handle(conn,domain,domainname)
    if dom is None:
	print_data(data)
	return
    disk_stats=dom.blockStats(disk)
    data['readrequests']=disk_stats[0]
    data['readbytes']=disk_stats[1]
    data['writerequests']=disk_stats[2]
    data['writebytes']=disk_stats[3]
    print_data(data)

def get_data_cpu(conn,domain,domainname):
    """Get detailed data on virtual CPUs"""
    data = dict()
    dom = get_dom_handle(conn,domain,domainname)
    if dom is None:
	print_data(data)
	return
    data['vcpus']=dom.vcpus()
    print_data(data)

def get_data_interface(conn,domain,domainname,interface):
    """Get stats on this interface for this domain"""
    data = dict()
    dom = get_dom_handle(conn,domain,domainname)
    if dom is None:
	print_data(data)
	return
    if_stats=dom.interfaceStats(interface)
    data['rxbytes'] = if_stats[0]
    data['rxpackets'] = if_stats[1]
    data['rxerrs'] = if_stats[2]
    data['rxdrops'] = if_stats[3]
    data['txbytes'] = if_stats[4]
    data['txpackets'] = if_stats[5]
    data['txerrs'] = if_stats[6]
    data['txdrops'] = if_stats[7]
    print_data(data)

def get_data_interfacelist(conn,domain,domainname):
    """List all interfaces on this domain"""
    data = dict()
    dom = get_dom_handle(conn,domain,domainname)
    if dom is None:
	print_data(data)
	return
    for dev in get_interface_devices(dom):
	data[dev] = dev
    print_data(data)

def get_data_list(conn):
    """List all domains on this host"""
    data = dict()
    for id in conn.listDomainsID():
	dom=conn.lookupByID(id)
	data[id]=dom.name()
    print_data(data)

def get_data_pool(conn,poolname):
    """Get data specific to a particular pool using the pool name to look it up"""
    pooldata = dict()
    pool = conn.storagePoolLookupByName(poolname)
    poolinfo = pool.info()
    [state,capacity,allocation,available] = poolinfo
    pooldata['allocation'] = capacity
    print_data(pooldata)

def get_data_volume(conn,volumepath):
    voldata = dict()
    volume = conn.storageVolLookupByPath(volumepath)
    volinfo = volume.info()
    [type,capacity,allocation] = volinfo
    voldata['allocation'] = allocation
    print_data(voldata)

def get_data_modeler(conn):
    """List all domains/pool/volumes on this host and spit it out in a pickle format for use by the modeling plugin later """
    poolstates = ['Inactive','Building','Running','Degraded']
    volumetypes = ['File','Block']
    data = dict()
    domains = dict()
    for name in conn.listDefinedDomains():
	dom=conn.lookupByName(name)
	domains[name]=dict()
	domains[name]['name'] = dom.name()
	domains[name]['ostype'] = dom.OSType()
	domains[name]['uuidstring'] = dom.UUIDString()
	domains[name]['maxmemory'] = dom.maxMemory()
	#data[name]['vcpus'] = dom.vcpus()
	info = dom.info()
	domains[name]['state'] = info[0]
	domains[name]['nrvirtcpus'] = info[3]
	domains[name]['disks'] = get_disk_devices(dom)
	domains[name]['interfaces'] = get_interface_devices(dom)
    for id in conn.listDomainsID():
	dom=conn.lookupByID(id)
	domains[id]=dict()
	domains[id]['name'] = dom.name()
	domains[id]['ostype'] = dom.OSType()
	domains[id]['uuidstring'] = dom.UUIDString()
	domains[id]['maxmemory'] = dom.maxMemory()
	#data[id]['vcpus'] = dom.vcpus()
	info = dom.info()
	domains[id]['state'] = info[0]
	domains[id]['nrvirtcpus'] = info[3]
	domains[id]['disks'] = get_disk_devices(dom)
	domains[id]['interfaces'] = get_interface_devices(dom)
    data['domains'] = domains
    pools = dict()
    volumes = dict()
    poolnames = []
    if connecttype != 'esx://': # Not working for ESX as of libvirt version 0.7.5
	for name in conn.listStoragePools():
	    poolnames += [name]
	for name in conn.listDefinedStoragePools():
	    poolnames += [name]
    for name in poolnames:
	pooldata = dict()
	pool = conn.storagePoolLookupByName(name)
	poolinfo = pool.info()
	[state,capacity,allocation,available] = poolinfo
	if verbose:
	    print "Pool:",poolstates[state],capacity,allocation,available,name
	pooldata['state'] = poolstates[state]
	pooldata['capacity'] = capacity
	# we don't assign allocation here, since we do it in RRD instead.
	pooldata['name'] = name
	pooldata['volumes'] = []
	if state: # Make sure the pool is active
	    for volumepath in pool.listVolumes():
		voldata = dict()
		volume = pool.storageVolLookupByName(volumepath)
		volinfo = volume.info()
		[type,capacity,allocation] = volinfo
		if verbose:
		    print "Volume: ",volumetypes[type],capacity,allocation,volume.name(),volume.key(),volume.path()
		voldata['type'] = volumetypes[type]
		voldata['capacity'] = capacity
		voldata['name'] = volume.name()
		voldata['key'] = volume.key()
		voldata['path'] = volume.path()
		voldata['pool'] = pooldata['name']
		# we don't assign allocation here, since we do it in RRD instead....
		volumes[volume.key()] = voldata
		pooldata['volumes'] += [volume.key()]
	pools[name] = pooldata
    data['pools'] = pools
    data['volumes'] = volumes
    if humanreadable:
	print data
    else:
	print pickle.dumps(data)


def request_credentials(credentials, user_data):
    for credential in credentials:
	if credential[0] == libvirt.VIR_CRED_AUTHNAME:
	    credential[4] = user_data[0]
	    if len(credential[4]) == 0:
		credential[4] = credential[3]
	elif credential[0] == libvirt.VIR_CRED_NOECHOPROMPT:
	    credential[4] = user_data[1]
	else:
	    return -1
	return 0


def get_data_all(conn):
    """Print all data for all domains"""
    print 'Listing running domains'
    for id in conn.listDomainsID():
	dom=conn.lookupByID(id)
	print dom.name()# ,dom.blockStats()
	print "\tid:", id
	print "\tostype:", dom.OSType()
	print "\tuuidstring:", dom.UUIDString()
	print "\tmaxmemory:", dom.maxMemory()
	print "\tvcpus:", dom.vcpus()
	info = dom.info()
	state = info[0]
	maxMem = info[1]
	memory = info[2]
	nrVirtCpu = info[3]
	cpuTime = info[4]
	print "\tinfo:", "state:",state,"maxMem:", maxMem,"memory:", memory,"nrVirtCpu:", nrVirtCpu,"cpuTime:", cpuTime
	#print "\tschedulerParameters:", dom.schedulerParameters()
	#print "\tschedulerType:", dom.schedulerType() # ?
	# print dom.XMLDesc, # details of domain config in XML format
	for dev in get_disk_devices(dom):
	    print "\tdiskdev: ",dev
	    disk_stats=dom.blockStats(dev)
	    print "\tdiskstats:","rr:",disk_stats[0],"rB:",disk_stats[1],"wr:",disk_stats[2],"wB:",disk_stats[3]
	    # disk_stats[0] = Read Requests
	    # disk_stats[1] = Read Bytes
	    # disk_stats[2] = Write Requests
	    # disk_stats[3] = Written Bytes
	for dev in get_interface_devices(dom):
	    interface_stats=dom.interfaceStats(dev)
	    rx_bytes = interface_stats[0]
	    rx_packets = interface_stats[1]
	    rx_errs = interface_stats[2]
	    rx_drop = interface_stats[3]
	    tx_bytes = interface_stats[4]
	    tx_packets = interface_stats[5]
	    tx_errs = interface_stats[6]
	    tx_drop = interface_stats[7]
	    print "\trx_ifstats:","rx_bytes: ",rx_bytes,"rx_packets:", rx_packets,"rx_errs:", rx_errs,"rx_drop:", rx_drop
	    print "\ttx_ifstats:","tx_bytes: ",tx_bytes,"tx_packets:", tx_packets,"tx_errs:", tx_errs,"tx_drop:", tx_drop
	# dom.memoryStats only exists in libvirt as of version 0.7.5 ....

    print 'Listing defined domains'
    for id in conn.listDefinedDomains():
	dom=conn.lookupByName(id)
	print dir(dom)

if __name__=='__main__':
    opts, args = getopt.getopt(args,shortopt,longopts)
    for opt in opts:
	if opt[0] == "-h":
	    help()
	elif opt[0] == "-H":
	    hostname = opt[1]
	elif opt[0] == "-u":
	    username = opt[1]
	elif opt[0] == "-p":
	    password = opt[1]
	elif opt[0] == "-c":
	    connecttype = opt[1]
	elif opt[0] == "-l":
	    datatype = opt[1]
	elif opt[0] == "-g":
	    domain = int(opt[1])
	elif opt[0] == "-n":
	    # We don't know which it will be, so just set them all:
	    domainname = opt[1]
	    volumepath = opt[1]
	    poolname = opt[1]
        elif opt[0] == "-2":
            socket = opt[1]
	elif opt[0] == "-i":
	    interface = opt[1]
	elif opt[0] == "-d":
	    disk = opt[1]
	elif opt[0] == "-v":
	    verbose = 1
	elif opt[0] == "-r":
	    humanreadable = 1

    version = libvirt.getVersion() # needed to know what features we support

    #conn=libvirt.openReadOnly('qemu+ssh://test8virt3/')
    #conn=libvirt.openReadOnly('remote://test8virt3/')
    #conn=libvirt.openReadOnly('qemu://test8virt3/system')
    
    # See: http://libvirt.org/uri.html
    # And: http://libvirt.org/remote.html
    if connecttype == 'qemu+ssh://':
	conn=libvirt.openReadOnly(connecttype+username+'@'+hostname+'/system'+'?socket='+socket)
    elif connecttype == 'qemu://': # untested
	conn=libvirt.openReadOnly(connecttype+hostname+'/system'+'?socket='+socket)
    elif connecttype == 'esx://': # partially implemented. (not all stats work)
	if version < 7000:
	    print "The ESX connect type only works correctly in libvirt 0.7.0 and newer with ESX compiled in"
	    help(1)
	auth = [[libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_NOECHOPROMPT], request_credentials, [username,password]]
	uri = connecttype+hostname+'/?no_verify=1'
	conn=libvirt.openAuth(uri, auth, 0)
    elif connecttype == 'xen://': # untested
	conn=libvirt.openReadOnly(connecttype+hostname)
    elif connecttype == 'xen+ssh://': # untested
	conn=libvirt.openReadOnly(connecttype+username+'@'+hostname+'/?socket='+socket)
    elif connecttype == 'openvz://': # untested
	conn=libvirt.openReadOnly(connecttype+hostname)
    elif connecttype == 'opennebula://': # untested
	conn=libvirt.openReadOnly(connecttype+hostname)
    elif connecttype == 'vbox://': # untested
	conn=libvirt.openReadOnly(connecttype+hostname)
    elif connecttype == 'uml://': # untested
	conn=libvirt.openReadOnly(connecttype+hostname)
    elif connecttype == 'lxc://': # untested
	conn=libvirt.openReadOnly(connecttype+hostname)
    else:
	print "Unsupported libvirt connect type:",connecttype
	help(1)

    if version >= 7005:
	remoteversion = conn.getLibVersion()

    if datatype == 'list':
	get_data_list(conn)
    elif datatype == 'modeler': # used for passing information to the zenoss modeler plugin.....
	get_data_modeler(conn)
    elif datatype == 'all':
	get_data_all(conn)
    elif datatype == 'disk':
	get_data_disk(conn,domain,domainname,disk)
    elif datatype == 'disklist':
	get_data_disklist(conn,domain,domainname)
    elif datatype == 'cpu':
	get_data_cpu(conn,domain,domainname)
    elif datatype == 'domain':
	get_data_domain(conn,domain,domainname)
    elif datatype == 'interface':
	get_data_interface(conn,domain,domainname,interface)
    elif datatype == 'interfacelist':
	get_data_interfacelist(conn,domain,domainname)
    elif datatype == 'volume':
	get_data_volume(conn,volumepath)
    elif datatype == 'pool':
	get_data_pool(conn,poolname)
    elif datatype == 'shutdown':
	set_shutdown(conn,domain,domainname)
    elif datatype == 'startup':
	set_startup(conn,domain,domainname)
    elif datatype == 'autostart':
	set_autostart(conn,domain,domainname)
    elif datatype == 'undefine':
	set_undefine(conn,domain,domainname)
    elif datatype == 'create':
	set_create(conn,domain,domainname)
    elif datatype == 'resume':
	set_resume(conn,domain,domainname)
    elif datatype == 'save':
	set_save(conn,domain,domainname)
    elif datatype == 'destroy':
	set_destroy(conn,domain,domainname)
    else:
	print "Unrecognized datatype:",datatype
	help(1)


