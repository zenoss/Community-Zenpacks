from Products.ZenModel.ZenossSecurity import ZEN_COMMON
from Products.ZenUtils.Utils import zenPath
from Products.CMFCore.DirectoryView import registerDirectory
from time import localtime,strftime
import re
import Globals
import os

#registerDirectory("skins", globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
		def _registerShowGraphPortlet(self, app):
                    zpm = app.zport.ZenPortletManager
		    portletsrc=os.path.join(os.path.dirname(__file__),'lib','ShowGraphPortlet.js')
		    #Its a dirty hack - register_portlet will add ZenPath one more time
		    #and we don't want to hardcode path explicitly here like in other ZenPacks
		    p=re.compile(zenPath(''))
		    portletsrc=p.sub('',portletsrc)
                    zpm.register_portlet(
                        sourcepath=portletsrc,
                        id='ShowGraphPortlet',
                        title='Show Graph',
                        permission=ZEN_COMMON)

		def install(self, app):
                    ZenPackBase.install(self, app)
                    self._registerShowGraphPortlet(app)
    
                def upgrade(self, app):
                    ZenPackBase.upgrade(self, app)
                    self._registerShowGraphPortlet(app)
        
                def remove(self, app, leaveObjects=False):
                    ZenPackBase.remove(self, app, leaveObjects)
                    zpm = app.zport.ZenPortletManager
                    zpm.unregister_portlet('ShowGraphPortlet')

import simplejson
import pdb

def getJSONReportList(self, path='/Device Reports'):
    """
    Given a report class path, returns a list of links to child
    reports in a format suitable for a TableDatasource.
    """

# This function will be monkey-patched onto zport, so
# references to self should be taken as referring to zport

# Add the base path to the path given
    path = '/zport/dmd/Reports/' + path.strip('/')

# Create the empty structure of the response object
    #response = { 'columns': ['Report'], 'data': [] }
    response = []
# Retrieve the ReportClass object for the path given. If
# nothing can be found, return an empty response
    try:
        reportClass = self.dmd.unrestrictedTraverse(path)
    except KeyError:
	return simplejson.dumps(response)

    # Get the list of reports under the class as (url, title) pairs
    reports = reportClass.reports()
    reportpairs = [(r.absolute_url_path(), r.id) for r in reports]

                # Iterate over the reports, create links, and append them to
                # the response object
 # Iterate over the reports, create links, and append them to
                # the response object
    for url, title in reportpairs:
                    link = "<a href='%s'>%s</a>" % (url, title)
                    row = title 
                    response.append(row)
#    link="<script language='javascript' type='text/javascript'>var ZenGraphs = new Array();</script>"
#    row= { 'Report': link }
#    response['data'].append(row)
#    comment=strftime("&comment=%d-%b-%Y%%20%H%%5C%%3A%M%%5C%%3A%S",localtime())
#    for g in graphs:
#        link = "<img src='%s%s' title='%s'>" % (g.getGraphUrl(), comment,'title')
#        row = { 'Report': link }
#        response['data'].append(row)

              # Serialize the response and return it
    return simplejson.dumps(response)

            # Monkey-patch onto zport
from Products.ZenModel.ZentinelPortal import ZentinelPortal
ZentinelPortal.getJSONReportList = getJSONReportList



def getJSONGraphList(self, path='/Device Reports',report='test'):
    """
    Givei sdn a report class path, returns a list of links to child
    reports in a format suitable for a TableDatasource.
    """

# This function will be monkey-patched onto zport, so
# references to self should be taken as referring to zport

# Add the base path to the path given
    path = '/zport/dmd/Reports/' + path.strip('/')

# Create the empty structure of the response object
    #response = []
    response = { 'columns': ['Report'], 'data': [] }

# Retrieve the ReportClass object for the path given. If
# nothing can be found, return an empty response
    try:
        reportClass = self.dmd.unrestrictedTraverse(path)
    except KeyError:
	return simplejson.dumps(response)

    # Get the list of reports under the class as (url, title) pairs
    reports = reportClass.reports()
    #reportpairs = [(r.absolute_url_path(), r.id) for r in reports]
    #for url, title in reportpairs:
    #    link=title
    #    row = { 'Report': link }
    #    response['data'].append(row)
    graphs=[]
    multi=0
    numColumns=1
    url=""
    for r in reports:
	    if r.id==report:
	 	try:
			numColumns=r.numColumns
            	 	graphs=r.getElements()
			multi=0
			ok=1
			url=r.absolute_url_path()
		except AttributeError:
			ok=0
		if ok==0:
	 		try:
             			graphs=r.getDefaultGraphDefs()
				ok=1
				multi=1
				numColumns=r.numColumns
				url=r.absolute_url_path()
	 		except AttributeError:
				ok=0
	 


    col=0
    result='<div style="WIDTH: 100%; OVERFLOW: auto"><table>'

    comment=strftime("&comment=%d-%b-%Y%%20%H%%5C%%3A%M%%5C%%3A%S",localtime())
    row={}
    for g in graphs:
	if multi==0:
	    text="%s" % (g.getSummary())
    	    # row = { 'Report': text }
    	    # response['data'].append(row)
            link = "%s<BR><a href='%s'><img src='%s%s' title='%s'/></a>" % (text,url,g.getGraphUrl(), comment,'title')
	if multi==1:
            #row = { 'Report': g['title'] }
	    text=g['title']
            #response['data'].append(row)
            link = "%s<BR><a href='%s'><img src='%s%s' title='%s'/></a>" % (text,url,g['url'], comment,g['title'])
	if (col==0):
		result="%s<tr>" % (result)
	result="%s<td>%s</td>" % (result,link)
	col=col+1
	if (col==numColumns):
		result="%s</tr>" % (result)
	col=col%numColumns
    if col>0:
    	while col<numColumns:
		result="%s<td></td>" % (result)
		col=col+1
	result="%s</tr>" % (result)
    result="%s</table></div>" % (result)
    row={'Report': result}
    response['data'].append(row)
    return simplejson.dumps(response)

ZentinelPortal.getJSONGraphList = getJSONGraphList


