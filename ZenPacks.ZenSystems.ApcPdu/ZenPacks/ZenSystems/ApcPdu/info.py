##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 3rd, 2011
# Revised:
#
# info.py for ApcPdu ZenPack
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of ApcPdu components.

$Id: info.py,v 1.2 2010/12/14 20:45:46 jc Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from ZenPacks.ZenSystems.ApcPdu import interfaces


class ApcPduOutletInfo(ComponentInfo):
    implements(interfaces.IApcPduOutletInfo)

    outNumber = ProxyProperty("outNumber")
    outName = ProxyProperty("outName")
    outState = ProxyProperty("outState")
    outBank = ProxyProperty("outBank")

class ApcPduBankInfo(ComponentInfo):
    implements(interfaces.IApcPduBankInfo)

    bankNumber = ProxyProperty("bankNumber")
    bankState = ProxyProperty("bankState")
    bankStateText = ProxyProperty("bankStateText")

class ApcPduPSInfo(ComponentInfo):
    implements(interfaces.IApcPduPSInfo)

    supply1Status = ProxyProperty("supply1Status")
    supply2Status = ProxyProperty("supply2Status")



