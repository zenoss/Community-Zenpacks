###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2009, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
import os

from Products.CMFCore.DirectoryView import registerDirectory

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    
    def install(self, app):
        """
        Add transforms to mutate add/change events from the modeler to
        migration events between esx servers.
        """
        ZenPackBase.install(self, app)

        add = app.dmd.Events.createOrganizer('/Change/Add')
        if add.transform.find('VMWARE TRANSFORM') < 0:
            add.transform = add.transform + """
#START VMWARE TRANSFORM
if evt.message.find('guestDevices') > -1:
    evt._action = 'status'
    evt.severity = 3
    evt.eventClass = '/VMware/MigrateAcquire'
    evt.summary = 'Acquire vm %s' % evt.component
#END VMWARE TRANSFORM
"""
        remove = app.dmd.Events.createOrganizer('/Change/Remove')
        if remove.transform.find('VMWARE TRANSFORM') < 0:
            remove.transform = remove.transform + """
#START VMWARE TRANSFORM
if evt.message.find('guestDevices') > -1:
    evt._action = 'status'
    evt.severity = 3
    evt.eventClass = '/VMware/MigrateRelease'
    evt.summary = 'Release vm %s' % evt.component
#END VMWARE TRANSFORM
"""

