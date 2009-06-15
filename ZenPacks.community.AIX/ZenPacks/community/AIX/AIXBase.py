from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenModel.Device import Device
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenStatus import ZenStatus
from ZenPacks.community.AIX.AIXOperatingSystem import AIXOperatingSystem
from ZenPacks.community.AIX.AIXDeviceHW import AIXDeviceHW

class AIXBase(Device):
    #Aix Base class


    # Initialize the new class and rebuild the relations
    # Need to override the os object
    # Need to override the hw object
    # Override factory_type_information
    # __init__ taken from Device.py and override os and hw
    def __init__(self, id, buildRelations=True):
        ManagedEntity.__init__(self, id, buildRelations=buildRelations)
        os = AIXOperatingSystem()
        self._setObject(os.id, os)
        hw = AIXDeviceHW()
        self._setObject(hw.id, hw)
        #self.commandStatus = "Not Tested"
        self._lastPollSnmpUpTime = ZenStatus(0)
        self._snmpLastCollection = 0
        self._lastChange = 0

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
                , 'action'        : 'aixdeviceOsDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'hwdetail'
                , 'name'          : 'Hardware'
                , 'action'        : 'aixdeviceHardwareDetail'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfServer'
                , 'name'          : 'Perf'
                , 'action'        : 'viewDevicePerformance'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'edit'
                , 'name'          : 'Edit'
                , 'action'        : 'editDevice'
                , 'permissions'   : ("Change Device",)
                },
            )
         },
        )

InitializeClass(AIXBase)
