###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################

import urllib2
import json

from zope.component import adapts
from zope.interface import implements
from Products.ZenModel.DataRoot import DataRoot
from Products.Zuul.search import ISearchProvider
from Products.Zuul.search import ISearchResult
from search import GoogleSearch, SearchError

def doMySearch( operators, keywords ):
    queryString = reconstructQueryString( operators, keywords )
    escapedQueryString = urllib2.quote(queryString)

    url = ('http://ajax.googleapis.com/ajax/services/search/web' +
           '?v=1.0&q=%s' % escapedQueryString )

    request = urllib2.Request( url, None )
    response = urllib2.urlopen(request)

    results = json.load(response)

    responseData = results['responseData']
    if responseData is not None:
        return [ GoogleSearchResult(result) for result in
                 responseData['results'] ]

def reconstructQueryString( operators, keywords ):
    atoms = keywords
    for pair in operators.items():
        opName, opValues = pair
        for opValue in opValues:
            atoms.append( ':'.join( ( opName, opValue ) ) )
    return ' '.join(atoms)

class GoogleSearchProvider(object):
    """
    Provider which searches Google
    """
    implements(ISearchProvider)
    adapts(DataRoot)

    def __init__(self, dmd):
        self._dmd = dmd
    

    def getSearchResults(self, parsedQuery,
                         sorter=None, unrestricted=False):
        """
        Queries the catalog.  Searches the searchKeywords index
        using *keyword1* AND *keyword2* AND so on. 
        If there are preferred categories, find maxResults # of instances
        before searching other categories.

        @rtype generator of BrainSearchResult objects
        """
        operators = parsedQuery.operators
        keywords = parsedQuery.keywords

        if not keywords:
            return

        # parsedQuery should keep original query
        results = doMySearch( operators, keywords )

        if results is not None and sorter is not None:
            results = sorter.limitSort(results)

        return results

    def getQuickSearchResults(self, parsedQuery, maxResults=None):
        """
        Currently just calls getSearchResults
        """
        return self.getSearchResults( parsedQuery, maxResults )


class GoogleSearchResult(object):
    """
    Wraps a brain from the search catalog for inclusion in search results.
    """

    implements(ISearchResult)

    def __init__(self, result):
        self._result = result

    @property
    def url(self):
        return self._result['url']

    @property
    def category(self):
        return 'Google'

    @property
    def excerpt(self):
        return '%s<br/><span style="font-size:smaller">(%s)</span>' % (self._result['title'], self._result['content'])

    @property
    def icon(self):
        return '<img src="http://www.google.com/favicon.ico"/>'
    
    @property
    def popout(self):
        return False

