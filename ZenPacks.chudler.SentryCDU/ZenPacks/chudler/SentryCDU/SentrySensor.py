from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_VIEW

#from Products.DataCollector.SnmpClient import SnmpClient
#from Products.DataCollector.plugins.CollectorPlugin import GetMap
from twisted.internet import defer, reactor
from Products.ZenUtils.Driver import drive
from pynetsnmp.twistedsnmp import AgentProxy

import logging

_kw = dict(mode='w')
TIMEOUT = 0.05                  # Set the timeout for poll/select

class SentrySensor(DeviceComponent, ManagedEntity):
    "A probe on a ServTech CDU.  The probe senses temperature and humidity."
    
    portal_type = meta_type = 'SentrySensor'

    snmpindex = -1
    sysName = ''
    tempProbeStatus = 6
    humProbeStatus = 6
    scale = -1
    tempOid = ''
    result = -1
    humidityOid = ''
    humidity = -1
    temperature = -2
    # finished with snmp defered?
    finished = False
    result = None

    _properties = (
        dict(id='snmpindex',  	type='int',	**_kw),
        dict(id='tempOid',  	type='string',	**_kw),
        dict(id='temperature', 	type='int',	**_kw),
        dict(id='humidity', 	type='int',	**_kw),
        dict(id='humidityOid',  	type='string',	**_kw),
        dict(id='sysName',  	type='string',	**_kw),
        dict(id='tempProbeStatus',  	type='int',	**_kw),
        dict(id='humProbeStatus',  	type='int',	**_kw),
        dict(id='scale',  	type='int',	**_kw),
        dict(id='id',  		type='string',	**_kw),
        )

    _relations = ( ('sentrydevice', ToOne(ToManyCont, 'ZenPacks.chudler.SentryCDU.SentryDevice', 'sentrysensors')),
        )

    factory_type_information = (
        {   
            'id'             : 'SentrySensor',
            'meta_type'      : 'SentrySensor',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'SentrySensor.gif',
            'product'        : 'ZenPacks.chudler.SunILOM.SentrySensor',
            'factory'        : 'manage_addSentrySensor',
            'immediate_view' : 'viewSentrySensor',
            'actions'        :
            (   
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewSentrySensor'
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
        return self.sentrydevice()

    def snmpIgnore(self):
        return ManagedEntity.snmpIgnore(self) or self.snmpindex < 0

    def statusBool(self):
        self.tempProbeStatus == 0 and self.humProbeStatus == 0
 
    def cmdHumidity(self):
        """
        Return a command that will give the current humidity for
	use in templates.
        """
	humidity = self.humidityFromSnmp()
	self.humidity = humidity
	return '/bin/echo -n "OK|relative=%s;;;;"' % self.humidity

    def humidityString(self):
        """
        Return the current humidity in degrees celsius as a string
        """
        return self.humidity is None and "unknown" or "%dR" % (self.humidity)

    def humidityFromSnmp(self):
        self.humidity = -2
        humidity = self.fetchOid(self.humidityOid)
	self.humidity = humidity
        return self.humidity

    def cmdTemperature(self):
        """
        Return a command that will give the current temperature for
	use in templates.
        """
	log = logging.getLogger('zen.ZenEvent')
	log.info('SENTRY: CMD TEMPERATURE RUNNING!!!')
	self.temperature = self.tempFromSnmp()
	log.info('GOT TEMP FROM SNMP: %s' % self.temperature)
	return '/bin/echo -n "OK|temp=%s;;;;"' % self.temperature

    def temperatureString(self):
        """
        Return the current temperature in degrees celsius as a string
        """
        temp = self.temperature
        return temp is None and "unknown" or "%dF" % (temp,)

    def tempFromSnmp(self):
        self.temperature = -2
	log = logging.getLogger('zen.ZenEvent')
	log.info('SENTRY: SENSOR FETCHING OID')
        temp = self.fetchOid(self.tempOid)
	log.info('SENTRY: FINISHED FETCHING, GOT TEMP %s' % temp)
	temp = self.temperature = long(temp) / 10
	if temp:
       	    if self.scale == 2 or self.scale == 0:
                # the cdu is set to celsius.  Convert to F.
                # some vendors allow the scale to be set to ZERO, which could be celsius
                temp = ((temp * 9) / 5) + 32
        return temp

    def fetchOid(self, oid):
        """
        Retrieve a single value from the device using the +oid+ supplied.
        This is necessary here because Zenoss component templates can only use
        SNMP index, but Sentry devices come from multiple vendors with their own
        MIB trees.
        """
        parent = self.device()
        proxy = AgentProxy(parent.id, parent.zSnmpPort, timeout=parent.zSnmpTimeout, community=parent.zSnmpCommunity, snmpVersion=parent.zSnmpVer, tries=2)
        proxy.open()
	log = logging.getLogger('zen.ZenEvent')
	log.info('SENTRY fetch FETCHING OID %s.  Got proxy open already' % oid)

        defered = proxy.get([ oid ])

        self.finished = False
        defered.addBoth(self.gotResult, proxy, oid)
        defered.addErrback(self.gotFailure)

	# wait until this call is done
        while not self.finished:
            reactor.iterate(TIMEOUT)

        return self.result

    def gotResult(self, result, proxy, oid):
	log = logging.getLogger('zen.ZenEvent')
	log.info('SENTRY: SENSOR FETCHING OID')
	log.info('SENTRY: GOT RESULT!!!!!!!!!!!!!!!!!!! %s' % result)
        proxy.close()
        self.result = result[oid]
	log.info('SENTRY: GOT RESULT!!!!!!!!!!!!!!!!!!! %s' % self.result)
	self.finished = True
        return self.result

    def gotFailure(self, why):
	log = logging.getLogger('zen.ZenEvent')
	log.info('SENTRY: SENSOR FETCHING OID')
	log.info('SENTRY: GOT FAILURE!!!!!!!!!!!!!!!!!!! %s' % why)
        self.finished = True

InitializeClass(SentrySensor)
