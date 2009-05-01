################################################################################
#
# This program is part of the deviceAdvDetail Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""LogicalDisk

LogicalDisk is an abstraction of a logicaldisk.

$Id: LogicalDisk.py,v 1.0 2009/04/23 14:56:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]


from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenUtils.Utils import convToUnits

from Products.ZenRelations.RelSchema import *

from Products.ZenModel.HWComponent import HWComponent
from Products.ZenModel.ZenossSecurity import *

def manage_addHardDisk(context, id, title = None, REQUEST = None):
    """make a filesystem"""
    hd = HardDisk(id, title)
    context._setObject(id, hd)
    hd = context._getOb(id)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()
                                     +'/manage_main') 

addHardDisk = DTMLFile('dtml/addHardDisk',globals())


class LogicalDisk(HWComponent):
    """LogicalDisk object"""

    portal_type = meta_type = 'LogicalDisk'

    manage_editHardDiskForm = DTMLFile('dtml/manageEditHardDisk',globals())
    
    description = ""
    hostresindex = 0
    size = 0
    stripesize = 0
    diskType = ""
    status = 1

    _properties = HWComponent._properties + (
                 {'id':'description', 'type':'string', 'mode':'w'},
                 {'id':'hostresindex', 'type':'int', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'size', 'type':'int', 'mode':'w'},
                 {'id':'stripesize', 'type':'int', 'mode':'w'},
                 {'id':'status', 'type':'int', 'mode':'w'},
                )    

    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "Products.ZenModel.DeviceHW", "logicaldisks")),
        )

    
    factory_type_information = ( 
        { 
            'id'             : 'LogicalDisk',
            'meta_type'      : 'LogicalDisk',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'deviceAdvDetail',
            'factory'        : 'manage_addHardDisk',
            'immediate_view' : 'viewLogicalDisk',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewLogicalDisk'
                , 'permissions'   : ('View',)
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

    def viewName(self): return self.description

    def sizeString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.size,divby=1000)

    def stripesizeString(self):
        """
        Return the Stripes Size in human readable form ie 64Kb
        """
        return convToUnits(self.stripesize)


InitializeClass(LogicalDisk)
