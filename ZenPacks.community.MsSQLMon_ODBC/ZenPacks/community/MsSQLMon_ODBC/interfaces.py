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

$Id: interfaces.py,v 1.1 2010/09/27 23:16:12 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from ZenPacks.community.RDBMS.interfaces import IDatabaseInfo, IDBSrvInstInfo
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t


class IMsSqlDatabaseInfo(IDatabaseInfo):
    """
    Info adapter for MS SQL Database components.
    """
    dbid = schema.Int(title=u"dbid", readonly=True, group=u"Details")
    contact = schema.Text(title=u"Owner", readonly=True, group=u"Details")
    activeTime = schema.Text(title=u"Created", readonly=True, group=u"Details")
    updateability = schema.Text(title=u"Updateability", readonly=True, group=u"Database Properties")
    useraccess = schema.Text(title=u"User Access", readonly=True, group=u"Database Properties")
    recovery = schema.Text(title=u"Recovery", readonly=True, group=u"Database Properties")
    version = schema.Text(title=u"Version", readonly=True, group=u"Database Properties")
    collation = schema.Text(title=u"Collation", readonly=True, group=u"Database Properties")
    sqlsortorder = schema.Text(title=u"SQL Sort Order", readonly=True, group=u"Database Properties")
    dbproperties = schema.List(title=u"Database Properties", readonly=True, group=u"Database Properties")

class IMsSqlSrvInstInfo(IDBSrvInstInfo):
    """
    Info adapter for MS SQL Server Instance components.
    """
    edition = schema.Text(title=u"Edition", readonly=True, group=u"Details")
    productVersion = schema.Text(title=u"Product Version", readonly=True, group=u"Details")
    productLevel = schema.Text(title=u"Product Level", readonly=True, group=u"Details")
    licenseType = schema.Text(title=u"License Type", readonly=True, group=u"Details")
    numLicenses = schema.Int(title=u"Licenses", readonly=True, group=u"Details")
    processID = schema.Int(title=u"Process ID", readonly=True, group=u"Details")
    dbsiproperties = schema.List(title=u"Instance Properties", readonly=True, group=u"Details")
