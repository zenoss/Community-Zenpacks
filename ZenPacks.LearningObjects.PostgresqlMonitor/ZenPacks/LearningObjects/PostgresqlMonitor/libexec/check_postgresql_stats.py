#!/usr/bin/env python
###########################################################################
#
#
# Copyright (C) 2008, Learning Objects Inc, http://www.learningobjects.com
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
#
###########################################################################

import sys
from optparse import OptionParser

try:
    import pgsql
except:
    print "Error importing pgsql module. This is a pre-requisite."
    sys.exit(1)

class ZenossPostgresqlStatsPlugin:
    def __init__(self, host, port, user, passwd, database):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database


    def run_query(self,cursor,stats,query):


        ret = cursor.execute(query)
        result = cursor.fetchall()[0]

        if not ret:
            cursor.close()
            print 'Error getting Postgresql statistics'
            sys.exit(1)

        ret = cursor.execute(query)
        result = cursor.fetchall()[0]


        for k,v in dict(zip(cursor.fields, result)).iteritems():
            stats=stats + "%s=%s " % (k,v)


        return(stats)

    def run(self):
        try:
            self.conn = pgsql.connect(database=self.database,user=self.user, password=self.passwd,
                        host=self.host,port=self.port)

            cursor = self.conn.cursor()
        except Exception, e:
            print "Postgresql Error: %s" % (e,)
            sys.exit(1)

        sVersion = ""
        query = "SELECT setting AS version from pg_settings WHERE name = 'server_version'"
        sVersion = self.run_query(cursor, sVersion, query)
        version = sVersion.split('=')[1]

        stats = ""

        query = "SELECT pg_database_size(pg_database.datname) AS db_size FROM pg_database WHERE pg_database.datname='%s'" % self.database

        stats = self.run_query(cursor,stats,query)

        query = "select numbackends, xact_commit, xact_rollback, blks_read, blks_hit"
        if version.startswith('8.3'):
            query +=  ", tup_returned, tup_fetched, tup_inserted, tup_updated, tup_deleted"
        query +=  " from pg_stat_database where datname='%s'" % self.database


        stats = self.run_query(cursor,stats,query)


        fields = "seq_scan seq_tup_read idx_scan idx_tup_fetch n_tup_ins n_tup_upd n_tup_del".split(" ")
        query = "SELECT"
        for field in fields:
                query = query + " SUM(%s) AS %s, " % (field, field)
        query = query.rstrip(', ') + " FROM pg_stat_user_tables"

        stats = self.run_query(cursor,stats,query)



        fields = "heap_blks_read heap_blks_hit idx_blks_read idx_blks_hit " \
                  "toast_blks_read toast_blks_hit tidx_blks_read tidx_blks_hit".split(" ")
        query = "SELECT"
        for field in fields:
                query = query + " SUM(%s) AS %s, " % (field, field)
        query = query.rstrip(', ') + " FROM pg_statio_user_tables"
        stats = self.run_query(cursor,stats,query)

        cursor.close()

        print "STATUS OK|%s" % stats

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-H', '--host', dest='host',
            help='Hostname of Postgresql server')
    parser.add_option('-p', '--port', dest='port', default=5432, type='int',
            help='Port of Postgresql server')
    parser.add_option('-u', '--user', dest='user', default='monitor',
            help='Postgresql username')
    parser.add_option('-w', '--password', dest='passwd', default='password',
            help='Postgresql password')
    parser.add_option('-d', '--database', dest='database', default='zenoss',
             help="Get database stats")
    options, args = parser.parse_args()

    if not options.host:
        print "You must specify the host parameter."
        sys.exit(1)

    if not options.database:
        print "You must specify the database parameter."
        sys.exit(1)



    cmd = ZenossPostgresqlStatsPlugin(options.host, options.port,
            options.user, options.passwd,  options.database)

    cmd.run()
