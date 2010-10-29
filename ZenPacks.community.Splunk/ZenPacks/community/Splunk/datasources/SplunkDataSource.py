######################################################################
#
# Copyright 2009 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

from AccessControl import ClassSecurityInfo
from Products.ZenModel.BasicDataSource import BasicDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenModel.ZenossSecurity import *
from Products.ZenWidgets import messaging


class SplunkDataSource(ZenPackPersistence, BasicDataSource):
    ZENPACKID = 'ZenPacks.community.Splunk'

    sourcetypes = ('Splunk',)
    sourcetype = 'Splunk'

    timeout = 60
    eventClass = '/App/Splunk'

    splunkServer = ''
    splunkPort = '8089'
    splunkUsername = ''
    splunkPassword = ''
    splunkSearch = ''

    _properties = BasicDataSource._properties + (
        dict(id='splunkServer', type='string', mode='w'),
        dict(id='splunkPort', type='string', mode='w'),
        dict(id='splunkUsername', type='string', mode='w'),
        dict(id='splunkPassword', type='string', mode='w'),
        dict(id='splunkSearch', type='string', mode='w'),
        )

    factory_type_information = (dict(
        immediate_view='editSplunkDataSource',
        actions=(
            dict(
                id='edit',
                name='Splunk Data Source',
                action='editSplunkDataSource',
                permissions=ZEN_VIEW),
            )
        ),)

    security = ClassSecurityInfo()


    def useZenCommand(self):
        return True


    def getDescription(self):
        return "%s: %s" % (
            self.splunkServer or "SPLUNK_SERVER", self.splunkSearch)


    def getCommand(self, context):
        parts = ['check_splunk.py']
        if self.splunkServer:
            parts.append("-s %s" % self.splunkServer)
        if self.splunkPort:
            parts.append("-p %s" % self.splunkPort)
        if self.splunkUsername:
            parts.append("-u '%s'" % self.splunkUsername)
        if self.splunkPassword:
            parts.append("-w '%s'" % self.splunkPassword)
        if self.splunkSearch:
            parts.append("'%s'" % self.splunkSearch)
        return BasicDataSource.getCommand(self, context, ' '.join(parts))


    def checkCommandPrefix(self, context, cmd):
        return self.getZenPack(context).path('libexec', cmd)


    def zmanage_editProperties(self, REQUEST=None):
        """Validate input before updating properties."""
        if REQUEST:
            if not REQUEST.form.get('splunkSearch'):
                messaging.IMessageSender(self).sendToBrowser(
                    'Update Failed',
                    'Search cannot be blank.',
                    priority=messaging.WARNING)
                return self.callZenScreen(REQUEST)
        return BasicDataSource.zmanage_editProperties(self, REQUEST)
