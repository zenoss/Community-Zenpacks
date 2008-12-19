###########################################################################
#
#
# Copyright (C) 2008, Learning Objects Inc, http://www.learningobjects.com
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
#
###########################################################################

__doc__='''PostgresqlMonitorDataSource.py

Defines datasource for PostgresqlMonitor
'''

import Products.ZenModel.BasicDataSource as BasicDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.ZenTales import talesCompile, getEngine

import os


class PostgresqlMonitorDataSource(ZenPackPersistence,
                                BasicDataSource.BasicDataSource):
    
    POSTGRESQL_MONITOR = 'PostgresqlMonitor'

    ZENPACKID = 'ZenPacks.LearningObjects.PostgresqlMonitor'

    sourcetypes = (POSTGRESQL_MONITOR,)
    sourcetype = POSTGRESQL_MONITOR

    timeout = 15
    eventClass = '/Status/POSTGRESQL'

    hostname = '${dev/manageIp}'
    port = 5432
    username = '${here/zPostgresqlUsername}'
    password = '${here/zPostgresqlPassword}'
    database = '${here/zPostgresqlDatabase}'
    _properties = BasicDataSource.BasicDataSource._properties + (
        {'id':'hostname', 'type':'string', 'mode':'w'},
        {'id':'port', 'type':'int', 'mode':'w'},
        {'id':'database', 'type':'string', 'mode':'w'},
	{'id':'username', 'type':'string', 'mode':'w'},
        {'id':'password', 'type':'string', 'mode':'w'},
        {'id':'timeout', 'type':'int', 'mode':'w'},
        )
        
    _relations = BasicDataSource.BasicDataSource._relations + (
        )


    factory_type_information = ( 
    { 
        'immediate_view' : 'editPostgresqlMonitorDataSource',
        'actions'        :
        ( 
            { 'id'            : 'edit',
              'name'          : 'Data Source',
              'action'        : 'editPostgresqlMonitorDataSource',
              'permissions'   : ( Permissions.view, ),
            },
        )
    },
    )

    security = ClassSecurityInfo()


    def __init__(self, id, title=None, buildRelations=True):
        BasicDataSource.BasicDataSource.__init__(self, id, title,
                buildRelations)


    def getDescription(self):
        if self.sourcetype == self.POSTGRESQL_MONITOR:
            return self.hostname
        return BasicDataSource.BasicDataSource.getDescription(self)


    def useZenCommand(self):
        return True


    def getCommand(self, context):
        parts = ['check_postgresql_stats.py']
        if self.hostname:
            parts.append('-H %s' % self.hostname)
        if self.port:
            parts.append('-p %s' % self.port)
        if self.username:
            parts.append('-u %s' % self.username)
        if self.password:
            parts.append("-w '%s'" % self.password)
        if self.database:
            parts.append("-d '%s'" % self.database)
        
	cmd = ' '.join(parts)
        cmd = BasicDataSource.BasicDataSource.getCommand(self, context, cmd)
        return cmd


    def checkCommandPrefix(self, context, cmd):
        if self.usessh:
            return os.path.join(context.zCommandPath, cmd)
        zp = self.getZenPack(context)
        return zp.path('libexec', cmd)


    def addDataPoints(self):
        dps = (
       		

		('blks_hit', 'COUNTER'),	
		('blks_read', 'COUNTER'),	
		('db_size', 'GAUGE'), 	
		('heap_blks_hit', 'COUNTER'),	
		('heap_blks_read', 'COUNTER'),	
		('idx_blks_hit', 'COUNTER'),	
		('idx_blks_read', 'COUNTER'),	
		('idx_scan', 'COUNTER'),	
		('idx_tup_fetch', 'COUNTER'),	
		('n_tup_del', 'COUNTER'),	
		('n_tup_ins', 'COUNTER'),	
		('n_tup_upd', 'COUNTER'),	
		('numbackends', 'GAUGE'),	
		('seq_scan', 'COUNTER'),	
		('seq_tup_read', 'COUNTER'),	
		('tidx_blks_hit', 'COUNTER'),	
		('tidx_blks_read', 'COUNTER'),	
		('toast_blks_hit', 'COUNTER'),	
		('toast_blks_read', 'COUNTER'),	
		('tup_deleted', 'COUNTER'),	
		('tup_fetched', 'COUNTER'),	
		('tup_inserted', 'COUNTER'),	
		('tup_returned', 'COUNTER'),	
		('tup_updated', 'COUNTER'),	
		('xact_commit', 'COUNTER'),	
		('xact_rollback', 'COUNTER'),	

	)

        for dpd in dps:
            dp = self.manage_addRRDDataPoint(dpd[0])
            dp.rrdtype = dpd[1]
            dp.rrdmin = 0


    def zmanage_editProperties(self, REQUEST=None):
        '''validation, etc'''
        if REQUEST:
            # ensure default datapoint didn't go away
            self.addDataPoints()
            # and eventClass
            if not REQUEST.form.get('eventClass', None):
                REQUEST.form['eventClass'] = self.__class__.eventClass
        return BasicDataSource.BasicDataSource.zmanage_editProperties(self,
                REQUEST)
