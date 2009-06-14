################################################################################
#
# This program is part of the NWMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__ = """filesystems

plugin for NetWare file systems usage report.

$Id: filesystems.py,v 1.00 2008/11/18 16:10:00 egor Exp $"""

__version__ = "$Revision: 1.00 $"[11:-2]

import Globals
from Products.ZenReports import Utils, Utilization

class filesystems:
    "The NetWare file systems report"

    def run(self, dmd, args):
        report = []
        summary = Utilization.getSummaryArgs(dmd, args)
        for d in Utilization.filteredDevices(dmd, args):
            for f in d.os.filesystems():
                if not f.monitored(): continue
                available, used = None, None
                used = f.usedBytes()
		available = f.availBytes()
                percent = Utils.percent(used, f.totalBytes())
                r = Utils.Record(device=d,
                                 deviceName=d.id,
                                 filesystem=f,
                                 mount=f.mount,
                                 usedBytes=used,
                                 availableBytes=available,
                                 percentFull=percent,
                                 totalBytes=f.totalBytes())
                report.append(r)
        return report
