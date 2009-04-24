################################################################################
#
# This program is part of the PrinterToner Zenpack for Zenoss.
# Copyright (C) 2009 Tonino Greco & Zenoss Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################
from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device

from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

import copy

class PrinterTonerDevice(Device):
    "The toner from a printer as a device "

    _relations = Device._relations + (
        ('printertoners', ToManyCont(ToOne,
            'ZenPacks.community.PrinterToner.PrinterToner', 'printertoner')),
        )

    factory_type_information = copy.deepcopy(Device.factory_type_information)
    custom_actions = []
    custom_actions.extend(factory_type_information[0]['actions'])
    custom_actions.insert(2,
           { 'id'              : 'PrinterTonerDevice'
           , 'name'            : 'PrinterToner'
           , 'action'          : 'viewPrinterToner'
           , 'permissions'     : (ZEN_VIEW, ) },
           )
    factory_type_information[0]['actions'] = custom_actions

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


