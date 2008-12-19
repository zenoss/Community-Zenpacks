###########################################################################
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
###########################################################################

__doc__='''WMIFilesMonitorDataSource.py

Defines datasource for WMIFilesMonitor
'''

import Products.ZenModel.BasicDataSource as BasicDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.ZenTales import talesCompile, getEngine

import os

class WMIFilesMonitorDataSource(ZenPackPersistence, BasicDataSource.BasicDataSource):

    ZENPACKID = 'ZenPacks.community.WMIFilesMonitor'
    WMIFILES_MONITOR = 'WMIFilesMonitor'
    
    sourcetypes = (WMIFILES_MONITOR,)
    sourcetype = WMIFILES_MONITOR
    timeout = 15
    eventClass = '/Storage/Files'
    fileChecks = '${here/zWMIFileChecks}'
    fileSizes = ''
    autoGraph = True
    hostname = '${dev/manageIp}'
    username = '${here/zWinUser}'
    password = '${here/zWinPassword}'

    _properties = BasicDataSource.BasicDataSource._properties + (
        {'id':'hostname', 'type':'string', 'mode':'w'},
        {'id':'username', 'type':'string', 'mode':'w'},
        {'id':'password', 'type':'string', 'mode':'w'},
        {'id':'fileChecks', 'type':'string', 'mode':'w'},
    	{'id':'fileSizes', 'type':'text', 'mode':'w'},
        {'id':'autoGraph', 'type':'boolean', 'mode':'w'},
        {'id':'timeout', 'type':'int', 'mode':'w'},
        )
        
    _relations = BasicDataSource.BasicDataSource._relations + (
        )

    factory_type_information = ( 
    { 
        'immediate_view' : 'editWMIFilesMonitorDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit',
              'name'          : 'Data Source',
              'action'        : 'editWMIFilesMonitorDataSource',
              'permissions'   : ( Permissions.view, ),
            },
        )
    },
    )

    security = ClassSecurityInfo()

    def __init__(self, id, title=None, buildRelations=True):
        BasicDataSource.BasicDataSource.__init__(self, id, title, buildRelations)

    def getDescription(self):
        if self.sourcetype == self.WMIFILES_MONITOR:
            return self.hostname
        return BasicDataSource.BasicDataSource.getDescription(self)

    def useZenCommand(self):
        return True

    def getCommand(self, context):
        parts = ['check_wmifiles.py']
        if self.hostname:
            parts.append('-H %s' % self.hostname)
        if self.username:
            parts.append('-u %s' % self.username)
        if self.password:
            parts.append("-w '%s'" % self.password)
        if self.fileChecks:
            parts.append('-e %s' % self.fileChecks.strip())
        if self.fileSizes:
            parts.append('-s "%s"' % self.fileSizes.strip().replace('\n', '" "'))
        cmd = ' '.join(parts)
        cmd = BasicDataSource.BasicDataSource.getCommand(self, context, cmd)
        return cmd

    def checkCommandPrefix(self, context, cmd):
        if self.usessh:
            return os.path.join(context.zCommandPath, cmd)
        zp = self.getZenPack(context)
        return zp.path('libexec', cmd)

    def addDataPoints(self):
        if (self.fileSizes.count('\n')) < 1:
            files = [self.fileSizes.strip()]
        else:
            files = [f.strip() for f in self.fileSizes.strip().split('\n')]
        while files.count('') > 0:
            files.remove('')
        n = len(files)
        for i in range(0, n):
            self.manage_addRRDDataPoint('file%i_size' % i)
            if self.autoGraph:
                graphs = self.rrdTemplate().getGraphDefs()
                if not graphs:
                    graph = self.rrdTemplate().manage_addGraphDefinition('File sizes')
                    graph.units = 'Bytes'
                    graph.base = True
                else:
                    graph = graphs[0]
                newgps = self.manage_addDataPointsToGraphs(
                        ['file%i_size' % i], [graph.id])
                graph.getGraphPoints(False)[i].legend = files[i].replace("\\t","\\ t")

    def zmanage_editProperties(self, REQUEST=None):
        '''validation, etc'''
        if REQUEST:
            # ensure default datapoint didn't go away
            self.addDataPoints()
            # and eventClass
            if not REQUEST.form.get('eventClass', None):
                REQUEST.form['eventClass'] = self.__class__.eventClass
        return BasicDataSource.BasicDataSource.zmanage_editProperties(self, REQUEST)


