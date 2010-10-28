#!/usr/bin/env python

################################################################################
#
# This program is part of the FormulaDataSource Zenpack for Zenoss.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

import Globals
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from transaction import commit

dmd = ZenScriptBase(connect=True, noopts=True).dmd

import re, sys

from math import *

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-d", "--device", dest="device",
                  help="Specify device name", metavar="DEVICE")

parser.add_option("-s", "--datasource", dest="datasource",
                  help="Specify datasource", metavar="DATASOURCE")

parser.add_option("-c", "--formula", dest="formula",
                  help="Specify formula to calculate", metavar="FORMULA")

(options, args) = parser.parse_args()

if not options.device and not options.datasource and not options.formula:
    parser.print_help()
    sys.exit()

d = dmd.Devices.findDevice(options.device)

formula = re.sub(r"\%(\w*)", r"d.getRRDValue('\1')", options.formula)
formula = re.sub(r"\here.(\w*)", r"d.\1", formula)

try:
    formula = eval(formula)
except SyntaxError:
    print "The formula generated an error: SyntaxError."
    sys.exit()
except NameError:
    print "The formula generated an error: NameError."
    sys.exit()
except TypeError:
    print "The formula generated an error: TypeError."
    sys.exit()

print "|%s=%s" % (options.datasource,formula)
