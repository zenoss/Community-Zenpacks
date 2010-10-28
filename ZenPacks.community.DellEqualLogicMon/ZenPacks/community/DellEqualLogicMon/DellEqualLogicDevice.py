################################################################################
#
# This program is part of the DellEqualLogicMon Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################


from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_DEVICE
from Products.ZenModel.Device import Device
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenModel.ZenStatus import ZenStatus
from Products.ZenModel.DeviceHW import DeviceHW
from ZenPacks.community.DellEqualLogicMon.DellEqualLogicDeviceOS import DellEqualLogicDeviceOS
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

class DellEqualLogicDevice(Device):

    def __init__(self, id, buildRelations=True):
        ManagedEntity.__init__(self, id, buildRelations=buildRelations)
        os = DellEqualLogicDeviceOS()
        self._setObject(os.id, os)
        hw = DeviceHW()
        self._setObject(hw.id, hw)
        self._lastPollSnmpUpTime = ZenStatus(0)
        self._snmpLastCollection = 0
        self._lastChange = 0
        self.buildRelations()

    factory_type_information = (
        {
            'immediate_view' : 'deviceStatus',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'deviceStatus'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'osdetail'
                , 'name'          : 'OS'
                , 'action'        : 'dellEqualLogicDeviceOsDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'hwdetail'
                , 'name'          : 'Hardware'
                , 'action'        : 'deviceHardwareDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfServer'
                , 'name'          : 'Graphs'
                , 'action'        : 'viewDevicePerformance'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'edit'
                , 'name'          : 'Edit'
                , 'action'        : 'editDevice'
                , 'permissions'   : (ZEN_CHANGE_DEVICE,)
                },
            )
         },
        )

InitializeClass(DellEqualLogicDevice)
