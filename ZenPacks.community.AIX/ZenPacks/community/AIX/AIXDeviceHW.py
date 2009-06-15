from Globals import InitializeClass
from Products.ZenModel.DeviceHW import DeviceHW
from Products.ZenModel.Hardware import Hardware
from Products.ZenRelations.RelSchema import *

class AIXDeviceHW(DeviceHW):

    # Define new relationships
    _relations = Hardware._relations + (
        ("cpus", ToManyCont(ToOne, "Products.ZenModel.CPU", "hw")),
        ("harddisks", ToManyCont(ToOne, "ZenPacks.community.AIX.AIXHardDisk", "hw")),
        ("cdrom", ToManyCont(ToOne, "ZenPacks.community.AIX.AIXCdrom", "hw")),
        ("tape", ToManyCont(ToOne, "ZenPacks.community.AIX.AIXTape", "hw")),
        ("printer", ToManyCont(ToOne, "ZenPacks.community.AIX.AIXPrinter", "hw")),
        ("cards", ToManyCont(ToOne, "ZenPacks.community.AIX.AIXExpansionCard", "hw")),
        ("lparinfo", ToManyCont(ToOne, "ZenPacks.community.AIX.AIXLparInfo", "hw")),
        ("fans", ToManyCont(ToOne, "Products.ZenModel.Fan", "hw")),
        ("powersupplies", ToManyCont(ToOne, "Products.ZenModel.PowerSupply",
            "hw")),
        ("temperaturesensors", ToManyCont(ToOne,
            "Products.ZenModel.TemperatureSensor", "hw")),
    )

InitializeClass(AIXDeviceHW)
