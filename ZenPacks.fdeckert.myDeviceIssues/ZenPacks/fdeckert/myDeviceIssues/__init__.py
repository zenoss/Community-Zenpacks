from Products.ZenModel.ZenossSecurity import ZEN_COMMON
from Products.ZenUtils.Utils import zenPath
from Products.CMFCore.DirectoryView import registerDirectory
from time import localtime,strftime
import re
import Globals
import os

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """
    Portlet ZenPack class
    """

    def install(self, app):
        """
        Initial installation of the ZenPack
        """
        ZenPackBase.install(self, app)
        self._registermyDeviceIssuesPortlet(app)

    def upgrade(self, app):
        """
        Upgrading the ZenPack procedures
        """
        ZenPackBase.upgrade(self, app)
        self._registermyDeviceIssuesPortlet(app)

    def remove(self, app, leaveObjects=False ):
        """
        Remove the ZenPack from Zenoss
        """
        # NB: As of Zenoss 2.2, this function now takes three arguments.
        ZenPackBase.remove(self, app, leaveObjects)
        zpm = app.zport.ZenPortletManager
        zpm.unregister_portlet('myDeviceIssuesPortlet')

    def _registermyDeviceIssuesPortlet(self, app):
        zpm = app.zport.ZenPortletManager
        portletsrc=os.path.join(os.path.dirname(__file__),'lib','myDeviceIssuesPortlet.js')
        #Its a dirty hack - register_portlet will add ZenPath one more time
        #and we don't want to hardcode path explicitly here
        p=re.compile(zenPath(''))
        portletsrc=p.sub('',portletsrc)
        zpm.register_portlet(
            sourcepath=portletsrc,
            id='myDeviceIssuesPortlet',
            title='myDeviceIssues',
            permission=ZEN_COMMON)

import simplejson
import pdb

def getmyDeviceIssuesJSON(self, path='/Devices'):
	"""
        Get devices with issues in a form suitable for a portlet on the
        dashboard.

        @return: A JSON representation of a dictionary describing devices
        @rtype: "{
            'columns':['Device', "Events'],
            'data':[
                {'Device':'<a href=/>', 'Events':'<div/>'},
                {'Device':'<a href=/>', 'Events':'<div/>'},
            ]}"
        """
        mydict = {'columns':[], 'data':[]}
        mydict['columns'] = ['Device', 'Events']
        deviceinfo = self.getmyDeviceDashboard(path)

        where=''
        if path.find("Devices")>0:
           where = "deviceClass like '%s%%'" % path[8:]
        elif path.find("Groups")>0:
           where = "deviceGroups like '%%|%s%%'" % path[7:]
        elif path.find("Systems")>0:
           where = "systems like '%%|%s%%'" % path[8:]
        elif path.find("Locations")>0:
           where = "location like '%s%%'" % path[10:]

	mydict['debug'] = where
	mydict['path'] = path
        for alink, pill in deviceinfo:
            mydict['data'].append({'Device':alink,
                                   'Events':pill})
        return mydict

            # Monkey-patch onto zport
from Products.ZenModel.ZentinelPortal import ZentinelPortal
ZentinelPortal.getmyDeviceIssuesJSON = getmyDeviceIssuesJSON

from Products.ZenEvents.browser.EventPillsAndSummaries import \
                                   getDashboardObjectsEventSummary, \
                                   ObjectsEventSummary,    \
                                   getEventPillME

def getmyDeviceDashboard(self, path):
	ZEN_VIEW='View'
        """return device info for bad device to dashboard"""
        zem = self.dmd.ZenEventManager
        where=''
        if path.find("Devices")>0:
           where = "deviceClass like '%s%%'" % path[8:]
        elif path.find("Groups")>0:
           where = "deviceGroups like '%%|%s%%'" % path[7:]
        elif path.find("Systems")>0:
           where = "systems like '%%|%s%%'" % path[8:]
        elif path.find("Locations")>0:
           where = "location like '%s%%'" % path[10:]

        devices = [d[0] for d in zem.getDeviceIssues(
                            where=where,
                            severity=4, state=1)]
        devdata = []
        devclass = zem.getDmdRoot("Devices")
        getcolor = re.compile(r'class=\"evpill-(.*?)\"', re.S|re.I|re.M).search
        colors = "red orange yellow blue grey green".split()
        def pillcompare(a,b):
            a, b = map(lambda x:getcolor(x[1]), (a, b))
            def getindex(x):
                try: 
                    color = x.groups()[0]
                    smallcolor = x.groups()[0].replace('-acked','')
                    isacked = 'acked' in color
                    index = colors.index(x.groups()[0].replace('-acked',''))
                    if isacked: index += .5
                    return index
                except: return 5
            a, b = map(getindex, (a, b))
            return cmp(a, b)
        for devname in devices:
            dev = devclass.findDevice(devname)
            if dev and dev.id == devname:
                if (not zem.checkRemotePerm(ZEN_VIEW, dev)
                    or dev.productionState < zem.prodStateDashboardThresh
                    or dev.priority < zem.priorityDashboardThresh):
                    continue
                alink = dev.getPrettyLink()
                try:
                    pill = getEventPillME(zem, dev)[0]
                except IndexError:
                    continue
                evts = [alink,pill]
                devdata.append(evts)
        devdata.sort(pillcompare)
        return devdata[:100]

ZentinelPortal.getmyDeviceDashboard = getmyDeviceDashboard
