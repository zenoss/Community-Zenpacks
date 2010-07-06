################################################################################
#
# This program is part of the HPEVAMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPEVAHostFCPort

HPEVAHostFCPort is an abstraction of a HPEVA_HostFCPort

$Id: HPEVAHostFCPort.py,v 1.3 2010/06/30 17:09:00 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Globals import DTMLFile, InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenModel.HWComponent import *
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import *
from HPEVAComponent import *

from Products.ZenUtils.Utils import convToUnits

import logging
log = logging.getLogger("zen.HPEVAHostFCPort")

class HPEVAHostFCPort(HWComponent, HPEVAComponent):
    """HPHostFCPort object"""

    portal_type = meta_type = 'HPEVAFCPort'

    interfaceName = ""
    fc4Types = []
    fullDuplex = True
    linkTechnology = ""
    networkAddresses = []
    type = ""
    description = ""
    speed = 0
    mtu = 0
    wwn = ""
    state = "OK"

    _properties = HWComponent._properties + (
                 {'id':'interfaceName', 'type':'string', 'mode':'w'},
                 {'id':'fc4Types', 'type':'lines', 'mode':'w'},
                 {'id':'fullDuplex', 'type':'boolean', 'mode':'w'},
                 {'id':'linkTechnology', 'type':'string', 'mode':'w'},
                 {'id':'networkAddresses', 'type':'lines', 'mode':'w'},
                 {'id':'type', 'type':'string', 'mode':'w'},
                 {'id':'description', 'type':'string', 'mode':'w'},
                 {'id':'speed', 'type':'int', 'mode':'w'},
                 {'id':'mtu', 'type':'int', 'mode':'w'},
                 {'id':'wwn', 'type':'string', 'mode':'w'},
                 {'id':'state', 'type':'string', 'mode':'w'},
                )


    _relations = HWComponent._relations + (
        ("hw", ToOne(ToManyCont,
                    "ZenPacks.community.HPEVAMon.HPEVADeviceHW",
                    "fcports")),
        ("controller", ToOne(ToMany,
                    "ZenPacks.community.HPEVAMon.HPEVAStorageProcessorCard",
                    "fcports")),
        )


    factory_type_information = (
        {
            'id'             : 'HostFCPort',
            'meta_type'      : 'HostFCPort',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HostFCPort_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addHostFCPort',
            'immediate_view' : 'viewHPEVAHostFCPort',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewHPEVAHostFCPort'
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

    security.declareProtected(ZEN_CHANGE_DEVICE, 'setController')
    def setController(self, cid):
        """
        Set the controller relationship to the Controller specified by the given
        id.
        """
        cntr = None
        for controller in self.hw().cards():
            if str(controller.id) != str(cid): continue
            cntr = controller
            break
        if cntr: self.controller.addRelation(cntr)
        else: log.warn("controller id:%s not found", cid)

    security.declareProtected(ZEN_VIEW, 'getController')
    def getController(self):
        try: return self.controller()
        except: return None

    def speedString(self):
        """
        Return the speed in human readable form ie 10MB
        """
        return convToUnits(self.speed, divby=1024)


    def networkString(self):
        """
        Return the networks string
        """
        if self.networkAddresses: return '<br>'.join(self.networkAddresses)
        else: return 'Unknown'

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(HPEVAHostFCPort)
