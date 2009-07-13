import Globals
import os.path
import logging
from Products.ZenModel.ZenPack import ZenPackBase

log = logging.getLogger('zen.OpenSolaris')

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

def findSolaris(dmd):
    return dmd.findChild('Devices/Server/SSH/Solaris')

class ZenPack(ZenPackBase):
    def install(self, app):
        """
        Set the collector plugins for Server/SSH/Solaris.
        """
        try:
            solaris = findSolaris(app.dmd)
        except Exception, e:
            import traceback
            log.debug(traceback.format_exc())
            raise Exception('Device class Server/SSH/Solaris does not exist. '
                            'Cannot install Solaris ZenPack.')
        ZenPackBase.install(self, app)

        plugins=[]
        for plugin in solaris.zCollectorPlugins:
            plugins.append(plugin)

        plugins.append('zenoss.cmd.solaris.opensolaris_uname_a')
        plugins.append('zenoss.cmd.solaris.cpu')
        plugins.append('zenoss.cmd.solaris.memory')
        plugins.append('zenoss.cmd.solaris.ifconfig')
        plugins.append('zenoss.cmd.solaris.netstat_an')
        plugins.append('zenoss.cmd.solaris.netstat_r_vn')
        plugins.append('zenoss.cmd.solaris.process')
        plugins.append('zenoss.cmd.solaris.pkginfo')
        plugins.append('zenoss.cmd.solaris.df')

        solaris.setZenProperty( 'zCollectorPlugins', plugins )

