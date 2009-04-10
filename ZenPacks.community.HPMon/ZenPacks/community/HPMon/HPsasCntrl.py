################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPsasCntrl

HPsasCntrl is an abstraction of a HP SAS Controller.

$Id: HPsasCntrl.py,v 1.0 2008/12/09 14:31:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ExpansionCard import *

class HPsasCntrl(ExpansionCard):
    """SAS Cntrl object"""

    type = ""
    model = ""
    FWRev = ""
    slot = 0
    
    # we monitor RAID Controllers
    monitor = True

    _properties = HWComponent._properties + (
        {'id':'type', 'type':'string', 'mode':'w'},
        {'id':'model', 'type':'string', 'mode':'w'},
        {'id':'FWRev', 'type':'string', 'mode':'w'},
        {'id':'slot', 'type':'int', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'ExpansionCard',
            'meta_type'      : 'ExpansionCard',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addExpansionCard',
            'immediate_view' : 'viewHPsasCntrl',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPsasCntrl'
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
	statusmap = [4, 4, 0, 2, 3]
        status = self.cacheRRDValue('status', default = 1)
	return statusmap[int(status)]

    def statusString(self):
        """
        Return the status stored in the rrd file
        """
	statusmap = ['Other',
	            'Other',
	            'Ok',
		    'Degraded',
		    'Failed',
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
        name = "HPsasCntrl"
        try:
            return getattr(self, name)
        except AttributeError:
            return super(DeviceComponent, self).getRRDTemplateByName(name)

InitializeClass(HPsasCntrl)
