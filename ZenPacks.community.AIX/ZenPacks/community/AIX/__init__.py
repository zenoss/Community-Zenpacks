
import Globals
import os.path
from Products.CMFCore.DirectoryView import registerDirectory
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenUtils.Utils import monkeypatch

#__import__('pkg_resources').declare_namespace(__name__)

# Code to register skins
skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

# Starting to create the menus for our new aixprintqueue objects
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenModel.ZenMenu import ZenMenu

class ZenPack(ZenPackBase):
    packZProperties = [
            ('zVolumeGroupIgnoreNames', '', 'string'),
            ('zLogicalVolumeIgnoreNames', '', 'string'),
            ]

    def install(self, app):
        ZenPackBase.install(self, app)
        self.installMenuItems(app.zport.dmd)
        dc  = app.zport.dmd.Devices.getOrganizer('Devices/Server/AIX')
        #dc._setProperty('zPythonClass', 'ZenPacks.community.AIX.AIXBase')

    def upgrade(self, app):
        ZenPackBase.upgrade(self, app)
        self.installMenuItems(app.zport.dmd)

    def remove(self, app, leaveObjects=False):
        self.removeMenuItems(app.zport.dmd)
        ZenPackBase.remove(self, app, leaveObjects)

    def installMenuItems(self, dmd):
        self.removeMenuItems(dmd)

        # Set an additional item in the More Menu
        #dmd.zenMenus.More.manage_addZenMenuItem("aixprintqueueDetail",
        #                                        action="aixprintqueueDetail",
        #                                        description="Aix Print Queue Details",
        #                                        ordering=5.0)

        # menu_id string:AixPrintQueues;
        # found in template
        pqmenu = ZenMenu('AixPrintQueues')
        dmd.zenMenus._setObject(pqmenu.id, pqmenu)
        pqmenu = dmd.zenMenus._getOb(pqmenu.id)

        # Add the item to the menu
        pqmenu.manage_addZenMenuItem('lockPrintQueue',
                                   action='aixdialog_lockPrintQueues',  # page template that is called
                                   description='Lock print queues...',
                                   ordering=2.0,
                                   isdialog=True)

        pqmenu.manage_addZenMenuItem('changeMonitoring',
                                   action='aixdialog_changePQMonitoring',  # page template that is called
                                   description='Monitoring...',
                                   ordering=0.0,
                                   isdialog=True)


        # menu_id string:AixFileSystem;
        # Do not use Filesystem menu as we are overriding things
        afsmenu = ZenMenu('AixFileSystem')
        dmd.zenMenus._setObject(afsmenu.id, afsmenu)
        afsmenu = dmd.zenMenus._getOb(afsmenu.id)

        # Add the item to the menu
        afsmenu.manage_addZenMenuItem('lockFileSystems',
                                   action='aixdialog_lockFileSystems',  # page template that is called
                                   description='Lock Filesystems...',
                                   ordering=2.0,
                                   isdialog=True)

        afsmenu.manage_addZenMenuItem('changeMonitoring',
                                   action='aixdialog_changeFSMonitoring',  # page template that is called
                                   description='Monitoring...',
                                   ordering=0.0,
                                   isdialog=True)

        # menu_id string:AixVolumeGroups;
        avgmenu = ZenMenu('AixVolumeGroups')
        dmd.zenMenus._setObject(avgmenu.id, avgmenu)
        avgmenu = dmd.zenMenus._getOb(avgmenu.id)

        # Add the item to the menu
        avgmenu.manage_addZenMenuItem('lockVolumeGroups',
                                   action='aixdialog_lockVolumeGroups',  # page template that is called
                                   description='Lock Volume Groups...',
                                   ordering=2.0,
                                   isdialog=True)

        avgmenu.manage_addZenMenuItem('changeMonitoring',
                                   action='aixdialog_changeVGMonitoring',  # page template that is called
                                   description='Monitoring...',
                                   ordering=0.0,
                                   isdialog=True)

        # menu_id string:AixLogicalVolumes;
        alvmenu = ZenMenu('AixLogicalVolumes')
        dmd.zenMenus._setObject(alvmenu.id, alvmenu)
        alvmenu = dmd.zenMenus._getOb(alvmenu.id)

        # Add the item to the menu
        alvmenu.manage_addZenMenuItem('lockLogicalVolumes',
                                   action='aixdialog_lockLogicalVolumes',  # page template that is called
                                   description='Lock Logical Volumes...',
                                   ordering=2.0,
                                   isdialog=True)

        alvmenu.manage_addZenMenuItem('changeMonitoring',
                                   action='aixdialog_changeLVMonitoring',  # page template that is called
                                   description='Monitoring...',
                                   ordering=0.0,
                                   isdialog=True)


        # menu_id string:AixPhysicalVolumes;
        apvmenu = ZenMenu('AixPhysicalVolumes')
        dmd.zenMenus._setObject(apvmenu.id, apvmenu)
        apvmenu = dmd.zenMenus._getOb(apvmenu.id)

        # Add the item to the menu
        apvmenu.manage_addZenMenuItem('lockPhysicalVolumes',
                                   action='aixdialog_lockPhysicalVolumes',  # page template that is called
                                   description='Lock Physical Volumes...',
                                   ordering=2.0,
                                   isdialog=True)

        apvmenu.manage_addZenMenuItem('changeMonitoring',
                                   action='aixdialog_changePVMonitoring',  # page template that is called
                                   description='Monitoring...',
                                   ordering=0.0,
                                   isdialog=True)

        # menu_id string:AixPagingSpaces;
        apsmenu = ZenMenu('AixPagingSpaces')
        dmd.zenMenus._setObject(apsmenu.id, apsmenu)
        apsmenu = dmd.zenMenus._getOb(apsmenu.id)

        # Add the item to the menu
        apsmenu.manage_addZenMenuItem('lockPagingSpaces',
                                   action='aixdialog_lockPagingSpaces',  # page template that is called
                                   description='Lock Paging Spaces...',
                                   ordering=2.0,
                                   isdialog=True)

        apsmenu.manage_addZenMenuItem('changeMonitoring',
                                   action='aixdialog_changePSMonitoring',  # page template that is called
                                   description='Monitoring...',
                                   ordering=0.0,
                                   isdialog=True)

    def removeMenuItems(self,dmd):
        # Remove an additional item in the More Menu
        #id = "aixprintqueueDetail"
        #try:
        #    dmd.zenMenus.More.manage_deleteZenMenuItem(("aixprintqueueDetail",))
        #except (KeyError, AttributeError):
        #    pass

        # Remove the new Menu
        try:
            dmd.zenMenus._delObject('AixPrintQueues')
        except AttributeError:
            pass

        try:
            dmd.zenMenus._delObject('AixFileSystem')
        except AttributeError:
            pass

        try:
            dmd.zenMenus._delObject('AixVolumeGroups')
        except AttributeError:
            pass

        try:
            dmd.zenMenus._delObject('AixLogicalVolumes')
        except AttributeError:
            pass

        try:
            dmd.zenMenus._delObject('AixPhysicalVolumes')
        except AttributeError:
            pass

        try:
            dmd.zenMenus._delObject('AixPagingSpaces')
        except AttributeError:
            pass
