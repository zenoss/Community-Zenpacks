from Globals import InitializeClass
from Products.ZenModel.Device import Device
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.OperatingSystem import OperatingSystem
from Products.ZenModel.ZenStatus import ZenStatus
from IBM3584DeviceHW import IBM3584DeviceHW

class IBM3584Device(Device):

    def __init__(self, id, buildRelations=True):
        ManagedEntity.__init__(self, id, buildRelations=buildRelations)
        os = OperatingSystem()
        self._setObject(os.id, os)
        hw = IBM3584DeviceHW()
        self._setObject(hw.id, hw)
        self._lastPollSnmpUpTime = ZenStatus(0)
        self._snmpLastCollection = 0
        self._lastChange = 0

InitializeClass(IBM3584Device)

