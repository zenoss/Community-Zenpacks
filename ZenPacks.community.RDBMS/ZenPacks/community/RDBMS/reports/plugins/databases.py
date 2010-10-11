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

$Id: databases.py,v 1.2 2010/09/20 23:56:15 egor Exp $"""

__version__ = "$Revision: 1.2 $"[11:-2]

import Globals
from Products.ZenUtils.ZenTales import talesEval
from Products.ZenReports import Utils, Utilization
from Products.ZenReports.AliasPlugin import AliasPlugin, Column, \
                                            RRDColumnHandler, PythonColumnHandler


class databases( AliasPlugin ):
    "The databases report"

    def _getComponents(self, device, componentPath):
        componentPath='here/%s' % componentPath
        try:
            return talesEval( componentPath, device )
        except:
            return []

    def getColumns(self):
        ##      alias/dp id : column name
        return [ Column( 'deviceName', PythonColumnHandler( 'device.titleOrId()' ) ),
                 Column( 'instance', PythonColumnHandler( 'component.getDBSrvInstLink()' ) ),
                 Column( 'dbname', PythonColumnHandler( 'component.dbname' ) ),
                 Column( 'type', PythonColumnHandler( 'component.type' ) ),
                 Column( 'usedBytes', PythonColumnHandler( 'component.usedBytes()' ) ),
                 Column( 'totalBytes', PythonColumnHandler( 'component.totalBytes()' ) ) ]

    def getCompositeColumns(self):
        return [ Column( 'availableBytes', PythonColumnHandler('totalBytes - usedBytes') ),
                 Column( 'percentFull', PythonColumnHandler( 'totalBytes and ' +
                        '( 100 - float(availableBytes) * 100 / float(totalBytes) )' +
                        ' or None' ) ) ]

    def getComponentPath(self):
        return 'os/softwaredatabases'

