##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 7th, 2011
# Revised:
#
# info.py for ApcAts ZenPack
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of ApcAts components.

$Id: info.py,v 1.2 2010/12/14 20:45:46 jc Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.component import ComponentInfo
from Products.Zuul.decorators import info
from ZenPacks.ZenSystems.ApcAts import interfaces


class ApcAtsInputInfo(ComponentInfo):
    implements(interfaces.IApcAtsInputInfo)

    inputType = ProxyProperty("inputType")
    inputName = ProxyProperty("inputName")
    inputFrequency = ProxyProperty("inputFrequency")
    inputVoltage = ProxyProperty("inputVoltage")
    statusSelectedSource = ProxyProperty("statusSelectedSource")


