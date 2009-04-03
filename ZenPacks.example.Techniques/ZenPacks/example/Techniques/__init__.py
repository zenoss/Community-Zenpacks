import os.path

import Globals
from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenUtils.Utils import monkeypatch


skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())


@monkeypatch('Products.ZenModel.IpInterface.IpInterface')
def setCustomerInfo(self, customerInfo):
    if hasattr(self, 'customerInfo'):
        self.customerInfo = customerInfo
    else:
        setattr(self, 'customerInfo', customerInfo)

@monkeypatch('Products.ZenModel.IpInterface.IpInterface')
def getCustomerInfo(self):
    if hasattr(self, 'customerInfo'):
        return self.customerInfo
    else:
        return ""

# This is an example of how to add a new tab to all devices. We do this by
# overridding the ZenModelBase.zentinelTabs method for Device objects and
# inserting our Custom tab immediately after the Perf tab.
from Products.ZenModel.ZenModelBase import ZenModelBase
@monkeypatch('Products.ZenModel.Device.Device')
def zentinelTabs(self, templateName):
    tabs = ZenModelBase.zentinelTabs(self, templateName)
    for i, tab in enumerate(tabs):
        if tab['name'] == 'Perf':
            tabs.insert(i+1, dict(
                id="custom",
                name="Custom",
                permissions=(ZEN_VIEW,),
                action="customTab"))
    return tabs
