import os

from Products.ZenRRD.tests.BaseParsersTestCase import BaseParsersTestCase

from Products.ZenRRD.parsers.uptime import uptime
from ZenPacks.community.LinuxMonitorAddOn.parsers.linux.ifconfig import ifconfig
class GentooLinuxParsersTestCase(BaseParsersTestCase):

    def testParsers(self):
        """
        Test all of the parsers that have test data files in the data
        directory.
        """
        datadir = "%s/parserdata/linux" % os.path.dirname(__file__)

        parserMap = {
                     '/usr/bin/uptime': uptime,
                     '/sbin/ifconfig -a': ifconfig
                    }

        self._testParsers(datadir, parserMap)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(GentooLinuxParsersTestCase))
    return suite


