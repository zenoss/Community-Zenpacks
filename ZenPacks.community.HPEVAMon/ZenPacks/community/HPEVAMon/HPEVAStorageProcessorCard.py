################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAStorageProcessorCard

HPEVAStorageProcessorCard is an abstraction of a HPEVA_StorageProcessorCard

$Id: HPEVAStorageProcessorCard.py,v 1.2 2010/05/18 13:37:38 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Globals import DTMLFile, InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenModel.ExpansionCard import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *
from HPEVAComponent import *

class HPEVAStorageProcessorCard(ExpansionCard, HPEVAComponent):
    """HPStorageProcessorCard object"""

    portal_type = meta_type = 'HPEVAStorageProcessorCard'


    caption = ""
    FWRev = 0
    state = "OK"

    monitor = True

    _properties = ExpansionCard._properties + (
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'FWRev', 'type':'string', 'mode':'w'},
                 {'id':'state', 'type':'string', 'mode':'w'},
                )

    _relations = ExpansionCard._relations + (
        ("fcports", ToMany(ToOne,
                    "ZenPacks.community.HPEVAMon.HPEVAHostFCPort",
                    "controller")),
        )

    factory_type_information = (
        {
            'id'             : 'HPEVAStorageProcessorCard',
            'meta_type'      : 'HPEVAStorageProcessorCard',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'StorageProcessorCard_icon.gif',
            'product'        : 'HPEVAMon',
            'factory'        : 'manage_addExpansionCard',
            'immediate_view' : 'viewHPEVAStorageProcessorCard',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPEVAStorageProcessorCard'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'fcports'
                , 'name'          : 'FC Ports'
                , 'action'        : 'viewHPEVAStorageProcessorCardPorts'
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

    security.declareProtected(ZEN_VIEW, 'getManufacturerLink')
    def getManufacturerLink(self, target=None):
        if self.productClass():
            url = self.productClass().manufacturer.getPrimaryLink()
            if target: url = url.replace(">", " target='%s'>" % target, 1)
            return url
        return ""

    security.declareProtected(ZEN_VIEW, 'getProductLink')
    def getProductLink(self, target=None):
        url = self.productClass.getPrimaryLink()
        if target: url = url.replace(">", " target='%s'>" % target, 1)
        return url

    def sysUpTime(self):
        """
        Return the controllers UpTime
        """
        cpuUpTime = round(self.cacheRRDValue('CntrCpuUpTime', -1))
        if cpuUpTime == -1: return -1
        return cpuUpTime / 10

    def uptimeString(self):
        """
        Return the controllers uptime string

        @rtype: string
        @permission: ZEN_VIEW
        """
        ut = self.sysUpTime()
        if ut < 0:
            return "Unknown"
        elif ut == 0:
            return "0d:0h:0m:0s"
        ut = float(ut)/100.
        days = ut/86400
        hour = (ut%86400)/3600
        mins = (ut%3600)/60
        secs = ut%60
        return "%02dd:%02dh:%02dm:%02ds" % (
            days, hour, mins, secs)

    def getRRDNames(self):
        """
        Return the datapoint name of this StorageProcessorCard
        """
        return ['StorageProcessorCard_CntrCpuUpTime']

InitializeClass(HPEVAStorageProcessorCard)
