__doc__='''
    TTyrantDatasource.py

    This datasource is part of the Zenpacks.community.TokyoTyrant Zenpack
    by B Maqueira / http://codelab.ferrarihaines.com

    It defines the datasource TokyoTyrantStats
'''
from Globals import InitializeClass
import Products.ZenModel.BasicDataSource as BasicDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.ZenTales import talesCompile, getEngine
from Products.ZenUtils.Utils import binPath

class TTyrantDataSource(ZenPackPersistence, BasicDataSource.BasicDataSource):

    ZENPACKID = 'ZenPacks.community.TokyoTyrant'
    TOKYO_TYRANT_STATS = 'TokyoTyrantStats'

    sourcetypes = (TOKYO_TYRANT_STATS,)
    sourcetype = TOKYO_TYRANT_STATS
    
    timeout = 3
    eventClass = '/Status/TokyoTyrant'
    component  = 'TokyoTyrant'
    hostname = '${dev/id}'
    ipAddress = '${dev/manageIp}'
    port = 1978

    _properties = BasicDataSource.BasicDataSource._properties + (
        {'id':'hostname', 'type':'string', 'mode':'w'},
        {'id':'ipAddress', 'type':'string', 'mode':'w'},
        {'id':'port', 'type':'int', 'mode':'w'},
        {'id':'timeout', 'type':'int', 'mode':'w'},
        )

    _relations = BasicDataSource.BasicDataSource._relations + ()


    factory_type_information = (
    {
        'immediate_view' : 'editTTDataSource',
        'actions'        :
        (
            { 'id'            : 'edit',
              'name'          : 'Data Source',
              'action'        : 'editTTDataSource',
              'permissions'   : ( Permissions.view, ),
            },
        )
    },
    )

    security = ClassSecurityInfo()

    def __init__(self, id, title=None, buildRelations=True):
        BasicDataSource.BasicDataSource.__init__(self, id, title, buildRelations)


    def getDescription(self):
        if self.sourcetype == self.TOKYO_TYRANT_STATS:
            return self.hostname 
        return BasicDataSource.BasicDataSource.getDescription(self)


    def useZenCommand(self):
        return True

    def getCommand(self, context):
        parts = ['check_ttserver.py']
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
        for stat in [ 'hit_percent', 'get_set_ratio', 'missed_percent',
                  'pointer_size', 'rusage_user',
                  'rusage_system', 'cmd_set', 'cmd_set_hits',
                  'cmd_set_misses', 'cmd_delete', 'cmd_delete_hits',
                  'cmd_delete_misses', 'cmd_get', 'cmd_get_hits',
                  'cmd_get_misses', 'cmd_flush', 'curr_items',
                  'total_items', 'bytes', 'threads']:
            if not self.datapoints._getOb(stat, None):
                self.manage_addRRDDataPoint(stat)

    def zmanage_editProperties(self, REQUEST=None):
        '''validation, etc'''
        if REQUEST:
            self.addDataPoints()
            if not REQUEST.form.get('eventClass', None):
                REQUEST.form['eventClass'] = self.__class__.eventClass

            if not REQUEST.form.get('component', None):
                REQUEST.form['component'] = self.__class__.component

        return BasicDataSource.BasicDataSource.zmanage_editProperties(self,
                REQUEST)

InitializeClass(TTyrantDataSource)
