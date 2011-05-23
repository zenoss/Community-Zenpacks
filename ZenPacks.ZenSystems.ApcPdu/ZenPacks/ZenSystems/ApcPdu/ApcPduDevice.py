##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 3rd, 2011
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


class ApcPduDevice(Device):
    "An APC PDU Device"

    _relations = Device._relations + (
        ('ApcPduOut', ToManyCont(ToOne, 'ZenPacks.ZenSystems.ApcPdu.ApcPduOutlet', 'ApcPduDevOut')),
        ('ApcPduBan', ToManyCont(ToOne, 'ZenPacks.ZenSystems.ApcPdu.ApcPduBank', 'ApcPduDevBan')),
        ('ApcPduP', ToManyCont(ToOne, 'ZenPacks.ZenSystems.ApcPdu.ApcPduPS', 'ApcPduDevP')),
        )

    factory_type_information = deepcopy(Device.factory_type_information)

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


InitializeClass(ApcPduDevice)
