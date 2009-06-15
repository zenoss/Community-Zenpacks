from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.HardDisk import HardDisk
from Products.ZenModel.HWComponent import HWComponent
from ZenPacks.community.AIX.AIXDeviceHW import AIXDeviceHW
import copy

class AIXHardDisk(HardDisk):
    "Aix HardDisk class"

    # Set so a template named PrintQueue will bind automatically
    portal_type = meta_type = 'HardDisk'

    # Attribute Defaults
    title = ""
    aixhdManufacturerName = ""
    aixhdModelName = ""
    aixhdSerialNumber= ""
    aixhdPartNumber= ""
    aixhdFRU = ""
    aixhdindex= ""
    aixhdtype= ""
    aixhdsize= ""
    aixhdinterface= ""
    aixhdstatus= ""
    aixhdlocation= ""
    aixhdidentifier= ""
    aixhddescription= ""
    aixhdEC= ""
    # Define New Properties for this class
    _properties = HWComponent._properties + (
        {'id':'title', 'type':'string', 'mode':''},
        {'id':'aixhdManufacturerName', 'type':'string', 'mode':''},
        {'id':'aixhdModelName', 'type':'string', 'mode':''},
        {'id':'aixhdSerialNumber', 'type':'string', 'mode':''},
        {'id':'aixhdPartNumber', 'type':'string', 'mode':''},
        {'id':'aixhdFRU', 'type':'string', 'mode':''},
        {'id':'aixhdindex', 'type':'string', 'mode':''},
        {'id':'aixhdtype', 'type':'string', 'mode':''},
        {'id':'aixhdsize', 'type':'string', 'mode':''},
        {'id':'aixhdinterface', 'type':'string', 'mode':''},
        {'id':'aixhdstatus', 'type':'string', 'mode':''},
        {'id':'aixhdlocation', 'type':'string', 'mode':''},
        {'id':'aixhdidentifier', 'type':'string', 'mode':''},
        {'id':'aixhddescription', 'type':'string', 'mode':''},
        {'id':'aixhdEC', 'type':'string', 'mode':''},
    )

    # Define new relationships
    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont, "ZenPacks.community.AIX.AIXDeviceHW", "harddisks")),
        )

InitializeClass(AIXDeviceHW)
