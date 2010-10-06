import re
import os
import string
import Globals
from Products.ZenModel.ZenPackable import ZenPackable
from transaction import commit


class ProfileModify(ZenPackable):
    """ Class to modify device.memberships
    """
    def __init__(self,dmd,devid,groupname):
        self.dmd = dmd
        self.device = self.dmd.Devices.findDeviceByIdOrIp(devid)
        self.groupname = groupname
        self.groups = self.device.getDeviceGroupNames()
        self.systems = self.device.getSystemNames()
        
    def addSystemToDevice(self):
        """ add a system organizer to a device
        """
        groups = self.systems
        if self.groupname not in groups:
            groups.append(self.groupname)
            groups.sort()
            self.device.setSystems(groups)
            commit()

    def removeSystemFromDevice(self):
        """ remove a system organizer from a device
        """
        groups = self.systems
        if self.groupname in groups:
            groups.remove(self.groupname)
            groups.sort()
            self.device.setSystems(groups)
            commit()

    def addGroupToDevice(self):
        """ add a group organizer to a device
        """
        groups = self.groups
        if self.groupname not in groups:
            groups.append(self.groupname)
            groups.sort()
            self.device.setGroups(groups)
            commit()
            
    def removeGroupFromDevice(self):
        """ remove a group organizer from a device
        """
        groups = self.groups
        if self.groupname in groups:
            groups.remove(self.groupname)
            groups.sort()
            self.device.setGroups(groups)
            commit()

            
