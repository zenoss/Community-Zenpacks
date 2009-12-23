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
from Products.ZenEvents.Availability import Availability

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

InitializeClass(Availability)

class Report:
    "Determine availability by counting the amount of time down"

    def __init__(self,
                 startDate = None,
                 endDate = None,
                 eventClass=Status_Ping,
                 severity=5,
                 device=None,
                 component='',
                 groupName=''):
        self.startDate = _round(startDate)
        self.endDate = _round(endDate)
        self.eventClass = eventClass
        self.severity = severity
        self.device = device
        self.component = component
        self.groupName = groupName


    def tuple(self):
        return (self.startDate, self.endDate, self.eventClass,
                self.severity, self.device, self.component)

    def __hash__(self):
        return hash(self.tuple())

    def __cmp__(self, other):
        return cmp(self.tuple(), other.tuple())


    def run(self, dmd):
        log.debug('in method report run')

        """Run the report, returning an Availability object for each device"""
        # Note: we don't handle overlapping "down" events, so down
        # time could get get double-counted.
        __pychecker__='no-local'
        zem = dmd.ZenEventManager
        cols = 'device, component, firstTime, lastTime'
        endDate = self.endDate or time.time()
        startDate = self.startDate
        if not startDate:
            days = zem.defaultAvailabilityDays
            startDate = time.time() - days*60*60*24
        env = self.__dict__.copy()
        env.update(locals())

        severity = self.severity
        groupName = self.groupName
    
        log.debug('groupName: %s', groupName)

        w =  ' WHERE severity >= %(severity)s '
        w += " AND DeviceGroups LIKE '%%%(groupName)s%%' "
        w += ' AND lastTime > %(startDate)s '
        w += ' AND firstTime <= %(endDate)s '
        w += ' AND firstTime != lastTime '
        w += " AND eventClass = '%(eventClass)s' "
        w += " AND prodState >= 1000 "
        if self.device:
            w += " AND device = '%(device)s' "
        if self.component:
            w += " AND component like '%%%(component)s%%' "
        env['w'] = w % env
        s = ('SELECT %(cols)s FROM ( '
             ' SELECT %(cols)s FROM history %(w)s '
             '  UNION '
             ' SELECT %(cols)s FROM status %(w)s '
             ') AS U  ' % env)
                  
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
                    last = min(last, endDate)
                    first = max(first, startDate)
                    k = (device, component)
                    try:
                        devices[k] += last - first
                    except KeyError:
                        devices[k] = last - first
        finally: zem.close(conn)
        total = endDate - startDate
        if self.device:
            log.debug('self.device defined')

            deviceList = []
            device = dmd.Devices.findDevice(self.device)
            if device:
                deviceList = [device]
                devices.setdefault( (self.device, self.component), 0)
        else:
            log.debug('self.undevice defined')
            groupNameLong = 'Groups'
            groupNameLong += groupName
            log.debug('groupNameLong: %s', groupNameLong)

            deviceList = [d for d in dmd.Groups.getDmdObj(groupNameLong).getSubDevices()]
            if not self.component:
                for d in dmd.Groups.getDmdObj(groupNameLong).getSubDevices():
                    devices.setdefault( (d.id, self.component), 0)
        deviceLookup = dict([(d.id, d) for d in deviceList])
        result = []
        for (d, c), v in devices.items():
            dev = deviceLookup.get(d, None)
            sys = (dev and dev.getSystemNamesString()) or ''
            result.append( Availability(d, c, v, total, sys) )
        # add in the devices that have the component, but no events
        if self.component:
            for d in deviceList:
                for c in d.getMonitoredComponents():
                    if c.name().find(self.component) >= 0:
                        a = Availability(d.id, c.name(), 0, total, 
                                                        d.getSystemNamesString())
                        result.append(a)
        return result


def query(dmd, *args, **kwargs):
    log.debug('in method query')
    r = Report(*args, **kwargs)
# caching disabled
#    try:
#        return _cache[r.tuple()]
#    except KeyError:
#        result = r.run(dmd)
#        _cache[r.tuple()] = result
#        return result
    result = r.run(dmd)
    _cache[r.tuple()] = result
    return result


class AvailabilityByGroup:
    def run(self, dmd, REQUEST):
        zem = dmd.ZenEventManager

        # Get values
        component    = REQUEST.get('component', '')
        eventClasses = REQUEST.get('eventClasses', '/Status/Ping')
        severity     = REQUEST.get('severity', '4')
        device       = REQUEST.get('device', '')
        groupName    = REQUEST.get('groupName', '/')
        startDate    = Time.ParseUSDate(REQUEST.get('startDate', zem.defaultAvailabilityStart()))
        endDate      = Time.ParseUSDate(REQUEST.get('endDate', zem.defaultAvailabilityEnd()))

        r = Report(startDate, endDate, eventClasses, severity, device, component, groupName)
        result = r.run(dmd)
        return result


if __name__ == '__main__':
    import pprint
    r = Report(time.time() - 60*60*24*30)
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
