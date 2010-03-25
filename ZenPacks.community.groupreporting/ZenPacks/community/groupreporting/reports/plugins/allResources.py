import Globals

from Products.ZenReports import Utils

class allResources:
    def getCPUSpeed(self,device):
	clockspeed = 0
	for cpu in device.hw.cpus():
	    try:
		clockspeed += int(cpu.clockspeed)
	    except:
		pass
	return clockspeed

    def getDiskSpaceUsed(self,device):
	space = 0
	for fs in device.os.filesystems():
	    try:
		space += int(fs.cacheRRDValue('usedBlocks')) * int(fs.blockSize)
	    except:
		pass
	return space

    def getDiskSpaceTotal(self,device):
	space = 0
	for fs in device.os.filesystems():
	    try:
		space += int(fs.totalBytes())
	    except:
		pass
	return space

    def getMemory(self,device):
	mem = device.hw.totalMemory
	if mem is None or mem < 0:
	    mem = 0
	return mem

    def run(self, dmd, args):
        report = []
        for g in dmd.Groups.getSubOrganizers():
	    t_mem = 0
	    t_disk_used = 0
	    t_disk_total = 0
	    t_devices = 0
	    t_cpuspeed = 0
            for d in g.getSubDevices():
		t_mem += self.getMemory(d)
		t_disk_used += self.getDiskSpaceUsed(d)
		t_disk_total += self.getDiskSpaceTotal(d)
		t_devices += 1
		t_cpuspeed += self.getCPUSpeed(d)
	    t_disk_used = int(t_disk_used / 1024 / 1024 / 1024)
	    t_disk_total = int(t_disk_total / 1024 / 1024 / 1024)
	    t_mem = int(t_mem / 1024 / 1024)
	    report.append(
		Utils.Record(
		    group = g,
		    groupname = g.getOrganizerName(),
		    tmem = t_mem,
		    tdiskused = t_disk_used,
		    tdisktotal = t_disk_total,
		    tcpuspeed = t_cpuspeed,
		    tdevices = t_devices
		)
	    )
        return report

