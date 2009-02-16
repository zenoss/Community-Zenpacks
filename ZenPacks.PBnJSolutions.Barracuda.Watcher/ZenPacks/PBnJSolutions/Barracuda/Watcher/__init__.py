
import Globals
import os
import os.path

from os.path import join
from Products.ZenModel.ZenPack import ZenPackBase

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

libexec = os.path.join(os.path.dirname(__file__), 'libexec')

class ZenPack(ZenPackBase):
    """ ZenPacks.PBnJSolutions.Barracuda.Watcher loader
    """

    packZProperties = [
        ('zZenPacksPBnJSolutionsBarracudaWatcherlibexec', libexec, 'string'),
        ]
