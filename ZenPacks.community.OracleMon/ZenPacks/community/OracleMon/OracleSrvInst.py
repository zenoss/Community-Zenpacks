################################################################################
#
# This program is part of the OracleMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""OracleSrvInst

OracleSrvInst is a SrvInst

$Id: OracleSrvInst.py,v 1.0 2010/12/13 09:57:49 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from ZenPacks.community.RDBMS.DBSrvInst import DBSrvInst


class OracleSrvInst(DBSrvInst):
    """
    MySQL SrvInst object
    """

    ZENPACKID = 'ZenPacks.community.OracleMon'


    dsn = ''


    _properties = DBSrvInst._properties + (
        {'id':'dsn', 'type':'string', 'mode':'w'},
        )

InitializeClass(OracleSrvInst)
