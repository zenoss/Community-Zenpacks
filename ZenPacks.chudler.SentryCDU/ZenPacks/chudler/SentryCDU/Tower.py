from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenModelRM import ZenModelRM
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

from ZenPacks.chudler.SentryCDU.InFeed import *

import logging

_kw = dict(mode='w')

class Tower(DeviceComponent, ManagedEntity):
    "A tower takes in feeds of power (phases) entering into the CDU"
    
    portal_type = meta_type = 'Tower'

    status = ''
    sysName = ''
    feeds = 0
    aggregateData = 0
    snmpindex = '-1'

    _properties = (
        # dict(id='infeeds',      type='lines', setter='setFeeds', **_kw),
        dict(id='id',  		type='int',	**_kw),
        dict(id='sysName',  	type='string',	**_kw),
        dict(id='status',  	type='int',	**_kw),
        dict(id='aggregateData',  	type='int',	**_kw),
        dict(id='feeds',  	type='int',	**_kw),
        dict(id='snmpindex',  	type='int',	**_kw),
        )

    _relations = (
        ("infeeds", ToManyCont(ToOne, "ZenPacks.chudler.SentryCDU.InFeed", "towers")),
        ('sentrydevice', ToOne(ToManyCont, 'ZenPacks.chudler.SentryCDU.SentryDevice', 'towers')),
        )

    factory_type_information = (
        {   
            'id'             : 'Tower',
            'meta_type'      : 'Tower',
            'description'    : 'Tower Description',
            'icon'           : 'Device_icon.gif',
            'product'        : 'ZenPacks.chudler.SunILOM.Tower',
            'factory'        : 'manage_addTower',
            'immediate_view' : 'towerPerformance',
            'actions'        :
            (   
                { 'id'            : 'perf'
                , 'name'          : 'towerPerformance'
                , 'action'        : 'towerPerformance'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'templates'
                , 'name'          : 'Templates'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_SETTINGS, )
                },
                )
            },
        )

    # used in a command template to get total tower load in a datapoint
    # FIXME:  better way to do this?
    def aggregateLoad(self):
        return '/bin/echo -n "OK|load=%s;;;;"' % (self.aggregateLoadInt())

    def aggregateLoadInt(self):
        log = logging.getLogger('zen.ZenEvent')
	log.info('SENTRY: Tower getting aggregate load')
        total = 0
        for feed in self.getFeedObjs():
            amps = feed.loadFromSnmp()
            if amps:
                total += amps
	log.info('SENTRY: TOWER aggregate load is: %s' % total)
        return total
    aggregateLoadInt = aggregateLoadInt

    def setFeeds(self, feeds):
        # remove all currently known feeds
        for feed_id in self.infeeds.objectIds(): self.infeeds._delObject(feed_id)
        for feedId in feeds:
            self.setFeed(feedId)

    def statusBool(self):
        self.status == 0 or False

    def setFeed(self, feed):
        inFeedObj = InFeed(feed['id'])
        # set properties here so we don't have to
        # override __init__ on InFeed
        inFeedObj.sysName = feed['sysName']
        inFeedObj.status = feed['status']
        inFeedObj.load = feed['load']
        inFeedObj.loadOid = feed['loadOid']
        inFeedObj.loadStatus = feed['loadStatus']
        inFeedObj.snmpindex = feed['snmpindex']
        self.infeeds._setObject(inFeedObj.id, inFeedObj)

    def getFeedObjs(self):
        retval = []
        for feed in self.infeeds.objectValuesAll():
            retval.append(feed)
        return retval

    def feedLinks(self):
        links = []
        for feed in self.getFeedObjs():
            links.append(ZenModelRM.urlLink(feed, feed.getId()))
        return ", ".join(links)

    def getFeeds(self):
        return map(str, self.getFeedObjs())

    def device(self):
        return self.sentrydevice()

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0
    
InitializeClass(Tower)
