#!/usr/bin/env python
"""

    check_ttserver.py 

    This script connects to ttserver instances and retrieves and parses
    the stats output
 
"""
import sys
from optparse import OptionParser
import Globals
from ZenPacks.community.TokyoTyrant.lib.TTServer import ttyrant

#import os
#sys.path.append( os.path.dirname(os.path.realpath(__file__))  + '/../lib')
#from TTServer import ttyrant

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-H', '--host', dest='host', default='localhost',
            help='Hostname of ttserver server')
    parser.add_option('-p', '--port', dest='port', default=1978,
            help='Port of ttserver server')
    parser.add_option('-t', '--timeout', dest='timeout', default=3,
            help="connection time out")
    options, args = parser.parse_args()

    if not options.host:
        print "You must specify the host parameter."
        sys.exit(1)

    try:
        ttStats = ttyrant(options.host, options.port, options.timeout)
    except Exception, e:
        print "CMD FAIL| %s" % e
        sys.exit(1)

    cmdOutPut = "CMD OK|" 
    for stat in [ 'get_set_ratio', 'hit_percent', 'missed_percent', 'pid', 'uptime',
                  'time', 'version', 'pointer_size', 'rusage_user',
                  'rusage_system', 'cmd_set', 'cmd_set_hits',
                  'cmd_set_misses', 'cmd_delete', 'cmd_delete_hits',
                  'cmd_delete_misses', 'cmd_get', 'cmd_get_hits',
                  'cmd_get_misses', 'cmd_flush', 'curr_items',
                  'total_items', 'bytes', 'threads'
                 ]:
       cmdOutPut += "%s=%s " % (stat, ttStats.get(stat))

    print cmdOutPut 
