################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMMemoryModule

IBMMemoryModule is an abstraction of a  Memory Module.

$Id: IBMMemoryModule.py,v 1.0 2009/06/23 22:17:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from ZenPacks.community.deviceAdvDetail.MemoryModule import *
from IBMComponent import *

class IBMMemoryModule(MemoryModule, IBMComponent):
    """MemoryModule object"""

    portal_type = meta_type = 'IBMMemoryModule'

InitializeClass(IBMMemoryModule)
