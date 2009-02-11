import Globals
import os
from os.path import join
from Products.ZenModel.ZenPack import ZenPackBase
from Products.CMFCore.DirectoryView import registerDirectory

registerDirectory("skins", globals())

libexec = os.path.join(os.path.dirname(__file__), 'libexec')

class ZenPack(ZenPackBase):
   """ ZenPacks.community.VMwareEsx loader
   """

   packZProperties = [
       ('zZenPackCommunityVMwareESXlibexec', libexec, 'string'),
       ]
