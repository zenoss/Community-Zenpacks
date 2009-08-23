__doc__="""SLAS

SLAS  - new device class for IP-SLA tests

$Id: $"""

__version__ = "$Revision: $"[11:-2]

import locale

from Globals import DTMLFile
from Globals import InitializeClass

from Products.ZenUtils.Utils import convToUnits
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.ZenossSecurity import ZEN_VIEW, ZEN_CHANGE_SETTINGS
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenUtils.Utils import prepId
#from ZenModelRM import ZenModelRM

class SLAS(DeviceComponent, ManagedEntity):
        """IP-SLA Onject"""

        portal_type = meta_type = 'SLAS'
        rttMonCtrlAdminOwner = ""
        rttMonCtrlAdminTag = ""
        rttMonCtrlAdminRttType = ""
        rttMonCtrlAdminThreshold = ""
        rttMonCtrlAdminFrequency = ""
        rttMonCtrlAdminTimeout = ""
        rttMonCtrlAdminVerifyData = ""
        rttMonCtrlAdminStatus = ""
        rttMonCtrlAdminNvgen = ""
        rttMonCtrlAdminGroupName = ""

        rttMonEchoAdminProtocol = ""
        rttMonEchoAdminTargetAddress = ""
        rttMonEchoAdminPktDataRequestSize = ""
        rttMonEchoAdminPktDataResponseSize = ""
        rttMonEchoAdminTargetPort = ""
        rttMonEchoAdminSourceAddress = ""
        rttMonEchoAdminSourcePort = ""
        rttMonEchoAdminControlEnable = ""
        rttMonEchoAdminTOS = ""
        rttMonEchoAdminLSREnable = ""
        rttMonEchoAdminTargetAddressString = ""
        rttMonEchoAdminNameServer = ""
        rttMonEchoAdminOperation = ""
        rttMonEchoAdminHTTPVersion = ""
        rttMonEchoAdminURL = ""
        rttMonEchoAdminCache = ""
        rttMonEchoAdminInterval = ""
        rttMonEchoAdminNumPackets = ""
        rttMonEchoAdminProxy = ""
        rttMonEchoAdminString1 = ""
        rttMonEchoAdminString2 = ""
        rttMonEchoAdminString3 = ""
        rttMonEchoAdminString4 = ""
        rttMonEchoAdminString5 = ""
        rttMonEchoAdminMode = ""
        rttMonEchoAdminVrfName = ""
        rttMonEchoAdminCodecType = ""
        rttMonEchoAdminCodecInterval = ""
        rttMonEchoAdminCodecPayload = ""
        rttMonEchoAdminCodecNumPackets = ""
        rttMonEchoAdminICPIFAdvFactor = ""
        rttMonEchoAdminLSPFECType = ""
        rttMonEchoAdminLSPSelector = ""
        rttMonEchoAdminLSPReplyMode = ""
        rttMonEchoAdminLSPTTL = ""
        rttMonEchoAdminLSPExp = ""
        rttMonEchoAdminPrecision = ""
        rttMonEchoAdminProbePakPriority = ""
        rttMonEchoAdminOWNTPSyncTolAbs = ""
        rttMonEchoAdminOWNTPSyncTolPct = ""
        rttMonEchoAdminOWNTPSyncTolType = ""
        rttMonEchoAdminCalledNumber = ""
        rttMonEchoAdminDetectPoint = ""
        rttMonEchoAdminGKRegistration = ""
        rttMonEchoAdminSourceVoicePort = ""
        rttMonEchoAdminCallDuration = ""
        rttMonEchoAdminLSPReplyDscp = ""
        rttMonEchoAdminLSPNullShim = ""
        rttMonEchoAdminTargetMPID = ""
        rttMonEchoAdminTargetDomainName = ""
        rttMonEchoAdminTargetVLAN = ""
        rttMonEchoAdminEthernetCOS = ""
        rttMonEchoAdminLSPVccvID = ""
        rttMonEchoAdminTargetEVC = ""

        _properties = (
                {'id':'rttMonCtrlAdminOwner', 'type':'string', 'mode':''},
                {'id':'rttMonCtrlAdminTag', 'type':'string', 'mode':''},
                {'id':'rttMonCtrlAdminRttType', 'type':'string', 'mode':''},
                {'id':'rttMonCtrlAdminThreshold', 'type':'int', 'mode':''},
                {'id':'rttMonCtrlAdminFrequency', 'type':'int', 'mode':''},
                {'id':'rttMonCtrlAdminTimeout', 'type':'int', 'mode':''},
                {'id':'rttMonCtrlAdminVerifyData', 'type':'int', 'mode':''},
                {'id':'rttMonCtrlAdminStatus', 'type':'int', 'mode':''},
                {'id':'rttMonCtrlAdminNvgen', 'type':'float', 'mode':''},
                {'id':'rttMonCtrlAdminGroupName', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminProtocol', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminTargetAddress', 'type':'int', 'mode':''},
                {'id':'rttMonEchoAdminPktDataRequestSize', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminPktDataResponseSize', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminTargetPort', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminSourceAddress', 'type':'int', 'mode':''},
                {'id':'rttMonEchoAdminSourcePort', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminControlEnable', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminTOS', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminLSREnable', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminTargetAddressString', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminNameServer', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminOperation', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminHTTPVersion', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminURL', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminCache', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminInterval', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminNumPackets', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminProxy', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminString1', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminString2', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminString3', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminString4', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminString5', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminMode', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminVrfName', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminCodecType', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminCodecInterval', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminCodecPayload', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminCodecNumPackets', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminICPIFAdvFactor', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminLSPFECType', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminLSPSelector', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminLSPReplyMode', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminLSPTTL', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminLSPExp', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminPrecision', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminProbePakPriority', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminOWNTPSyncTolAbs', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminOWNTPSyncTolPct', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminOWNTPSyncTolType', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminCalledNumber', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminDetectPoint', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminGKRegistration', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminSourceVoicePort', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminCallDuration', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminLSPReplyDscp', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminLSPNullShim', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminTargetMPID', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminTargetDomainName', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminTargetVLAN', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminEthernetCOS', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminLSPVccvID', 'type':'string', 'mode':''},
                {'id':'rttMonEchoAdminTargetEVC', 'type':'string', 'mode':''},
                )

        _relations = (
                ('host', ToOne(ToManyCont,
                'ZenPacks.ipSLA.SLADevice.SLAS',
                        'ipSLAs')
                ),
        )

        factory_type_information = (
                {
                        'id'             : 'SLAS',
                        'meta_type'      : 'SLAS',
                        'description'    : """IP Service Level Agreement Test Object""",
                        'icon'           : 'Device_icon.gif',
                        'product'        : 'SLAS',
                        'factory'        : 'manage_addSLAS',
                        'immediate_view' : 'ipSLAsPerformance',
                        'actions'        :
                        (
                                { 'id'            : 'perf'
                                , 'name'          : 'Perf'
                                , 'action'        : 'ipSLAsPerformance'
                                , 'permissions'   : (ZEN_VIEW, )
                                },
                                { 'id'            : 'templates'
                                , 'name'          : 'Templates'
                                , 'action'        : 'objTemplates'
                                , 'permissions'   : (ZEN_CHANGE_SETTINGS, )
                                },
                                { 'id'            : 'zProps'
                                , 'name'          : 'Properties'
                                , 'action'        : 'zPropertyEdit'
                                , 'permissions'   : (ZEN_CHANGE_SETTINGS, )
                                },
                                { 'id'            : 'SLAedit'
                                , 'name'          : 'Edit'
                                , 'action'        : 'SLAedit'
                                , 'permissions'   : (ZEN_CHANGE_SETTINGS, )
                                },

                        )
                },
        )

        def viewName(self):
                return self.rttMonCtrlAdminTag
        name = primarySortKey = viewName

        def device(self):
                return self.host()

        def managedDeviceLink(self):
                from Products.ZenModel.ZenModelRM import ZenModelRM
                d = self.getDmdRoot("Devices").findDevice(self.rttMonCtrlAdminTag)
                if d:
                        return ZenModelRM.urlLink(d, 'link')
                return None

	def manage_editProperties(self, REQUEST):
        	"""
	        Override from propertiyManager so we can trap errors
	        """
	        try:
        		return ConfmonPropManager.manage_editProperties(self, REQUEST)
	        except IpAddressError, e:
           		return   MessageDialog(
		                title = "Input Error",
		                message = e.args[0],
		                action = "manage_main")

	def getRRDTemplateName(self):
	        """
	        Return the interface type as the target type name.
	        """
	        return self.prepId(self.rttMonCtrlAdminRttType or "Unknown")


	def getRRDTemplates(self):
	        """
	        Return a list containing the appropriate RRDTemplate for this SLA.
	        """
	        templateName = self.getRRDTemplateName()
	        default = self.getRRDTemplateByName(templateName)

        	if not default:
	        	default = self.getRRDTemplateByName("New_SLA")

	        if default:
	        	return [default]
	        return []

	def device(self):
	        return self.host()

        def getId(self):
                return self.id

InitializeClass(SLAS)
