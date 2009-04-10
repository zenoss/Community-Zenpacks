################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPfcaCntrl

HPfcaCntrl is an abstraction of a HP FC Array Controller.

$Id: HPfcaCntrl.py,v 1.0 2008/12/03 08:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ExpansionCard import *

class HPfcaCntrl(ExpansionCard):
    """DACntrl object"""

    type = ""
    model = ""
    FWRev = ""
    slot = 0
    redundancyType = ""
    wwpn = ""
    wwnn = ""
    
    # we monitor RAID Controllers
    monitor = True

    _properties = HWComponent._properties + (
        {'id':'type', 'type':'string', 'mode':'w'},
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'FWRev', 'type':'string', 'mode':'w'},
        {'id':'slot', 'type':'int', 'mode':'w'},
        {'id':'redundancyType', 'type':'string', 'mode':'w'},
        {'id':'wwpn', 'type':'string', 'mode':'w'},
        {'id':'wwnn', 'type':'string', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'ExpansionCard',
            'meta_type'      : 'ExpansionCard',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addExpansionCard',
            'immediate_view' : 'viewHPfcaCntrl',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPfcaCntrl'
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

    def statusDot(self):
        """
        Return the Status stored in the rrd file
	0:'green', 1:'yellow', 2:'orange', 3:'red', 4:'grey'
        """
	statusmap = [4, 4, 0, 2, 3, 3, 2, 2, 2, 3, 3, 3, 2]
        status = self.cacheRRDValue('status', default = 1)
	return statusmap[int(status)]

    def statusString(self):
        """
        Return the status stored in the rrd file
        """
	statusmap = ['Other',
	            'Other',
	            'No Failure',
		    'No Redundant Controller',
		    'Different Hardware',
		    'No Link',
		    'Different Firmware',
		    'Different Cache',
		    'Other Cache Failure',
		    'No Drives',
		    'Other no Drives',
		    'Unsupported Drives',
		    'Expand in Progress',
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
        name = "HPfcaCntrl"
        try:
            return getattr(self, name)
        except AttributeError:
            return super(DeviceComponent, self).getRRDTemplateByName(name)

InitializeClass(HPfcaCntrl)
