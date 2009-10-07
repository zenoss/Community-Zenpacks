# -*- coding: utf-8 -*-
import Globals
import os.path
import logging
from Products.ZenModel.ZenPack import ZenPackBase

log = logging.getLogger('zen.MandrivaMonitor')

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

def findMandriva(dmd):
    return dmd.findChild('Devices/Server/SSH/Linux/Mandriva')

class ZenPack(ZenPackBase):

    def install(self, app):
        """
        Set the collector plugins for Server/SSH/Linux/Mandriva
        """
        try:
            mandriva = findMandriva(app.dmd)
        except Exception, e:
            import traceback
            log.debug(traceback.format_exc())
            raise Exception('Device class Server/SSH/Linux/Mandriva does not exist. '
                            'Cannot install Mandriva ZenPack.')
        ZenPackBase.install(self, app)

        plugins=[]
        for plugin in mandriva.zCollectorPlugins:
            if plugin != "zenoss.cmd.uname_a":
                plugins.append(plugin)
            else:
                plugins.append('zenoss.cmd.linux.mandriva_uname_a')

        plugins.append('zenoss.cmd.linux.mandriva_rpm')

        mandriva.setZenProperty( 'zCollectorPlugins', plugins )

        mandriva.register_devtype('Mandriva Server', 'SSH')

    def remove(self, app, leaveObjects=False):
        """
        Remove the collector plugins.
        """
        ZenPackBase.remove(self, app, leaveObjects)
        mandriva = findMandriva(app.dmd)
        if not leaveObjects:
            newlist=[]
            for plugin in mandriva.zCollectorPlugins:
                if plugin == "zenoss.cmd.linux.mandriva_rpm":
                    pass
                elif plugin == "zenoss.cmd.linux.mandriva_uname_a":
                    newlist.append("zenoss.cmd.uname_a")
                else:
                    newlist.append(plugin)

            mandriva.zCollectorPlugins = newlist
