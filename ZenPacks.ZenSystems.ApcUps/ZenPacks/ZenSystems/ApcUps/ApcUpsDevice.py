##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 28th, 2011
# Revised:
#
# ApcPduDevice object class
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


class ApcUpsDevice(Device):
    "An APC UPS Device"

    #**************Custom data Variables here from modeling************************

    numBatteryPacks = 0
    numBadBatteryPacks = 0
    basicOutputStatus = 0
    basicOutputStatusText = ''

    #**************END CUSTOM VARIABLES *****************************


    #*************  Those should match this list below *******************
    _properties = Device._properties + (
        {'id':'numBatteryPacks', 'type':'int', 'mode':''},
        {'id':'numBadBatteryPacks', 'type':'int', 'mode':''},
        {'id':'basicOutputStatus', 'type':'int', 'mode':''},
        {'id':'basicOutputStatusText', 'type':'string', 'mode':''},
        )
    #****************

    _relations = Device._relations + (
        ('ApcUpsBat', ToManyCont(ToOne, 'ZenPacks.ZenSystems.ApcUps.ApcUpsBattery', 'ApcUpsDevBat')),
        )

    factory_type_information = deepcopy(Device.factory_type_information)
    factory_type_information[0]['actions'] += (
            { 'id'              : 'ApcUpsInfo'
            , 'name'            : 'APC UPS Information'
            , 'action'          : 'ApcUpsDeviceDetail'
            , 'permissions'     : (ZEN_VIEW, ) },
            )



    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


InitializeClass(ApcUpsDevice)
