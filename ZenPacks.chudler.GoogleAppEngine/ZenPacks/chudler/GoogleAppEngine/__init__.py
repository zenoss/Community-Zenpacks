"""Heavily inspired by the Enterprise VMware monitor zenpack"""

import Globals
import os.path
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.Utils import monkeypatch

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

def checkForExistingInstance( instanceOrganizers, username ):
    for organizer in instanceOrganizers:
        if getattr( organizer,
                    'zAppEngineInstanceUsername', None ).lower() == username.lower():
            return organizer
    return None

def closeOutRequestWithMessage( REQUEST, handler, message=None ):
    from Products.ZenUtils.Utils import clearWebLoggingStream

    if message:
        REQUEST.RESPONSE.write(
            '<tr class="tableheader"><td colspan="4">%s</td></tr>' % message )
    REQUEST.RESPONSE.write("</table></body></html>")
    clearWebLoggingStream(handler)

def addAppEngineInstanceOrganizer( appEngineOrganizer, id, username,
                                performanceMonitor, password):
    newInstanceOrganizerPath='/AppEngine/%s' % id
    appEngineOrganizer.manage_addOrganizer(id)
    newOrganizer=appEngineOrganizer.getOrganizer(newInstanceOrganizerPath)
    newOrganizer.setZenProperty('zAppEngineInstanceUser', username)
    newOrganizer.setZenProperty('zAppEngineInstanceMonitor', performanceMonitor)
    newOrganizer.setZenProperty('zAppEngineInstancePassword', password)

    def createSubOrganizer( parentOrganizerPath, parentOrganizer,
                            name, pythonClass, template ):
        subOrganizerPath=('%s/%s' % (parentOrganizerPath, name))
        parentOrganizer.manage_addOrganizer(subOrganizerPath)
        subOrganizer=parentOrganizer.getOrganizer(subOrganizerPath)
        subOrganizer.setZenProperty('zPythonClass',  pythonClass )
        templates=subOrganizer.getZ('zDeviceTemplates')[:]
        templates.append(template)
        subOrganizer.setZenProperty('zDeviceTemplates',templates)

    subOrganizers=[('Applications', 'ZenPacks.chudler.GoogleAppEngine.AppEngineApplication', 'AppEngineApplication')]

    for name, clazz, template in subOrganizers:
        createSubOrganizer( newInstanceOrganizerPath, newOrganizer,
                            name, clazz, template )

    return newOrganizer


@monkeypatch('Products.ZenModel.DeviceClass.DeviceClass')
def manage_addGoogleAppEngineInstance( self, id, username,
                                            password, performanceMonitor='localhost',
                                            REQUEST=None):
    """
    Add a AppEngine instance and kick off modeling

    @type id: string
    @param id: the id of the new AppEngine organizer being added
    @type username: string
    @param username: the username to use when connecting to Google
    @type password: string
    @param password: the password to use
    @type performanceMonitor: string
    @param performanceMonitor: the collector that will monitor the instance
    @param REQUEST: the request object (if this is an http request)
    """
    from Products.ZenUtils.Utils import executeCommand, setupLoggingHeader
    if REQUEST:
        handler = setupLoggingHeader(self, REQUEST)
    import transaction

    if not id or len(id) == 0:
        id='AppEngine Instance'
    organizerPath='/AppEngine'
    appEngineOrganizer=self.getOrganizer(organizerPath)

    existingInstance = checkForExistingInstance(appEngineOrganizer.children(), username)

    if existingInstance:
        if REQUEST:
            devurl = existingInstance.absolute_url()
            message = ( 'Existing instance <a href=%s>%s</a> already' + \
                      ' modeled for that user (%s)' ) % ( devurl,
                      existingInstance.id, username )
            closeOutRequestWithMessage(REQUEST, handler, message)
        return

    newOrganizer = addAppEngineInstanceOrganizer( appEngineOrganizer, id, username, performanceMonitor, password)

    transaction.commit()

    args = ( 'run', '-a', id , '--monitor', performanceMonitor)
    if REQUEST:
        args += ('--weblog',)
    monitor = self.getDmdRoot('Monitors').getPerformanceMonitor(performanceMonitor)
    retcode = monitor.executeCollectorCommand('appenginemodeler', args, REQUEST)
    closeOutMessage = None
    if retcode!=0:
        appEngineOrganizer.manage_deleteOrganizers(
                                (newOrganizer.getOrganizerName(),))
    else:
        if REQUEST:
            devurl = newOrganizer.absolute_url()
            closeOutMessage = """New AppEngine instance at <a href=%s>%s</a>"""  \
                % (devurl, newOrganizer.getId())

    if REQUEST:
        closeOutRequestWithMessage(REQUEST, handler, closeOutMessage )

    if retcode == 0:
        # Modeling has finished.  Now push the instance configuration to
        # the daemons.
        newOrganizer.pushConfig()

