################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPMemoryModule

HPMemoryModule is an abstraction of a  Memory Module.

$Id: HPMemoryModule.py,v 1.0 2008/12/03 08:46:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenUtils.Utils import convToUnits
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ExpansionCard import *

class HPMemoryModule(ExpansionCard):
    """MemoryModule object"""
    slot = ""
    size = 0
    type = ""
    moduletype = ""
    speed = 0
    frequency = 0
    
    # we monitor Memory modules
    monitor = True

    _properties = HWComponent._properties + (
        {'id':'slot', 'type':'int', 'mode':'w'},
        {'id':'size', 'type':'int', 'mode':'w'},
        {'id':'type', 'type':'string', 'mode':'w'},
        {'id':'moduletype', 'type':'string', 'mode':'w'},
        {'id':'speed', 'type':'int', 'mode':'w'},
        {'id':'frequency', 'type':'int', 'mode':'w'},
    )

    factory_type_information = ( 
        { 
            'id'             : 'ExpansionCard',
            'meta_type'      : 'ExpansionCard',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addExpansionCard',
            'immediate_view' : 'viewHPMemoryModule',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPMemoryModule'
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

    def sizeString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
	if self.size > 0:
            return convToUnits(self.size)
	else:
	    return ''

    def speedString(self):
        """
        Return the speed in human readable form
        """
	if self.size > 0:
            return "%dns" % self.speed
	else:
	    return ''

    def frequencyString(self):
        """
        Return the memory module frequency in MHz
        """
	if self.size > 0:
            return "%dMHz" % self.frequency
	else:
	    return ''

    def statusDot(self):
        """
        Return the Status stored in the memorymodule's rrd file
	0:'green', 1:'yellow', 2:'orange', 3:'red', 4:'grey'
        """
	statusmap = [4, 4, 4, 1, 0, 1, 1, 2, 2, 3, 3, 3]
        status = self.cacheRRDValue('status', default = 1)
	return statusmap[int(status)]

    def statusString(self):
        """
        Return the status stored in the MemoryModules rrd file
        """
	statusmap = ['Other',
	             'Other',
	            'Not Present',
		    'Present',
		    'Good',
		    'Add',
		    'Upgraded',
		    'Missing',
		    'Dos not Match',
		    'Not Supported',
		    'Bad Config',
		    'Degraded',
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
        name = "HPMemoryModule"
        try:
            return getattr(self, name)
        except AttributeError:
            return super(DeviceComponent, self).getRRDTemplateByName(name)

InitializeClass(HPMemoryModule)
