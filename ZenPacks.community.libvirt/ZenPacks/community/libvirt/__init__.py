
__doc__="libvirt Monitoring ZenPack"

import Globals
import os

from Products.CMFCore.DirectoryView import registerDirectory

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

import ZenPacks.community.libvirt

def initialize(registrar):
    registrar.registerClass( libvirtGuest.libvirtGuest, permission='Add DMD Objects' )
    registrar.registerClass( libvirtPool.libvirtPool, permission='Add DMD Objects' )
    registrar.registerClass( libvirtVolume.libvirtVolume, permission='Add DMD Objects' )


class ZenPack(ZenPackBase):
    """ libvirt loader
    """

    packZProperties = [
            ('zLibvirtConnectType', 'qemu+ssh://', 'string'),
            ('zLibvirtUsername', 'zenoss', 'string'),
            ('zLibvirtPassword', 'password', 'string'),
            ]

