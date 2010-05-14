################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStorageVolume

HPEVAStorageVolume is an abstraction of a HPEVA_StorageVolume

$Id: HPEVAStorageVolume.py,v 1.0 2010/03/09 16:28:27 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import DTMLFile, InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenModel.OSComponent import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *
from HPEVAComponent import *

from AccessControl import ClassSecurityInfo
from Products.ZenUtils.Utils import convToUnits

from Products.ZenUtils.Utils import prepId

import logging
log = logging.getLogger("zen.HPEVAStorageVolume")


def manage_addStorageVolume(context, id, userCreated, REQUEST=None):
    """make StorageVolume"""
    svid = prepId(id)
    sv = HPEVAStorageVolume(svid)
    context._setObject(svid, sv)
    sv = context._getOb(svid)
    if userCreated: sv.setUserCreatedFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return sv

class HPEVAStorageVolume(OSComponent, HPEVAComponent):
    """HPStorageVolume object"""

    portal_type = meta_type = 'HPEVAStorageVolume'

    accessType = ""
    caption = ""
    blockSize = 0
    mirrorCache = ""
    preferredPath = ""
    raidType = ""
    readCachePolicy = ""
    writeCachePolicy = ""
    diskType = ""
    
    _properties = OSComponent._properties + (
                 {'id':'accessType', 'type':'string', 'mode':'w'},
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'blockSize', 'type':'int', 'mode':'w'},
                 {'id':'mirrorCache', 'type':'string', 'mode':'w'},
                 {'id':'preferredPath', 'type':'string', 'mode':'w'},
                 {'id':'raidType', 'type':'string', 'mode':'w'},
                 {'id':'readCachePolicy', 'type':'string', 'mode':'w'},
                 {'id':'writeCachePolicy', 'type':'string', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                )    

    _relations = OSComponent._relations + (
        ("os", ToOne(ToManyCont,
	    "ZenPacks.community.HPEVAMon.HPEVADevice.HPEVADeviceOS",
	    "virtualdisks")),
        ("storagepool", ToOne(ToMany,
	    "ZenPacks.community.HPEVAMon.HPEVAStoragePool",
	    "virtualdisks")),
	)

    factory_type_information = ( 
        { 
            'id'             : 'StorageVolume',
            'meta_type'      : 'StorageVolume',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'StorageVolume_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addStorageVolume',
            'immediate_view' : 'viewHPEVAStorageVolume',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPEVAStorageVolume'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : ("Change Device", )
                },                
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )


    security = ClassSecurityInfo()

    security.declareProtected('Change Device', 'setStoragePool')
    def setStoragePool(self, spid):
        """
        Set the storagepool relationship to the storage pool specified by the given
        id.
        """
        strpool = None
        for storagepool in self.os().storagepools():
            if storagepool.id != spid: continue
	    strpool = storagepool
	    break
        if strpool: self.storagepool.addRelation(strpool)
        else: log.warn("storage pool id:%s not found", spid)

    security.declareProtected('View', 'getStoragePool')
    def getStoragePool(self):
        try: return self.storagepool()
	except: return None

    def getStatus(self):
        """
        Return the components status
	"""
        return int(round(self.cacheRRDValue('OperationalStatus', 0)))


    def totalBytes(self):
        """
        Return the number of total bytes
        """
        return self.cacheRRDValue('NumberOfBlocks', 0) * self.blockSize

    def totalBytesString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.totalBytes(), divby=1024)

    def viewName(self): 
        """
        Return the mount point name of a filesystem '/boot'
        """
        return self.caption
    name = viewName

InitializeClass(HPEVAStorageVolume)
