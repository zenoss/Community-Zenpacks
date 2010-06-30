################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellPowerSupply

DellPowerSupply is an abstraction of a PowerSupply.

$Id: DellPowerSupply.py,v 1.1 2010/06/30 22:07:35 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

import inspect
from Products.ZenModel.PowerSupply import *
from DellComponent import *

class DellPowerSupply(PowerSupply, DellComponent):
    """PowerSupply object"""

    state = property(fget=lambda self: self.statusString())
    status = 1
    volts = 0
    vpsnmpindex = ""
    vptype = 0
    apsnmpindex = ""
    aptype = 0
    __snmpindex = ""

    _properties = PowerSupply._properties + (
        {'id':'status', 'type':'int', 'mode':'w'},
        {'id':'volts', 'type':'int', 'mode':'w'},
        {'id':'vpsnmpindex', 'type':'string', 'mode':'w'},
        {'id':'vptype', 'type':'int', 'mode':'w'},
        {'id':'apsnmpindex', 'type':'string', 'mode':'w'},
        {'id':'aptype', 'type':'int', 'mode':'w'},
    )

    factory_type_information = (
        {
            'id'             : 'PowerSupply',
            'meta_type'      : 'PowerSupply',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'PowerSupply_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addPowerSupply',
            'immediate_view' : 'viewDellPowerSupply',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDellPowerSupply'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )


    def milliampsString(self):
        """
        Return the current milliamps as a string
        """
        milliamps = self.milliamps()
        return milliamps is None and "unknown" or "%dmA" % (milliamps,)

    def milliamps(self, default=None):
        """
        Return the current milliamps for the power supply
        """
        milliamps = self.cacheRRDValue('milliamps', default)
        if milliamps is not None:
            if self.aptype == 23 or self.aptype == 25:
                return long(milliamps) * 100
            elif self.aptype == 24 or self.aptype == 26:
                return long(milliamps) / self.millivolts() / 650
            else:
                return long(milliamps)
        return None


    def millivoltsString(self):
        """
        Return the current millivolts as a string
        """
        millivolts = self.millivolts()
        return millivolts is None and "unknown" or "%dV" % (millivolts / 1000,)


    def getRRDTemplates(self):
        templates = []
        tnames = ['DellPowerSupply',]
        if self.vpsnmpindex and self.vptype != 16: tnames.append('DellPowerSupplyVP')
        if self.vpsnmpindex and self.vptype == 16: tnames.append('DellPowerSupplyVPD')
        if self.apsnmpindex and self.aptype != 16: tnames.append('DellPowerSupplyAP')
        if self.apsnmpindex and self.aptype == 16: tnames.append('DellPowerSupplyAPD')
        for tname in tnames:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

    def _getSnmpIndex(self):
        snmpindex = self.__snmpindex
        frame = inspect.currentframe(2)
        try:
            if 'templ' in frame.f_locals:
                templ = frame.f_locals['templ'].id
                if templ == 'DellPowerSupplyVP':
                    snmpindex = self.vpsnmpindex
                if templ == 'DellPowerSupplyAP':
                    snmpindex = self.apsnmpindex
        finally: del frame
        return snmpindex

    def _setSnmpIndex(self, value):
        self.__snmpindex = value

    snmpindex = property(fget=lambda self: self._getSnmpIndex(),
                        fset=lambda self, v: self._setSnmpIndex(v)
                        )

    def setState(self, value):
        self.status = 0
        for intvalue, status in self.statusmap.iteritems():
            if status[2].upper() != value.upper(): continue 
            self.status = value
            break

    state = property(fget=lambda self: self.statusString(),
                     fset=lambda self, v: self.setState(v)
                     )

InitializeClass(DellPowerSupply)
