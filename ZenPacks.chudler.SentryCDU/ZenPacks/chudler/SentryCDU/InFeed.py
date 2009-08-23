from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from twisted.internet import defer, reactor
from Products.ZenUtils.Driver import drive
from pynetsnmp.twistedsnmp import AgentProxy

import logging

_kw = dict(mode='w')
TIMEOUT = 0.05

class InFeed(DeviceComponent, ManagedEntity):
    "A feed of power coming into the CDU through a tower"
    
    portal_type = meta_type = 'InFeed'

    snmpindex = -1
    sysName = ''
    status = 1
    loadStatus = ''
    load = -1
    loadOid = ''
    finished = False

    _properties = (
        dict(id='snmpindex',  	type='int',	**_kw),
        dict(id='sysName',  	type='string',	**_kw),
        dict(id='status',  	type='int',	**_kw),
        dict(id='loadStatus',  	type='int',	**_kw),
        dict(id='load',  	type='int',	**_kw),
        dict(id='loadOid',  	type='string',	**_kw),
        dict(id='id',  		type='string',	**_kw),
        )

    _relations = ( ('towers', ToOne(ToManyCont, 'ZenPacks.chudler.SentryCDU.Tower', 'infeeds')),
        )

    factory_type_information = (
        {   
            'id'             : 'InFeed',
            'meta_type'      : 'InFeed',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'InFeed_icon.gif',
            'product'        : 'ZenPacks.chudler.SunILOM.InFeed',
            'factory'        : 'manage_addInFeed',
            'immediate_view' : 'viewInFeed',
            'actions'        :
            (   
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewInFeed'
                , 'permissions'   : ('View',)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : ("Change Device", )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW,)
                },
            )
          },
        )

    def device(self):
        return self.towers().device()

    def towerId(self):
        return self.towers().id

    def snmpIgnore(self):
        return False
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0

    def statusBool(self):
        self.status == 0 or False

    def cmdLoad(self):
        """
        Return a command that will give the current load for
        use in templates.
        """
        log = logging.getLogger('zen.hub')
        log.info('ASDF: InFeed, cmd loadfrom snmp')
        load = self.loadFromSnmp()
        return '/bin/echo -n "OK|amps=%s;;;;"' % self.load

    def loadString(self):
        """
        Return the current load in degrees celsius as a string
        """
        return self.load is None and "unknown" or "%dF" % (self.load,)
    loadString = loadString

    def loadFromSnmp(self):
        self.load = -2
        self.load = self.fetchLoad()
        return self.load

    def fetchLoad(self):
        parent = self.device()
        proxy = AgentProxy(parent.id, parent.zSnmpPort, timeout=parent.zSnmpTimeout, community=parent.zSnmpCommunity, snmpVersion=parent.zSnmpVer, tries=2)
        proxy.open()
        d = proxy.get([ self.loadOid ])

        self.finished = False
        d.addBoth(self.gotResult, proxy)
        d.addErrback(self.gotFailure)

        # wait until this call is done
        while not self.finished:
            reactor.iterate(TIMEOUT)

        return self.load

    def gotResult(self, result, proxy):
        proxy.close()
        self.load = long(result[self.loadOid]) / 10
        self.finished = True
        return self.load

    def gotFailure(self, why):
        self.finished = True

    
InitializeClass(InFeed)
