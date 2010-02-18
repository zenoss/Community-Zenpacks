__doc__="""AppEngineConfigService

Provides Google AppEngine config to appenginemodeler and (someday) appenginevents clients.

Inspired by the Zenoss Enterprise VMware ESX Plugin

"""

# TODO 03FEB10:  Clean this up.  It is very ugly and many methods are extraneous

import transaction
from sets import Set
from itertools import izip, chain

from Products.ZenRelations.Exceptions import ObjectNotFound
from Products.ZenRelations.ToManyContRelationship import ToManyContRelationship
from Products.ZenEvents import Event
from Products.ZenUtils.Utils import prepId
from Products.ZenHub.HubService import HubService
from Products.ZenHub.services.Procrastinator import Procrastinate
from Products.ZenHub.PBDaemon import translateError
from Products.ZenModel.Device import manage_createDevice
from Products.ZenHub.services.ThresholdMixin import ThresholdMixin

from ZenPacks.chudler.GoogleAppEngine.AppEngineInstanceConfiguration import \
    AppEngineInstanceConfiguration
from ZenPacks.chudler.GoogleAppEngine.AppEngineObjectProperties import \
    AppEngineInstance, applyPropertiesToObject


DEFAULT_TXN_CHUNK_SIZE=100

def getAppEngineInstanceId( entity ):
    """
    Given a AppEngine instance, retrieve the id of the organizer that represents
    the endpoint
    """
    # 0-'' 1-'zport' 2-'dmd' 3-'Devices' 4-'AppEngine' 5-endpointid
    return entity.getPrimaryPath()[5]


