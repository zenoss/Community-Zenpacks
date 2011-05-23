##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 16th, 2011
# Revised:
#
# info.py for Juniper ZenPack
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of Juniper components.

$Id: info.py,v 1.2 2010/12/14 20:45:46 jc Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from ZenPacks.ZenSystems.Juniper import interfaces


class JuniperContentsInfo(ComponentInfo):
    implements(interfaces.IJuniperContentsInfo)

    containerIndex = ProxyProperty("containerIndex")
    containerDescr = ProxyProperty("containerDescr")
    containerParentIndex = ProxyProperty("containerParentIndex")
    containerParentDescr = ProxyProperty("containerParentDescr")
    contentsType = ProxyProperty("contentsType")
    contentsDescr = ProxyProperty("contentsDescr")
    contentsSerialNo = ProxyProperty("contentsSerialNo")
    contentsRevision = ProxyProperty("contentsRevision")
    contentsPartNo = ProxyProperty("contentsPartNo")
    contentsChassisId = ProxyProperty("contentsChassisId")
    contentsChassisDescr = ProxyProperty("contentsChassisDescr")
    contentsChassisCLEI = ProxyProperty("contentsChassisCLEI")
    contentsCPU = ProxyProperty("contentsCPU")
    contentsTemp = ProxyProperty("contentsTemp")
    contentsState = ProxyProperty("contentsState")
    contentsUpTime = ProxyProperty("contentsUpTime")
    contentsMemory = ProxyProperty("contentsMemory")

    @property
    @info
    def manufacturer(self):
        pc = self._object.productClass()
        if (pc):
            return pc.manufacturer()

class JuniperFanInfo(ComponentInfo):
    implements(interfaces.IJuniperFanInfo)

    fanContainerIndex = ProxyProperty("fanContainerIndex")
    fanDescr = ProxyProperty("fanDescr")
    fanType = ProxyProperty("fanType")
    fanSerialNo = ProxyProperty("fanSerialNo")
    fanRevision = ProxyProperty("fanRevision")
    fanChassisId = ProxyProperty("fanChassisId")
    fanState = ProxyProperty("fanState")

class JuniperPowerSupplyInfo(ComponentInfo):
    implements(interfaces.IJuniperPowerSupplyInfo)

    powerSupplyContainerIndex = ProxyProperty("powerSupplyContainerIndex")
    powerSupplyDescr = ProxyProperty("powerSupplyDescr")
    powerSupplyType = ProxyProperty("powerSupplyType")
    powerSupplySerialNo = ProxyProperty("powerSupplySerialNo")
    powerSupplyPartNo = ProxyProperty("powerSupplyPartNo")
    powerSupplyRevision = ProxyProperty("powerSupplyRevision")
    powerSupplyChassisId = ProxyProperty("powerSupplyChassisId")
    powerSupplyState = ProxyProperty("powerSupplyState")
    powerSupplyTemp = ProxyProperty("powerSupplyTemp")
    powerSupplyCPU = ProxyProperty("powerSupplyCPU")
    powerSupplyMemory = ProxyProperty("powerSupplyMemory")
    powerSupplyUpTime = ProxyProperty("powerSupplyUpTime")

class JuniperFPCInfo(ComponentInfo):
    implements(interfaces.IJuniperFPCInfo)

    containerIndex = ProxyProperty("containerIndex")
    containerDescr = ProxyProperty("containerDescr")
    containerParentIndex = ProxyProperty("containerParentIndex")
    containerParentDescr = ProxyProperty("containerParentDescr")
    FPCType = ProxyProperty("FPCType")
    FPCDescr = ProxyProperty("FPCDescr")
    FPCSerialNo = ProxyProperty("FPCSerialNo")
    FPCRevision = ProxyProperty("FPCRevision")
    FPCPartNo = ProxyProperty("FPCPartNo")
    FPCChassisId = ProxyProperty("FPCChassisId")
    FPCChassisDescr = ProxyProperty("FPCChassisDescr")
    FPCChassisCLEI = ProxyProperty("FPCChassisCLEI")
    FPCCPU = ProxyProperty("FPCCPU")
    FPCTemp = ProxyProperty("FPCTemp")
    FPCState = ProxyProperty("FPCState")
    FPCUpTime = ProxyProperty("FPCUpTime")
    FPCMemory = ProxyProperty("FPCMemory")

