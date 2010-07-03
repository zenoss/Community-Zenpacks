###############################################################################
#
# SerialPortParser command parser plugin
#
###############################################################################

__doc__ = """ SerialPortParser

SerialPortParser maps Opengear the "config -g config" command to zenoss data

$id: $"""

__version__ = "$Revision: 1.1 $"[11:-2]

import logging
import os
import sys

import Globals
from transaction import commit

from pprint import pformat

from Products.ZenRRD.CommandParser import CommandParser
from Products.ZenUtils.ZenScriptBase import ZenScriptBase

log = logging.getLogger(
    "ZenPack.Opengear.ConsoleServer.parsers.SerialPortParser")

class SerialPortParser(CommandParser):

    DEVICE_PATH = "/Server/Console/Opengear"
    ENTRY = ".1.3.6.1.4.1.25049.16.1.1"
    POINTS = {
        "ogSerialPortStatusPort"    : "%s.%d" % (ENTRY, 2,),
        "ogSerialPortStatusRxBytes" : "%s.%d" % (ENTRY, 3,),
        "ogSerialPortStatusTxBytes" : "%s.%d" % (ENTRY, 4,),
        "ogSerialPortStatusSpeed"   : "%s.%d" % (ENTRY, 5,),
        "ogSerialPortStatusDCD"     : "%s.%d" % (ENTRY, 6,),
        "ogSerialPortStatusDTR"     : "%s.%d" % (ENTRY, 7,),
        "ogSerialPortStatusDSR"     : "%s.%d" % (ENTRY, 8,),
        "ogSerialPortStatusCTS"     : "%s.%d" % (ENTRY, 9,),
        "ogSerialPortStatusRTS"     : "%s.%d" % (ENTRY, 10,),
    }

    def dataForParser(self, context, datapoint):
        rv = {}
        try:
            rv = dict(portid = context.id, snmpindex = context.snmpindex)
        except:
            log.error("Object had no snmpindex or devicename: %s" % (
                context,))
            return {}

        log.debug("Returning: %s" % (str(rv),))
        return rv

    def processResults(self, cmd, results):
        # split data into component blocks
        lines = cmd.result.output.split('\n')

        data = {}
        for line in lines:

            if len(line) == 0:
                continue

            splitted = line.split(' ')
            if len(splitted) < 2:
                continue

            data[splitted[0]] = ' '.join(splitted[1:])

        scriptbase = ZenScriptBase(noopts = 1, connect = True)
        for point in cmd.points:
            if point.id not in self.POINTS:
                continue

            if 'portid' not in point.data:
                log.error("No port id provided: %s" % (point.id,))
                continue

            if 'snmpindex' not in point.data:
                log.error("No snmpindex provided: %s" % (point.id,))
                continue

            oid = self.POINTS[point.id]
            devname = cmd.deviceConfig.device
            portid = point.data['portid']
            snmpindex = point.data['snmpindex']
            key = "%s.%d" % (oid, snmpindex,)

            if key not in data:
                continue

            try:
                value = float(data[key])
            except ValueError:
                continue


            # Update current model
            d = scriptbase.findDevice(devname)
            if d is not None and d.getDeviceClassPath() == self.DEVICE_PATH:

                port = d.SerialPrt._getOb(portid)
                if port is not None:
                    log.debug("setattr(%s, %s, %s)" % (d, point.id, value,))
                    setattr(port, point.id, value)
                    id = d.SerialPrt._setObject(portid, port)
                    commit()
                    #print "*** _getOb(%s)" % (portid,)
                    #print pformat(d.SerialPrt._getOb(portid).__dict__)
                else:
                    log.error("No such attribute: %s on %s" % (
                        point.id, d.getDeviceName(),))

            log.debug("Appending result %s: (%s / %s) %s" % (
                point.id, type(value), value, value,))
            results.values.append((point, value,))

        log.debug(pformat(results))
        return results
