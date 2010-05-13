import os

from Products.ZenRRD.tests.BaseParsersTestCase import BaseParsersTestCase
from Products.ZenRRD.parsers.uptime import uptime

class OSXParsersTestCase(BaseParsersTestCase):

    def testOSXParsers(self):
        """
        Test all of the parsers that have test data files in the data directory.
        """
        parserMap = {'/usr/bin/uptime': uptime,
                     }
        datadir = "%s/parserdata/osx" % os.path.dirname(__file__)
        self._testParsers(datadir, parserMap)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(OSXParsersTestCase))
    return suite

