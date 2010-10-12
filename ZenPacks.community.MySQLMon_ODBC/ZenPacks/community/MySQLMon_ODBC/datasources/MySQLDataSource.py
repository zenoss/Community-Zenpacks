################################################################################
#
# This program is part of the SQLDS_example Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""MySQLDataSource

Defines attributes for how a datasource will be graphed
and builds the nessesary DEF and CDEF statements for it.

$Id: MySQLDataSource.py,v 1.0 2010/06/16 15:17:10 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from ZenPacks.community.SQLDataSource.datasources import SQLDataSource

class MySQLDataSource(SQLDataSource.SQLDataSource):

    ZENPACKID = 'ZenPacks.community.SQLDS_example'

    sourcetypes = ('MySQL',)
    sourcetype = 'MySQL'

    timeout = 15

    hostname = '${dev/manageIp}'
    port = '3306'
    username = '${here/zMySqlUsername}'
    password = '${here/zMySqlPassword}'
    dbname = 'information_schema'

    _properties = SQLDataSource.SQLDataSource._properties + (
        {'id':'dbname', 'type':'string', 'mode':'w'},
        {'id':'hostname', 'type':'string', 'mode':'w'},
        {'id':'port', 'type':'string', 'mode':'w'},
        {'id':'username', 'type':'string', 'mode':'w'},
        {'id':'password', 'type':'string', 'mode':'w'},
        {'id':'timeout', 'type':'int', 'mode':'w'},
        )

    _relations = SQLDataSource.SQLDataSource._relations + (
        )

    # Screen action bindings (and tab definitions)
    factory_type_information = ( 
    { 
        'immediate_view' : 'editMySQLDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit'
            , 'name'          : 'Data Source'
            , 'action'        : 'editMySQLDataSource'
            , 'permissions'   : ( 'View', )
            },
        )
    },
    )


    def getConnectionString(self, context):
        return "MySQLdb,%s"%SQLDataSource.SQLDataSource.getCommand(self,context,
                                        ','.join(["host='%s'"%self.hostname,
                                                 "port=%s"%self.port,
                                                 "user='%s'"%self.username,
                                                 "passwd='%s'"%self.password,
                                                 "db='%s'"%self.dbname,
                                                 ]))


    def zmanage_editProperties(self, REQUEST=None):
        'add some validation'
        if REQUEST:
            self.hostname = REQUEST.get('hostname', '')
            self.port = REQUEST.get('port', '')
            self.username = REQUEST.get('username', '')
            self.password = REQUEST.get('password', '')
            self.dbname = REQUEST.get('dbname', '')
            self.sql = REQUEST.get('sql', '')
            self.sqlparsed, self.sqlkb = self.parseSqlQuery(self.sql)
        return SQLDataSource.SQLDataSource.zmanage_editProperties(self, REQUEST)
