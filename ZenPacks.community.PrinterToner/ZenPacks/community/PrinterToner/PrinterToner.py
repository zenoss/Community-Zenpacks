################################################################################
#
# This program is part of the PrinterToner Zenpack for Zenoss.
# Copyright (C) 2009 Tonino Greco & Zenoss Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################
__doc__="""PrinterToner

PrinterToner - new device class for Printer Toner on HP Printers

$Id: $"""

__version__ = "$Revision: $"[11:-2]

import locale

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenUtils.Utils import convToUnits
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import prepId
#from ZenModelRM import ZenModelRM


class PrinterToner(DeviceComponent, ManagedEntity):
    """PrinterToner object"""

    portal_type = meta_type = 'PrinterToner'

    tonerName = ""
    maxToner = ""
    currentToner = ""
    tonerType = ""

    _properties = (
        {'id':'tonerName', 'type':'string', 'mode':''},
        {'id':'maxToner', 'type':'string', 'mode':''},
        {'id':'currentToner', 'type':'string', 'mode':''},
        {'id':'tonerType', 'type':'string', 'mode':''},
        )
    
    _relations = (
        ("printertoner", ToOne(ToManyCont,
            "ZenPacks.community.PrinterToner.PrinterTonerDevice", "printertoners")),
        )


    factory_type_information = (
        {
            'id'             : 'PrinterToner',
            'meta_type'      : 'PrinterToner',
            'description'    : """Arbitrary Printer Toner grouping class""",
            'icon'           : 'printer_toner.gif',
            'product'        : 'PrinterToner',
            'factory'        : 'manage_addPrinterToner',
            'immediate_view' : 'viewPrinterTonerDetail',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewPrinterTonerDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
            )
          },
        )

    def viewName(self):
        return self.tonerName
    name = primarySortKey = viewName

    def device(self):
        return self.printertoner()

    def getId(self):
        return self.id

    def currentValue(self, default=None):
        """
        Return the current toner levels
        """
        currentVal = self.cacheRRDValue('toner_toner', default)
        if currentVal is None:
            return "no value"
        if currentVal is not None:
            return long(currentVal)
        return None
    currentvalue = currentValue


InitializeClass(PrinterToner)
