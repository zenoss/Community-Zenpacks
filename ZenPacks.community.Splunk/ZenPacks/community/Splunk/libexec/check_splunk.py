#!/usr/bin/env python
######################################################################
#
# Copyright 2009 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

import os
import sys
import time
from cPickle import dump, load
from md5 import md5
from optparse import OptionParser
from tempfile import gettempdir
from xml.dom.minidom import parseString

import splunklib


def getText(element):
    return element.childNodes[0].data


def isNumeric(value):
    try:
        unused = float(value)
        return True
    except (TypeError, ValueError):
        return False
    

class ZenossSplunkPlugin:
    _state = None
    _server = None
    _port = None
    _username = None
    _password = None


    def __init__(self, server, port, username, password):
        self._server = server
        self._port = int(port)
        self._username = username
        self._password = password


    def _loadState(self):
        state_filename = os.path.join(gettempdir(), 'check_splunk.pickle')
        if os.path.isfile(state_filename):
            try:
                state_file = open(state_filename, 'r')
                self._state = load(state_file)
                state_file.close()
            except Exception, ex:
                print 'unable to load state from %s' % state_filename
                sys.exit(1)
        else:
            self._state = {
                'sessionkeys':{},
                }


    def _saveState(self):
        state_filename = os.path.join(gettempdir(), 'check_splunk.pickle')
        try:
            state_file = open(state_filename, 'w')
            dump(self._state, state_file)
            state_file.close()
        except Exception, ex:
            print 'unable to save state in %s' % state_filename
            sys.exit(1)


    def cacheSessionKey(self, sessionkey):
        if not sessionkey: return
        key = md5('|'.join([self._server, str(self._port), self._username,
            self._password])).hexdigest()
        self._state['sessionkeys'][key] = sessionkey


    def getCachedSessionKey(self):
        key = md5('|'.join([self._server, str(self._port), self._username,
            self._password])).hexdigest()
        return self._state['sessionkeys'].get(key, None)


    def run(self, search, **kwargs):
        self._loadState()
        s = splunklib.Connection(
            self._server, self._port, self._username, self._password)

        # Try using a cached session key if we have one.
        s.setSessionKey(self.getCachedSessionKey())

        search = 'search %s' % search

        # Run our search job.
        sid = None
        try:
            sid = s.createSearch(search, **kwargs)
        except splunklib.Unauthorized:
            s.setSessionKey(None)
            
            try:
                sid = s.createSearch(search, **kwargs)
            except splunklib.Unauthorized, ex:
                print "invalid Splunk username or password"
                sys.exit(1)
        except splunklib.Failure, ex:
            print ex
            sys.exit(1)

        # Periodically check back for the results of our query.
        results = None
        for i in [1, 2, 3, 5, 7, 10, 13, 15]:
            try:
                results = s.getSearchResults(sid)
                break
            except:
                time.sleep(i)
                continue

        # Cleanup after ourselves.
        self.cacheSessionKey(s.getSessionKey())
        self._saveState()
        try:
            s.deleteSearch(sid)
        except:
            pass

        if not results:
            print "no results from Splunk search"
            sys.exit(1)

        dps = dict(count=0)
        xml = parseString(results)
        for result in xml.getElementsByTagName('result'):
            dps['count'] += 1
            fields = result.getElementsByTagName('field')
            dpPrefix = getText(fields[0].getElementsByTagName('text')[0])
            for field in fields[1:]:
                value = field.getElementsByTagName('text')
                value = len(value) and getText(value[0]) or None
                if not isNumeric(value): continue
                dps['%s_%s' % (dpPrefix, field.getAttribute('k'))] = value

        print "OK|%s" % ' '.join(['%s=%s' % (x, y) for x, y in dps.items()])
        sys.exit(0)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-s', '--server', dest='server',
        help='Hostname or IP address of Splunk server')
    parser.add_option('-p', '--port', dest='port',
        help='splunkd port on Splunk server')
    parser.add_option('-u', '--username', dest='username',
        help='Splunk username')
    parser.add_option('-w', '--password', dest='password',
        help='Splunk password')
    options, args = parser.parse_args()

    if not options.server:
        if 'SPLUNK_SERVER' in os.environ:
            options.server = os.environ['SPLUNK_SERVER']
        else:
            print 'no Splunk server specified'
            sys.exit(1)

    if not options.port:
        if 'SPLUNK_PORT' in os.environ:
            options.port = os.environ['SPLUNK_PORT']
        else:
            options.port = 8089

    if not options.username:
        if 'SPLUNK_USERNAME' in os.environ:
            options.username = os.environ['SPLUNK_USERNAME']
        else:
            print 'no Splunk username specified'
            sys.exit(1)

    if not options.password:
        if 'SPLUNK_PASSWORD' in os.environ:
            options.password = os.environ['SPLUNK_PASSWORD']
        else:
            print 'no Splunk password specified'
            sys.exit(1)

    if len(args) < 1:
        print 'no Splunk search specified'
        sys.exit(1)

    zsp = ZenossSplunkPlugin(
        options.server, options.port, options.username, options.password)
    zsp.run(' '.join(args))
