##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 April 19th, 2011
# Revised:
#
# info.py for Predictive Threshold ZenPack
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""info.py

Representation of Predictive Threshold components.

$Id: info.py,v 1.2 2010/12/14 20:45:46 jc Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from zope.interface import implements
from Products.Zuul.infos import ProxyProperty
from Products.Zuul.interfaces import template as templateInterfaces
from Products.Zuul.infos.template import ThresholdInfo
from Products.Zuul.decorators import info
from ZenPacks.community.PredictiveThreshold import interfaces

class PredThresholdInfo(ThresholdInfo):
    implements(interfaces.IPredThresholdInfo)
#    pointval = ProxyProperty("pointval")
    severity = ProxyProperty("severity")
    eventClass = ProxyProperty("eventClass")
    escalateCount = ProxyProperty("escalateCount")
    alpha = ProxyProperty("alpha")
    beta = ProxyProperty("beta")
    gamma = ProxyProperty("gamma")
    rows = ProxyProperty("rows")
    season = ProxyProperty("season")
    window = ProxyProperty("window")
    threshold = ProxyProperty("threshold")
    delta = ProxyProperty("delta")
    predcolor = ProxyProperty("predcolor")
    cbcolor = ProxyProperty("cbcolor")
    tkcolor = ProxyProperty("tkcolor")



