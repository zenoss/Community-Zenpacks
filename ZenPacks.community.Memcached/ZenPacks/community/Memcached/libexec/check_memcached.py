#!/usr/bin/env python

################################################################################
# This program is part of the Zenpack.community.Memcached Zenpack for Zenoss.
# Copyright (C) 2011 B Maqueira
#
# This program can be used under the GNU General Public License version 2
# For complete information please visit: http://www.zenoss.com/oss/
################################################################################

from twisted.internet import reactor, protocol
from twisted.protocols.memcache import MemCacheProtocol, DEFAULT_PORT
from twisted.python import usage
from ZenPacks.community.Memcached.datasources.MemcachedDataSource import MEMCACHED_STATS
import sys

class MemcachedMonitor( MemCacheProtocol ):

    def connectionMade(self):
        return self.stats()\
		.addCallback( self.calculatePercentages )\
                .addCallback( self.outputResults )\
                .addErrback( self.handleErrors )\

    def calculatePercentages( self, stats):
        #cast
        for k,v in stats.items():
            try:
                stats[k] = float(v)
            except:
                stats[k] = v

        stats['hit_percent'] = 0
        if ('get_hits' in stats 
            and 'cmd_get' in stats
            and stats['cmd_get'] > 0):
            stats['hit_percent'] = 100 * stats['get_hits'] / stats['cmd_get']

        stats['usage_percent'] = 0
        if ('bytes' in stats  
            and 'limit_maxbytes' in stats
            and stats['limit_maxbytes'] > 0):
            stats['usage_percent'] = 100 * stats['bytes'] / stats['limit_maxbytes']
	
        stats['get_set_ratio'] = 0
        if ('cmd_set' in stats
           and 'cmd_get' in stats
           and stats['cmd_set'] > 0):
           stats['get_set_ratio'] = stats['cmd_get'] / stats['cmd_set']

        stats['missed_percent'] = 0 
        if ('get_misses' in stats
            and 'cmd_get' in stats
            and stats['cmd_get'] > 0):
            stats['missed_percent'] = 100 * stats['get_misses'] / stats['cmd_get']
        
        statNames = MEMCACHED_STATS.keys()
        return dict(zip( statNames, [ stats.get(x, None) for x in statNames ]))  

    def outputResults(self, stats):
        print "CMD OK|%s" % ' '.join(["%s=%s" %(k,v) for k,v in stats.items()])
        self.transport.loseConnection()

    def handleErrors(self, failure):
        print "CMD FAIL|%s" % failure.getErrorMessage().replace('\n', ' ')
        self.factory.exitCode = 1
        self.transport.loseConnection()

class MemcachedMonitorFactory( protocol.ClientFactory ):
    
    protocol = MemcachedMonitor

    def __init__(self, timeout=60):
        self.memcachedTimeout = timeout    
        self.exitCode = 0

    def clientConnectionFailed(self, connector, reason):
        print "CMD FAIL| %s" % reason.getErrorMessage().replace('\n', ' ')
        self.exitCode = 1
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        reactor.stop()	

    def buildProtocol(self, addr):    
        p = protocol.ClientFactory.buildProtocol(self, addr)
        p.persistentTimeOut = p.timeOut = self.memcachedTimeout
        return p

class Options(usage.Options):
    optParameters = [
        ["host",    "H", "localhost",  "memcached server hostname"],
        ["port",    "p", DEFAULT_PORT, "memcached server port"],
        ["timeout", "t", 3,            "connection time out"]
    ]


if __name__ == '__main__':
    options = Options()
    try:
        options.parseOptions()
    except usage.UsageError, errortext:
        print 'CMD FAIL|%s: %s' % (sys.argv[0], errortext)
        sys.exit(1)

    m = MemcachedMonitorFactory( int(options['timeout']) )
    reactor.connectTCP(options['host'], int(options['port']), m)
    reactor.run()
    sys.exit( m.exitCode )
