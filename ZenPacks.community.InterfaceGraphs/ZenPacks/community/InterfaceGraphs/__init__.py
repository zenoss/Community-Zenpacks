
import Globals
import os.path
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.Utils import monkeypatch

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

class ZenPack(ZenPackBase):
    """
    Interface Graph ZenPack Definition
    """

    packZProperties = [
        ('zInterfaceGraphContents', ['Throughput', 'Errors', 'Packets'], 'lines'),
        ('zInterfaceGraphGroupByInterface', False, 'boolean')
    ]



# Monkeypatching the "Device" object to include a custom function
# and to add an "Interface Graphs" tab for all devices.
# we look for either the "graphs" or the "perf" tabs, since 2.5
# uses "perf"
from Products.ZenModel.ZenModelBase import ZenModelBase
@monkeypatch('Products.ZenModel.Device.Device')
def zentinelTabs(self, templateName):
    tabs = ZenModelBase.zentinelTabs(self, templateName)
    for i, tab in enumerate(tabs):
        if tab['name'] == 'Graphs' or tab['name'] == 'Perf':
            tabs.insert(i+1, dict(
                    id="interfaceGraphs",
                    name="Interface Graphs",
                    permissions=(ZEN_VIEW,),
                    action="interfaceGraphs"))
    return tabs

@monkeypatch('Products.ZenModel.Device.Device')
def getInterfaceGraphDefs(self):
    """
        Return a dict with all the interface graphs
        which is also tagged with interface name
        This also checks the two zProperties to 
        decide what goes in the dict, and what order
        the dict items are presented in.
    """
    # If zInterfaceGraphContents is empty, just return
    # an empty list, no point faffing about
    if len(self.zInterfaceGraphContents) == 0:
        return []

    # Time to do some actual work, grabbing and tagging
    # the graph defs.
    graphDefs = []
    for int in self.os.interfaces():
        tempGds = int.getDefaultGraphDefs()
        for gd in tempGds:
            gd['interfaceName'] = int.id
            gd['interfaceDesc'] = int.description
            graphDefs.append(gd)

    # Process the graphdefs, to create a the order the 
    # zProperties define. There's probably some awesome
    # map/reduce one-liner that would do this, but I'm not
    # smart enough for that kind of malarky.
    # If you like map/reduce, you'll probably like this:
    # http://browsertoolkit.com/fault-tolerance.png
    #
    defsToReturn = []

    if self.zInterfaceGraphGroupByInterface:
        # No reordering needed, just filter by our list
        for gd in graphDefs:
            if gd['title'] in self.zInterfaceGraphContents:
                defsToReturn.append(gd)
    else:
        # We want to group by graph type, not interface
        for gt in self.zInterfaceGraphContents:
            for gd in graphDefs:
                if gd['title'] == gt:
                    defsToReturn.append(gd)

    return defsToReturn


