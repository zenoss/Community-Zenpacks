import Globals
import re
from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class SentryCDUTowerMap(SnmpPlugin):

    relname = "towers"
    modname = 'ZenPacks.chudler.SentryCDU.Tower'
    
    towers = {
        '.2': 'id',
        '.3': 'sysName',
        '.4': 'status',
        '.5': 'feeds',
    }

    feeds = {
         '.2': 'id',
         '.3': 'sysName',
         '.5': 'status',
         '.6': 'loadStatus',
         '.7': 'load',
         }

    vendors = { 'sentry': '1718.3',
		'rittal': '2606.100.1'
	      }

    snmpGetTableMaps = []
    for vendor, oid in vendors.items():
	towerName = vendor + 'towers'
	towerOid = '.1.3.6.1.4.1.' + oid + '.2.1.1'
	towerMap = GetTableMap(towerName, towerOid, towers)
 	snmpGetTableMaps.append(towerMap)

	feedName = vendor + 'feeds'
	feedOid = '.1.3.6.1.4.1.' + oid + '.2.2.1'
	feedMap = GetTableMap(feedName, feedOid, feeds)
 	snmpGetTableMaps.append(feedMap)

    def process(self, device, results, log):
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        towerRegex = re.compile('^Tower(\w+)_Infeed(\w+)$')
        for vendor, oid in self.vendors.items():
        	towers = tabledata.get(vendor + 'towers')
        	feeds = tabledata.get(vendor + 'feeds')
        	for idx, towerInfo in towers.items():
            		log.info('Found a Tower on this CDU named %s', towerInfo['sysName'])
            		towerInfo['snmpindex'] = oid + '2.1.1.' + str(idx)
            		om = self.objectMap(towerInfo)
            		if not hasattr(om, 'setFeeds'): om.setFeeds = []
            		for feedIdx, feedInfo in feeds.items():
              			feedInfo['snmpindex'] = str(feedIdx)
              			feedInfo['loadOid'] = '.1.3.6.1.4.1.' + oid + '.2.2.1.7.' + str(feedIdx)
              			self.linkFeedtoTower(feedInfo, towerInfo, towerRegex, om, log)
            		rm.append(om)
        return [rm]

    def linkFeedtoTower(self, feed, tower, towerRegex, om, log):
        result = towerRegex.match(feed['sysName'])
        if result:
          feedTowerId, feedId = result.groups()
          if feedTowerId == tower['id']:
            log.info('Found a feed %s for tower %s', feed['id'], feedTowerId)
            # need to store all feed attributes to
            # build the infeed object after collection is complete
            om.setFeeds.append(feed)
