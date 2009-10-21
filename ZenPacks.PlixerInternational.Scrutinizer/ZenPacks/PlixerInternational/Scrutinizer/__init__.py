from Products.ZenModel.ZenossSecurity import ZEN_COMMON
from Products.ZenUtils.Utils import zenPath
from Products.CMFCore.DirectoryView import registerDirectory
from time import localtime,strftime
import re
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """
    Load zProperties for the Scrutinizer ZenPack
    """
    packZProperties=[
                    ('zScrutinizerIp','127.0.0.1','string'),
                    ('zScrutinizerUsername','admin','string'),
                    ('zScrutinizerPassword','admin','string'),
                    ]
    def _registerScrutinizerPortlet(self, app):
	zpm = app.zport.ZenPortletManager
	portletsrc=os.path.join(os.path.dirname(__file__),'lib','ScrutinizerPortlet.js')
	#Its a dirty hack - register_portlet will add ZenPath one more time
	#and we don't want to hardcode path explicitly here
	p=re.compile(zenPath(''))
	portletsrc=p.sub('',portletsrc)
	zpm.register_portlet(
		sourcepath=portletsrc,
		id='ScrutinizerPortlet',
		title='Scrutinizer NBA Volume',
		permission=ZEN_COMMON)

    def install(self, app):
	ZenPackBase.install(self, app)
	self._registerScrutinizerPortlet(app)

    def upgrade(self, app):
	ZenPackBase.upgrade(self, app)
	self._registerScrutinizerPortlet(app)

    def remove(self, app, leaveObjects=False):
	ZenPackBase.remove(self, app, leaveObjects)
	zpm = app.zport.ZenPortletManager
	zpm.unregister_portlet('ScrutinizerPortlet')

