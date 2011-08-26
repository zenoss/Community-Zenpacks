################################################################################
# This program is part of the Zenpack.community.Memcached Zenpack for Zenoss.
# Copyright (C) 2011 B Maqueira
#
# This program can be used under the GNU General Public License version 2
# For complete information please visit: http://www.zenoss.com/oss/
################################################################################

__doc__='''

    MemcachedDatasource.py

    Provides the MemcachedStats datasource for the Zenpacks.community.Memcached
    zenpack by B Maqueira

'''

import Products.ZenModel.BasicDataSource as BasicDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.ZenTales import talesCompile, getEngine
from Products.ZenUtils.Utils import binPath

MEMCACHED_STATS = {
    'accepting_conns':          'GAUGE',
    'bytes':                    'GAUGE',
    'bytes_read':               'GAUGE',
    'bytes_written':            'GAUGE',
    'cas_badval':               'GAUGE',
    'cas_hits':                 'GAUGE',
    'cas_misses':               'GAUGE',
    'cmd_flush':                'GAUGE',
    'cmd_get':                  'GAUGE',
    'cmd_set':                  'GAUGE',
    'conn_yields':              'GAUGE',
    'connection_structures':    'GAUGE',
    'curr_connections':         'GAUGE',
    'curr_items':               'GAUGE',
    'decr_hits':                'GAUGE',
    'decr_misses':              'GAUGE',
    'delete_hits':              'GAUGE',
    'delete_misses':            'GAUGE',
    'evictions':                'GAUGE', 
    'get_hits':                 'GAUGE',
    'get_misses':               'GAUGE',
    'incr_hits':                'GAUGE',
    'incr_misses':              'GAUGE',
    'limit_maxbytes':           'GAUGE',
    'listen_disabled_num':      'GAUGE',
    'pointer_size':             'GAUGE',
    'rusage_system':            'GAUGE',
    'rusage_user':              'GAUGE',
    'threads':                  'GAUGE',
    'time':                     'GAUGE',
    'total_connections':        'GAUGE',
    'total_items':              'GAUGE',
    'uptime':                   'GAUGE',
    'hit_percent':              'GAUGE',
    'usage_percent':            'GAUGE',
    'get_set_ratio':            'GAUGE',
    'missed_percent':           'GAUGE',
}

class MemcachedDataSource(ZenPackPersistence,
                          BasicDataSource.BasicDataSource):

    ZENPACKID = 'ZenPacks.community.Memcached'
    MEMCACHED_STATS = 'MemcachedStats'

    sourcetypes = (MEMCACHED_STATS,)
    sourcetype  = MEMCACHED_STATS

    timeout    = 3 
    eventClass = '/Status/Memcached'
    component  = 'Memcached'
    hostname   = '${dev/id}'
    ipAddress  = '${dev/manageIp}'
    port       = 11211
    parser     = 'Nagios'

    _properties = BasicDataSource.BasicDataSource._properties + (
        {'id':'eventClass', 'type':'string', 'mode':'w'},
        {'id':'hostname',   'type':'string', 'mode':'w'},
        {'id':'ipAddress',  'type':'string', 'mode':'w'},
        {'id':'port',       'type':'int',    'mode':'w'},
        {'id':'timeout',    'type':'int',    'mode':'w'},
        )

    _relations = BasicDataSource.BasicDataSource._relations + ()


    factory_type_information = (
    {
        'immediate_view' : 'editMemcachedDataSource',
        'actions'        :
        (
            { 'id'            : 'edit',
              'name'          : 'Data Source',
              'action'        : 'editMemcachedDataSource',
              'permissions'   : ( Permissions.view, ),
            },
        )
    },
    )

    security = ClassSecurityInfo()

    def __init__(self, id, title=None, buildRelations=True):
        BasicDataSource.BasicDataSource.__init__(self, id, title, buildRelations)


    def getDescription(self):
        if self.sourcetype == self.MEMCACHED_STATS:
            return self.hostname 
        return BasicDataSource.BasicDataSource.getDescription(self)


    def useZenCommand(self):
        return True

    def getCommand(self, context):
        parts = ['check_memcached.py']
        if self.hostname:
            parts.append('-H %s' % self.hostname)
        if self.port:
            parts.append('-p %s' % self.port)
        if self.timeout:
            parts.append("-t %s" % self.timeout)
        cmd = ' '.join(parts)
        cmd = BasicDataSource.BasicDataSource.getCommand(self, context, cmd)
        return cmd

    def checkCommandPrefix(self, context, cmd):
        zp = self.getZenPack(context)
        return zp.path('libexec', cmd)

    def addDataPoints(self):
        for stat, rrdType in MEMCACHED_STATS.items():
            if not self.datapoints._getOb(stat, None):
                dp = self.manage_addRRDDataPoint(stat)

                if rrdType == 'COUNTER':
                    dp.rrdtype = 'DERIVE'
                    dp.rrdmin  = 0
                else:
                    dp.rrdtype = rrdType


    def zmanage_editProperties(self, REQUEST=None):
        '''validation, etc'''
        if REQUEST:
            # ensure default datapoint didn't go away
            self.addDataPoints()
            # and eventClass
            if not REQUEST.form.get('eventClass', None):
                REQUEST.form['eventClass'] = self.__class__.eventClass

            if not REQUEST.form.get('component', None):
                REQUEST.form['component'] = self.__class__.component

        return BasicDataSource.BasicDataSource.zmanage_editProperties(self,
                REQUEST)