class JuniperPICInfo(ComponentInfo):
    implements(interfaces.IJuniperPICInfo)

    containerIndex = ProxyProperty("containerIndex")
    containerDescr = ProxyProperty("containerDescr")
    containerParentIndex = ProxyProperty("containerParentIndex")
    containerParentDescr = ProxyProperty("containerParentDescr")
    PICType = ProxyProperty("PICType")
    PICDescr = ProxyProperty("PICDescr")
    PICSerialNo = ProxyProperty("PICSerialNo")
    PICRevision = ProxyProperty("PICRevision")
    PICPartNo = ProxyProperty("PICPartNo")
    PICChassisId = ProxyProperty("PICChassisId")
    PICChassisDescr = ProxyProperty("PICChassisDescr")
    PICChassisCLEI = ProxyProperty("PICChassisCLEI")
    PICCPU = ProxyProperty("PICCPU")
    PICTemp = ProxyProperty("PICTemp")
    PICState = ProxyProperty("PICState")
    PICUpTime = ProxyProperty("PICUpTime")
    PICMemory = ProxyProperty("PICMemory")

class JuniperMICInfo(ComponentInfo):
    implements(interfaces.IJuniperMICInfo)

    containerIndex = ProxyProperty("containerIndex")
    containerDescr = ProxyProperty("containerDescr")
    containerParentIndex = ProxyProperty("containerParentIndex")
    containerParentDescr = ProxyProperty("containerParentDescr")
    MICType = ProxyProperty("MICType")
    MICDescr = ProxyProperty("MICDescr")
    MICSerialNo = ProxyProperty("MICSerialNo")
    MICRevision = ProxyProperty("MICRevision")
    MICPartNo = ProxyProperty("MICPartNo")
    MICChassisId = ProxyProperty("MICChassisId")
    MICChassisDescr = ProxyProperty("MICChassisDescr")
    MICChassisCLEI = ProxyProperty("MICChassisCLEI")
    MICCPU = ProxyProperty("MICCPU")
    MICTemp = ProxyProperty("MICTemp")
    MICState = ProxyProperty("MICState")
    MICUpTime = ProxyProperty("MICUpTime")
    MICMemory = ProxyProperty("MICMemory")

class JuniperBaseCompInfo(ComponentInfo):
    implements(interfaces.IJuniperBaseCompInfo)

    containerIndex = ProxyProperty("containerIndex")
    containerDescr = ProxyProperty("containerDescr")
    containerParentIndex = ProxyProperty("containerParentIndex")
    containerParentDescr = ProxyProperty("containerParentDescr")
    BaseCompType = ProxyProperty("BaseCompType")
    BaseCompDescr = ProxyProperty("BaseCompDescr")
    BaseCompSerialNo = ProxyProperty("BaseCompSerialNo")
    BaseCompRevision = ProxyProperty("BaseCompRevision")
    BaseCompPartNo = ProxyProperty("BaseCompPartNo")
    BaseCompChassisId = ProxyProperty("BaseCompChassisId")
    BaseCompChassisDescr = ProxyProperty("BaseCompChassisDescr")
    BaseCompChassisCLEI = ProxyProperty("BaseCompChassisCLEI")
    BaseCompCPU = ProxyProperty("BaseCompCPU")
    BaseCompTemp = ProxyProperty("BaseCompTemp")
    BaseCompState = ProxyProperty("BaseCompState")
    BaseCompUpTime = ProxyProperty("BaseCompUpTime")
    BaseCompMemory = ProxyProperty("BaseCompMemory")

