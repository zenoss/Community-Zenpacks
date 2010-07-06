################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStorageDiskEnclosure

HPEVAStorageDiskEnclosure is an abstraction of a HPEVA_StorageDiskEnclosure

$Id: HPEVAStorageDiskEnclosure.py,v 1.3 2010/06/30 17:10:07 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Globals import DTMLFile, InitializeClass
from Products.ZenModel.HWComponent import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *
from HPEVAComponent import *

from Products.ZenUtils.Utils import convToUnits

LINKTMPLT='<a href="%s" target="_top"><img src="%s%s.png"  /></a>'

class HPEVAStorageDiskEnclosure(HWComponent, HPEVAComponent):
    """HPStorageDiskEnclosure object"""

    portal_type = meta_type = 'HPEVAStorageDiskEnclosure'

    state = "OK"

    #enclosureLayout = '1 2 3 4 5 6 7 8 9 10 11 12 13 14'
    #hLayout = 'v'
    enclosureLayout = '1 4 7 10,2 5 8 11,3 6 9 12'
    hLayout = True

    linkimg = '/zport/dmd/hpevaselink'
    rightimg = '/zport/dmd/hpevaseright_'
    blankimg = '/zport/dmd/hpevadisk_blank'


    _properties = HWComponent._properties + (
                 {'id':'state', 'type':'string', 'mode':'w'},
                 {'id':'enclosureLayout', 'type':'string', 'mode':'w'},
                 {'id':'hLayout', 'type':'boolean', 'mode':'w'},
                )

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont,
                    "ZenPacks.community.HPEVAMon.HPEVADeviceHW",
                    "enclosures")),
        ("harddisks", ToMany(ToOne,
                    "ZenPacks.community.HPEVAMon.HPEVADiskDrive",
                    "enclosure")),
        )

    factory_type_information = (
        {
            'id'             : 'HPEVAStorageDiskEnclosure',
            'meta_type'      : 'HPEVAStorageDiskEnclosure',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'StorageDiskEnclosure_icon.gif',
            'product'        : 'HPEVAMon',
            'factory'        : 'manage_addStorageDiskEnclosure',
            'immediate_view' : 'viewHPEVAStorageDiskEnclosure',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPEVAStorageDiskEnclosure'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'layout'
                , 'name'          : 'Layout'
                , 'action'        : 'viewHPEVAStorageDiskEnclosureLayout'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'disks'
                , 'name'          : 'Disks'
                , 'action'        : 'viewHPEVAStorageDiskEnclosureDisks'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )



    def getStatus(self):
        """
        Return the components status
        """
        return int(round(self.cacheRRDValue('OperationalStatus', 0)))


    def layout(self):
        bays = {}
        for disk in self.harddisks():
            bays[int(disk.bay)] = LINKTMPLT % ( disk.getPrimaryUrlPath(),
                                                disk.diskImg(),
                                                self.hLayout and '_h' or '_v')
        result = "<table border='0'>\n<tr>\n<td>"
        result = result + LINKTMPLT % (self.getPrimaryUrlPath(), self.linkimg,
                                        int(self.id) < 28 and self.id or '')
        result=result+"<td><table border='0'>\n"
        for line in self.enclosureLayout.split(','):
            result = result + "<tr>\n"
            for bay in line.strip().split():
                result = result + "<td>%s</td>\n"%bays.get(int(bay), 
                                    '<img src="%s%s.png" />'%(self.blankimg,
                                                self.hLayout and '_h' or '_v'))
            result = result + "</tr>\n"
        result = result + "</table>\n</td>\n<td>"
        result = result + LINKTMPLT % (self.getPrimaryUrlPath(), self.rightimg,
                                                            self.statusDot())
        result = result + "</td>\n</td>\n</tr>\n</table>\n"
        return result

    def getRRDNames(self):
        """
        Return the datapoint name of this StorageDiskEnclosure
        """
        return ['StorageDiskEnclosure_OperationalStatus']

InitializeClass(HPEVAStorageDiskEnclosure)
