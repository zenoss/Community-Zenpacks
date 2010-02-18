"""Inspired by the Zenoss Enterprise VMware ESX Plugin"""
# TODO 03FEB10:  clean up vetiges of vmware, and remove unused or improper classes and methods

from twisted.spread import pb
import types

def applyPropertiesToObject( object, properties ):
    dontoverride = ('id',)
    for key in properties.keys():
        if key in dontoverride: continue
        if hasattr(object, key):
            setattr(object, key, properties[key])
    if hasattr( object, 'postApplyProperties' ):
        getattr( object, 'postApplyProperties' )()
    return object


class AppEngineObjectProperties:

    mapLink={}

    def keys(self):
        return self.attributes.keys()

    def __getitem__(self, attr):
        if self.attributes.has_key( attr ):
            return self.attributes[attr]
        else:
            return None

    def __str__(self):
        outString = ""
        for key, value in self.attributes.iteritems():
            outString += "%s : %s, " % ( key, str(value) )
        return "Properties -- %s" % outString

pb.setUnjellyableForClass(AppEngineObjectProperties,AppEngineObjectProperties)


class AppEngineManagedObjectProperties(AppEngineObjectProperties, pb.RemoteCopy,pb.Copyable):

    componentMapLink={}

    def __init__(self, propSetMaps ):

        self.attributes=self._getAttributesFromMaps(propSetMaps)
        self.attributes['ref']=propSetMaps['ref']
        self.components=self._getComponentsFromMaps(propSetMaps)

    def _getAttributesFromMaps(self, mapMap):
        attributes={}
        for k in mapMap.keys():
            value=mapMap[k]
            #is this an attribute?
            if self.mapLink.has_key(k):
                if hasattr( value, 'ManagedObjectReference' ) and \
                    type(value.ManagedObjectReference) is types.ListType:
                    attributes[ self.mapLink[ k ] ] = [
                        str( i ) for i in value.ManagedObjectReference ]
                else:
                    if type(value) is types.ListType or (
                            hasattr( value, 'typecode' )
                            and value.typecode.type[-1].startswith( 'ArrayOf' ) ):
                        attributes[self.mapLink[k]] = value
                    else:
                        attributes[self.mapLink[k]] = str( value )
        self.processAttributes(attributes)
        return attributes

    def _getComponentsFromMaps(self,mapMap):
        components={}
        for key, value in mapMap.iteritems():
            if self.componentMapLink.has_key(key):
                viType, propClazz=self.componentMapLink[key]
                if not hasattr( value, viType ):
                    values=[value]
                else:
                    values=getattr(value,viType)
                    if type(values) is not types.ListType:
                        values=[value]
                for each in values:
                    component=propClazz( each )
                    if not components.has_key(propClazz.componentName):
                        components[propClazz.componentName]=[]
                    components[propClazz.componentName].append(component)
        return components

    def processAttributes(self, attributes):
        pass

    def __getitem__(self,attr):
        item = AppEngineObjectProperties.__getitem__(self,attr)
        if not item and self.components.has_key(attr):
            item = self.components[attr]
        return item

    def __str__(self):
        attributeString=AppEngineObjectProperties.__str__(self)
        componentString='Components--'
        for componentName, componentList in self.components.iteritems():
            reducedComponentList=reduce(lambda x,y:str(x) + ',' + str(y),
                                        componentList)
            componentString+='%s: %s' % (componentName, reducedComponentList)
        return attributeString + componentString

pb.setUnjellyableForClass(AppEngineManagedObjectProperties,
                          AppEngineManagedObjectProperties)


class ApplicationComponentProperties(AppEngineObjectProperties,
                                pb.RemoteCopy,pb.Copyable):
    """This used to be called the VMwareComponentProperties"""
    """It is getting changed in a way to have applications with components"""
    componentName=''
    componentRelations=''
    instanceIdAttr='id'

    def __init__(self, valueObject):
        self.attributes=self._applyComponentProperties(valueObject)

    def _applyComponentProperties( self, valueObject ):
        attributes={}
        for objectAttribute, propertyName in self.mapLink.iteritems():
            if hasattr(valueObject, objectAttribute):
                attributes[propertyName]=getattr(valueObject,objectAttribute)
        self.processAttributes(attributes)
        return attributes;

    def processAttributes(self, attributes):
        attributes['instanceId']=attributes[self.instanceIdAttr]

pb.setUnjellyableForClass(ApplicationComponentProperties,ApplicationComponentProperties)


class ApplicationProperties(AppEngineManagedObjectProperties,pb.Copyable,pb.RemoteCopy):

    mapLink={
             'name':'id',
             'Title':'title',
             'url':'url',
             'Current Version':'version',
             'billing':'billing',
             }

    componentMapLink={ }

    def processAttributes(self, attributes):
        pass

    def getId(self):
        return self.attributes['id']

    def __init__(self, propSetMaps):
        propSetMaps['ref'] = 'Application'
        AppEngineManagedObjectProperties.__init__(self, propSetMaps)

pb.setUnjellyableForClass(ApplicationProperties,ApplicationProperties)


class GAEProperties(AppEngineManagedObjectProperties,pb.Copyable,pb.RemoteCopy):

    mapLink={
             'googleAccount':'id',
             'application':'ApplicationRef',
             'remainingApplications':'remainingApplications',
             }

    def __init__(self, propSetMaps):
        AppEngineManagedObjectProperties.__init__(self, propSetMaps)

    def processAttributes( self, attributes ):
        AppEngineManagedObjectProperties.processAttributes(self, attributes)



pb.setUnjellyableForClass(GAEProperties,GAEProperties)

class AppEngineInstance(pb.Copyable, pb.RemoteCopy):


    def __init__(self):
        self.applications=[]
        self.refApplicationMap={}

    def addApplications(self, newApplications):
        self.applications.extend(newApplications)
        for newApplication in newApplications:
            self.refApplicationMap[newApplication['ref']]=newApplication

    def getApplication(self, ref):
        return self.refApplicationMap[ref]

pb.setUnjellyableForClass(AppEngineInstance, AppEngineInstance)
