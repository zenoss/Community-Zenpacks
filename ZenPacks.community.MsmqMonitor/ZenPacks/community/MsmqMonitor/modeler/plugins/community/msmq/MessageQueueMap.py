__doc__="""MessageQueueMap

MsmqPlugin retrieves a list of queues currently on a system

$Id: MessageQueueMap.py v1.0 2010/04/14 13:37:00 sheparju Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from subprocess import Popen, PIPE
import re

from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin

class MessageQueueMap(PythonPlugin):

    ZENPACKID = 'ZenPacks.community.MsmqMonitor'

    maptype = "MessageQueue"
    compname = "os"
    relname = "msmq"
    modname = "ZenPacks.community.MsmqMonitor.MessageQueue"

    deviceProperties = PythonPlugin.deviceProperties + ('zWinUser',
                                                        'zWinPassword')

    def prepare(self, device, log):
        cmd = "$ZENHOME/bin/wmic -U '%s'%%'%s' //%s '%s'" % (
                getattr(device, 'zWinUser',None),
                getattr(device, 'zWinPassword',None),
                str(device.manageIp),
                'SELECT Name FROM Win32_PerfRawData_MSMQ_MSMQQueue')
        log.debug( "MSMQ: Command prepared: %s", cmd )
        return cmd

    def collect(self, device, log):
        wcmd = self.prepare(device, log)
        wrun = Popen(wcmd, shell=True, stdout=PIPE).stdout
        return wrun.read()

    def process(self, device, results, log):
        log.info('MSMQ: Processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        log.info('Results = %s', results)
        qlist = results.split('\n')[3:]
        qmatch = re.compile('^[^\\\\]+\\\\([^\\\\$]+)(\$?\\\\)?([^\\\\$]+)\$?$')
        qcount = 0
        for q in qlist:
            if q not in (None, ''):
                match = qmatch.search(q)
                if not match:
                    log.debug('MSMQ: Queue %s did not match regex %s',q,qmatch.pattern)
                    continue
                om = self.objectMap()
                if 'private$' in q.lower():
                    om.id = match.groups()[2]
                    om.queueType = 'private'
                else:
                    om.id = match.groups()[0]
                    om.queueType = 'public'
                log.debug('MSMQ: Found %s queue %s (%s)',om.queueType,om.id,q)
                om.discoveryAgent = self.name()
                om.isUserCreatedFlag = True
                om.monitor = False
                rm.append(om)
                qcount += 1
        log.info('MSMQ: Found %d queues.',qcount)
        return rm



