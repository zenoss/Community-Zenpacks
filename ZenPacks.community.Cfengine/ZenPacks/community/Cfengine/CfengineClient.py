from transaction import commit
from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS

_kw = dict(mode='w')

class CfengineClient(DeviceComponent, ManagedEntity):
    "Cfengine Client Information"
    
    portal_type = meta_type = 'CfengineClient'

    cfcDisplayName = ""
    cfcDeviceClass = ""
    cfcCompliance = 0

    _properties = (
	dict(id='cfcDisplayName', type='string',  **_kw),
	dict(id='cfcDeviceClass', type='string',  **_kw),
	dict(id='cfcCompliance', type='int',  **_kw),
    )

    _relations = (
	('cfengineserver', ToOne(ToManyCont, 'ZenPacks.community.Cfengine.CfengineDevice', 'cfengineclients')),
    )

    factory_type_information = (
	{
	    'id'             : 'CfengineClient',
	    'meta_type'      : 'Cfengine Client',
	    'description'    : 'Cfengine Client Description',
	    'icon'           : 'Device_icon.gif',
	    'product'        : 'CfengineClients',
	    'factory'        : 'manage_addCfengineClient',
	    'immediate_view' : 'cfengineclientDetail',
	    'actions'        :
	    (
		{ 'id'            : 'perf'
		, 'name'          : 'perf'
		, 'action'        : 'cfengineclientDetail'
		, 'permissions'   : (ZEN_VIEW, )
		},
		{ 'id'            : 'templates'
		, 'name'          : 'Templates'
		, 'action'        : 'objTemplates'
		, 'permissions'   : (ZEN_CHANGE_SETTINGS, )
		},
	    )
	},
    )

    def device(self):
	return self.cfengineserver()

    def managedDeviceLink(self):
	from Products.ZenModel.ZenModelRM import ZenModelRM
	d = self.getDmdRoot("Devices").findDevice(self.cfcDisplayName)
	if d:
	    return ZenModelRM.urlLink(d, 'link')
	return None

    def getCfengineClient(self):
        pass

    def setCfengineClient(self, name, dclass, serverId):
        devdmd = self.getDmdRoot("Devices")
        needsModeling = False
        #find the device
        dev = devdmd.findDeviceByIdOrIp(name)
        #create it if missing
        if dev == None:
            dev = devdmd.createInstance(name)
            needsModeling = True
        #find the Device Class
        fclass = devdmd.getOrganizer(dclass)
        #set to /Discovered if nonexistent
        if fclass == None:
            fclass = devdmd.getOrganizer("/Discovered")
            dclass="/Discovered"
            needsModeling = True
        #check for existing membership, move into class
        if dev not in fclass.getDevices():
            devdmd.moveDevices(dclass, name)
            needsModeling = True
        #add the 'Cfengine' template to our Device
        templates =  dev.zDeviceTemplates
        if 'Cfengine' not in templates:
            dev.setZenProperty('zDeviceTemplates', templates+['Cfengine'])
            needsModeling = True
        #log.info('CfengineClient Device Class: %s' % fclass)
        if needsModeling:
            #get the collector for the Cfengine server
            server = devdmd.findDevice(serverId)
            collectorId = server.getPerformanceServerName()
            #set the managed device to the same collector as the server
            dev.setPerformanceMonitor(collectorId)
            commit()
            #model this junk
            #dev.collectDevice()

InitializeClass(CfengineClient)

