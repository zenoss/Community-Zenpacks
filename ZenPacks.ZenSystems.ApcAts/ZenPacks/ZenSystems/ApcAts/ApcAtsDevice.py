##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 7th, 2011
# Revised:
#
# ApcAtsDevice object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from copy import deepcopy


class ApcAtsDevice(Device):
    "An APC ATS Device"

#    portal_type = meta_type = 'ApcAtsDevice'

    #**************Custom data Variables here from modeling************************

    statusSelectedSource = 0
    statusRedundancyState = 0
    statusSourceAStatus = 0
    statusSourceBStatus = 0
    statusPhaseSyncStatus = 0

    #**************END CUSTOM VARIABLES *****************************


    #*************  Those should match this list below *******************
    _properties = Device._properties + (
        {'id':'statusSelectedSource', 'type':'int', 'mode':''},
        {'id':'statusRedundancyState', 'type':'int', 'mode':''},
        {'id':'statusSourceAStatus', 'type':'int', 'mode':''},
        {'id':'statusSourceBStatus', 'type':'int', 'mode':''},
        {'id':'statusPhaseSyncStatus', 'type':'int', 'mode':''},
        )
    #****************

    _relations = Device._relations + (
        ('ApcAtsIn', ToManyCont(ToOne, 'ZenPacks.ZenSystems.ApcAts.ApcAtsInput', 'ApcAtsDevIn')),
        )

    factory_type_information = deepcopy(Device.factory_type_information)
    factory_type_information[0]['actions'] += (
            { 'id'              : 'ApcAtsIn'
            , 'name'            : 'APC ATS Information'
            , 'action'          : 'ApcAtsDeviceDetail'
            , 'permissions'     : (ZEN_VIEW, ) },
            )

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


InitializeClass(ApcAtsDevice)
