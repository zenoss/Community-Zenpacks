###############################################################################
#
# UpsParser command parser plugin
#
###############################################################################

__doc__ = """ UpsParser

UpsParser maps Opengear the "config -g config" command to zenoss data

$id: $"""

__version__ = "$Revision: 1.1 $"[11:-2]

import logging
import os
import string
import sys

from pprint import pformat
from HTMLParser import HTMLParser

import Globals

from Products.ZenRRD.CommandParser import CommandParser

log = logging.getLogger("ZenPack.Opengear.ConsoleServer.parsers.UpsParser")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

class UpsRow(object):

    system = None
    model = None
    online = None
    battery = None
    input = None
    output = None
    load = None
    temp = None
    runtime = None
    data = None

    def __init__(self):
        pass

    def __str__(self):
        rv = []
        rv.append("%s = %s" % ("system", self.system,))
        rv.append("%s = %s" % ("model", self.model,))
        rv.append("%s = %s" % ("online", self.online,))
        rv.append("%s = %s" % ("battery", self.battery,))
        rv.append("%s = %s" % ("input", self.input,))
        rv.append("%s = %s" % ("output", self.output,))
        rv.append("%s = %s" % ("load", self.load,))
        rv.append("%s = %s" % ("temp", self.temp,))
        rv.append("%s = %s" % ("runtime", self.runtime,))
        rv.append("%s = %s" % ("data", self.data,))
        return "{%s}" % (', '.join(rv),)

class Spider(HTMLParser):
    """ Parse HTML output of the UPS command

    This HTML parser for the NUT output is extremely fragile due to the
    invalid tags which are produced.

    """

    COL_SYSTEM  = 1
    COL_MODEL   = 2
    COL_STATUS  = 3
    COL_BATTERY = 4
    COL_INPUT   = 5
    COL_OUTPUT  = 6
    COL_LOAD    = 7
    COL_TEMP     = 8
    COL_RUNTIME = 9
    COL_DATA    = 10

    row = False
    cell = 0
    input = False
    upsrow = None
    upsrows = []
    tempskip = False
    callback = None

    def __init__(self, contents, callback = None):
        HTMLParser.__init__(self)
        #req = urlopen(url)
        self.feed(contents)

    def handle_starttag(self, tag, attrs):
        if tag == 'tr' and attrs:
            self.row = True
            log.debug("Found row => %s" % (attrs[0][1],))
        elif tag == 'td' and attrs:
            self.cell += 1
            log.debug("Found cell => '%s'" % (attrs[0][1],))
            if attrs[0][1] == 'field-input':
                self.input = True
                if self.upsrow is None:
                    self.upsrow = UpsRow()

    def float(self, value):

        rv = 0.0
        if value is None:
            return rv

        last = len(value) - 1
        data = value
        if value[last] == "%":
            data = value[:last]

        try:
            rv = float(data)
        except ValueError:
            log.exception("Failed parsing float: %s" % (data,))

        return rv

    def handle_data(self, data):

        # Temperature values are broken up by escaped HTML tokens
        if self.tempskip:
            self.tempskip = False
            return

        log.debug("Found data => %s" % (data,))
        data = data.translate(string.maketrans("", ""), string.whitespace)
        if len(data) == 0:
            return

        log.info("Found clean data => '%s'" % (data,))
        if self.input:
            if self.cell == self.COL_SYSTEM:
                self.upsrow.system = data
            elif self.cell == self.COL_MODEL:
                self.upsrow.model = data
            elif self.cell == self.COL_STATUS:
                if data.upper() in ("ONLINE",):
                    self.upsrow.online = 1.0
                else:
                    self.upsrow.online = 0.0
            elif self.cell == self.COL_BATTERY:
                self.upsrow.battery = self.float(data)
            elif self.cell == self.COL_INPUT:
                self.upsrow.input = self.float(data)
            elif self.cell == self.COL_OUTPUT:
                self.upsrow.output = self.float(data)
            elif self.cell == self.COL_LOAD:
                self.upsrow.load = self.float(data)
            elif self.cell == self.COL_TEMP:
                self.upsrow.temp = self.float(data)
                self.tempskip = True
            elif self.cell == self.COL_RUNTIME:
                self.upsrow.runtime = data
            elif self.cell == self.COL_DATA:
                self.upsrow.data = data
            else:
                log.error("No field for data: %s" % (data,))

    def handle_endtag(self, tag):
        if tag == 'tr':
            if self.row:
                self.row = False
            else:
                log.error("closed row which wasnt open")

            self.cell = 0
            self.input = False

            if self.upsrow is not None:
                log.debug("UPS row: %s" % (self.upsrow,))
                self.upsrows.append(self.upsrow)
                self.upsrow = None

class UpsParser(CommandParser):

    DEVICE_PATH = "/Server/Console/Opengear"

    def dataForParser(self, context, datapoint):
        rv = {}
        try:
            rv = dict(upsname = context.upsName, snmpindex = context.snmpindex)
        except:
            log.error("Object had no snmpindex or upsame: %s" % (
                context,))
            return {}

        log.debug("Returning: %s" % (str(rv),))
        return rv


    def processResults(self, cmd, results):
        output = cmd.result.output
        spider = Spider(output)

        for point in cmd.points:

            if 'upsname' not in point.data:
                log.error("No UPS name provided: %s" % (point.id,))
                continue

            devname = cmd.deviceConfig.device
            upsname = point.data['upsname']

            found = False
            for upsrow in spider.upsrows:
                if upsrow.system == upsname:
                    found = True
                    break

            if found == False:
                log.error("No such UPS: %s" % (upsname,))
                continue

            if point.id == "ogUpsStatusOnline":
                results.values.append((point, upsrow.online))
            elif point.id == "ogUpsStatusBattery":
                results.values.append((point, upsrow.battery))
            elif point.id == "ogUpsStatusInput":
                results.values.append((point, upsrow.input))
            elif point.id == "ogUpsStatusOutput":
                results.values.append((point, upsrow.output))
            elif point.id == "ogUpsStatusLoad":
                results.values.append((point, upsrow.load))
            elif point.id == "ogUpsStatusTemperature":
                results.values.append((point, upsrow.temp))
            #elif point.id == "ogUpsStatusRuntime":
            #    results.values.append((point, upsrow.runtime))
            else:
                log.error("Unknown point id: %s" % (point.id,))

        log.debug(pformat(results))
        return results
