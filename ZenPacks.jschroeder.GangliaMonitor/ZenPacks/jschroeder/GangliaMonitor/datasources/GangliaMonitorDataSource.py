###########################################################################
#
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

__doc__='''GangliaMonitorDataSource.py

Defines datasource for GangliaMonitor
'''

import Products.ZenModel.BasicDataSource as BasicDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.ZenTales import talesCompile, getEngine

import os

class GangliaMonitorDataSource(ZenPackPersistence,
                                BasicDataSource.BasicDataSource):
    GANGLIA_MONITOR = 'GangliaMonitor'
    ZENPACKID = 'ZenPacks.jschroeder.GangliaMonitor'

    sourcetypes = (GANGLIA_MONITOR,)
    sourcetype = GANGLIA_MONITOR

    timeout    = 60
    eventClass = '/Status/Ganglia'
    host = '${dev/zGangliaHost}'
    port = '${dev/zGangliaPort}'

    _properties = BasicDataSource.BasicDataSource._properties + (
            {'id':'timeout',    'type':'int', 'mode':'w'},
            {'id':'eventClass', 'type':'string', 'mode':'w'},
            {'id':'host', 'type':'string', 'mode':'w'},
            {'id':'port', 'type':'string', 'mode':'w'},
            )

    _relations = BasicDataSource.BasicDataSource._relations + (
            )

    factory_type_information = (
        {
            'immediate_view': 'editGangliaMonitorDataSource',
            'actions':
            (
                { 'id': 'edit',
                  'name': 'Data Source',
                  'action': 'editGangliaMonitorDataSource',
                  'permissions': ( Permissions.view ),
                },
            )
        },
    )

    security = ClassSecurityInfo()


    def __init__(self, id, title=None, buildRelations=True):
        BasicDataSource.BasicDataSource.__init__(self, id, title,
                buildRelations)


    def getDescription(self):
        if self.sourcetype == self.GANGLIA_MONITOR:
            return self.hostname
        return BasicDataSource.BasicDataSource.getDescription(self)


    def useZenCommand(self):
        return True


    def getCommand(self, context):
        parts = ['check_ganglia.py', self.host, self.port, '${dev/manageIp}', str(self.cycletime)]
        cmd = ' '.join(parts)
        cmd = BasicDataSource.BasicDataSource.getCommand(self, context, cmd)
        return cmd

    def checkCommandPrefix(self, context, cmd):
        zp = self.getZenPack(context)
        return zp.path('libexec', cmd)

    def addDataPoints(self):
        for dpname in ('bytes_in', 'bytes_out', 'cpu_idle', 'cpu_nice',
                       'cpu_system', 'cpu_user', 'cpu_wio', 'disk_free',
                       'disk_total', 'lastUpdate', 'load_fifteen', 'load_five',
                       'load_one', 'mem_buffers', 'mem_cached', 'mem_free',
                       'mem_shared', 'mem_total', 'pkts_in', 'pkts_out',
                       'proc_run', 'proc_total', 'swap_free', 'swap_total'):
            dp = self.manage_addRRDDataPoint(dpname)
            dp.rrdtype = 'GAUGE'
            dp.rrdmin = 0

    def zmanage_editProperties(self, REQUEST=None):
        '''validation, etc'''
        if REQUEST:
            self.addDataPoints()
            if not REQUEST.form.get('eventClass', None):
                REQUEST.form['eventClass'] = self.__class__.eventClass
        return BasicDataSource.BasicDataSource.zmanage_editProperties(self,
                REQUEST)

