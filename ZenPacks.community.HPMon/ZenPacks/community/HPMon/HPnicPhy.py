################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPnicPhy

HPnicPhy is an abstraction of a HP NIC.

$Id: HPnicPhy.py,v 1.0 2008/12/05 15:14:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ExpansionCard import *

class HPnicPhy(ExpansionCard):
    """NIC object"""

    type = ""
    model = ""
    role = ""
    slot = 0
    macaddress = ""
    duplex = ""
    speed = 0
    
    # we monitor RAID Controllers
    monitor = True

    _properties = HWComponent._properties + (
        {'id':'type', 'type':'string', 'mode':'w'},
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'role', 'type':'string', 'mode':'w'},
        {'id':'slot', 'type':'int', 'mode':'w'},
        {'id':'macaddress', 'type':'string', 'mode':'w'},
        {'id':'duplex', 'type':'string', 'mode':'w'},
        {'id':'speed', 'type':'int', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'ExpansionCard',
            'meta_type'      : 'ExpansionCard',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addExpansionCard',
            'immediate_view' : 'viewHPnicPhy',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPnicPhy'
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

    def speedString(self):
        """
        Return the speed in human readable form
        """
        if not self.speed:
            return 'Unknown'
        speed = self.speed
        for unit in ('bps', 'Kbps', 'Mbps', 'Gbps'):
            if speed < 1000: break
            speed /= 1000.0
        return "%.0f%s" % (speed, unit)

    def statusDot(self):
        """
        Return the Status stored in the rrd file
	0:'green', 1:'yellow', 2:'orange', 3:'red', 4:'grey'
        """
	statusmap = [4, 4, 0, 3, 2]
        status = self.cacheRRDValue('status', default = 1)
	return statusmap[int(status)]

    def statusString(self):
        """
        Return the status stored in the rrd file
        """
	statusmap = ['Other',
	            'Other',
	            'Ok',
		    'General Failure',
		    'Link Failure',
		    ]
        status = self.cacheRRDValue('status', default = 1)
	return statusmap[int(status)]

    def getRRDNames(self):
        """
        Return the datapoint name of this fan 'status_status'
        """
        return ['status_status']

    def getRRDTemplateByName(self, name):
        """
        Return the closest RRDTemplate named name by walking our aq chain.
        """
        name = "HPnicPhy"
        try:
            return getattr(self, name)
        except AttributeError:
            return super(DeviceComponent, self).getRRDTemplateByName(name)

InitializeClass(HPnicPhy)
