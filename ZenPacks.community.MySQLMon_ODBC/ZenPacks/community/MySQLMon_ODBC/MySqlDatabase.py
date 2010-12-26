################################################################################
#
# This program is part of the MySQLMon_ODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MySqlDatabase

MySqlDatabase is a Database

$Id: MySqlDatabase.py,v 1.2 2010/10/05 21:20:30 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from ZenPacks.community.RDBMS.Database import Database


class MySqlDatabase(Database):
    """
    MySQL Database object
    """

    ZENPACKID = 'ZenPacks.community.MySQLMon_ODBC'

    collation = ''


    _properties = Database._properties + (
        {'id':'collation', 'type':'string', 'mode':'w'},
        )


    factory_type_information = (
        {
            'id'             : 'MySqlDatabase',
            'meta_type'      : 'MySqlDatabase',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'FileSystem_icon.gif',
            'product'        : 'MySQLMon_ODBC',
            'factory'        : 'manage_addDatabase',
            'immediate_view' : 'viewMySqlDatabase',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewMySqlDatabase'
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


    def totalBytes(self):
        """
        Return the number of total bytes
        """
        su = self.cacheRRDValue('sizeUsed_sizeUsed', 0)
        return long(su) * long(self.blockSize)

    def hostname(self):
        """
        Return the hostname attribute of DBSrvInst
        """
        inst = self.getDBSrvInst()
        if inst: return inst.hostname
        else: return self.device().manageIp

    def port(self):
        """
        Return the port attribute of DBSrvInst
        """
        inst = self.getDBSrvInst()
        if inst: return inst.port
        else: return 3306

    def zMySqlConnectionString(self):
        """
        Return the ODBC connection string
        """
        inst = self.getDBSrvInst()
        if inst: return inst.zMySqlConnectionString()
        else: return 'DRIVER={MySQL}'

InitializeClass(MySqlDatabase)
