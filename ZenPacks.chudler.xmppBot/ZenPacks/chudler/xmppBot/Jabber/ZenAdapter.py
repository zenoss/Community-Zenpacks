import Globals
import logging
import glob
import logging

log = logging.getLogger('zen.xmppBot')

from Products.ZenUtils.ZCmdBase import ZCmdBase
from Products.AdvancedQuery import MatchGlob, Eq, Or

"""Thin wrapper for accessing and controlling parts of zenoss"""

class ZenAdapter:

    def __init__(self):
        # I don't know a suitable way to get dmd, so
        # ask ZCmdBase for it.
        # FIXME 09JUN09:  This can have side-effects
        cmd = ZCmdBase(noopts = True)
        self.dmd = cmd.dmd
        self.evManager = self.dmd.ZenEventManager
        self.stateMap = self.eventStates()

    def userSettings(self):
        return self.dmd.ZenUsers.getAllUserSettings()

    def newEvents(self):
        """list of all events that are new"""
        newState = self.stateMap['New']
        allEvents = self.events()
        return filter(lambda event: event.eventState == newState, allEvents)

    def acknowledgedEvents(self):
        """list of all events that have been acknowledged"""
        ackState = self.stateMap['Acknowledged']
        allEvents = self.events()
        return filter(lambda event: event.eventState == ackState, allEvents)

    def ackEvents(self, user, eventsToAck):
        """Change list of events to acknowledged"""
	events = self.dmd.ZenEventManager.manage_setEventStates(1, eventsToAck, user)

    def events(self):
        return self.evManager.getEventList()

    def eventStates(self):
        mapping = {}
        for state, num in self.evManager.getEventStates():
            mapping[state] = num
        return mapping

    def devices(self, name):
        """return managed devices from ip, name or mac address
           taken from ZentinelPortal.py"""
        zcatalog = self.dmd.Devices.deviceSearch
        glob = name.rstrip('*') + '*'
        glob = MatchGlob('id', glob)
        query = Or(glob, Eq('getDeviceIp', name))
        brains = zcatalog.evalAdvancedQuery(query)
        brains += self.dmd.Networks.ipSearch.evalAdvancedQuery(glob)
        return [ b.getObject() for b in brains ]

    def loadDevice(self, **kw):
        loader = self.dmd.DeviceLoader
        return loader.loadDevice(**kw)
