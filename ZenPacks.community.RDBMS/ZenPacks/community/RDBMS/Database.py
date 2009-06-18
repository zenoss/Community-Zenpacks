################################################################################
#
# This program is part of the RDBMS Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""Database

Database is a Database

$Id: Database.py,v 1.0 2009/05/15 16:18:23 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]
from Globals import InitializeClass
from Globals import DTMLFile

from ZenPacks.community.deviceAdvDetail.HWStatus import *
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from Products.ZenUtils.Utils import convToUnits
from Products.ZenRelations.RelSchema import *

from Products.ZenModel.OSComponent import OSComponent
from Products.ZenUtils.Utils import prepId

from Products.ZenModel.ZenossSecurity import *

def manage_addDatabase(context, id, userCreated, REQUEST=None):
    """make a database"""
    dbid = prepId(id)
    db = Database(dbid)
    context._setObject(dbid, db)
    db = context._getOb(dbid)
    db.dbname = id
    if userCreated: db.setUserCreateFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main') 

addDatabase = DTMLFile('dtml/addDatabase',globals())

class Database(OSComponent, HWStatus):
    """
    Database object
    """

    ZENPACKID = 'ZenPacks.community.RDBMS'

    portal_type = meta_type = 'Database'

    manage_editDatabaseForm = DTMLFile('dtml/manageDatabase',globals())

    dbname = ""
    type = "RDBMS Database"
    totalBlocks = 0L
    blockSize = 1L
    status = 1

    statusmap ={1: (DOT_GREY, SEV_WARNING, 'Unknown'),
	        2: (DOT_GREEN, SEV_CLEAN, 'Active'),
		3: (DOT_YELLOW, SEV_WARNING, 'Available'),
		4: (DOT_ORANGE, SEV_ERROR, 'Restricted'),
		5: (DOT_RED, SEV_CRITICAL, 'Unavailable'),
		}

    _properties = OSComponent._properties + (
        {'id':'dbname', 'type':'string', 'mode':'w'},
        {'id':'type', 'type':'string', 'mode':'w'},
        {'id':'totalBlocks', 'type':'long', 'mode':'w'},
        {'id':'blockSize', 'type':'long', 'mode':'w'},
        {'id':'status', 'type':'int', 'mode':'w'},
        )

    _relations = OSComponent._relations + (
        ("os", ToOne(ToManyCont, "Products.ZenModel.OperatingSystem", "softwaredatabases")),
        )
    

    factory_type_information = ( 
        { 
            'id'             : 'Database',
            'meta_type'      : 'Database',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'FileSystem_icon.gif',
            'product'        : 'RDBMS',
            'factory'        : 'manage_addDatabase',
            'immediate_view' : 'viewDatabase',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewDatabase'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW, )
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : ("Change Device", )
                },                
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )

    def totalBytes(self):
        """
        Return the number of allocated bytes
        """
        return long(self.totalBlocks) * long(self.blockSize)

    def totalString(self):
        """
        Return the number of allocated bytes in human readable form ie 10MB
        """
        sas = self.totalBytes()
        return convToUnits(sas)

    def usedBytes(self):
        """
        Return the number of used bytes
        """
        su = self.cacheRRDValue('sizeUsed_sizeUsed', 0)
        return long(su) * long(self.blockSize)

    def usedString(self):
        """
        Return the number of used bytes in human readable form ie 10MB
        """
        sus = self.usedBytes()
        return convToUnits(sus)

    def blockSizeString(self):
        """
        Return the size of unit in bytes in human readable form ie 10MB
        """
        sus = long(self.blockSize)
        return convToUnits(sus)

    def availString(self):
        """
        Return the Available bytes in human readable form ie 10MB
        """
        sa = long(self.totalBytes()) - long(self.usedBytes())
        if 0 > sa: sa = 0 
        return convToUnits(sa)

    def capacity(self):
        """
        Return the percentage capacity of a database using its rrd file
        """
        __pychecker__='no-returnvalues'
        usedBytes = long(self.usedBytes())
        totalBytes = long(self.totalBytes())
        if usedBytes > 0  and totalBytes > 0:
            return int(100.0 * usedBytes / totalBytes)
        return 'Unknown'

    def getRRDNames(self):
        """
        Return the datapoint name of this Database
        """
        return ['sizeUsed_sizeUsed']

    def viewName(self): 
        """
        Return the name of a Database
        """
        return self.dbname
    name = viewName

    def manage_editDatabase(self, monitor=False,
                dbname=None, type=None, blockSizes=None, 
                sizeAllocated=None, REQUEST=None):
        """
        Edit a Service from a web page.
        """
        if dbname:
            self.dbname = dbname
            self.type = type
            self.blockSize = blockSize
            self.totalBlocks = totalBlocks
        
        self.monitor = monitor
        self.index_object()

        if REQUEST:
            REQUEST['message'] = "Database updated"
            return self.callZenScreen(REQUEST)


InitializeClass(Database)
