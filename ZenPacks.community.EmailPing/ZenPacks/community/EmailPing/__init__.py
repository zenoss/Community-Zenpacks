
import Globals
import os.path
import os

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

# Create a simlink to the configuration file. This is so the config can be 
# accessed from the Settings > Daemons page
from Products.ZenUtils.Utils import zenPath
import sys

# The full path to emailping.py is passed as sys.argv[0]. First, we use the
# filename to see if the symlink exists
epFileName = os.path.basename( sys.argv[0] )

# strip '.py' add '.conf'
configFileName = epFileName[:-3] + '.conf'
linkFile = zenPath( 'etc', configFileName )

# if the link file doesn't exist, create it
if not os.path.exists( linkFile ):
    zenpackRootDir = os.path.dirname( sys.argv[0] )
    configFile = os.path.join( zenpackRootDir, 'etc', configFileName )
    if os.path.exists( configFile ):
        try:
            cmd = 'ln -s %s %s' % ( configFile, linkFile )
            os.system( cmd )
        except:
            pass
