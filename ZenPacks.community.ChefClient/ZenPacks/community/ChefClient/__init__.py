import Globals
import os.path
from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenModel.ZenPack import ZenPackBase

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

class ZenPack(ZenPackBase):
    """ ChefClient loader
    """

    packZProperties = [
        ('zChefRole', '', 'string'),
        ]
