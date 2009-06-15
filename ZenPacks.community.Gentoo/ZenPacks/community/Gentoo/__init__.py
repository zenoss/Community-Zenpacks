
import Globals
import os.path
import logging
from Products.ZenModel.ZenPack import ZenPackBase

log = logging.getLogger('zen.GentooMonitor')

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

def findGentoo(dmd):
    return dmd.findChild('Devices/Server/SSH/Linux/Gentoo')

class ZenPack(ZenPackBase):

    def install(self, app):
        """
        Set the collector plugins for Server/SSH/Linux/Gentoo.
        """
        try:
            gentoo = findGentoo(app.dmd)
        except Exception, e:
            import traceback
            log.debug(traceback.format_exc())
            raise Exception('Device class Server/SSH/Linux/Gentoo does not exist. '
                            'Cannot install Gentoo ZenPack.')
        ZenPackBase.install(self, app)

        plugins=[]
        for plugin in gentoo.zCollectorPlugins:
            if plugin != "zenoss.cmd.uname_a":
                plugins.append(plugin)
            else:
                plugins.append('zenoss.cmd.linux.gentoo_uname_a')

        plugins.append('zenoss.cmd.linux.eix')

        gentoo.setZenProperty( 'zCollectorPlugins', plugins )

        gentoo.register_devtype('Gentoo Server', 'SSH')

    def remove(self, app, leaveObjects=False):
        """
        Remove the collector plugins.
        """
        ZenPackBase.remove(self, app, leaveObjects)
        gentoo = findGentoo(app.dmd)
        if not leaveObjects:
            newlist=[]
            for plugin in gentoo.zCollectorPlugins:
                if plugin == "zenoss.cmd.linux.eix":
                    pass
                elif plugin == "zenoss.cmd.linux.gentoo_uname_a":
                    newlist.append("zenoss.cmd.uname_a")
                else:
                    newlist.append(plugin)


            gentoo.zCollectorPlugins = newlist
