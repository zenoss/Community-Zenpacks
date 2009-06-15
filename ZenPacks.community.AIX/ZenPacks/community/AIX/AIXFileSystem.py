__doc__="""AIXFileSystem

AIXFileSystem is a file system on an aix server

$Id: FileSystem.py,v 1.12 2004/04/06 22:33:23 edahl Exp $"""

import logging
log = logging.getLogger("zen.AIXFileSystem")

from Globals import DTMLFile
from Globals import InitializeClass
from Products.ZenUtils.Utils import prepId
from Products.ZenRelations.RelSchema import *
from Products.ZenModel.OSComponent import OSComponent
from Products.ZenModel.FileSystem import FileSystem
from Products.ZenModel.ZenossSecurity import *
import copy

def manage_addFileSystem(context, id, userCreated, REQUEST=None):
    """make a filesystem"""
    fsid = prepId(id)
    fs = AIXFileSystem(fsid)
    context._setObject(fsid, fs)
    fs = context._getOb(fsid)
    if userCreated: fs.setUserCreateFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')
    return fs

addFileSystem = DTMLFile('dtml/addFileSystem',globals())

class AIXFileSystem(FileSystem):
    """
    AIXFileSystem object
    """
    # This is set in the FileSystem Object
    # portal_type = meta_type = 'FileSystem'
    #manage_editFileSystemForm = DTMLFile('dtml/manageEditFileSystem',globals())
    #mount = ""
    #storageDevice = ""
    #type = ""
    #totalBlocks = 0L
    #totalFiles = 0L
    #capacity = 0
    #inodeCapacity = 0
    #maxNameLen = 0

    # Define our new properties
    aixFsFree = ""
    aixFsNumInodes = ""
    aixFsUsedInodes = ""
    aixFsStatus = ""
    aixFsExecution = ""
    aixFsResultMsg = ""
    blockSize = 1024**2

    _properties = FileSystem._properties + (
        {'id':'blockSize', 'type':'int', 'mode':''},
        {'id':'aixFsFree', 'type':'string', 'mode':''},
        {'id':'aixFsNumInodes', 'type':'string', 'mode':''},
        {'id':'aixFsUsedInodes', 'type':'string', 'mode':''},
        {'id':'aixFsStatus', 'type':'string', 'mode':''},
        {'id':'aixFsExecution', 'type':'string', 'mode':''},
        {'id':'aixFsResultMsg', 'type':'string', 'mode':''},
        )

    # Extend the Relationship Model
    # Base off of OSComponent as we want to override Filesystems relations
    _relations = OSComponent._relations + (
        ("logicalvolume", ToOne(ToManyCont, "ZenPacks.community.AIX.AIXLogicalVolume", "filesystem")),
        )

    # Override the web templates
    factory_type_information = (
        {
            'id'             : 'FileSystem',
            'meta_type'      : 'FileSystem',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'FileSystem_icon.gif',
            'product'        : 'ZenModel',
            'factory'        : 'manage_addFileSystem',
            'immediate_view' : 'viewAIXFileSystem',
            'actions'        :
            (
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewAIXFileSystem'
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

    def usedInodes(self, default = None):
        """
        Return the number of used inodes stored in the filesystem's rrd file
        """
        inodes = self.getRRDValue('usedInodes_usedInodes')
        if inodes is not None:
            return long(inodes)
        else:
            return None

    def usedInodesString(self):
        """
        Return the number of used Inodes in human readable form ie 10MB
        """
        __pychecker__='no-constCond'
        ui = self.usedInodes()
        return ui is None and "unknown" or ui

    def numInodes(self, default = None):
        """
        Return the number of inodes stored in the filesystem's rrd file
        """
        inodes = self.getRRDValue('numInodes_numInodes')
        if inodes is not None:
            return long(inodes)
        else:
            return None

    def numInodesString(self):
        """
        Return the number of Inodes in human readable form ie 10MB
        """
        __pychecker__='no-constCond'
        ni = self.numInodes()
        return ni is None and "unknown" or ni

InitializeClass(AIXFileSystem)
