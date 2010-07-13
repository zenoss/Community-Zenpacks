################################################################################
#
# This program is part of the ZenODBC Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""OdbcDataSource

Defines attributes for how a datasource will be graphed
and builds the nessesary DEF and CDEF statements for it.

$Id: OdbcDataSource.py,v 1.4 2010/06/15 16:40:35 egor Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from ZenPacks.community.SQLDataSource.datasources import SQLDataSource

class OdbcDataSource(SQLDataSource.SQLDataSource):

    ZENPACKID = 'ZenPacks.community.ZenODBC'

    sourcetypes = ('ODBC',)
    sourcetype = 'ODBC'

    _properties = SQLDataSource.SQLDataSource._properties + (
        )

    _relations = SQLDataSource.SQLDataSource._relations + (
        )

    # Screen action bindings (and tab definitions)
    factory_type_information = ( 
    { 
        'immediate_view' : 'editODBCDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit'
            , 'name'          : 'Data Source'
            , 'action'        : 'editODBCDataSource'
            , 'permissions'   : ( 'View', )
            },
        )
    },
    )


    def getConnectionString(self, context):
        return "findodbc, '%s'"%SQLDataSource.SQLDataSource.getCommand(self,
                                                                    context,
                                                                    self.cs)
