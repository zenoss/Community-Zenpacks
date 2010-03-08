
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class PuppetModeler(CommandPlugin):
    """
    Run puppetca on remote host to get list of managed hosts
    """
    relname = "puppetclients"
    modname = 'ZenPacks.community.puppet.PuppetClient'
    command = '/usr/sbin/puppetca --list --all'

    def process(self, device, results, log):
        log.info('Collecting puppet client list for device %s' % device.id)
        rm = self.relMap()
        rlines = results.split("\n")
        for line in rlines:
            om = self.objectMap()
            if line.startswith("+ "):
		om.pcSigned = 1
	    else:
		om.pcSigned = 0
	    om.pcDisplayName = line.lstrip("+ ")
            if om.pcDisplayName == '':
                continue
	    log.info('Collecting puppet client list for device %s: Found client = %s' % (device.id,om.pcDisplayName))
	    om.id = self.prepId(om.pcDisplayName)
	    rm.append(om)
        return [rm]

#root@ubuntu1:/var/lib/puppet# puppetca --list --all
#ubuntu4
#+ ubuntu1
#+ ubuntu2
#+ ubuntu3
#root@ubuntu1:/var/lib/puppet# puppetlast
#ubuntu1 checked in 2 minutes ago
#ubuntu2 checked in 2 minutes ago
#ubuntu3 checked in 2 minutes ago

# from puppetlist....
###  puts "#{node.name} #{node.expired? ? 'cached expired, ' : ''}checked in #{((Time.now - node.values[:_timestamp]) / 60).floor} minutes ago"



