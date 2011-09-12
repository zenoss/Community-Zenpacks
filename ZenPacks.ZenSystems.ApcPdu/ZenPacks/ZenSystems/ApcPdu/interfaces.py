##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 February 3rd, 2011
# Revised:
#
# interfaces.py for ApcPdu ZenPack
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


class IApcPduOutletInfo(IComponentInfo):
    """
Info adapter for ApcPduOutlet component
"""
    outNumber = schema.Text(title=u"Number", readonly=True, group='Details')
    outName = schema.Text(title=u"Name", readonly=True, group='Details')
    outState = schema.Text(title=u"State", readonly=True, group='Details')
    outBank = schema.Text(title=u"Bank", readonly=True, group='Details')

class IApcPduBankInfo(IComponentInfo):
    """
Info adapter for ApcPduBank component
"""
    bankNumber = schema.Int(title=u"Number", readonly=True, group='Details')
#    bankState = schema.Int(title=u"State (value)", readonly=True, group='Details')
    bankStateText = schema.Text(title=u"State", readonly=True, group='Details')

class IApcPduPSInfo(IComponentInfo):
    """
Info adapter for ApcPduPScomponent
"""
    supply1Status = schema.Text(title=u"Power Supply 1 Status", readonly=True, group='Details')
    supply2Status = schema.Text(title=u"Power Supply 2 Status", readonly=True, group='Details')

