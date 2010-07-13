################################################################################
#
# This program is part of the ZenODBC Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""findodbc

find installed ODBC driver

$Id: findodbc.py,v 1.0 2010/06/16 23:40:16 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

try:
    from pyodbc import *
except:
    from isql import *