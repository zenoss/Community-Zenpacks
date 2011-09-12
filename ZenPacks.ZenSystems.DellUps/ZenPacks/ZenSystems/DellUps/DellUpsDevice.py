##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 8th, 2011
# Revised:
#
# DellUpsDevice object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenModel.ZenossSecurity import *
from copy import deepcopy

class DellUpsDevice(Device):
    "A Dell UPS Device"

    _relations = Device._relations + (
        ('DellUpsBat', ToManyCont(ToOne, 'ZenPacks.ZenSystems.DellUps.DellUpsBattery', 'DellUpsDevBat')),
        )

    factory_type_information = deepcopy(Device.factory_type_information)

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()

InitializeClass(DellUpsDevice)
