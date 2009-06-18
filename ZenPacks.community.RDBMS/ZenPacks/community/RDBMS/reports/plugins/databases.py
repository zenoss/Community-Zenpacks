###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################


import Globals
from Products.ZenReports import Utils, Utilization

class databases:
    "The databases report"

    def run(self, dmd, args):
        report = []
        summary = Utilization.getSummaryArgs(dmd, args)
        for d in Utilization.filteredDevices(dmd, args):
            for f in d.os.softwaredatabases():
                if not f.monitored(): continue
                total = f.totalBytes()
                used = f.usedBytes()
                available = total - used
                percent = Utils.percent(used, total)
                r = Utils.Record(device=d,
                                 deviceName=d.id,
                                 database=f,
                                 dbname=f.dbname,
				 type=f.type,
                                 usedBytes=used,
                                 availBytes=available,
                                 percentFull=percent,
                                 totalBytes=total)
                report.append(r)
        return report
