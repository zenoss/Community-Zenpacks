##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 7th, 2011
# Revised:
#
# interfaces.py for ApcAts ZenPack
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


class IApcAtsInputInfo(IComponentInfo):
    """
Info adapter for ApcAtsInput component
"""
    inputType = schema.Text(title=u"Input Type", readonly=True, group='Details')
    inputName = schema.Text(title=u"Input Name", readonly=True, group='Details')
    inputFrequency = schema.Text(title=u"Input Frequency", readonly=True, group='Details')
    inputVoltage = schema.Text(title=u"Input Voltage", readonly=True, group='Details')
    statusSelectedSource = schema.Text(title=u"Currently Selected Source", readonly=True, group='Details')

