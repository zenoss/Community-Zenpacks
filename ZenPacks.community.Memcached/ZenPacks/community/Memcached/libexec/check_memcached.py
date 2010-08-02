#!/usr/bin/env python
"""

    check_memcached.py 

    This script is part of the Zenpacks.community.Memcached by B Maqueira.
    It connects to memcached instances and retrieves and parses
    the stats output
 
"""
import sys
from optparse import OptionParser
import Globals
from ZenPacks.community.Memcached.lib.Memcached import memcached

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-H', '--host', dest='host', default='localhost',
            help='Hostname of memcached server')
    parser.add_option('-p', '--port', dest='port', default=11211,
            help='Port of memcached server')
    parser.add_option('-t', '--timeout', dest='timeout', default=3,
            help="connection time out")
    options, args = parser.parse_args()

    if not options.host:
        print "You must specify the host parameter."
        sys.exit(1)

    try:
        memStats = memcached(options.host, options.port, options.timeout)
    except Exception, e:
        print "CMD FAIL| %s" % e
        sys.exit(1)

    cmdOutPut = "CMD OK|" 
    for stat in [ 'hit_percent', 'usage_percent', 'uptime', 'time', 'rusage_user', 'rusage_system', 'curr_items',
                  'total_items', 'bytes', 'curr_connections', 
                  'total_connections', 'connection_structures', 'cmd_flush', 'cmd_get', 'cmd_set', 
                  'get_hits', 'get_misses', 'evictions', 
                  'bytes_read', 'bytes_written', 'limit_maxbytes', 'threads', 'accepting_conns',
                  'listen_disabled_num', 'get_set_ratio', 'missed_percent'
                 ]:
       cmdOutPut += "%s=%s " % (stat, memStats.get(stat))

    print cmdOutPut 
