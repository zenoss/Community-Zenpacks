import Globals
import os.path
import logging
from Products.ZenModel.ZenPack import ZenPackBase

log = logging.getLogger('zen.LinuxMonitorAddon')

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

def findLinux(dmd):
    return dmd.findChild('Devices/Server/SSH/Linux')

class ZenPack(ZenPackBase):
    def install(self, app):
        """
        Set the collector plugins for Server/SSH/Linux.
        """
        try:
            linux = findLinux(app.dmd)
        except Exception, e:
            import traceback
            log.debug(traceback.format_exc())
            raise Exception('Device class Server/SSH/Linux does not exist. '
                            'Cannot install LinuxMonitor ZenPack.')
        ZenPackBase.install(self, app)

        plugins=[]
        for plugin in linux.zCollectorPlugins:
            plugins.append(plugin)

        plugins.append('zenoss.cmd.linux.cpuinfo')
        plugins.append('zenoss.cmd.linux.memory')
        plugins.append('zenoss.cmd.linux.ifconfig')
        plugins.append('zenoss.cmd.linux.netstat_an')
        plugins.append('zenoss.cmd.linux.netstat_rn')
        plugins.append('zenoss.cmd.linux.process')

        linux.setZenProperty( 'zCollectorPlugins', plugins )
