################################################################################
#
# This program is part of the RDBMS Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""databases

Databases reports plugin

$Id: databases.py,v 1.1 2010/09/12 18:28:05 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

import Globals
from Products.ZenReports import Utils, Utilization
from Products.ZenReports.AliasPlugin import AliasPlugin, Column, \
                                            RRDColumnHandler, PythonColumnHandler

class databases( AliasPlugin ):
    "The databases report"

    def getColumns(self):
        ##      alias/dp id : column name
        return [ Column( 'deviceName', PythonColumnHandler( 'device.titleOrId()' ) ),
                 Column( 'instance', PythonColumnHandler( 'component.dbSrvInstName()' ) ),
                 Column( 'dbname', PythonColumnHandler( 'component.dbname' ) ),
                 Column( 'type', PythonColumnHandler( 'component.type' ) ),
                 Column( 'usedBytes', RRDColumnHandler( 'component.usedBytes()' ) ),
                 Column( 'totalBytes', PythonColumnHandler( 'component.totalBytes()' ) ) ]

    def getCompositeColumns(self):
        return [ Column( 'availableBytes', PythonColumnHandler('totalBytes - usedBytes') ),
                 Column( 'percentFull', PythonColumnHandler( 'totalBytes and ' +
                        '( 100 - float(availableBytes) * 100 / float(totalBytes) )' +
                        ' or None' ) ) ]

    def getComponentPath(self):
        return 'os/softwaredatabases'