ALL_PERFORMANCE_MONITORS="__ALL__"

@monkeypatch('Products.ZenModel.DeviceClass.DeviceClass')
def findAppEngineOrganizers( self, instanceOrganizerId='', performanceMonitor='localhost'):
    """
    Retrieve the organizer with the given id.  If no instance is given,
    return all the children of /Devices/AppEngine that are monitored by the given
    performance monitor.  If performanceMonitor == "__ALL__", organizers
    monitored by any collectors are returned

    @type instanceOrganizerId: string
    @param instanceOrganizerId: the organizer that represents the
                                AppEngine Instance (defaults to empty string)
    @type performanceMonitor: string
    @param performanceMonitor: the collector that monitors the returned
                               instances (defaults to 'localhost')
    @rtype: L{DeviceClass}
    @return: the organizer that represents the AppEngine instance
    """
    #if no instanceOrganizerId specified get all
    instances=[]
    if not instanceOrganizerId or len( instanceOrganizerId ) == 0:
        appEngineOrganizer = self.getDmdRoot(self.dmdRootName).getOrganizer('AppEngine')
        instanceOrganizers=appEngineOrganizer.children()
        if performanceMonitor == ALL_PERFORMANCE_MONITORS:
            instances.extend( instanceOrganizers )
        else:
            #only get instances bound to performanceMonitor
            for instanceOrganizer in instanceOrganizers:
                zMonitor = instanceOrganizer.getZ('zAppEngineInstanceMonitor')
                if zMonitor == performanceMonitor:
                    instances.append(instanceOrganizer)
    else:
        dmdRoot=self.getDmdRoot(self.dmdRootName)
        instances.append( dmdRoot.getOrganizer('/AppEngine/%s' %
                                               instanceOrganizerId) )

    return instances

@monkeypatch('Products.ZenModel.DeviceClass.DeviceClass')
def findAppEngineDevices( self, instanceOrganizerId='', performanceMonitor=ALL_PERFORMANCE_MONITORS):
    """
    Retrieves all AppEngine devices (Applications, Task Queues)
    for the given instance.  If the instance id is an empty string, devices
    for all the organizers for this collector are returned

    @type instanceOrganizerId: string
    @param instanceOrganizerId: the id of the instance (defaults to '')
    @type performanceMonitor: string
    @param performanceMonitor: the collector (defaults to 'localhost')
    @rtype: list of L{Device}
    @return: the requested devices
    """

    def _findDevices(instanceOrganizerId=''):
        zcat=self._getCatalog()
        if not zcat: return []
        query='/zport/dmd/Devices/AppEngine'
        if instanceOrganizerId and len( instanceOrganizerId ) > 0:
            query += '/%s' % instanceOrganizerId
        results = zcat({'path':query})
        return self._convertResultsToObj(results)
    # if no instanceOrganizerId specified get all
    if not instanceOrganizerId or len( instanceOrganizerId ) == 0:
        instanceOrganizers=self.findAppEngineOrganizers( instanceOrganizerId,
                                                      ALL_PERFORMANCE_MONITORS )
        instanceIds = [org.getId() for org in instanceOrganizers]
    else:
        instanceIds = [instanceOrganizerId]

    results = []
    for id in instanceIds:
        devices = _findDevices(id)
        if performanceMonitor and \
           performanceMonitor != ALL_PERFORMANCE_MONITORS:
            monitorFilter = lambda x: x.perfServer().id == performanceMonitor
            results.extend( filter( monitorFilter, devices ) )
        else:
            results.extend( devices )
    return results


class ZenPack(ZenPackBase):
    "loads zProperties used by this ZenPack"
    packZProperties = [
                       ('zAppEngineInstanceUser', 'googleuser@google.com', 'string'),
                       ('zAppEngineInstancePassword', '', 'string'),
                       ('zAppEngineInstanceMonitor', 'localhost', 'string')
                       ]
