import Globals
import os

from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.Utils import zenPath

class ZenPack(ZenPackBase):
    """ zencollectortool loader
    """
    def install(self, app):
        self.symlinkPlugins()

    def symlinkPlugins(self):
        os.system('chmod +x %s/zencollectortool' % (self.path('bin')))
        os.system('ln -sf %s/zencollectortool %s/' % (self.path('bin'), zenPath('bin')))
