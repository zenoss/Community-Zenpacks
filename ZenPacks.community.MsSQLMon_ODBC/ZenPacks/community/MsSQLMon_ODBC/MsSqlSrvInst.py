################################################################################
#
# This program is part of the MsSQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MsSqlSrvInst

MsSqlSrvInst is a MS SQL Server Instance

$Id: MsSqlSrvInst.py,v 1.1 2010/09/14 14:57:44 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from Globals import InitializeClass

from ZenPacks.community.RDBMS.DBSrvInst import DBSrvInst
from Products.ZenModel.ZenossSecurity import *
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence

class MsSqlSrvInst(DBSrvInst):
    """
    Database Server Instance object
    """

    ZENPACKID = 'ZenPacks.community.MsSQLMon_ODBC'

    edition = ''
    licenseType = ''
    numLicenses = 0
    processID = 0
    productVersion = ''
    productLevel = ''
    dbsiproperties = []

    _properties = DBSrvInst._properties + (
        {'id':'edition', 'type':'string', 'mode':'w'},
        {'id':'licenseType', 'type':'string', 'mode':'w'},
        {'id':'numLicenses', 'type':'int', 'mode':'w'},
        {'id':'processID', 'type':'int', 'mode':'w'},
        {'id':'productVersion', 'type':'string', 'mode':'w'},
        {'id':'productLevel', 'type':'string', 'mode':'w'},
        {'id':'dbsiproperties', 'type':'lines', 'mode':'w'},
        )

    factory_type_information = (
        {
            'id'             : 'MsSqlSrvInst',
            'meta_type'      : 'MsSqlSrvInst',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'FileSystem_icon.gif',
            'product'        : 'MsSQLMon_ODBC',
            'factory'        : 'manage_addDBSrvInst',
            'immediate_view' : 'viewMsSqlSrvInst',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewMsSqlSrvInst'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'databases'
                , 'name'          : 'Databases'
                , 'action'        : 'viewDBSrvInstDatabases'
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

    def manageIp(self):
        """
        Return manageIp with DB Server Instance name if needed
        """
        manageIp = self.device().manageIp
        return '%s\%s' % (manageIp, self.dbsiname)

InitializeClass(MsSqlSrvInst)
