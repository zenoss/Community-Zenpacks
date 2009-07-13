import re

from ZenPacks.community.OpenSolaris.modeler.plugins.zenoss.cmd.solaris.SolarisCommandPlugin \
     import SolarisCommandPlugin

class ifconfig(SolarisCommandPlugin):
    """
    ifconfig maps a solaris ifconfig command to the interfaces relation.
    """
    # echo __COMMAND__ is used to delimit the results
    command = '/sbin/ifconfig -a && echo __COMMAND__ && /usr/sbin/dladm show-ether && echo __COMMAND__ && /usr/sbin/arp -a'
    compname = "os"
    relname = "interfaces"
    modname = "Products.ZenModel.IpInterface"

    ifstart = re.compile(r"^(\w+):\s.*<(.*)>\smtu\s(\d+)\s.*")
    v4addr = re.compile(r"inet\s(\S+)\snetmask\s(\S+)\sbroadcast\s(\S+)")

    def process(self, device, results, log):
        log.info('Collecting interfaces for device %s' % device.id)
        ifconfig, dladm, arp = results.split('__COMMAND__\n')
        relMap = self.parseIfconfig(ifconfig, arp, dladm, self.relMap())
        return relMap

    def parsearp(self, arpstring):
        """
        Parse the output of the arp command.
        """
        results={}

        # Strip the header off
        arpdata=arpstring.split('-\n')[1]
        for arpline in arpdata.split('\n'):
            arpcolumns=arpline.split()
            #e1000g0 192.168.31.133       255.255.255.255 SPLA     00:0c:29:22:94:aa
            if len(arpcolumns) == 5:
                results[ "%s_%s" % ( arpcolumns[0], arpcolumns[1] ) ]= arpcolumns[4]
        return results

    def parsedladm(self, dladmstring):
        """
        Parse the output of the dladm command.
        """
        results={}
        SPEED_CONVERSION= {
            '1G':  1000000000,
            '100M': 100000000,
            '10M': 10000000
           }

        dladmdata=dladmstring.split('PAUSE\n')[1]
        for dladmline in dladmdata.split('\n'):
            dladmcolumns=dladmline.split()
            if len(dladmcolumns) == 6:
                speed, duplex = dladmcolumns[4].split('-')
                speed=SPEED_CONVERSION.get(speed,100000000)
                results[ dladmcolumns[0] ]= (speed,duplex)
        return results

    def parseIfconfig(self, ifconfig, arpstring,dladmstring, relMap):
        """
        Parse the output of the ifconfig -a command.
        """

        # Parse arp data
        arpdict=self.parsearp(arpstring)

        # Parse dladm data
        dladmdict=self.parsedladm(dladmstring)
        rlines = ifconfig.splitlines()
        iface = None
        for line in rlines:
            # reset state to no interface
            if not line.strip():
                iface = None

            # new interface starting
            miface = self.ifstart.search(line)
            if miface:
                # start new interface and get name, type, and macaddress
                iface = self.objectMap()
                if miface.lastindex == 3:
                    name, flags, mtu=miface.groups()[:3]
                iface.interfaceName = name
                iface.id = self.prepId(name)
                iface.mtu = int(mtu)
                flag = flags.split(',')
                if "RUNNING" in flag: iface.adminStatus = 1
                else:  iface.adminStatus = 2
                if "UP" in flag: iface.operStatus = 1
                else:  iface.operStatus = 2
                if "IPv4" in flag: relMap.append(iface)
                continue

            # get the ip address of an interface
            maddr = self.v4addr.search(line)
            if maddr and iface:
                itype = "ethernetCsmacd"
                # get ip and netmask
                ip, netmask, broadcast= maddr.groups()
                netmask = self.hexToBits("%s%s" % ('0x',netmask))
                #netmask = self.maskToBits(netmask)
                iface.setIpAddresses = ["%s/%s" % (ip, netmask)]
                iface.macaddress=arpdict[ "%s_%s" % ( iface.interfaceName,ip ) ]
                iface.speed=dladmdict[ iface.interfaceName][0]
                iface.duplex=dladmdict[ iface.interfaceName][1]

        print relMap
        return relMap

