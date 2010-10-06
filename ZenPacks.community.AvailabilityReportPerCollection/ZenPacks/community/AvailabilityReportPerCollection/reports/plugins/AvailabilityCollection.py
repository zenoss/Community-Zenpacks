###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import time

from Globals import InitializeClass
from Products.ZenUtils import Map
from Products.ZenUtils import Time
from Products.ZenEvents.ZenEventClasses import Status_Ping, Status_Snmp
from Products.ZenEvents.ZenEventClasses import Status_OSProcess

from AccessControl import ClassSecurityInfo

import logging
log = logging.getLogger("zen.Reports")


CACHE_TIME = 60.

_cache = Map.Locked(Map.Timed({}, CACHE_TIME))

def _round(value):
    if value is None: return None
    return (value // CACHE_TIME) * CACHE_TIME

def _findComponent(device, name):
    for c in device.getMonitoredComponents():
        if c.name() == name:
            return c
    return None

# This is based on the Availability class in $ZENHOME/Products/ZenEvents/Availability.py
# It adds groups and location to the class, as well as systems
class AvailabilityColl:
    security = ClassSecurityInfo()
    security.setDefaultAccess('allow')

    "Simple record for holding availability information"
    def __init__(self, device, component, downtime, total, groups='', Csystems='', location='', DeviceClass=''):
        self.device = device
        self.component = component
        self.groups = groups
        self.Csystems = Csystems
        self.location = location
        self.DeviceClass = DeviceClass

        # Guard against endDate being equal to or less than startDate.
        if total <= 0:
            self.availability = downtime and 0 or 1
        else:
            self.availability = max(0, 1 - (downtime / total))

    def floatStr(self):
        return '%2.3f%%' % (self.availability * 100)

    def __str__(self):
        return self.floatStr()

    def __repr__(self):
        return '[%s %s %s]' % (self.device, self.component, self.floatStr())

    def __float__(self):
        return float(self.availability)

    def __int__(self):
        return int(self.availability * 100)

    def __cmp__(self, other):
        return cmp((self.availability, self.device, self.component()),
                   (other.availability, other.device, other.component()))

    def getDevice(self, dmd):
        return dmd.Devices.findDevice(self.device)

    def getComponent(self, dmd):
        if self.device and self.component:
            device = self.getDevice(dmd)
            if device:
                return _findComponent(device, self.component)
        return None

    def getDeviceLink(self, dmd):
        device = self.getDevice(dmd)
        if device:
            return device.getDeviceLink()
        return None


InitializeClass(AvailabilityColl)

class CReport:
    "Determine availability by counting the amount of time down"

    def __init__(self,
                 startDate = None,
                 endDate = None,
                 eventClass=Status_Ping,
                 severity=5,
                 device=None,
                 component='',
                 groups=None,
                 Csystems=None,
                 location=None,
                 DeviceClass=None):
# Default dd/mm/yyy date resolves to 00:00 local time
# This means startDate is beginning of startDate day but endDate is also the start of endDate day
# If endDate is within 1 day (86400 seconds) of "now" then use "now" as endDate
# This calculation alone tends to provide availabilty close to 0 but not 0 because of likely
# sampling intervals of events - hence 5 mins (300 secs) is subtracted to give endDate
#
# Note that the standard availability report evaluates endDate of "today" to the END of today
# and startDate to START of the date given;
# this means that availability that includes today will not be 0 until the end of today
# Hence you should not closely compare availability from this ZenPack with the standard 
# Availability figures.
        self.startDate = _round(startDate)
        self.endDate = _round(endDate)
        if ((time.time() - self.endDate) < 86400 ):
            self.endDate = time.time() - 300
        self.eventClass = eventClass
        self.severity = severity
        self.device = device
        self.component = component
        self.groups = groups
        self.Csystems = Csystems
        self.location = location
        self.DeviceClass = DeviceClass


    def tuple(self):
        return (
            self.startDate, self.endDate, self.eventClass, self.severity,
            self.device, self.component,
            self.groups, self.Csystems,
            self.location, self.DeviceClass)

    def __hash__(self):
        return hash(self.tuple())

    def __cmp__(self, other):
        return cmp(self.tuple(), other.tuple())


    def run(self, dmd):
        """Run the report, returning an Availability object for each device"""
        # Note: we don't handle overlapping "down" events, so down
        # time could get get double-counted.
#        availColLog = open('/usr/local/zenoss/zenoss/log/availCol.log', 'w')
#        availColLog.write(' Start of run method \n')
        __pychecker__='no-local'
        zem = dmd.ZenEventManager
        cols = 'device, component, firstTime, lastTime'
        prodState = 1000
        endDate = self.endDate or time.time()
        startDate = self.startDate
        if not startDate:
            days = zem.defaultAvailabilityDays
            startDate = time.time() - days*60*60*24
        env = self.__dict__.copy()
        env.update(locals())
        w =  ' WHERE severity >= %(severity)s '
        w += ' AND lastTime > %(startDate)s '
        w += ' AND firstTime <= %(endDate)s '
        w += ' AND firstTime != lastTime '
        w += " AND (eventClass = '%s' OR eventClass LIKE '%s/%%%%') " % (self.eventClass,
                                                                         self.eventClass.rstrip('/'))
        w += " AND prodState >= %(prodState)s "
        if self.device:
            w += " AND device = '%(device)s' "
        if self.component:
            w += " AND component like '%%%(component)s%%' "
#  not None tests don't work as you can only select / not the null string
        if self.location != '/':
            w += " AND (Location = '%s' " % self.location
            w += " OR Location LIKE '%s/%%%%') " % self.location.rstrip('/')
        if self.Csystems != '/':
            w += " AND Systems LIKE '%%%(Csystems)s%%' "
        if self.groups != '/':
            w += " AND DeviceGroups LIKE '%%%(groups)s%%' "
        if self.DeviceClass != '/':
            w += " AND (DeviceClass = '%s' " % self.DeviceClass
            w += " OR DeviceClass LIKE '%s/%%%%') " % self.DeviceClass.rstrip('/')
#        availColLog.write(' in w statement %s \n' %(w))
        env['w'] = w % env
        s = ('SELECT %(cols)s FROM ( '
             ' SELECT %(cols)s FROM history %(w)s '
             '  UNION '
             ' SELECT %(cols)s FROM status %(w)s '
             ') AS U  ' % env)

#        availColLog.write(' after w statement - s is  %s \n' %(s))
        devices = {}
        conn = zem.connect()
        try:
            curs = conn.cursor()
            curs.execute(s)
            while 1:
                rows = curs.fetchmany()
                if not rows: break
                for row in rows:
                    device, component, first, last = row
#                    availColLog.write(' in eval loop - device is  %s, component is %s, first is %12.1f, last is %12.1f  \n' %(device, component, first, last))
                    last = min(last, endDate)
                    first = max(first, startDate)
#                    availColLog.write(' in rows loop - last is  %12.1f, first is %12.1f  \n' %(last,first))
# Next lines commented out are from 3.0.1 Availability.py code.  They mean that you multiple-count
# events for different component values over a potentially overlapping period.  Your total value is
# still only endDate - startDate so you can end up with your totalled downtime greater than
# your total time - this makes a nonsense.  Better to always split out component and do availability
# calculations on device / component pairs.  This is what the comment means at the start of def run
# 
                    # Only treat component specially if a component filter was
                    # specified.
#                    k = None
#                    if self.component:
#                        k = (device, component)
#                    else:
#                        k = (device, '')
                    k = (device, component)
                    try:
                        devices[k] += last - first
                    except KeyError:
                        devices[k] = last - first
        finally: zem.close(conn)
        total = endDate - startDate
#        availColLog.write(' total is %12.1f \n' %(total))
        if self.device:
            deviceList = []
            device = dmd.Devices.findDevice(self.device)
            if device:
                deviceList = [device]
                devices.setdefault( (self.device, self.component), 0)
        else:
            deviceList = []
#            if not self.DeviceClass and not self.location \
#            if not self.DeviceClass and self.location == '/' \
            if self.DeviceClass == '/' and self.location == '/' \
                and self.Csystems == '/' and self.groups == '/':
                deviceList = dmd.Devices.getSubDevices()
            else:
                allDevices = {}
                for d in dmd.Devices.getSubDevices():
                    allDevices[d.id] = d

                deviceClassDevices = set()
                if self.DeviceClass:
                    try:
                        org = dmd.Devices.getOrganizer(self.DeviceClass)
                        for d in org.getSubDevices():
                            deviceClassDevices.add(d.id)
                    except KeyError:
                        pass
                else:
                    deviceClassDevices = set(allDevices.keys())

                locationDevices = set()
                if self.location != '/':
                    try:
                        org = dmd.Locations.getOrganizer(self.location)
                        for d in org.getSubDevices():
                            locationDevices.add(d.id)
                    except KeyError:
                        pass
                else:
                    locationDevices = set(allDevices.keys())

                systemDevices = set()
                if self.Csystems != '/':
                    try:
                        org = dmd.Systems.getOrganizer(self.Csystems)
                        for d in org.getSubDevices():
                            systemDevices.add(d.id)
                    except KeyError:
                        pass
                else:
                    systemDevices = set(allDevices.keys())

                deviceGroupDevices = set()
                if self.groups != '/':
                    try:
                        org = dmd.Groups.getOrganizer(self.groups)
                        for d in org.getSubDevices():
                            deviceGroupDevices.add(d.id)
                    except KeyError:
                        pass
                else:
                    deviceGroupDevices = set(allDevices.keys())

                # Intersect all of the organizers.
                for deviceId in (deviceClassDevices & locationDevices & \
                    systemDevices & deviceGroupDevices):
                    deviceList.append(allDevices[deviceId])

            if not self.component:
                for d in dmd.Devices.getSubDevices():
                    devices.setdefault( (d.id, self.component), 0)
        deviceLookup = dict([(d.id, d) for d in deviceList])
        result = []
        for (d, c), v in devices.items():
#            availColLog.write(' in result loop - d is  %s, c is %s, v is %12.1f  \n' %(d, c, v))
            dev = deviceLookup.get(d, None)
            if dev is None:
                continue
#  Note that groups and systems are lists so convert to strings
# $ZENHOME/Products/ZenModel/Device.py provides getSystemNameString but not getDeviceGroupNamesString
            grp = ', '.join(dev.getDeviceGroupNames())
            sys = dev.getSystemNamesString()
            loc = dev.getLocationName()
            devclass = dev.getDeviceClassPath()
# Only include this device if it is in production state
            if dev.productionState == 1000:
                result.append( AvailabilityColl(d, c, v, total, grp, sys, loc, devclass) )
        # add in the devices that have the component, but no events
        if self.component:
            for d in deviceList:
# Only include this device if it is in production state
                if d.productionState == 1000:
                    for c in d.getMonitoredComponents():
                        if c.name().find(self.component) >= 0:
                            a = AvailabilityColl(d.id, c.name(), 0, total,
                                ', '.join(d.getDeviceGroupNames()), d.getSystemNamesString(), d.getLocationName(), d.getDeviceClassPath())
                            result.append(a)
#        availColLog.close()
        return result


# From $ZENHOME/Products/ZenEvents/Availability.py
def query(dmd, *args, **kwargs):
    r = CReport(*args, **kwargs)
    try:
        return _cache[r.tuple()]
    except KeyError:
        result = r.run(dmd)
        _cache[r.tuple()] = result
        return result

class AvailabilityCollection:
    def run(self, dmd, REQUEST):
        zem = dmd.ZenEventManager

        # Get values
        component    = REQUEST.get('component', '')
        eventClass   = REQUEST.get('eventClass', '/Status/Ping')
        severity     = REQUEST.get('severity', '4')
        device       = REQUEST.get('device', '')
        groups       = REQUEST.get('groups', '/')
        Csystems      = REQUEST.get('Csystems', '/')
        location     = REQUEST.get('location', '/')
        DeviceClass  = REQUEST.get('DeviceClass', '/')
        startDate    = Time.ParseUSDate(REQUEST.get('startDate', zem.defaultAvailabilityStart()))
        endDate      = Time.ParseUSDate(REQUEST.get('endDate', zem.defaultAvailabilityEnd()))

        r = CReport(startDate, endDate, eventClass, severity, device, component, groups, Csystems, location, DeviceClass)
        result = r.run(dmd)
        return result


if __name__ == '__main__':
    import pprint
    r = CReport(time.time() - 60*60*24*30)
    start = time.time() - 60*60*24*30
    # r.component = 'snmp'
    r.component = None
    r.eventClass = Status_Snmp
    r.severity = 3
    from Products.ZenUtils.ZCmdBase import ZCmdBase
    z = ZCmdBase()
    pprint.pprint(r.run(z.dmd))
    a = query(z.dmd, start, device='gate.zenoss.loc', eventClass=Status_Ping)
    assert 0 <= float(a[0]) <= 1.
    b = query(z.dmd, start, device='gate.zenoss.loc', eventClass=Status_Ping)
    assert a == b
    assert id(a) == id(b)
    pprint.pprint(r.run(z.dmd))
    r.component = 'httpd'
    r.eventClass = Status_OSProcess
    r.severity = 4
    pprint.pprint(r.run(z.dmd))
    r.device = 'gate.zenoss.loc'
    r.component = ''
    r.eventClass = Status_Ping
    r.severity = 4
    pprint.pprint(r.run(z.dmd))

