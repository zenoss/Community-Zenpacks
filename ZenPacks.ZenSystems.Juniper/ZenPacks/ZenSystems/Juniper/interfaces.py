##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 16th, 2011
# Revised:
#
# interfaces.py for Juniper ZenPack
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.2 2010/12/14 20:46:34 jc Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IJuniperContentsInfo(IComponentInfo):
    """
Info adapter for JuniperContents component
"""
    containerIndex = schema.Int(title=u"Container Index", readonly=True, group='Details')
    containerDescr = schema.Text(title=u"Container Description", readonly=True, group='Details')
    containerParentIndex = schema.Int(title=u"Parent Index", readonly=True, group='Details')
    containerParentDescr = schema.Text(title=u"Parent Description", readonly=True, group='Details')
    contentsType = schema.Text(title=u"Type", readonly=True, group='Details')
    contentsDescr = schema.Text(title=u"Description", readonly=True, group='Details')
    contentsSerialNo = schema.Text(title=u"Serial No.", readonly=True, group='Details')
    contentsRevision = schema.Text(title=u"Revision", readonly=True, group='Details')
    contentsPartNo = schema.Text(title=u"Part No.", readonly=True, group='Details')
    contentsChassisId = schema.Text(title=u"Chassis Id.", readonly=True, group='Details')
    contentsChassisDescr = schema.Text(title=u"Chassis Description", readonly=True, group='Details')
    contentsChassisCLEI = schema.Text(title=u"Chassis CLEI", readonly=True, group='Details')
    contentsCPU = schema.Int(title=u"CPU Util", readonly=True, group='Details')
    contentsTemp = schema.Text(title=u"Temperature", readonly=True, group='Details')
    contentsState = schema.Text(title=u"State", readonly=True, group='Details')
    contentsUpTime = schema.Text(title=u"Up Time", readonly=True, group='Details')
    contentsMemory = schema.Text(title=u"Memory Used", readonly=True, group='Details')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True, group='Details')

class IJuniperFanInfo(IComponentInfo):
    """
Info adapter for JuniperFan component
"""
    fanContainerIndex = schema.Int(title=u"Container Index", readonly=True, group='Details')
    fanDescr = schema.Text(title=u"Description", readonly=True, group='Details')
#    fanType = schema.Text(title=u"Type", readonly=True, group='Details')
    fanSerialNo = schema.Text(title=u"SerialNo", readonly=True, group='Details')
    fanRevision = schema.Text(title=u"Revision", readonly=True, group='Details')
    fanChassisId = schema.Text(title=u"ChassisId", readonly=True, group='Details')
    fanState = schema.Text(title=u"State", readonly=True, group='Details')

class IJuniperPowerSupplyInfo(IComponentInfo):
    """
Info adapter for JuniperPowerSupply component
"""
    powerSupplyContainerIndex = schema.Int(title=u"Container Index", readonly=True, group='Details')
    powerSupplyDescr = schema.Text(title=u"Description", readonly=True, group='Details')
#    powerSupplyType = schema.Text(title=u"Type", readonly=True, group='Details')
    powerSupplySerialNo = schema.Text(title=u"SerialNo", readonly=True, group='Details')
    powerSupplyPartNo = schema.Text(title=u"PartNo", readonly=True, group='Details')
    powerSupplyRevision = schema.Text(title=u"Revision", readonly=True, group='Details')
#    powerSupplyChassisId = schema.Text(title=u"ChassisId", readonly=True, group='Details')
    powerSupplyState = schema.Text(title=u"State", readonly=True, group='Details')
#    powerSupplyTemp = schema.Text(title=u"Temp", readonly=True, group='Details')
#    powerSupplyCPU = schema.Text(title=u"CPU", readonly=True, group='Details')
#    powerSupplyMemory = schema.Text(title=u"Memory", readonly=True, group='Details')
    powerSupplyUpTime = schema.Text(title=u"Up Time (days)", readonly=True, group='Details')

