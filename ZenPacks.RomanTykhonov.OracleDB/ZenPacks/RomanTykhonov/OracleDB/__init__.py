###################
#Roman@Tikhonov.org
###################
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())
from Products.ZenModel.ZenPack import ZenPackBase
class ZenPack(ZenPackBase):
      """ Oracle loader
      """
      packZProperties = [
          ('zOracleDBInstance','hpqc','string'),
          ('zOracleUser','sys', 'string'),
          ('zOraclePass','','password'),
          ('zOracleHome','/opt/oracle/client','string'),
          ]

