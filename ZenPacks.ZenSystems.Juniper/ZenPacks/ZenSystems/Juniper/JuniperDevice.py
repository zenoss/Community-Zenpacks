##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 15th, 2011
# Revised:
#
# JuniperDevice object class
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

from Globals import InitializeClass
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from copy import deepcopy


class JuniperDevice(Device):
    "A Juniper Device"

#    portal_type = meta_type = 'JuniperDevice'

    #**************Custom data Variables here from modeling************************

    memoryUsedPercent = 0
    psuAvailable = 0

    #**************END CUSTOM VARIABLES *****************************


    #*************  Those should match this list below *******************
    _properties = Device._properties + (
        {'id':'memoryUsedPercent', 'type':'int', 'mode':''},
        {'id':'psuAvailable', 'type':'int', 'mode':''},
        )
    #****************

    _relations = Device._relations + (
        ('JuniperConte', ToManyCont(ToOne, 'ZenPacks.ZenSystems.Juniper.JuniperContents', 'JuniperDevConte')),
        ('JuniperComp', ToManyCont(ToOne, 'ZenPacks.ZenSystems.Juniper.JuniperComponents', 'JuniperDevComp')),
        ('JuniperRE', ToManyCont(ToOne, 'ZenPacks.ZenSystems.Juniper.JuniperRoutingEngine', 'JuniperDevRE')),
        ('JuniperFP', ToManyCont(ToOne, 'ZenPacks.ZenSystems.Juniper.JuniperFPC', 'JuniperDevFP')),
        ('JuniperPI', ToManyCont(ToOne, 'ZenPacks.ZenSystems.Juniper.JuniperPIC', 'JuniperDevPI')),
        ('JuniperMI', ToManyCont(ToOne, 'ZenPacks.ZenSystems.Juniper.JuniperMIC', 'JuniperDevMI')),
        ('JuniperBC', ToManyCont(ToOne, 'ZenPacks.ZenSystems.Juniper.JuniperBaseComp', 'JuniperDevBC')),
        ('JuniperBG', ToManyCont(ToOne, 'ZenPacks.ZenSystems.Juniper.JuniperBGP', 'JuniperDevBG')),
        ('JuniperIpSecV', ToManyCont(ToOne, 'ZenPacks.ZenSystems.Juniper.JuniperIpSecVPN', 'JuniperDevIpSecV')),
        ('JuniperIpSecN', ToManyCont(ToOne, 'ZenPacks.ZenSystems.Juniper.JuniperIpSecNAT', 'JuniperDevIpSecN')),
        ('JuniperIpSecP', ToManyCont(ToOne, 'ZenPacks.ZenSystems.Juniper.JuniperIpSecPolicy', 'JuniperDevIpSecP')),
        ('JuniperVl', ToManyCont(ToOne, 'ZenPacks.ZenSystems.Juniper.JuniperVlan', 'JuniperDevVl')),
        )

    factory_type_information = deepcopy(Device.factory_type_information)
    factory_type_information[0]['actions'] += (
            { 'id'              : 'JuniperStuff'
            , 'name'            : 'Juniper Information'
            , 'action'          : 'JuniperDeviceDetail'
            , 'permissions'     : (ZEN_VIEW, ) },
            )

    def __init__(self, *args, **kw):
        Device.__init__(self, *args, **kw)
        self.buildRelations()


InitializeClass(JuniperDevice)
