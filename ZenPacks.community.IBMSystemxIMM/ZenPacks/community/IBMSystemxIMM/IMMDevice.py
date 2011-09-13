# ==============================================================================
# IMMDevice object class
#
# Zenoss community Zenpack for IBM SystemX Integrated Management Module
# version: 0.3
#
# (C) Copyright IBM Corp. 2011. All Rights Reserved.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# ==============================================================================

__doc__="""IMMDevice is the object class for the IMM at the device level"""
__author__ = "IBM"
__copyright__ = "(C) Copyright IBM Corp. 2011. All Rights Reserved."
__license__ = "GPL"
__version__ = "0.3.0"

from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from copy import deepcopy

class IMMDevice(Device):
    "IBM Integrated Management Module"

    _relations = Device._relations + (
        ('IMMFWVPD', ToManyCont(ToOne,
            'ZenPacks.community.IBMSystemxIMM.IMMFwVpd', 'IMMDev')),
        ('IMMCPUVPD', ToManyCont(ToOne,
            'ZenPacks.community.IBMSystemxIMM.IMMCpuVpd', 'IMMDev')),
        ('IMMMEMVPD', ToManyCont(ToOne,
            'ZenPacks.community.IBMSystemxIMM.IMMMemVpd', 'IMMDev')),
        ('IMMCOMPVPD', ToManyCont(ToOne,
            'ZenPacks.community.IBMSystemxIMM.IMMComponentVpd', 'IMMDev')),
        ('IMMCOMPLOG', ToManyCont(ToOne,
            'ZenPacks.community.IBMSystemxIMM.IMMComponentLog', 'IMMDev')),
        ('IMMFANMON', ToManyCont(ToOne,
            'ZenPacks.community.IBMSystemxIMM.IMMFanMon', 'IMMDev')),
        ('IMMVOLTMON', ToManyCont(ToOne,
            'ZenPacks.community.IBMSystemxIMM.IMMVoltMon', 'IMMDev')),
        )

    # Previously these were tabs but in 3.0 the appear as separate menu item in the device view
    factory_type_information = deepcopy(Device.factory_type_information)
    factory_type_information[0]['actions'] += (
            { 'id'              : 'IMMFWVPD'
            , 'name'            : 'IMM Firmware VPD'
            , 'action'          : 'IMMFwVpdDetail'
            , 'permissions'     : (ZEN_VIEW, ) 
            },
            { 'id'              : 'IMMCPUPD'
            , 'name'            : 'IMM CPU VPD'
            , 'action'          : 'IMMCpuVpdDetail'
            , 'permissions'     : (ZEN_VIEW, ) 
            },
            { 'id'              : 'IMMMEMVPD'
            , 'name'            : 'IMM Memory VPD'
            , 'action'          : 'IMMMemVpdDetail'
            , 'permissions'     : (ZEN_VIEW, ) 
            },
            { 'id'              : 'IMMCOMPVPD'
            , 'name'            : 'IMM Chassis Component VPD'
            , 'action'          : 'IMMComponentVpdDetail'
            , 'permissions'     : (ZEN_VIEW, ) 
            },
            { 'id'              : 'IMMCOMPLOG'
            , 'name'            : 'IMM Chassis Component Log'
            , 'action'          : 'IMMComponentLogDetail'
            , 'permissions'     : (ZEN_VIEW, ) 
            },
            { 'id'              : 'IMMFANMON'
            , 'name'            : 'IMM Fan Monitor'
            , 'action'          : 'IMMFanMonDetail'
            , 'permissions'     : (ZEN_VIEW, )
            },
            { 'id'              : 'IMMVOLTMON'
            , 'name'            : 'IMM Voltage Monitor'
            , 'action'          : 'IMMVoltMonDetail'
            , 'permissions'     : (ZEN_VIEW, )
            },
    )

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()

InitializeClass(IMMDevice)
