################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPFanMap

HPFanMap maps the cpqHeFltTolFanTable table to fab objects

$Id: HPFanMap.py,v 1.2 2010/06/30 21:25:39 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]


from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class HPFanMap(SnmpPlugin):
    """Map HP/Compaq insight manager Fans table to model."""

    maptype = "HPFanMap"
    modname = "ZenPacks.community.HPMon.HPFan"
    relname = "fans"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('cpqHeFltTolFanTable',
                    '.1.3.6.1.4.1.232.6.2.6.7.1',
                    {
                        '.3': '_locale',
                        '.4': '_present',
                        '.5': 'type',
                        '.9': 'status',
                        '.12': '_rpm',
                    }
        ),
    )


    typemap = {1: 'other', 
                2: 'Tach Output',
                3: 'Spin Detect',
                }

    localemap = {1: 'other', 
                2: 'unknown',
                3: 'system',
                4: 'systemBoard',
                5: 'ioBoard',
                6: 'cpu',
                7: 'memory',
                8: 'storage',
                9: 'removableMedia',
                10: 'powerSupply',
                11: 'ambient',
                12: 'chassis',
                13: 'bridgeCard',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        fantable = tabledata.get('cpqHeFltTolFanTable')
        localecounter = {}
        for oid, fan in fantable.iteritems():
            try:
                om = self.objectMap(fan)
                if om._present < 3: continue
                if not hasattr(om, '_rpm'):
                    om.modname = "ZenPacks.community.HPMon.HPsdFan"
                om.snmpindex = oid.strip('.')
                om.type = self.typemap.get(getattr(om,'type',1),self.typemap[1])
                if om._locale in localecounter:
                    localecounter[om._locale] = localecounter[om._locale] + 1
                else:
                    localecounter[om._locale] = 1
                om.id = self.prepId("%s%d" % (self.localemap.get(
                                            getattr(om, '_locale', 1),
                                            self.localemap[1]),
                                            localecounter[om._locale]))
            except AttributeError:
                continue
            rm.append(om)
        return rm
