##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 9th, 2011
# Revised:
#
# interfaces.py for DellUps ZenPack
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


class IDellUpsBatteryInfo(IComponentInfo):
    """
Info adapter for DellUpsBattery component
"""
#    batteryABMStatus = schema.Text(title=u"Advanced Battery Monitoring Status (value)", readonly=True, group='Details')
    batteryABMStatusText = schema.Text(title=u"Advanced Battery Monitoring Status", readonly=True, group='Details')
    batteryTestStatus = schema.Text(title=u"Battery Test Status", readonly=True, group='Details')

