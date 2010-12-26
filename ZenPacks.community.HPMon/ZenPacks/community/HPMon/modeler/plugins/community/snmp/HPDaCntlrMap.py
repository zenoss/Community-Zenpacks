################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPDaCntlrMap

HPDaCntlrMap maps the cpqDaCntlrTable table to cpqDaCntlr objects

$Id: HPDaCntlrMap.py,v 1.2 2010/11/05 14:33:55 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from Products.ZenUtils.Utils import convToUnits
from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from HPExpansionCardMap import HPExpansionCardMap

class HPDaCntlrMap(HPExpansionCardMap):
    """Map HP/Compaq insight manager cpqDaCntlrTable table to model."""

    maptype = "cpqDaCntlr"
    modname = "ZenPacks.community.HPMon.cpqDaCntlr"

    snmpGetTableMaps = (
        GetTableMap('cpqDaCntlrTable',
                    '.1.3.6.1.4.1.232.3.2.2.1.1',
                    {
                        '.2': 'model',
                        '.3': 'FWRev',
                        '.5': 'slot',
                        '.6': 'status',
                        '.9': 'role',
                        '.15': 'serialNumber',
                        '.16': 'redundancyType',
                    }
        ),
    )

    models = {1: 'Unknown Array Controller',
            2: 'Compaq 32-Bit Intelligent Drive Array Controller',
            3: 'Compaq 32-Bit Intelligent Drive Array Expansion Controller',
            4: 'Compaq Intelligent Drive Array Controller-2',
            5: 'Compaq SMART Array Controller',
            6: 'Compaq SMART-2/E Array Controller',
            7: 'Compaq SMART-2/P Array Controller',
            8: 'Compaq SMART-2SL Array Controller',
            9: 'Compaq Smart Array 3100ES Controller',
            10: 'Compaq Smart Array 3200 Controller',
            11: 'Compaq SMART-2DH Array Controller',
            12: 'Compaq Smart Array 221 Controller',
            13: 'Compaq Smart Array 4250ES Controller',
            14: 'Compaq Smart Array 4200 Controller',
            15: 'Compaq Integrated Smart Array Controller',
            16: 'Compaq Smart Array 431 Controller',
            17: 'HP Smart Array 5300 Controller',
            18: 'Compaq RAID LC2 Controller',
            19: 'HP Smart Array 5i Controller',
            20: 'Compaq Smart Array 532 Controller',
            21: 'Compaq Smart Array 5312 Controller',
            22: 'HP Smart Array 641 Controller',
            23: 'HP Smart Array 642 Controller',
            24: 'HP Smart Array 6400 Controller',
            25: 'HP Smart Array 6400 EM Controller',
            26: 'HP Smart Array 6i Controller',
            27: 'HP Array Controller',
            28: 'Reserved',
            29: 'HP Smart Array P600 Controller',
            30: 'HP Smart Array P400 Controller',
            31: 'HP Smart Array E200 Controller',
            32: 'HP Smart Array E200i Controller',
            33: 'HP Smart Array P400i Controller',
            34: 'HP Smart Array P800 Controller',
            35: 'HP Smart Array E500 Controller',
            36: 'HP Smart Array P700m Controller',
            }

    redundancyTypes = {1: 'other',
                        2: 'Not Redundancy',
                        3: 'Driver Duplexing',
                        4: 'Active-Standby',
                        5: 'Primary-Secondary',
                        }


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        cardtable = tabledata.get('cpqDaCntlrTable')
        if not device.id in HPExpansionCardMap.oms:
            HPExpansionCardMap.oms[device.id] = []
        for oid, card in cardtable.iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex = oid.strip('.')
                om.id = self.prepId("cpqDaCntlr%s" % om.snmpindex)
                om.slot = getattr(om, 'slot', 0)
                om.model = self.models.get(getattr(om, 'model', 1), '%s (%d)' %(self.models[1], om.model))
                om.setProductKey = "%s" % om.model
                om.redundancyType = self.redundancyTypes.get(getattr(om, 'redundancyType', 1))
            except AttributeError:
                continue
            HPExpansionCardMap.oms[device.id].append(om)
        return

