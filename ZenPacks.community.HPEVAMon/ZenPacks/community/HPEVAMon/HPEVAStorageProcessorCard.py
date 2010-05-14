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

$Id: HPEVAStorageProcessorCard.py,v 1.1 2010/05/14 18:43:11 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Globals import DTMLFile, InitializeClass
from Products.ZenModel.ExpansionCard import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *
from HPEVAComponent import *

class HPEVAStorageProcessorCard(ExpansionCard, HPEVAComponent):
    """HPStorageProcessorCard object"""

    portal_type = meta_type = 'HPEVAStorageProcessorCard'


    caption = ""
    FWRev = 0

    monitor = True

    _properties = ExpansionCard._properties + (
                 {'id':'caption', 'type':'string', 'mode':'w'},
                 {'id':'FWRev', 'type':'string', 'mode':'w'},
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


    def getStatus(self):
        """
        Return the components status
        """
        return int(round(self.cacheRRDValue('OperationalStatus', 0)))


    def sysUpTime(self):
        """
        Return the controllers UpTime
        """
        return int(round(self.cacheRRDValue('CntrCpuUpTime', -1))) / 10

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

InitializeClass(HPEVAStorageProcessorCard)
