##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 March 28th, 2011
# Revised:
#
# interfaces.py for ApcUps ZenPack
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


class IApcUpsBatteryInfo(IComponentInfo):
    """
Info adapter for ApcUpsBattery component
"""
#    batteryStatus = schema.Int(title=u"Battery Status Value", readonly=True, group='Details')
    batteryStatusText = schema.Text(title=u"Battery Status", readonly=True, group='Details')
    timeOnBattery = schema.Text(title=u"Time on Battery", readonly=True, group='Details')
    batteryLastReplacementDate = schema.Text(title=u"Battery Last Replacement Date", readonly=True, group='Details')
#    batteryReplaceIndicator = schema.Int(title=u"Battery Replace Indicator Value", readonly=True, group='Details')
    batteryReplaceIndicatorText = schema.Text(title=u"Battery Replace Indicator", readonly=True, group='Details')

