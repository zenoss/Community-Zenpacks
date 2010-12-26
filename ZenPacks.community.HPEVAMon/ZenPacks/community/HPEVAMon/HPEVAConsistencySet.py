################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAConsistencySet

HPEVAConsistencySet is an abstraction of a HPEVA_ConsistencySet

$Id: HPEVAConsistencySet.py,v 1.2 2010/12/06 09:55:38 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Globals import DTMLFile, InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenModel.OSComponent import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *
from HPEVAComponent import *

from Products.ZenUtils.Utils import convToUnits
from Products.ZenUtils.Utils import prepId

import logging
log = logging.getLogger("zen.HPEVAConsistencySet")


def manage_addConsistencySet(context, id, userCreated, REQUEST=None):
    """make ConsistencySet"""
    svid = prepId(id)
    sv = HPEVAConsistencySet(svid)
    context._setObject(svid, sv)
    sv = context._getOb(svid)
    if userCreated: sv.setUserCreatedFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return sv

class HPEVAConsistencySet(OSComponent, HPEVAComponent):
    """HPConsistencySet object"""

    portal_type = meta_type = 'HPEVAConsistencySet'

    caption = ""
    failSafe = ""
    hostAccessMode = ""
    participationType = ""
    remoteCellName = ""
    suspendMode = ""
    writeMode = ""
    state = "OK"

    _properties = OSComponent._properties + (
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'failSafe', 'type':'string', 'mode':'w'},
                 {'id':'hostAccessMode', 'type':'string', 'mode':'w'},
                 {'id':'participationType', 'type':'string', 'mode':'w'},
                 {'id':'remoteCellName', 'type':'string', 'mode':'w'},
                 {'id':'suspendMode', 'type':'string', 'mode':'w'},
                 {'id':'writeMode', 'type':'string', 'mode':'w'},
                 {'id':'state', 'type':'string', 'mode':'w'},
                )

    _relations = OSComponent._relations + (
        ("os", ToOne(ToManyCont,
            "ZenPacks.community.HPEVAMon.HPEVADevice.HPEVADeviceOS",
            "drgroups")),
        ("storagepool", ToOne(ToMany,
            "ZenPacks.community.HPEVAMon.HPEVAStoragePool",
            "drgroups")),
        ("virtualdisks", ToMany(
            ToOne,
            "ZenPacks.community.HPEVAMon.HPEVAStorageVolume",
            "drgroup")),
        )

    factory_type_information = (
        {
            'id'             : 'ConsistencySet',
            'meta_type'      : 'ConsistencySet',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ConsistencySet_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addConsistencySet',
            'immediate_view' : 'viewHPEVAConsistencySet',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPEVAConsistencySet'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'members'
                , 'name'          : 'Members'
                , 'action'        : 'viewHPEVAConsistencySetMembers'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
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


    security.declareProtected(ZEN_CHANGE_DEVICE, 'setStoragePool')
    def setStoragePool(self, spid):
        """
        Set the storagepool relationship to the storage pool specified by the given
        id.
        """
        strpool = getattr(self.os().storagepools, str(spid), None)
        if strpool: self.storagepool.addRelation(strpool)
        else: log.warn("storage pool id:%s not found", spid)


    security.declareProtected(ZEN_VIEW, 'getStoragePool')
    def getStoragePool(self):
        return self.storagepool()


    security.declareProtected(ZEN_VIEW, 'getStoragePoolName')
    def getStoragePoolName(self):
        return getattr(self.getStoragePool(), 'caption', 'Unknown')


    def getCurrentPercentLogLevel(self):
        return "%s%%"%self.cacheRRDValue('CurrentPercentLogLevel', 0)


    def getLogDiskReservedCapacity(self):
        return convToUnits(self.cacheRRDValue('LogDiskReservedCapacity', 0)*512)


    def getRRDNames(self):
        """
        Return the datapoint name of this ConsistencySet
        """
        return ['ConsistencySet_CurrentPercentLogLevel',
                'ConsistencySet_LogDiskReservedCapacity',
                ]

InitializeClass(HPEVAConsistencySet)
