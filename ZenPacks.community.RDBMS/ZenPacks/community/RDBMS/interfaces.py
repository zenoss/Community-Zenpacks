################################################################################
#
# This program is part of the RDBMS Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""interfaces

describes the form field to the user interface.

$Id: interfaces.py,v 1.3 2010/09/27 00:05:28 egor Exp $"""

__version__ = "$Revision: 1.3 $"[11:-2]

from Products.Zuul.interfaces import IComponentInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IDatabaseInfo(IComponentInfo):
    """
    Info adapter for Database components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    dbSrvInst = schema.Entity(title=u"DB Server Instance", readonly=True, group='Details')
    type = schema.Text(title=u"Type", readonly=True, group='Details')
    version = schema.Text(title=u"Version", readonly=True, group='Details')
    contact = schema.Text(title=u"Contact", readonly=True, group='Details')
    activeTime = schema.Text(title=u"Active Time", readonly=True, group='Details')
    blockSizeString = schema.Text(title=u"Units Size", readonly=True, group='Details')
    totalBytesString = schema.Text(title=u"Size Allocated", readonly=True, group='Details')
    usedBytesString = schema.Text(title=u"Size Used", readonly=True, group='Details')
    capacity = schema.Text(title=u"Utilization", readonly=True, group='Details')

class IDBSrvInstInfo(IComponentInfo):
    """
    Info adapter for DB Server Instance components.
    """
    status = schema.Text(title=u"Status", readonly=True, group='Overview')
    contact = schema.Text(title=u"Contact", readonly=True, group='Details')
    manufacturer = schema.Entity(title=u"Manufacturer", readonly=True,
                                group='Details')
    product = schema.Entity(title=u"Model", readonly=True, group='Details')
