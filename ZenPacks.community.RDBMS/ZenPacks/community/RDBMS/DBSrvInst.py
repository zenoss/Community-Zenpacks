################################################################################
#
# This program is part of the RDBMS Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DBSrvInst

DBSrvInst is a DBSrvInst

$Id: DBSrvInst.py,v 1.0 2010/09/06 13:29:32 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass, DTMLFile
from ZenPacks.community.deviceAdvDetail.HWStatus import *
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenModel.ZenossSecurity import *
from Products.ZenUtils.Utils import prepId
from Products.ZenRelations.RelSchema import *
from Products.ZenWidgets import messaging

from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.Software import Software
from Products.ZenModel.MEProduct import MEProduct

def manage_addDBSrvInst(context, id, userCreated, REQUEST=None):
    """make a database"""
    dbsiid = prepId(id)
    dbsi = DBSrvInst(dbsiid)
    context._setObject(dbsiid, dbsi)
    dbsi = context._getOb(dbsiid)
    dbsi.dbsiname = id
    if userCreated: dbsi.setUserCreateFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main') 

addDBSrvInst = DTMLFile('dtml/addDBSrvInst',globals())

class DBSrvInst(DeviceComponent, Software, HWStatus):
    """
    DBSrvInst object
    """

    ZENPACKID = 'ZenPacks.community.RDBMS'

    portal_type = meta_type = 'DBSrvInst'

    manage_editDBSrvInstForm = DTMLFile('dtml/manageDBSrvInst',globals())

    isUserCreatedFlag = False
    dbsiname = ""
    status = 0

    statusmap ={0: (DOT_GREEN, SEV_CLEAN, 'Up'),
                1: (DOT_RED, SEV_CRITICAL, 'Down'),
                }

    _properties = Software._properties + (
        {'id':'dbsiname', 'type':'string', 'mode':'w'},
        {'id':'status', 'type':'int', 'mode':'w'},
        )


    _relations = MEProduct._relations + (
        ("os", ToOne(ToManyCont, "Products.ZenModel.OperatingSystem", "softwaredbsrvinstances")),
        ("databases", ToMany(ToOne, "ZenPacks.community.RDBMS.Database", "dbsrvinstance")),
        )


    factory_type_information = (
        {
            'id'             : 'DBSrvInst',
            'meta_type'      : 'DBSrvInst',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'FileSystem_icon.gif',
            'product'        : 'RDBMS',
            'factory'        : 'manage_addDBSrvInst',
            'immediate_view' : 'viewDBSrvInst',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDBSrvInst'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'databases'
                , 'name'          : 'Databases'
                , 'action'        : 'viewDBSrvInstDatabase'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE,)
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )


    def setUserCreateFlag(self):
        """
        Sets self.isUserCreatedFlag to True.  This indicated that the
        component was created by a user rather than via modelling.
        """
        self.isUserCreatedFlag = True


    def isUserCreated(self):
        """
        Returns the value of isUserCreated.  See setUserCreatedFlag() above.
        """
        return self.isUserCreatedFlag


    def device(self):
        """
        Return our device object for DeviceResultInt.
        """
        os = self.os()
        if os: return os.device()


    def manage_deleteComponent(self, REQUEST=None):
        """
        Delete OSComponent
        """
        url = None
        if REQUEST is not None:
            url = self.device().os.absolute_url()
        self.getPrimaryParent()._delObject(self.id)
        '''
        eventDict = {
            'eventClass': Change_Remove,
            'device': self.device().id,
            'component': self.id or '',
            'summary': 'Deleted by user: %s' % 'user',
            'severity': Event.Info,
            }
        self.dmd.ZenEventManager.sendEvent(eventDict)
        '''
        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(url)


    def manage_updateComponent(self, datamap, REQUEST=None):
        """
        Update OSComponent
        """
        url = None
        if REQUEST is not None:
            url = self.device().os.absolute_url()
        self.getPrimaryParent()._updateObject(self, datamap)
        '''
        eventDict = {
            'eventClass': Change_Set,
            'device': self.device().id,
            'component': self.id or '',
            'summary': 'Updated by user: %s' % 'user',
            'severity': Event.Info,
            }
        self.dmd.ZenEventManager.sendEvent(eventDict)
        '''
        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(url)


    def getPrettyLink(self):
        """
        Gets a link to this object, plus an icon
        """
        template = ("<a href='%s' class='prettylink'>"
                    "<div class='device-icon-container'> "
                    "<img class='device-icon' src='%s'/> "
                    "</div>%s</a>")
        icon = self.getIconPath()
        href = self.getPrimaryUrlPath()
        name = self.titleOrId()
        return template % (href, icon, name)

    def viewName(self): 
        """
        Return the name of a DB Server Instance
        """
        return self.dbsiname
    name = viewName

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

    def manage_editDBSrvInst(self, monitor=False, dbsiname=None, REQUEST=None):
        """
        Edit a DB Server Instance from a web page.
        """
        if dbsiname:
            self.dbsiname = dbsiname

        self.monitor = monitor
        self.index_object()

        if REQUEST:
            REQUEST['message'] = "DB Server Instance updated"
            messaging.IMessageSender(self).sendToBrowser(
                'DB Server Instance Updated',
                'DB Server Instance %s was updated.' % dbsiname
            )
            return self.callZenScreen(REQUEST)


InitializeClass(DBSrvInst)
