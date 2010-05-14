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

$Id: HPEVAStorageDiskEnclosure.py,v 1.0 2010/03/10 10:38:27 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import DTMLFile, InitializeClass
from Products.ZenModel.HWComponent import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *
from HPEVAComponent import *

from Products.ZenUtils.Utils import convToUnits

class HPEVAStorageDiskEnclosure(HWComponent, HPEVAComponent):
    """HPStorageDiskEnclosure object"""

    portal_type = meta_type = 'HPEVAStorageDiskEnclosure'

#    enclosureLayout = ((1,2,3,4,5,6,7,8,9,10,11,12),)
    enclosureLayout = ( (1,4,7,10),
                        (2,5,8,11),
                        (3,6,9,12))
    diskOrientation = 'h'

    linkimg = '/zport/dmd/hpevaselink'
    rightimg = '/zport/dmd/hpevaseright'
    blankimg = '/zport/dmd/hpevadisk_blank'


    _properties = HWComponent._properties + (
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
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : ("Change Device", )
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
            bays[int(disk.bay)]='<a href=\"%s\"><img src=\"%s_%s.png\"  /></a>'%(
                disk.getPrimaryUrlPath(), disk.diskImg(), self.diskOrientation)
        result = "\t\t\t<table border=\"0\">\n\t\t\t\t<tr>\n\t\t\t\t\t"
        result=result+"<td><a href=\"%s\"><img src=\"%s%s.png\" /></a></td>\n"%(
                                            self.getPrimaryUrlPath(),
                                            self.linkimg,
                                            int(self.id) < 28 and self.id or '')
        result= result + "\t\t\t\t\t<td><table border=\"0\">\n"
        for line in self.enclosureLayout:
            result = result + "\t\t\t\t<tr>\n"
            for bay in line:
                result = result + "\t\t\t\t\t<td>%s</td>\n"%bays.get(bay, 
                                    '<img src=\"%s_%s.png\" />'%(self.blankimg,
                                                        self.diskOrientation))
            result = result + "\t\t\t\t</tr>\n"
        result = result + "\t\t\t\t\t</table>\t\t\t\t\t</td>\n\t\t\t\t\t<td>"
        result = result +"<a href=\"%s\"><img src=\"%s_%s.png\" /></a></td>\n"%(
                                                    self.getPrimaryUrlPath(),
                                                    self.rightimg,
                                                    self.statusDot())
        result = result + "\t\t\t\t\t</td>\n\t\t\t\t</tr>\n"
        result = result + "\t\t\t</table>\n"
        return result


InitializeClass(HPEVAStorageDiskEnclosure)
