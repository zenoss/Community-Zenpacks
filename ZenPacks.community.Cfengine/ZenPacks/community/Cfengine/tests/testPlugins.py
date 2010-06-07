import os.path
import logging
from Products.DataCollector.ApplyDataMap import ApplyDataMap
from Products.ZenTestCase.BaseTestCase import BaseTestCase
from ZenPacks.community.Cfengine.modeler.plugins.community.cfenginemodeler \
    import cfenginemodeler

log = logging.getLogger("zen.Cfengine")

def loadData(filename):
    dataDir = os.path.join(os.path.dirname(__file__), 'plugindata/cfengine')
    dataFile = open(os.path.join(dataDir, filename))
    data = dataFile.read()
    dataFile.close()
    return data

class CfenginePluginsTestCase(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self)
        self.plugin = cfenginemodeler()
        self.device = self.dmd.Devices.createInstance('testDevice')

    def testCfengineModeler(self):
        data = loadData("cfenginemodeler")
        om = self.plugin.process(self.device, data, log)
        print om

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(CfenginePluginsTestCase))
    return suite

