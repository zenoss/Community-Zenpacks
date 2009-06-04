from Products.ZenModel.ZenossSecurity import ZEN_COMMON
from Products.ZenUtils.Utils import zenPath
from Products.CMFCore.DirectoryView import registerDirectory
from time import localtime,strftime
import re
import Globals
import os

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """
    Portlet ZenPack class
    """

    def install(self, app):
        """
        Initial installation of the ZenPack
        """
        ZenPackBase.install(self, app)
        self._registerFavoriteReportsPortlet(app)

    def upgrade(self, app):
        """
        Upgrading the ZenPack procedures
        """
        ZenPackBase.upgrade(self, app)
        self._registerFavoriteReportsPortlet(app)

    def remove(self, app, leaveObjects=False ):
        """
        Remove the ZenPack from Zenoss
        """
        # NB: As of Zenoss 2.2, this function now takes three arguments.
        ZenPackBase.remove(self, app, leaveObjects)
        zpm = app.zport.ZenPortletManager
        zpm.unregister_portlet('FavoriteReportsPortlet')

    def _registerFavoriteReportsPortlet(self, app):
        zpm = app.zport.ZenPortletManager
        portletsrc=os.path.join(os.path.dirname(__file__),'lib','reportsPortlet.js')
        #Its a dirty hack - register_portlet will add ZenPath one more time
        #and we don't want to hardcode path explicitly here
        p=re.compile(zenPath(''))
        portletsrc=p.sub('',portletsrc)
        zpm.register_portlet(
            sourcepath=portletsrc,
            id='FavoriteReportsPortlet',
            title='Favorite Reports',
            permission=ZEN_COMMON)

