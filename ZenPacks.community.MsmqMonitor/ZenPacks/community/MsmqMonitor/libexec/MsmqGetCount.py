#!/usr/bin/env python

import sys
from optparse import OptionParser
from subprocess import Popen, PIPE

class MsmqGetCount:

    def __init__(self, host, user, pswd, que):
        self.host = host
        self.user = user
        self.pswd = pswd
        self.que  = que
        self.count= 0

    def run(self):

        if self.que:
            wcmd = ' '.join([
              "$ZENHOME/bin/wmic -U '%s'%%'%s' //%s",
              '"SELECT MessagesInQueue FROM Win32_PerfRawData_MSMQ_MSMQQueue',
              "WHERE Name LIKE '%%%s'\""]
              ) % (self.user,self.pswd,self.host,self.que)
            wrun = Popen(wcmd, shell=True, stdout=PIPE).stdout
            wdta = wrun.read().split('\n')
            for d in wdta:
                if d not in (None,''):
                    if self.que.lower() not in d.lower(): continue
                    self.count,n = d.split('|')
            print 'queueCount:%s' % self.count

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "Usage: %s host user password queue" % sys.argv[0]
        sys.exit(1)

    (h,u,p,q) = sys.argv[1:]

    cmd = MsmqGetCount(h,u,p,q)
    cmd.run()


