"""03FEB10 This file doesn't do anything.  It still references some vmware specific
things, and in general needs work"""

import types
from Products.ZenUtils.Utils import prepId

_rcvtime_field='rcvtime'
def byRcvtimeField(x,y):
    xtime=x.fields[_rcvtime_field]
    ytime=y.fields[_rcvtime_field]
    if xtime > ytime:
        return 1
    if xtime < ytime:
        return -1
    return 0

noConvert=lambda name, value: {name:value}

AppEngineSlots={
    'ChainId':noConvert,
    'ComputeResource' : lambda name, value:
         { 'ComputeResourceRef':str(value.ComputeResource),
           'ComputeResourceName':value.Name },
    'CreatedTime': lambda name, value:
         { _rcvtime_field:tupleToTime(value)},
    'Datacenter' : lambda name, value:
         {'DataCenterRef':str(value.Datacenter),
          'DatacenterName':value.Name },
    'FullFormattedMessage':lambda name, value:
         {'summary':value},
    'Host': lambda name, value:
         {'HostRef':str(value.Host),
          'HostName':value.Name },
    'Key':noConvert,
    'UserName':noConvert,
    'Application':lambda name, value:
         {'ApplicationRef':str(value.Application),
          'ApplicationName':value.Name },
    'From' : noConvert,
    'To' : noConvert
}

DEFAULT_IDS={'device':'AppEngineInstanceName', 'component':'AppEngineApplicationName'}
EventClassIdentifierMap={
        'AppEngineApplicationEvent':DEFAULT_IDS,
                        }

EVENT_CLASS_KEY='eventClassKey'
APPENGINE_EVENT_TYPE='eventGroup'

def getSecondaryBaseType( typecodeClass ):

    def getBaseRecursively( typecodeClass ):
        bases=typecodeClass.__bases__
        if bases[0] is ns0.Event_Def:
            return typecodeClass
        elif bases[0] is object:
            return None
        else:
            return getBaseRecursively( bases[0] )

    return getBaseRecursively( typecodeClass ) or typecodeClass


class AppEngineEvent:
    def __init__(self, eventDataObject):
        self.fields={}
        typecode=eventDataObject.typecode
        eventType=typecode.type[-1]
        evclass, evclasskey = _getEventClass(eventType)
        self.fields[EVENT_CLASS_KEY]= evclasskey
        self.fields[APPENGINE_EVENT_TYPE]=eventType
        self.fields['eventClass'] = evclass
        for slot, convert in AppEngineSlots.iteritems():
            if hasattr( eventDataObject, slot ):
                value=getattr(eventDataObject,slot)
                self.fields.update(convert(slot,value))
        secondaryBaseType=getSecondaryBaseType( typecode.__class__ )
        self.processOnType( secondaryBaseType.type[-1] )

    def processOnType(self, baseType ):
        idKeys=EventClassIdentifierMap.get(baseType,DEFAULT_IDS)
        for key, mappedSlotKey in idKeys.iteritems():
            if self.fields.has_key( mappedSlotKey ):
                self.fields[key]=prepId(self.fields[mappedSlotKey])

    def hasKey(self, key):
        return self.fields.has_key(key)

    def addField(self,key,value):
        self.fields[key]=value

    def __str__(self):
        return str( self.fields )


from eventclasskey_map import EVENTCLASSKEY_MAP
def _getEventClass(classkey):
    try:
        evclass = EVENTCLASSKEY_MAP[classkey]
    except KeyError:
        evclass = '/GoogleAppEngine'
    return evclass, evclass.replace('/','')

