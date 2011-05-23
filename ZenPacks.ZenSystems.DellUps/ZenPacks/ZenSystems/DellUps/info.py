##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 9th, 2011
# Revised:
#
# info.py for DellUps ZenPack
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of DellUps components.

$Id: info.py,v 1.2 2010/12/14 20:45:46 jc Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from ZenPacks.ZenSystems.DellUps import interfaces


class DellUpsBatteryInfo(ComponentInfo):
    implements(interfaces.IDellUpsBatteryInfo)

    batteryABMStatus = ProxyProperty("batteryABMStatus")
    batteryABMStatusText = ProxyProperty("batteryABMStatusText")
    batteryTestStatus = ProxyProperty("batteryTestStatus")


