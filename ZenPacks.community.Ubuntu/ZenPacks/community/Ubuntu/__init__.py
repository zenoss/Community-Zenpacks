import Globals
import os.path
import logging
from Products.ZenModel.ZenPack import ZenPackBase

log = logging.getLogger('zen.UbuntuMonitor')

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

def findUbuntu(dmd):
    return dmd.findChild('Devices/Server/SSH/Linux/Ubuntu')

class ZenPack(ZenPackBase):

    def install(self, app):
        """
        Set the collector plugins for Server/SSH/Linux/Ubuntu
        """
        try:
            ubuntu = findUbuntu(app.dmd)
        except Exception, e:
            import traceback
            log.debug(traceback.format_exc())
            raise Exception('Device class Server/SSH/Linux/Ubuntu does not exist. '
                            'Cannot install Ubuntu ZenPack.')
        ZenPackBase.install(self, app)

        plugins=[]
        for plugin in ubuntu.zCollectorPlugins:
            if plugin != "zenoss.cmd.uname_a":
                plugins.append(plugin)
            else:
                plugins.append('zenoss.cmd.linux.ubuntu_uname_a')

        plugins.append('zenoss.cmd.linux.ubuntu_aptitude')

        ubuntu.setZenProperty( 'zCollectorPlugins', plugins )

        ubuntu.register_devtype('Ubuntu Server', 'SSH')

    def remove(self, app, leaveObjects=False):
        """
        Remove the collector plugins.
        """
        ZenPackBase.remove(self, app, leaveObjects)
        ubuntu = findUbuntu(app.dmd)
        if not leaveObjects:
            newlist=[]
            for plugin in ubuntu.zCollectorPlugins:
                if plugin == "zenoss.cmd.linux.ubuntu_aptitude":
                    pass
                elif plugin == "zenoss.cmd.linux.ubuntu_uname_a":
                    newlist.append("zenoss.cmd.uname_a")
                else:
                    newlist.append(plugin)

            ubuntu.zCollectorPlugins = newlist
