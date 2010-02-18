"""
This file acts as a shim between google_soup and the consumers of appengine config data and metrics.
If google creates a dashboard API, we might be able to replace google_soup with a real client someday.
"""

import sys
import types, getopt, gc
import logging
from logging import StreamHandler
from datetime import datetime, timedelta
from time import sleep
from itertools import groupby
from ZenPacks.chudler.GoogleAppEngine.AppEngineObjectProperties import ApplicationProperties
from ZenPacks.chudler.GoogleAppEngine.AppEngineInstanceConfiguration import \
    AppEngineInstanceConfiguration

from google_soup import *
from twisted.spread import pb

def createTargetGAEUrl():
    return 'https://appengine.google.com'

class MetricId( pb.Copyable, pb.RemoteCopy):

    instance=''

    def __init__(self, counterId, instance='' ):
        self.counterId=counterId
        self.instance=instance

    def __str__(self):
        retString = str( self.counterId )
        if self.instance and len( self.instance ) > 0:
            retString += '|' + self.instance
        return retString

pb.setUnjellyableForClass(MetricId,MetricId)

clientCache={}

def createGAEClient( username, password,
                     printTrace=False, nocache=False,
                     logseverity=logging.INFO ):
    client=None
    if not nocache and clientCache.has_key(username):
        client = clientCache[username]
        if not client.loggedIn:
            client = None
    if not client:
        client = GAEClient(username,password,printTrace,logseverity)
    if not nocache:
        clientCache[username]=client

    return client

def removeClientFromCache( username ):
    if clientCache.has_key( username ):
        del clientCache[ username ]

def ApplicationCreator(propMaps):
    return map( ApplicationProperties, propMaps )

class GAEClient:

    eventCollector=None
    loggedIn=False

    def __init__(self, username, password, printTrace=False, logSeverity=logging.INFO):
        """Given google credentials, create a GAEClient"""
        self.log = logging.getLogger('gaeclient')
        self.log.setLevel( logSeverity )
        self.url = createTargetGAEUrl()
        self.username = username
        self.password = password
        self.gaeConf = { 'url' : self.url }
        self.googleSoup = GoogleSoup(username, password, logSeverity)
        if printTrace:
            self.gaeConf.update( {'tracefile' : sys.stdout} )

        self.cachedCollector=None

    def login(self):
        """Login to Google"""
        try:
            loginResponse = self.googleSoup.login(self.username, self.password)
            self.loggedIn=True
            return loginResponse
        except SoupLoginError:
            self.loggedIn=False

    def logout(self):
        logoutRequest = LogoutRequestMsg()
        self.loggedIn=False

    def resetPort( self ):
        self.login(self.username,self.password)

    def findHostByIp(self, ipAddress):
        '''
        @ipAddress ip of the host
        @return: vm reference
        Search for the host with the given ip address.
        '''
        findRequest = FindByIpRequestMsg()
        thisParam=findRequest.new__this(self.searchIndex)
        thisParam.set_attribute_type("SearchIndex")
        findRequest.set_element__this(thisParam)
        findRequest.set_element_ip(ipAddress)
        findRequest.set_element_vmSearch(True)
        findResponse=self.vimPort.FindByIp(findRequest)._returnval
        return findResponse

    def getAllApplicationsWithProperties(self, properties=[] ):
        '''
        @properties list of properties to retrieve with each host
        @return a list of ApplicationProperties objects
        '''
        return ApplicationCreator(self.googleSoup.findApplications())

    def getAllApplicationsWithDefaultProperties(self):
        '''
        @return list of GAEProperties with the default
            properties specified in GAEProperties
        '''
        return self.getAllApplicationsWithProperties(
            ApplicationProperties.mapLink.keys() +
            ApplicationProperties.componentMapLink.keys())

    def retrieveDataPoints(self, applicationNames = '__ALL__'):
        '''
        @param applicationName: the application that should be retrieved.
        @return map of stat -> value.
        Retrieve datapoints for AppEngine managed objects (instances, apps, etc).
        '''
        returnMap={}
        applicationName = 'mac2vendor'
        stats = self.googleSoup.queryApplicationPerfs(applicationNames)
        return stats
