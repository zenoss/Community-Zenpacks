#!/usr/bin/env python
###########################################################################
#
# Copyright (c) 2008, University of Salford, 
#                     J.B Giraudeau <jbgiraudeau@gmail.com>.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
###########################################################################

import sys
from optparse import OptionParser
from subprocess import Popen,PIPE
from string import Template

class WMIFilesPlugin:

    def __init__(self, host, user, passwd, fileChecks, fileSizes):
        cmdstr =  "$$$$ZENHOME/bin/wmic -U '$username'%'$password' //$hostname" \
                + " 'SELECT $$something FROM CIM_DataFile WHERE Name=\"$$search\"'"
        self.cmdt = Template(Template(cmdstr).substitute(username=user, \
                hostname=host, password=passwd))
        self.fileChecks = fileChecks
        self.fileSizes = fileSizes

    def run(self):
        critical = False
        unknown = False

        if self.fileChecks:
            # Remove duplicates
            fileChecks = {}.fromkeys([file.lower() for file in self.fileChecks]).keys()

            search = '\" OR Name =\"'\
                    .join([file.replace("\\","\\\\") for file in fileChecks])
            cmd = self.cmdt.substitute(search=search, something='Status')
            p = Popen(cmd, shell=True, stdout=PIPE,stderr=PIPE)
            out = p.stdout.readlines()
            if out:
                if out[0] == 'CLASS: CIM_DataFile\n':
                    del out[0:2]
                    for line in out:
                        filename = line.split("|")[0].rstrip('\n')
                        i = fileChecks.index(filename)
                        del fileChecks[i]
                else:
                    unknown = True
            critical = len(fileChecks) > 0

        if not unknown and self.fileSizes:
            fileSizes = [file.lower() for file in self.fileSizes]
            search = '\" OR Name =\"'\
                    .join([file.replace("\\","\\\\") for file in fileSizes])
            cmd = self.cmdt.substitute(search=search, something='FileSize')
            p = Popen(cmd, shell=True, stdout=PIPE,stderr=PIPE)
            out = p.stdout.readlines() 
            results = ['']*len(fileSizes)
            if out:
                if out[0] == 'CLASS: CIM_DataFile\n':
                    del out[0:2]
                    for line in out:
                        l = line.split("|")
                        filesize = l[0]
                        filename = l[1].rstrip('\n')
                        while filename in fileSizes:
                            i = fileSizes.index(filename)
                            results[i] = "file%i_size=%s" % (i, filesize)
                            fileSizes[i] = ''
                else:
                    unknown = True
            if not unknown:
                while '' in results:
                    i = results.index('')
                    results[i] = "file%i_size=%s" % (i, '-1')
        
        if unknown:
            print "Unknown: Connection error|"
            sys.exit(3)

        if critical:
            print "Critical: File(s) disappeared: %s |%s" % \
                    (' '.join(fileChecks), ' '.join(results))
            sys.exit(2)

        print "OK|%s" % ' '.join(results)
        sys.exit(0)

def vararg_callback(option, opt_str, value, parser):
    assert value is None
    done = 0
    value = []
    rargs = parser.rargs
    while rargs:
        arg = rargs[0]
        if ((arg[:2] == "--" and len(arg) > 2) or
            (arg[:1] == "-" and len(arg) > 1 and arg[1] != "-")):
            break
        value.append(arg)
        del rargs[0]
        
    setattr(parser.values, option.dest, value)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-H', '--host', dest='host',
            help='Windows server hostname')
    parser.add_option('-u', '--user', dest='user', default='zenoss',
            help='Windows username')
    parser.add_option('-w', '--password', dest='passwd', default='',
            help='Windows password')
    parser.add_option('-s', '--sizesof', dest='fileSizes', default=[],
            help='List of files to check',
            action="callback" , callback=vararg_callback)
    parser.add_option('-e', '--exist', dest='fileChecks', default=[],
            help='List of files to check for existence',
    		action="callback" , callback=vararg_callback)
    options, args = parser.parse_args()

    if not (options.host):
        print "missing host '-h' option"
        sys.exit(1)
    if not (options.user):
        print "missing user '-u' option"
        sys.exit(1)
    if not (options.passwd):
        print "missing passsword '-w' option"
        sys.exit(1)
    if not (options.fileChecks or options.fileSizes):
        print "OK|Nothing to do"
        sys.exit(0)

    cmd = WMIFilesPlugin(options.host, options.user, 
            options.passwd, options.fileChecks, options.fileSizes)

    cmd.run()
