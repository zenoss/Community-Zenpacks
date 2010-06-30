################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqFcaPhyDrv

cpqFcaPhyDrv is an abstraction of a HP FCA Hard Disk.

$Id: cpqFcaPhyDrv.py,v 1.1 2010/06/30 16:22:01 egor Exp $"""

__version__ = "$Revision: 1.1 $"[11:-2]

from HPHardDisk import *

class cpqFcaPhyDrv(HPHardDisk):
    """cpqFcaPhyDrv object
    """

    chassis = ""
    busNumber = 1
    external = False

    _properties = HPHardDisk._properties + (
                    {'id':'chassis', 'type':'string', 'mode':'w'},
                    {'id':'busNumber', 'type':'int', 'mode':'w'},
                    {'id':'external', 'type':'boolean', 'mode':'w'},
                )

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'other'),
                2: (DOT_YELLOW, SEV_WARNING, 'Not Configured'),
                3: (DOT_GREEN, SEV_CLEAN, 'Ok'),
                4: (DOT_ORANGE, SEV_ERROR, 'Threshold Exceeded'),
                5: (DOT_ORANGE, SEV_ERROR, 'Predictive Failure'),
                6: (DOT_RED, SEV_CRITICAL, 'Failed'),
                7: (DOT_RED, SEV_CRITICAL, 'Unsupported Drive'),
                }

InitializeClass(cpqFcaPhyDrv)
