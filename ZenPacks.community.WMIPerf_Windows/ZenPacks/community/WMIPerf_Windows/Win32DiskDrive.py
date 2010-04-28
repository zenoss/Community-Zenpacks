################################################################################
#
# This program is part of the WMIPerf_Windows Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Win32DiskDrive

Win32DiskDrive is an abstraction of a HardDisk.

$Id: Win32DiskDrive.py,v 1.0 2010/04/21 18:50:10 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.ZenossSecurity import *
from Products.ZenUtils.Utils import convToUnits
from Products.ZenModel.HardDisk import HardDisk

class Win32DiskDrive(HardDisk):
    """HardDisk object"""

    portal_type = meta_type = 'Win32DiskDrive'

    rpm = 0
    size = 0
    diskType = ""
    hotPlug = 0
    bay = 0
    FWRev = ""
    perfindex = ""

    statusmap ={0: ('grey', 3, 'Unknown'),
                1: ('grey', 3, 'Other'),
                2: ('green', 0, 'OK'),
                3: ('orange', 4, 'Degraded'),
                4: ('yellow', 3, 'Stressed'),
                5: ('yellow', 3, 'Predictive Failure'),
                6: ('orange', 4, 'Error'),
                7: ('red', 5, 'Non-Recoverable Error'),
                8: ('blue', 2, 'Starting'),
                9: ('yellow', 3, 'Stopping'),
                10: ('orange', 4, 'Stopped'),
                11: ('blue', 2, 'In Service'),
                12: ('grey', 3, 'No Contact'),
                13: ('orange', 4, 'Lost Communication'),
                14: ('orange', 4, 'Aborted'),
                15: ('grey', 3, 'Dormant'),
                16: ('orange', 4, 'Stopping Entity in Error'),
                17: ('green', 0, 'Completed'),
                18: ('yellow', 3, 'Power Mode'),
                }

    _properties = HardDisk._properties + (
                 {'id':'rpm', 'type':'int', 'mode':'w'},
                 {'id':'diskType', 'type':'string', 'mode':'w'},
                 {'id':'size', 'type':'int', 'mode':'w'},
                 {'id':'bay', 'type':'int', 'mode':'w'},
                 {'id':'FWRev', 'type':'string', 'mode':'w'},
                 {'id':'perfindex', 'type':'string', 'mode':'w'},
                )

    factory_type_information = ( 
        { 
            'id'             : 'HardDisk',
            'meta_type'      : 'HardDisk',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'HardDisk_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addHardDisk',
            'immediate_view' : 'viewWin32DiskDrive',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewWin32DiskDrive'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )


    def sizeString(self):
        """
        Return the number of total bytes in human readable form ie 10MB
        """
        return convToUnits(self.size,divby=1000)

    def rpmString(self):
        """
        Return the RPM in tradition form ie 7200, 10K
        """
        return 'Unknown'

    def getStatus(self):
        """
        Return the components status
        """
        return round(self.cacheRRDValue('OperationalStatus', 0))

    def statusDot(self, status=None):
        """
        Return the Dot Color based on maximal severity
        """
        if status is None:
            colors=['grey', 'green', 'purple', 'blue', 'yellow','orange', 'red']
            if not self.monitor: return 'grey'
            status = self.getStatus()
            severity = colors.index(self.statusmap[status][0])
            eseverity = self.ZenEventManager.getMaxSeverity(self) + 1
            if severity == 0 and eseverity == 1: return 'grey'
            if eseverity > severity:
                severity = eseverity
            return colors[severity]
        return self.statusmap.get(status, ('grey', 3, 'other'))[0]

    def statusSeverity(self, status=None):
        """
        Return the severity based on status
        0:'Clean', 1:'Debug', 2:'Info', 3:'Warning', 4:'Error', 5:'Critical'
        """
        if status is None: status = self.getStatus()
        return self.statusmap.get(status, ('grey', 3, 'other'))[1]

    def statusString(self, status=None):
        """
        Return the status string
        """
        if status is None: status = self.getStatus()
        return self.statusmap.get(status, ('grey', 3, 'other'))[2]


InitializeClass(Win32DiskDrive)
