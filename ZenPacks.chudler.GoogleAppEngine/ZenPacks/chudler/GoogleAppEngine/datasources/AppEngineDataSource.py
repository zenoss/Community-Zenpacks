__doc__='''AppEngineDataSource.py

Defines datasource for AppEngine collection.  '''

from Products.ZenModel.RRDDataSource import SimpleRRDDataSource
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from ZenPacks.chudler.GoogleAppEngine.AppEngineEvents import *

Base = SimpleRRDDataSource
class AppEngineDataSource(ZenPackPersistence, Base):

    ZENPACKID = 'ZenPacks.chudler.GoogleAppEngine'

    APPENGINE_TYPE = 'AppEngine'

    sourcetypes = (APPENGINE_TYPE,)
    sourcetype = APPENGINE_TYPE

    timeout = 15
    eventClass = '/GoogleAppEngine'
    eventKey = ''   # TODO 03FEB10 figure this out
    component = APPENGINE_TYPE

    ref= '${here/ref}'
    instance=''
    group_key=''
    counter_key=''
    rollup=''
    entitytype=''

    _properties = Base._properties + (
        {'id':'ref', 'type':'string', 'mode':'w'},
        {'id':'instance', 'type':'string', 'mode':'w'},
        {'id':'entitytype', 'type':'string', 'mode':'w'}
        )

    _relations = Base._relations + (
        )

    factory_type_information = (
    {
        'immediate_view' : 'editAppEngineDataSource',
        'actions'        :
        (
            { 'id'            : 'edit',
              'name'          : 'Data Source',
              'action'        : 'editAppEngineDataSource',
              'permissions'   : ( Permissions.view, ),
            },
        )
    },
    )

    security = ClassSecurityInfo()

    def __init__(self, id, title=None, buildRelations=True):
        Base.__init__(self, id, title, buildRelations)

    def getDescription(self):
        if self.sourcetype == self.APPENGINE_TYPE:
            return self.hostname
        return RRDDataSource.getDescription(self)

    def zmanage_editProperties(self, REQUEST=None):
        '''validation, etc'''
        return Base.zmanage_editProperties(self, REQUEST)
