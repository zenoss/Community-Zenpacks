import Globals
import os.path
import logging
from Products.ZenModel.ZenPack import ZenPackBase

log = logging.getLogger('zen.SuSEMonitor')

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

def findSuSE(dmd):
    return dmd.findChild('Devices/Server/SSH/Linux/SUSE')

class ZenPack(ZenPackBase):

    def install(self, app):
        """
        Set the collector plugins for Server/SSH/Linux/SUSE
        """
        try:
            suse = findSuSE(app.dmd)
        except Exception, e:
            import traceback
            log.debug(traceback.format_exc())
            raise Exception('Device class Server/SSH/Linux/SUSE does not exist. '
                            'Cannot install SUSE ZenPack.')
        ZenPackBase.install(self, app)

        plugins=[]
        for plugin in suse.zCollectorPlugins:
            if plugin != "zenoss.cmd.uname_a":
                plugins.append(plugin)
            else:
                plugins.append('zenoss.cmd.linux.suse_uname_a')

        plugins.append('zenoss.cmd.linux.suse_rpm')

        suse.setZenProperty( 'zCollectorPlugins', plugins )

        suse.register_devtype('SuSE Server', 'SSH')

    def remove(self, app, leaveObjects=False):
        """
        Remove the collector plugins.
        """
        ZenPackBase.remove(self, app, leaveObjects)
        suse = findSuSE(app.dmd)
        if not leaveObjects:
            newlist=[]
            for plugin in suse.zCollectorPlugins:
                if plugin == "zenoss.cmd.linux.eix":
                    pass
                elif plugin == "zenoss.cmd.linux.suse_uname_a":
                    newlist.append("zenoss.cmd.uname_a")
                else:
                    newlist.append(plugin)

            suse.zCollectorPlugins = newlist
