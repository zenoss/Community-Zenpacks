##########################################################################
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 April 19th, 2011
# Revised:
#
# interfaces.py for Predictive Threshold ZenPack
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces.py

Representation of Predictive Threshold components.

$Id: info.py,v 1.2 2010/12/14 20:45:46 jc Exp $"""

__version__ = "$Revision: 1.4 $"[11:-2]

from Products.Zuul.interfaces import IInfo, IFacade
from Products.Zuul.interfaces.template import IThresholdInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t

class IPredThresholdInfo(IThresholdInfo):
    """
    Interfaces for Predictive Threshold
    """
#    pointval = schema.List(title=_t(u"Data Point"), xtype='datapointitemselector', order=6)
    escalateCount = schema.Int(title=_t(u'Escalate Count'), order=9)
    alpha = schema.Text(title=_t(u'Alpha'), order=10)
    beta = schema.Text(title=_t(u'Beta'), order=11)
    gamma = schema.Text(title=_t(u'Gamma'), order=12)
    rows = schema.Text(title=_t(u'Rows'), order=13)
    season = schema.Text(title=_t(u'Season'), order=14)
    window = schema.Text(title=_t(u'Window'), order=15)
    threshold = schema.Text(title=_t(u'Threshold'), order=16)
    delta = schema.Text(title=_t(u'Delta'), order=17)
    predcolor = schema.Text(title=_t(u'Prediction Color'), order=18)
    cbcolor = schema.Text(title=_t(u'Confidence Band Color'), order=19)
    tkcolor = schema.Text(title=_t(u'Tick Color'), order=20)
#    pointval = schema.List(title=_t(u"Data Point"), xtype='datapointitemselector')
#    escalateCount = schema.Int(title=_t(u'Escalate Count'))
#    alpha = schema.Text(title=_t(u'Alpha'))
#    beta = schema.Text(title=_t(u'Beta'))
#    gamma = schema.Text(title=_t(u'Gamma'))
#    rows = schema.Text(title=_t(u'Rows'))
#    season = schema.Text(title=_t(u'Season'))
#    window = schema.Text(title=_t(u'Window'))
#    threshold = schema.Text(title=_t(u'Threshold'))
#    delta = schema.Text(title=_t(u'Delta'))
#    predcolor = schema.Text(title=_t(u'Prediction Color'))
#    cbcolor = schema.Text(title=_t(u'Confidence Band Color'))
#    tkcolor = schema.Text(title=_t(u'Tick Color'))



