import os

from Products.ZenRRD.tests.BaseParsersTestCase import BaseParsersTestCase

from ZenPacks.community.OpenSolaris.parsers.opensolaris.uptime import uptime
from ZenPacks.community.OpenSolaris.parsers.opensolaris.dladm import dladm
from ZenPacks.community.OpenSolaris.parsers.opensolaris.mpstat_a import mpstat_a
from ZenPacks.community.OpenSolaris.parsers.opensolaris.df_ag import df_ag

class OpenSolarisParsersTestCase(BaseParsersTestCase):

    def testParsers(self):
        """
        Test all of the parsers that have test data files in the data
        directory.
        """
        datadir = "%s/parserdata/opensolaris" % os.path.dirname(__file__)

        parserMap = {
                     '/bin/uptime': uptime,
                     '/usr/sbin/dladm show-link -s': dladm,
                     '/usr/bin/mpstat -a': mpstat_a,
                     '/bin/df -ag': df_ag,
                    }

        self._testParsers(datadir, parserMap)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(OpenSolarisParsersTestCase))
    return suite


