__doc__='''

    MemcachedDatasource.py

    Provides the MemcachedStats datasource for the Zenpacks.community.Memcached
    zenpack by B Maqueira

'''
from Globals import InitializeClass
import Products.ZenModel.BasicDataSource as BasicDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.ZenTales import talesCompile, getEngine
from Products.ZenUtils.Utils import binPath

class MemcachedDataSource(ZenPackPersistence, BasicDataSource.BasicDataSource):

    ZENPACKID = 'ZenPacks.community.Memcached'
    MEMCACHED_STATS = 'MemcachedStats'

    sourcetypes = (MEMCACHED_STATS,)
    sourcetype = MEMCACHED_STATS

    timeout = 3 
    eventClass = '/Status/Memcached'
    component  = 'Memcached'
    hostname = '${dev/id}'
    ipAddress = '${dev/manageIp}'
    port = 11211

    _properties = BasicDataSource.BasicDataSource._properties + (
        {'id':'hostname', 'type':'string', 'mode':'w'},
        {'id':'ipAddress', 'type':'string', 'mode':'w'},
        {'id':'port', 'type':'int', 'mode':'w'},
        {'id':'timeout', 'type':'int', 'mode':'w'},
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
        # create gauges
        for stat in [ 'hit_percent', 'usage_percent', 'uptime', 'time',
                      'rusage_user', 'rusage_system', 'curr_items',
                      'bytes', 'curr_connections', 'connection_structures',
                      'cmd_flush', 'cmd_get', 'cmd_set', 'bytes_read',
                      'bytes_written', 'limit_maxbytes', 'threads', 'accepting_conns',
                      'listen_disabled_num', 'get_set_ratio', 'missed_percent', 
                      'get_hits', 'get_misses', 'total_items']:
            if not self.datapoints._getOb(stat, None):
                self.manage_addRRDDataPoint(stat)

        # and these as counters
        for stat in [ 'total_connections', 'evictions' ]:
            if not self.datapoints._getOb(stat, None):
                dp = self.manage_addRRDDataPoint(stat)
                dp.rrdtype = 'DERIVE'
                dp.rrdmin  = 0

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

InitializeClass(MemcachedDataSource)
