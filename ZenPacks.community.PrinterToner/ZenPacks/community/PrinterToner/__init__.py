################################################################################
#
# This program is part of the PrinterToner Zenpack for Zenoss.
# Copyright (C) 2009 Tonino Greco & Zenoss Inc.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

import Globals
import os
from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenModel.ZenPack import ZenPackBase


skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

class ZenPack(ZenPackBase):
    # Zepack addition of printerTonerMap on install and remove on de-install
    # generic installer - just set the 2 variables below
    new_plugin = "community.snmp.PrinterTonerMap"
    #object = app.zport.dmd.Devices.Printer.Laser

    # install the zpython class for the printertoner tab to be displayed
    def install(self, app):
        ZenPackBase.install(self, app)
        dc  = app.zport.dmd.Devices.getOrganizer('Devices/Printer/Laser')
        dc._setProperty('zPythonClass', 'ZenPacks.community.PrinterToner.PrinterTonerDevice')
        self.modifyPlugins(app.zport.dmd.Devices.Printer.Laser,"add")

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        self.modifyPlugins(app.zport.dmd.Devices.Printer.Laser,"add")

    def remove(self, app, leaveObjects=False):
        self.modifyPlugins(app.zport.dmd.Devices.Printer.Laser,"remove")
        #ZenPackBase.remove(app, leaveObjects)
        ZenPackBase.remove(self, app)

    def modifyPlugins(self, obj, action):
        newPlugins = []
        for plugin in obj.zCollectorPlugins:
            if plugin == self.new_plugin:
                continue
            else:
                newPlugins.append(plugin)
        if action == "add":
            newPlugins.append(self.new_plugin)
        obj.zCollectorPlugins = newPlugins