class AppEngineConfigService(HubService, ThresholdMixin):
    """
    Provides AppEngine connection information to the appenginemodeler and
    appengineevents daemons, as well as accepting and saving modeling info
    from the appenginemodeler daemon.
    """

    def __init__(self, dmd, instance):
        """
        Create the service (Called by the hub)

        param dmd: root db node
        type instance: string
        param instance: Perf Monitor (Collector) name for this service
        """
        HubService.__init__(self, dmd, instance)
        self.log.debug('__init__():initializing AppEngineConfigService')
        self.config = self.dmd.Monitors.Performance._getOb(self.instance)

    def update(self, object):
        """
        This is overridden to forward changes in the AppEngine connection
        information to the daemons

        param object: the hook that is called when objects are changed in ZODB
        """
        from Products.ZenModel.DeviceClass import DeviceClass
        if isinstance( object, DeviceClass ):
            if hasattr( object, 'zAppEngineInstanceApplication') and \
                object.__primary_parent__.id == 'AppEngine':
                procrastinator = Procrastinate(
                                        self.updateEndpointConfiguration )
                procrastinator.doLater( object.id )
        HubService.update( self, object )

    @translateError
    def remote_getDefaultRRDCreateCommand(self, *args, **kwargs):
        """
        Get the default create command for this collector
        """
        return self.config.getDefaultRRDCreateCommand(*args, **kwargs)

    def updateEndpointConfiguration(self, organizerName):
        """
        Send updated connection information to the the daemons for this
        organizer

        type organizerName: string
        param organizerName: the name of the organizer that represents the
                             endpoint whose connection characteristics
                             have changed
        """
        endpointConfig = self.getAppEngineInstanceConfigurationFromName(organizerName)
        for listener in self.listeners:
            listener.callRemote('updateEndpointConfiguration', endpointConfig)

    def getAppEngineInstanceOrganizer(self, organizerName):
        """
        Return the organizer underneath /Devices/AppEngine with the given name.
        This organizer represents the Google AppEngine account that will provide
        all the information about a AppEngine infrastructure

        @param organizerName: the name of the organizer
        @type organizerName: C{string}
        @return: the organizer
        @rtype: L{DeviceOrganizer}
        """
        return self.dmd.Devices.getOrganizer('AppEngine/%s' % organizerName)

    @translateError
    def remote_getAppEngineInstanceConfiguration(self, organizerName):
        """
        Remote version of L{getAppEngineInstanceConfigurationFromName}
        """
        return self.getAppEngineInstanceConfigurationFromName(organizerName)

    def getAppEngineInstanceConfigurationFromName(self, organizerName):
        """
        Returns the information needed to connect to a Google AppEngine account
        represented by the given organizer name

        @param organizerName: name of the organizer
        @type organizerName: C{string}
        @return: the connection parameters
        @rtype: L{AppEngineInstanceConfiguration}
        """
        self.log.debug( 'getAppengineInstanceConfiguration():getting configuration ' +
                        'for %s' % organizerName )
        organizer=self.getAppEngineInstanceOrganizer(organizerName)
        return self.getAppEngineInstanceConfiguration(organizer)

    def getAppEngineInstanceConfiguration(self, organizer):
        """
        Returns the information needed to connect to the Google AppEngine
        instance represented by the given organizer

        @param organizer: the organizer
        @type organizerName: L{DeviceOrganizer}
        @return: the connection parameters
        @rtype: L{AppEngineInstanceConfiguration}
        """
        user = organizer.zAppEngineInstanceUser
        password = organizer.zAppEngineInstancePassword
        instanceConfig=AppEngineInstanceConfiguration(organizer.id, user, password)
        self.log.debug('getAppEngineInstanceConfiguration():retrieved instance' +
                       ' config %s' % instanceConfig)
        return instanceConfig

    @translateError
    def remote_getAllAppEngineInstanceConfigurations(self):
        """
        Returns the information needed to connect to Google to
        be monitored from this collector

        @return: all of the connections to be monitored from this daemon
        @rtype: C{list} of L{AppEngineInstanceConfiguration}s
        """
        appEngineOrganizer=self.dmd.Devices.AppEngine
        instanceOrganizers=appEngineOrganizer.children()
        configs=[]
        for instanceOrganizer in instanceOrganizers:
            zMonitor = instanceOrganizer.getZ('zAppEngineInstanceMonitor')
            if zMonitor == self.instance:
                config = self.getAppEngineInstanceConfiguration(instanceOrganizer)
                configs.append( config )
            else:
                msg ="filtering out %s; does not belong to monitor %s"
                self.log.debug(msg % (instanceOrganizer.id, self.instance))
        return configs

    @translateError
    def remote_getMonitoredInstances(self):
        """
        Remote call that returns the application instances (Google accounts) to be monitored
        from this collector
        """
        find=self.dmd.Devices.findAppEngineOrganizers
        organizers=find(performanceMonitor=self.instance)
        instanceConfigs=[]
        for organizer in organizers:
            instanceConfig=self.getAppEngineInstanceConfiguration(organizer)
            instanceConfigs.append(instanceConfig)
        return instanceConfigs

    @translateError
    def remote_addInfrastructure(self, organizerName, infrastructure,
                                 instanceApplicationsOnly=False ):
        """
        Store the items that were found when the Google account is queried

        @param organizerName: the name of organizer that represents the
                              account that was queried
        @type organizerName: C{string}
        @param infrastructure: the items that were discovered
        @type infrastructure: L{AppEngineInfrastructure}
        @param instanceApplicationsOnly: whether this is only information about hosts and
                            applications (as opposed to information about all possible
                            AppEngine entities, like task queues, cronjobs, etc.)
                            Defaults to I{False}.
        """
        self.log.debug('addInfrastructure():adding or updating infrastructure')
        self.log.debug('applications %s' % infrastructure.applications )
        applicationOrganizer=self.getAppEngineInstanceOrganizer('%s/Applications' % organizerName)

        idApplicationMap = self.createAndUpdateModelObjects( infrastructure.applications,
                                                      applicationOrganizer,
                                                      not instanceApplicationsOnly )

        #Stitch instances and applications together
        idApplicationMap={}
        allApplicationPropertiesMap={}
        for instance in idApplicationMap.values():
            currentApplicationMap = mapIdsToModelItems(instance.hostedApplications())
            newApplicationMap = \
                mapIdAttributesToObjectProperties(
                                    infrastructure.getApplicationsForApplication( instance.ref ) )

            currentSet=Set(currentApplicationMap.keys())
            newSet=Set(newApplicationMap.keys())
            applicationsToAdd = newSet.difference(currentSet)
            applicationsToDelete = currentSet.difference(newSet)
            for newApplicationId in newApplicationMap.keys():
                applicationProperties=newApplicationMap[newApplicationId]
                if newApplicationId in applicationsToAdd:
                    application=manage_createAppEngineApplication(instance.hostedApplications,newApplicationId)
                    action='adding'
                else:
                    application=currentApplicationMap[newApplicationId]
                    action='updating'

                applyPropertiesToObject(application, applicationProperties)

                self.log.debug( ( 'addInfrastructure():%s application ' +
                                '%s with properties %s ' )
                                % (action, application, applicationProperties) )

                idApplicationMap[newApplicationId]=application
                allApplicationPropertiesMap.update(newApplicationMap)
            transaction.commit()

            for applicationIdToDelete in applicationsToDelete:
                instance.hostedApplications._delObject(applicationIdToDelete)

                self.log.debug( 'addInfrastructure():Deleting application %s'
                                % (applicationIdToDelete) )
            transaction.commit()

        if not instanceApplicationsOnly:
            pass

    def createAndUpdateModelObjects( self,
                                     newObjectPropertiesList,
                                     organizer,
                                     warnOnMissingDevices=True,
                                     allowDuplicates=False ):
        """
        Modifies model information in the database given the information
        received from scraping the google account.  New objects are created,
        existing objects are updated.

        @param newObjectPropertiesList: a group of object properties, all
                                        representing a common type of object
                                        (Application, Task Queue, etc)
        @type newObjectPropertiesList: C{list} of
                                       L{AppEngineManagedObjectProperties}
        @param organizer: the organizer that holds items of this type. For
                          example, if we have modeled the infrastructure
                          represented by the organizer /Devices/AppEngine/test and
                          these are the Application property sets, then the
                          organizer at /Devices/AppEngine/test/Applications would be
                          passed
        @type organizer: L{DeviceOrganizer}
        @param warnOnMissingDevices: if I{True} and the item exists in the
                                     organizer but is not present in the
                                     supplied property sets, then an event
                                     is created and the device in the
                                     database is marked as I{Decommissioned}
        @type warnOnMissingDevices: C{boolean}
        """
        currentModelItemMap = mapIdsToModelItems( organizer.devices() )
        newObjectPropertiesMap = mapIdAttributesToObjectProperties(
                                                    newObjectPropertiesList )

        organizerPath=organizer.getOrganizerName()
        modelItemsToAdd = Set( newObjectPropertiesMap.keys() ).difference(
                                        Set(currentModelItemMap.keys() ) )
        modelItemsToDelete = Set( currentModelItemMap.keys()).difference(
                                        Set( newObjectPropertiesMap.keys() ) )
        modelItems={}

        for objectRef, objectProperties in newObjectPropertiesMap.iteritems():
            objectId = prepId( str ( objectProperties.getId() ).encode('ascii') )
            if objectRef in modelItemsToAdd:
                existingDevices = self.dmd.Devices._findDevice( objectId )
                if not existingDevices:
                    perfMonitor = organizer.getZ('zAppEngineInstanceMonitor')
                    modelItem = manage_createDevice(self.dmd, objectId,
                                                    organizerPath,
                                                    performanceMonitor=perfMonitor )
                action = 'adding'
            else:
                modelItem = currentModelItemMap[objectId]
                action = 'updating'

            #Handle id and name attributes
            idValue=objectProperties.attributes['id']
            if not objectProperties.attributes.has_key( 'name' ):
                objectProperties.attributes['name']=idValue
            objectProperties.attributes['id']=prepId(idValue)

            applyPropertiesToObject(modelItem, objectProperties)

            for componentList in objectProperties.components.values():
                self.createComponents( componentList, modelItem )

            self.log.debug( ( 'addInfrastructure():%s model object %s ' +
                            'with properties %s ' )
                     % (action, modelItem, objectProperties) )

            modelItems[objectId]=modelItem

        transaction.commit()

        if modelItemsToDelete and warnOnMissingDevices:

            events=[]
            for deviceToDelete in [ currentModelItemMap[id]
                                   for id in modelItemsToDelete ]:
                deviceId=deviceToDelete.id
                events.append({
                   'severity' : Event.Warning,
                   'eventClass' : "/Status/AppEngine",
                   'eventKey' : "DeviceNotFound",
                   'summary' : "%s/%s not found on target AppEngine instance"\
                            % (organizer.getOrganizerName(),deviceId ),
                   'device' : deviceId
                           })
                # decommission the device
                if deviceToDelete.productionState != -1:
                    self.log.info( 'Last AppEngine modeling did not find %s; '
                            + 'setting production state to Decommissioned' % deviceId)
                    deviceToDelete.setProdState(-1)
            self.zem.sendEvents(events)

        return modelItems

    def createComponents(self, componentList, modelItem):
        """
        Creates/updates/deletes components in the database after comparing
        what exists to the components returned from querying the
        infrastructure.

        @param componentList: the components returned from modeling
        @type componentList: C{list} for L{AppEngineComponentProperties} of
                             a common type (Task Queue,Cron Jobs,etc.)
        @param modelItem: the device which these components belong to
        @type modelItem: L{Device}
        """
        if not componentList or len(componentList) == 0:
            return
        else:
            firstProperties=componentList[0]
            componentClass=firstProperties.componentClass
            componentContainerString=firstProperties.componentContainer
            componentRelationString=firstProperties.componentRelation
            idAttr=firstProperties.instanceIdAttr
        componentContainer=getattr( modelItem, componentContainerString )
        currentComponents=getattr( componentContainer, componentRelationString )
        currentIdObjectMap=mapIdsToModelItems(currentComponents())
        newIdPropertiesMap=mapIdAttributesToObjectProperties( componentList,
                                                              idAttr)
        componentsToAdd=Set( newIdPropertiesMap.keys() ).difference(
                                                    currentIdObjectMap.keys() )
        componentsToDelete=Set( currentIdObjectMap.keys() ).difference(
                                                    newIdPropertiesMap.keys() )
        for id, componentProperties in newIdPropertiesMap.iteritems():
            if id in componentsToAdd:
                component=componentClass(id)
                currentComponents._setObject( id, component )
                component=currentComponents._getOb(id)
            else:
                component=currentIdObjectMap[id]

            applyPropertiesToObject(component, componentProperties)

        for componentId in componentsToDelete:
            componentToRemove=currentIdObjectMap[componentId]
            currentComponents.removeRelation(componentToRemove)

def mapIdsToModelItems( modelItems ):
    """
    Takes an iterable of model items (devices, components, etc) and returns
    and map of ids->items

    @param modelItems: the items to map
    @type modelItems: any iterable
    @return: the map of ids -> items
    @rtype: C{map} of C{string}, L{Device} or L{DeviceComponent}
    """
    ids=[ modelItem.id for modelItem in modelItems]
    itemMap=dict(zip(ids, modelItems))
    return itemMap

def mapIdAttributesToObjectProperties( objectPropertiesList,
                                       idAttributeName='id'):
    """
    Takes an iterable of L{AppEngineObjectProperties}s and creates a map
    of id attributes to the objects

    @param objectPropertiesList: the properties objects
    @type objectPropertiesList: iterable of L{AppEngineObjectProperties}
    @param idAttributeName: the key of the property whose value is the id;
                            defaults to I{id}
    @type idAttributeName: C{string}
    """
    objectIds=[ prepId( str(
                            objectProperties[idAttributeName]
                            ).encode('ascii') )
                for objectProperties in objectPropertiesList ]
    objectPropertiesMap=dict(zip(objectIds,objectPropertiesList))
    return objectPropertiesMap
