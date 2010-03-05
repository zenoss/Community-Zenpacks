#!/usr/bin/env python
"""
Simply connect to a redis server and issue the info command.  Spit out the
results in a Nagios format.
"""

import sys
from optparse import OptionParser
import ZenPacks.chudler.redis.lib.redis as redis

class RedisPlugin:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        db = redis.Redis(host=self.host, port=self.port)

        # fetch stats
        metrics = db.info()

        nagios_values = []

        for metric, value in metrics.iteritems():
            # per-database stats get their own datapoints, db# is the namespace
            if type(value) == dict:
                for sub_metric, sub_value in value.iteritems():
                     nagios_values.append('%s_%s=%s' % (metric, sub_metric, sub_value))
            # other types of stats (server-wide) are named after their redis name
            else:
                nagios_values.append('%s=%s' % (metric, value))

        return 'Redis Database Statistics|' + ' '.join(nagios_values)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-H', '--host', dest='host',
        help='Hostname/IP of the redis server')
    parser.add_option('-p', '--port', type='int', dest='port', default='6379',
        help='Port of the redis database listener')
    options, args = parser.parse_args()

    if not options.host:
        print "You must specify the host parameter."
        sys.exit(1)

    cmd = RedisPlugin(options.host, options.port)
    print cmd.run()