class IJuniperFPCInfo(IComponentInfo):
    """
Info adapter for JuniperFPC component
"""
    containerIndex = schema.Int(title=u"Container Index", readonly=True, group='Details')
    containerDescr = schema.Text(title=u"Container Description", readonly=True, group='Details')
    containerParentIndex = schema.Int(title=u"Parent Index", readonly=True, group='Details')
    containerParentDescr = schema.Text(title=u"Parent Description", readonly=True, group='Details')
#    FPCType = schema.Text(title=u"Type", readonly=True, group='Details')
    FPCDescr = schema.Text(title=u"Description", readonly=True, group='Details')
    FPCSerialNo = schema.Text(title=u"Serial No.", readonly=True, group='Details')
    FPCRevision = schema.Text(title=u"Revision", readonly=True, group='Details')
    FPCPartNo = schema.Text(title=u"Part No.", readonly=True, group='Details')
    FPCChassisId = schema.Text(title=u"Chassis Id.", readonly=True, group='Details')
    FPCChassisDescr = schema.Text(title=u"Chassis Description", readonly=True, group='Details')
    FPCChassisCLEI = schema.Text(title=u"Chassis CLEI", readonly=True, group='Details')
    FPCCPU = schema.Int(title=u"CPU Util", readonly=True, group='Details')
    FPCMemory = schema.Int(title=u"Memory", readonly=True, group='Details')
    FPCTemp = schema.Text(title=u"Temperature", readonly=True, group='Details')
    FPCState = schema.Text(title=u"State", readonly=True, group='Details')
    FPCUpTime = schema.Text(title=u"Up Time", readonly=True, group='Details')

class IJuniperPICInfo(IComponentInfo):
    """
Info adapter for JuniperPIC component
"""
    containerIndex = schema.Int(title=u"Container Index", readonly=True, group='Details')
    containerDescr = schema.Text(title=u"Container Description", readonly=True, group='Details')
    containerParentIndex = schema.Int(title=u"Parent Index", readonly=True, group='Details')
    containerParentDescr = schema.Text(title=u"Parent Description", readonly=True, group='Details')
#    PICType = schema.Text(title=u"Type", readonly=True, group='Details')
    PICDescr = schema.Text(title=u"Description", readonly=True, group='Details')
    PICSerialNo = schema.Text(title=u"Serial No.", readonly=True, group='Details')
    PICRevision = schema.Text(title=u"Revision", readonly=True, group='Details')
    PICPartNo = schema.Text(title=u"Part No.", readonly=True, group='Details')
    PICChassisId = schema.Text(title=u"Chassis Id.", readonly=True, group='Details')
    PICChassisDescr = schema.Text(title=u"Chassis Description", readonly=True, group='Details')
    PICChassisCLEI = schema.Text(title=u"Chassis CLEI", readonly=True, group='Details')
    PICCPU = schema.Int(title=u"CPU Util", readonly=True, group='Details')
    PICMemory = schema.Int(title=u"Memory", readonly=True, group='Details')
    PICTemp = schema.Text(title=u"Temperature", readonly=True, group='Details')
    PICState = schema.Text(title=u"State", readonly=True, group='Details')
    PICUpTime = schema.Text(title=u"Up Time", readonly=True, group='Details')

class IJuniperMICInfo(IComponentInfo):
    """
Info adapter for JuniperMIC component
"""
    containerIndex = schema.Int(title=u"Container Index", readonly=True, group='Details')
    containerDescr = schema.Text(title=u"Container Description", readonly=True, group='Details')
    containerParentIndex = schema.Int(title=u"Parent Index", readonly=True, group='Details')
    containerParentDescr = schema.Text(title=u"Parent Description", readonly=True, group='Details')
