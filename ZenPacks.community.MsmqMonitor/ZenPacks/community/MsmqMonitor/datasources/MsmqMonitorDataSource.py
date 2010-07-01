
__doc__='''MsmqMonitorDataSource.py

Defines data source for "MsmqMonitor"

'''

from Globals import InitializeClass

import Products.ZenModel.RRDDataSource as RRDDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions

class MsmqMonitorDataSource(ZenPackPersistence, RRDDataSource.RRDDataSource):

    ZENPACKID = 'ZenPacks.community.MsmqMonitor'

    MSMQ_MONITOR = 'MsmqMonitor'
    sourcetypes = (MSMQ_MONITOR,)
    sourcetype = MSMQ_MONITOR

    eventClass = '/Win/MSMQ'

    hostname = '${dev/manageIp}'
    username = '${here/zWinUser}'
    password = '${here/zWinPassword}'
    queuename= '${here/id}'

    _properties = RRDDataSource.RRDDataSource._properties + (
            {'id':'hostname', 'type':'string', 'mode':'w'},
            {'id':'username', 'type':'string', 'mode':'w'},
            {'id':'password', 'type':'string', 'mode':'w'},
            {'id':'queuename','type':'string', 'mode':'w'},
            )

    _relations = RRDDataSource.RRDDataSource._relations + ()

    _factory_type_information = ({
        'immediate_view'    : 'editMsmqMonitorDataSource',
        'actions'           : (
           { 'id'           : 'edit'
            ,'name'         : 'Data Source'
            ,'action'       : 'editMsmqMonitorDataSource'
            ,'permissions'  : (Permissions.view,)
            },
            )
        },)

    security = ClassSecurityInfo()

    def __init__(self, id, title=None, buildRelations=True):
        RRDDataSource.RRDDataSource.__init__(self, id, title, buildRelations)

    def getDescription(self):
        if self.sourcetype == self.MSMQ_MONITOR:
            return self.hostname
        return RRDDataSource.RRDDataSource.getDescription(self)

    def useZenCommand(self):
        return True

    def checkCommandPrefix(self, context, cmd):
        return self.getZenPack(context).path('libexec',cmd)

    def getCommand(self, context):
        parts = ['MsmqGetCount.py']
        if self.hostname:
            parts.append(self.hostname)
        if self.username:
            parts.append(self.username)
        if self.password:
            parts.append(self.password)
        if self.queuename:
            parts.append(self.queuename)
        cmd = ' '.join(parts)
        cmd = RRDDataSource.RRDDataSource.getCommand(self, context, cmd)
        return cmd

    def addDataPoints(self):
        if not hasattr(self.datapoints,'queueCount'):
            self.manage_addRRDDataPoint('queueCount')

    def zmanage_editProperties(self, REQUEST=None):
        if REQUEST:
            self.addDataPoints()
            if not REQUEST.form.get('eventClass',None):
                REQUEST.form['eventClass'] = self.__class__.eventClass
        return RRDDataSource.RRDDataSource.zmanage_editProperties(self, REQUEST)


InitializeClass(MsmqMonitorDataSource)

