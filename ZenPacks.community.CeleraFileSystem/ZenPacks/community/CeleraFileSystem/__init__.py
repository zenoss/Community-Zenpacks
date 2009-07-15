import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.Utils import zenPath

class ZenPack(ZenPackBase):
    def install(self, app):
        ZenPackBase.install(self, app)
        self.symlinkPlugin()

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        self.symlinkPlugin()

    def remove(self, app, leaveObjects=False):
        self.removePluginSymlink()
        ZenPackBase.remove(self, app, leaveObjects)


    def symlinkPlugin(self):
        os.system('ln -sf %s/CelerraDf.sh %s/' %
            (self.path('libexec'), zenPath('libexec')))

    def removePluginSymlink(self):
        os.system('rm -f %s/CelerraDf.sh' % (zenPath('libexec')))
