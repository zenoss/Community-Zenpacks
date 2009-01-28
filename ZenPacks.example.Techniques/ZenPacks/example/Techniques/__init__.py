import os.path

import Globals
from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenUtils.Utils import monkeypatch


skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())


@monkeypatch('Products.ZenModel.IpInterface.IpInterface')
def setCustomerInfo(self, customerInfo):
    if hasattr(self, 'customerInfo'):
        self.customerInfo = customerInfo
    else
        setattr(self, 'customerInfo', customerInfo)

@monkeypatch('Products.ZenModel.IpInterface.IpInterface')
def getCustomerInfo(self):
    if hasattr(self, 'customerInfo'):
        return self.customerInfo
    else:
        return ""