class JuniperRoutingEngineInfo(ComponentInfo):
    implements(interfaces.IJuniperRoutingEngineInfo)

    containerIndex = ProxyProperty("containerIndex")
    containerDescr = ProxyProperty("containerDescr")
    containerParentIndex = ProxyProperty("containerParentIndex")
    containerParentDescr = ProxyProperty("containerParentDescr")
    RoutingEngineType = ProxyProperty("RoutingEngineType")
    RoutingEngineDescr = ProxyProperty("RoutingEngineDescr")
    RoutingEngineSerialNo = ProxyProperty("RoutingEngineSerialNo")
    RoutingEngineRevision = ProxyProperty("RoutingEngineRevision")
    RoutingEnginePartNo = ProxyProperty("RoutingEnginePartNo")
    RoutingEngineChassisId = ProxyProperty("RoutingEngineChassisId")
    RoutingEngineChassisDescr = ProxyProperty("RoutingEngineChassisDescr")
    RoutingEngineChassisCLEI = ProxyProperty("RoutingEngineChassisCLEI")
    RoutingEngineCPU = ProxyProperty("RoutingEngineCPU")
    RoutingEngineTemp = ProxyProperty("RoutingEngineTemp")
    RoutingEngineState = ProxyProperty("RoutingEngineState")
    RoutingEngineUpTime = ProxyProperty("RoutingEngineUpTime")
    RoutingEngineMemory = ProxyProperty("RoutingEngineMemory")

class JuniperBGPInfo(ComponentInfo):
    implements(interfaces.IJuniperBGPInfo)

    bgpLocalAddress = ProxyProperty("bgpLocalAddress")
    bgpRemoteAddress = ProxyProperty("bgpRemoteAddress")
    bgpRemoteASN = ProxyProperty("bgpRemoteASN")
    bgpStateInt = ProxyProperty("bgpStateInt")
    bgpStateText = ProxyProperty("bgpStateText")
    bgpLastUpDown = ProxyProperty("bgpLastUpDown")

class JuniperComponentsInfo(ComponentInfo):
    implements(interfaces.IJuniperComponentsInfo)

    containerIndex = ProxyProperty("containerIndex")
    containerDescr = ProxyProperty("containerDescr")
    containerParentIndex = ProxyProperty("containerParentIndex")
    containerParentDescr = ProxyProperty("containerParentDescr")
    containerType = ProxyProperty("containerType")
    containerLevel = ProxyProperty("containerLevel")
    containerNextLevel = ProxyProperty("containerNextLevel")

class JuniperIpSecVPNInfo(ComponentInfo):
    implements(interfaces.IJuniperIpSecVPNInfo)

    vpnPhase1LocalGwAddr = ProxyProperty("vpnPhase1LocalGwAddr")
    vpnPhase1LocalIdValue = ProxyProperty("vpnPhase1LocalIdValue")
    vpnPhase1RemoteIdValue = ProxyProperty("vpnPhase1RemoteIdValue")
    vpnPhase1State = ProxyProperty("vpnPhase1State")
    vpnPhase2LocalGwAddr = ProxyProperty("vpnPhase2LocalGwAddr")

class JuniperIpSecNATInfo(ComponentInfo):
    implements(interfaces.IJuniperIpSecNATInfo)

    natId = ProxyProperty("natId")
    natNumPorts = ProxyProperty("natNumPorts")
    natNumSess = ProxyProperty("natNumSess")
    natPoolType = ProxyProperty("natPoolType")

class JuniperIpSecPolicyInfo(ComponentInfo):
    implements(interfaces.IJuniperIpSecPolicyInfo)

    policyId = ProxyProperty("policyId")
    policyAction = ProxyProperty("policyAction")
    policyState = ProxyProperty("policyState")
    policyFromZone = ProxyProperty("policyFromZone")
    policyToZone = ProxyProperty("policyToZone")
    policyName = ProxyProperty("policyName")

class JuniperVlanInfo(ComponentInfo):
    implements(interfaces.IJuniperVlanInfo)

    vlanName = ProxyProperty("vlanName")
    vlanType = ProxyProperty("vlanType")
    vlanTag = ProxyProperty("vlanTag")
    vlanPortGroup = ProxyProperty("vlanPortGroup")
    vlanInterfaceInfo = ProxyProperty("vlanInterfaceInfo")