#    MICType = schema.Text(title=u"Type", readonly=True, group='Details')
    MICDescr = schema.Text(title=u"Description", readonly=True, group='Details')
    MICSerialNo = schema.Text(title=u"Serial No.", readonly=True, group='Details')
    MICRevision = schema.Text(title=u"Revision", readonly=True, group='Details')
    MICPartNo = schema.Text(title=u"Part No.", readonly=True, group='Details')
    MICChassisId = schema.Text(title=u"Chassis Id.", readonly=True, group='Details')
    MICChassisDescr = schema.Text(title=u"Chassis Description", readonly=True, group='Details')
    MICChassisCLEI = schema.Text(title=u"Chassis CLEI", readonly=True, group='Details')
    MICCPU = schema.Int(title=u"CPU Util", readonly=True, group='Details')
    MICMemory = schema.Int(title=u"Memory", readonly=True, group='Details')
    MICTemp = schema.Text(title=u"Temperature", readonly=True, group='Details')
    MICState = schema.Text(title=u"State", readonly=True, group='Details')
    MICUpTime = schema.Text(title=u"Up Time", readonly=True, group='Details')

class IJuniperBaseCompInfo(IComponentInfo):
    """
Info adapter for JuniperBaseComp component
"""
    containerIndex = schema.Int(title=u"Container Index", readonly=True, group='Details')
    containerDescr = schema.Text(title=u"Container Description", readonly=True, group='Details')
    containerParentIndex = schema.Int(title=u"Parent Index", readonly=True, group='Details')
    containerParentDescr = schema.Text(title=u"Parent Description", readonly=True, group='Details')
#    BaseCompType = schema.Text(title=u"Type", readonly=True, group='Details')
    BaseCompDescr = schema.Text(title=u"Description", readonly=True, group='Details')
    BaseCompSerialNo = schema.Text(title=u"Serial No.", readonly=True, group='Details')
    BaseCompRevision = schema.Text(title=u"Revision", readonly=True, group='Details')
    BaseCompPartNo = schema.Text(title=u"Part No.", readonly=True, group='Details')
    BaseCompChassisId = schema.Text(title=u"Chassis Id.", readonly=True, group='Details')
    BaseCompChassisDescr = schema.Text(title=u"Chassis Description", readonly=True, group='Details')
    BaseCompChassisCLEI = schema.Text(title=u"Chassis CLEI", readonly=True, group='Details')
    BaseCompCPU = schema.Int(title=u"CPU Util", readonly=True, group='Details')
    BaseCompMemory = schema.Int(title=u"Memory", readonly=True, group='Details')
    BaseCompTemp = schema.Text(title=u"Temperature", readonly=True, group='Details')
    BaseCompState = schema.Text(title=u"State", readonly=True, group='Details')
    BaseCompUpTime = schema.Text(title=u"Up Time", readonly=True, group='Details')

class IJuniperRoutingEngineInfo(IComponentInfo):
    """
Info adapter for JuniperRoutingEngine component
"""
    containerIndex = schema.Int(title=u"Container Index", readonly=True, group='Details')
    containerDescr = schema.Text(title=u"Container Description", readonly=True, group='Details')
    containerParentIndex = schema.Int(title=u"Parent Index", readonly=True, group='Details')
    containerParentDescr = schema.Text(title=u"Parent Description", readonly=True, group='Details')
#    RoutingEngineType = schema.Text(title=u"Type", readonly=True, group='Details')
    RoutingEngineDescr = schema.Text(title=u"Description", readonly=True, group='Details')
    RoutingEngineSerialNo = schema.Text(title=u"Serial No.", readonly=True, group='Details')
    RoutingEngineRevision = schema.Text(title=u"Revision", readonly=True, group='Details')
    RoutingEnginePartNo = schema.Text(title=u"Part No.", readonly=True, group='Details')
    RoutingEngineChassisId = schema.Text(title=u"Chassis Id.", readonly=True, group='Details')
    RoutingEngineChassisDescr = schema.Text(title=u"Chassis Description", readonly=True, group='Details')
    RoutingEngineChassisCLEI = schema.Text(title=u"Chassis CLEI", readonly=True, group='Details')
    RoutingEngineCPU = schema.Int(title=u"CPU Util", readonly=True, group='Details')
    RoutingEngineMemory = schema.Int(title=u"Memory", readonly=True, group='Details')
    RoutingEngineTemp = schema.Text(title=u"Temperature", readonly=True, group='Details')
    RoutingEngineState = schema.Text(title=u"State", readonly=True, group='Details')
    RoutingEngineUpTime = schema.Text(title=u"Up Time", readonly=True, group='Details')

class IJuniperBGPInfo(IComponentInfo):
    """
Info adapter for JuniperBGP component
"""
    bgpLocalAddress = schema.Text(title=u"Local address", readonly=True, group='Details')
    bgpRemoteAddress = schema.Text(title=u"Remote address", readonly=True, group='Details')
    bgpRemoteASN = schema.Text(title=u"Remote ASN", readonly=True, group='Details')
    bgpStateInt = schema.Int(title=u"State (int)", readonly=True, group='Details')
    bgpStateText = schema.Text(title=u"State", readonly=True, group='Details')
    bgpLastUpDown = schema.Text(title=u"Last Up/Down (days)", readonly=True, group='Details')

class IJuniperComponentsInfo(IComponentInfo):
    """
Info adapter for JuniperComponents component
"""
    containerIndex = schema.Int(title=u"Container Index", readonly=True, group='Details')
    containerDescr = schema.Text(title=u"Description", readonly=True, group='Details')
    containerParentIndex = schema.Int(title=u"Parent Index", readonly=True, group='Details')
    containerParentDescr = schema.Text(title=u"Parent Description", readonly=True, group='Details')
    containerType = schema.Text(title=u"Type", readonly=True, group='Details')
    containerLevel = schema.Int(title=u"Level", readonly=True, group='Details')
    containerNextLevel = schema.Int(title=u"Next Level", readonly=True, group='Details')

class IJuniperIpSecVPNInfo(IComponentInfo):
    """
Info adapter for JuniperIpSecVPN component
"""
    vpnPhase1LocalGwAddr = schema.Text(title=u"Phase 1 Local G/w", readonly=True, group='Details')
    vpnPhase1LocalIdValue = schema.Text(title=u"Local Id", readonly=True, group='Details')
    vpnPhase1RemoteIdValue = schema.Text(title=u"Remote Id", readonly=True, group='Details')
    vpnPhase1State = schema.Text(title=u"State", readonly=True, group='Details')
    vpnPhase2LocalGwAddr = schema.Text(title=u"Phase 2 Local G/w", readonly=True, group='Details')

class IJuniperIpSecNATInfo(IComponentInfo):
    """
Info adapter for JuniperIpSecNAT component
"""
    natId = schema.Text(title=u"NAT Id", readonly=True, group='Details')
    natNumPorts = schema.Int(title=u"Num. of Ports", readonly=True, group='Details')
    natNumSess = schema.Int(title=u"Num. of Sessions", readonly=True, group='Details')
    natPoolType = schema.Text(title=u"Pool Type", readonly=True, group='Details')


class IJuniperIpSecPolicyInfo(IComponentInfo):
    """
Info adapter for JuniperIpSecPolicy component
"""
    policyId = schema.Text(title=u"Policy Id", readonly=True, group='Details')
    policyAction = schema.Text(title=u"Action", readonly=True, group='Details')
    policyState = schema.Text(title=u"State", readonly=True, group='Details')
    policyFromZone = schema.Text(title=u"From Zone", readonly=True, group='Details')
    policyToZone = schema.Text(title=u"To Zone", readonly=True, group='Details')
    policyName = schema.Text(title=u"Policy Name", readonly=True, group='Details')

class IJuniperVlanInfo(IComponentInfo):
    """
Info adapter for JuniperVlan component
"""
    vlanName = schema.Text(title=u"Name", readonly=True, group='Details')
    vlanType = schema.Text(title=u"Type", readonly=True, group='Details')
    vlanTag = schema.Int(title=u"Tag", readonly=True, group='Details')
    vlanPortGroup = schema.Int(title=u"Port Group", readonly=True, group='Details')
    vlanInterfaceInfo = schema.Text(title=u"Interface Info", readonly=True, group='Details')

