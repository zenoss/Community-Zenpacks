
import re
import os
import sys
import urllib
import tarfile
import zipfile
import os.path
import tempfile
from urllib import quote, unquote
from urllib2 import urlopen
from urlparse import urljoin, urlsplit
from subprocess import *
from xml.dom.minidom import parseString
from StringIO import StringIO

import Globals
from Products.ZenModel.ZenossSecurity import ZEN_COMMON
from Products.ZenUtils.Utils import zenPath
from Products.CMFCore.DirectoryView import registerDirectory

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())


from Products.ZenModel.ZenPack import ZenPackBase
class ZenPack(ZenPackBase):
    def install( self, app):
        ZenPackBase.install( self, app )

    def upgrade( self, app):
        ZenPackBase.upgrade( self, app )

    def remove( self, app, leaveObjects=False):
        ZenPackBase.remove( self, app, leaveObjects=False )



def show_xml(self, path="/zport" ):
    """Dump the XML output from any object(s)"""

    #
    # Attempt to resolve the path into an object
    #
    try:
        zport_class= self.dmd.unrestrictedTraverse( path )    
    except:
        return "It blew up!"

    #
    # Export the objects into a string
    #
    xml_output= StringIO()

    xml_output.write( "<objects>" )

    for object in zport_class.objectValues():
        object.exportXml( xml_output )

    xml_output.write( "</objects>" )

    #
    # Take the resulting string and XML-ize it
    #
    tree= parseString( xml_output.getvalue() )

    return tree.toprettyxml( "    ", "" )



def oidcmp( node1, node2 ):
    """Compare two OIDs based on the numerical value,
       rather than lexical ordering."""

    a= node1.oid.split('.')
    b= node2.oid.split('.')

    # Find the point where the OIDs diverge
    i=0
    min_len = min(len(a), len(b))
    for i in range(min_len):
        if a[i] == b[i]:
            continue

        # Compare the two oids at the branch, *numerically*
        return cmp( int(a[i]), int(b[i]) )

    # This case occurs when one OID is the parent of another
    return cmp(len(a), len(b))



def dump_mib_node2xml( xml_output, oid_tree ):
    """Dump the contents of an oid_tree to the file xml_output
    using the oid_tree.id as the element name"""

    oidlist= sorted( oid_tree.objectValues(), oidcmp )
    if len( oidlist ) == 0:
        return
    #
    # For compliance with the DTD, empty <nodes> or
    # <notifications> are not allowed, but we don't need to
    # declare them if we don't have them.
    #
    xml_output.write( "<%s>" % oid_tree.id )

    #
    # For those of us keeping track, we're not producing
    # _valid_ smi documents, only _well-formed_ ones.
    # If you don't know what I mean, don't worry about it.
    #
    for oid in oidlist:
        xml_output.write( """<node name="%s" oid="%s" status="%s" type="%s">
<description>%s</description>
</node>
""" % ( oid.id, oid.oid, oid.status, oid.nodetype, quote( oid.description ) ) )

    xml_output.write( "</%s>\n" % oid_tree.id )



def mib2xml(self, path="/zport/dmd/Mibs/mibs", REQUEST=None ):
    """Display the MIB at path in XML format.

  Notes:
    * The output format is roughly equivalent to smidump -fxml mibfile, where data exists in Zenoss.  Specifically, Zenoss does not store "imports" or enumerations.
    * This function is necessary as regular Zenoss XML exports expose tons of internal detail and also don't provide some MIB information.

"""

    #
    # Attempt to resolve the path into an object
    #
    try:
        mib_class= self.dmd.unrestrictedTraverse( path )    
    except:
        return "Unable to find %s and obtain a class" % path

    #
    # Create our XML "file" and headers...
    #
    xml_output= StringIO()

    xml_output.write( """<?xml version="1.0" encoding="ISO-8859-1" standalone="yes" ?>
<!--

   This XML file was created by Zenoss to describe the MIB: %s

   Note that as Zenoss doesn't store all the necessary data to
faithfully recreate the MIB, the MIB *cannot* be recreated solely
from Zenoss except for trivial MIBs. Specifically, "imports" and 
enumerations are not stored.


  -->

<smi >
""" % path )

    #
    # Populate with static info...
    #
    xml_output.write( """<module name="%s" language="%s">
""" % ( mib_class.id, mib_class.language ) )

    xml_output.write( """<contact>%s</contact>\n""" % quote(mib_class.contact) )
    xml_output.write( """<description>%s</description>\n""" % quote( mib_class.description ) )

    xml_output.write( """</module>

""" )

    #
    # Populate with table-ized info...
    #
    for oid_tree in mib_class.objectValues():
        if oid_tree.id in ( "nodes", "notifications" ):
           dump_mib_node2xml( xml_output, oid_tree )

    xml_output.write( "</smi>" )

    #
    # Take the resulting string and XML-ize it
    #
    tree= parseString( xml_output.getvalue() )
    pretty= tree.toprettyxml( "    ", "" )

    #
    # Strip out the XML header as the XML header 
    # will be supplied by showMibasXML.
    #
    pretty= re.sub( r'<\?.*\?>', '', pretty, 1 )

    if REQUEST:
        REQUEST.RESPONSE.setHeader( 'content-type', 'text/xml;charset=ISO-8859-1' )
        out = REQUEST.RESPONSE
        self.write( out, pretty )

    else:
        return pretty




#
# --- Globals  ---------------------------
#

download_dir= tempfile.gettempdir()
extract_dir= tempfile.gettempdir() + "/mibs_extract"
mymib_dir= os.sep.join( [ os.environ[ 'ZENHOME' ], "share", "mibs", "site" ] )

#
# --  Functions  -------------------------
#
def dump_command_output( context, out, cmd, timeout=120 ):
    """Run a command and spit out the output onto the web page
       using the context and out descriptors.
"""

    import fcntl
    import popen2
    import signal
    import time
    import select

    child = None
    try:
        try:       
            child = popen2.Popen4(cmd)
            flags = fcntl.fcntl(child.fromchild, fcntl.F_GETFL)
            fcntl.fcntl(child.fromchild, fcntl.F_SETFL, flags | os.O_NDELAY)
            endtime = time.time() + timeout
            context.write(out, '%s' % cmd)
            context.write(out, '')
            pollPeriod = 1
            firstPass = True
            while time.time() < endtime and (firstPass or child.poll()==-1):
                firstPass = False
                r, w, e = select.select([child.fromchild],[],[], pollPeriod)
                if r:
                    t = child.fromchild.read()
                    #We are sometimes getting to this point without any data
                    # from child.fromchild. I don't think that should happen
                    # but the conditional below seems to be necessary.
                    if t:
                        context.write(out, t)
            if child.poll() == -1:
                context.write(out,
                           'Command timed out for %s' % cmd +
                           ' (timeout is %s seconds)' %
                           timeout )
        except:
            context.write( out, 'Error running command' )
            context.write( out, 'type: %s  value: %s' % tuple(sys.exc_info()[:2]))
            context.write(out, '')
    finally:
        if child and child.poll() == -1:
            os.kill(child.pid, signal.SIGKILL)



def download_mib( mibfile_url, download_dir ):
    """Download the addon from the given URL"""

    path= urlsplit( mibfile_url )[2]
    file= path.split( '/' )[-1]
    ( filename, headers )= urllib.urlretrieve( mibfile_url, download_dir + os.sep + file )

    return filename



def add_mib_to_site_mibs( mib_context, out, mib_file ):
    """Load a MIB (mib_file) and display the output into the command output window (mib_context)
 using the 'out' handle.   If the zenmib command hangs, process will be killed."""

    cmd= "zenmib run -v 10 %s" % mib_file
    dump_command_output( mib_context, out, cmd )



def unzip_mib( mib_context, out, mib ):
    """Unzip the given file into the current directory and return
       the directory in which MIBs can be loaded."""

    #
    # Sanity checks on the file
    #
    if not zipfile.is_zipfile( mib ):
        mib_context.write( out, "The file %s is not a valid zip file!" % mib )
        return ""

    mib_zip= zipfile.ZipFile( mib, 'r' )
    if mib_zip.testzip() != None:
        mib_context.write( out, "MIB %s is corrupted -- please download again" % mib )
        return ""

    #
    # The first entry in the ZIP should be a directory...
    #
    base_dir= mib_zip.namelist()[0]
    for file in mib_zip.namelist():
        mib_context.write( out, "Unzipping %s..." % file )
        try:
            if re.search( r'/$', file ) != None:
                os.makedirs( file )

            else:
                contents= mib_zip.read( file )

                unzipped= open( file, "w" )
                unzipped.write( contents )
                unzipped.close()

        except:
            mib_context.write( out, "Error in extracting %s because %s" % ( file, sys.exc_info()[1] ) )
            return ""

    #
    # We should have extracted everything by now.
    # Check to see if the first file really was a directory or not
    #
    if not os.path.isdir( base_dir ):
        base_dir= extract_dir

    return base_dir



def untar_mib( mib ):
    """Given a tar file, extract the tar to the current directory."""
    mib_tar= tarfile.open( mib, 'r' )

    for tarinfo in mib_tar:
        mib_tar.extract( tarinfo )

    mib_tar.close()



def cleanup_extract_dir( mib_dir ):
    """Remove any clutter left over from the installation"""

    for root, dirs, files in os.walk( mib_dir, topdown=False ):
        if root == os.sep: # Should *never* get here
            break

        for name in files:
            os.remove( os.path.join( root, name ) )

        for name in dirs:
            os.rmdir( os.path.join( root, name ) )

        os.rmdir( mib_dir )



#
# NB: zenmib will process all of the files, generate a 
#     dependency graph, and then import the MIBs in the 
#     correct order. Okay, if the glossy is to be believed... :)
#
def process_mib_dir( mib_context, out, base_dir ):
    """Load all of the MIBs in a directory."""
    for mib_file in os.listdir( base_dir ):
        if os.path.isdir(mib_file):
            process_mib_dir( mib_context, out, mib_file)
        else:
            add_mib_to_site_mibs( mib_context, out, mib_file )



def process_mib_zip( mib_context, out, mib, extract_dir ):
    """Extract the file and then call the MIB installer"""

    #
    # Set up the extraction directory
    #
    mib_context.write( out, "Setting up extraction directory %s" % extract_dir )
    if not os.path.exists( extract_dir ):
        try:
            os.makedirs( extract_dir )
        except:
            mib_context.write( out, "Error in creating %s because %s" % ( file, sys.exc_info()[1] ) )
            return
    else:
            mib_context.write( out, "Path exists" )

    os.chdir( extract_dir )

    base_dir= unzip_mib( mib_context, out, mib )

    if base_dir == "":
        cleanup_extract_dir( extract_dir )
        return

    mib_context.write( out, "Starting MIB extraction in %s" % base_dir )
    process_mib_dir( mib_context, out, base_dir )

    cleanup_extract_dir( base_dir )

    return



def process_mib_tar( mib_context, out, mib, extract_dir ):
    """Extract the file and then call the MIB installer"""

    #
    # Set up the extraction directory
    #
    if not os.path.exists( extract_dir ):
        try:
            os.makedirs( extract_dir )
        except:
            mib_context.write( out, "Error in creating %s because %s" % ( file, sys.exc_info()[1] ) )
            return

    os.chdir( extract_dir )
    try:
        mib_context.write( out, "Extracting files from tar..." )
        untar_mib( mib )
    except:
        mib_context.write( out, "Error in un-tarring %s because %s" % ( file, sys.exc_info()[1] ) )
        return

    process_mib_dir( mib_context, out, extract_dir )

    cleanup_extract_dir( extract_dir )



def process_mib_package( mib_context, out, local_mib ):
    """Figure out what type of file we have and extract out any
       MIB files and then load the MIB files."""

    mib_context.write( out, "Determining file type of %s" % local_mib )
    if zipfile.is_zipfile( local_mib ):
        mib_context.write( out, "Found a zip file..." )
        process_mib_zip( mib_context, out, local_mib, extract_dir )

    elif tarfile.is_tarfile( local_mib ):
        mib_context.write( out, "Found a tar file..." )
        process_mib_tar( mib_context, out, local_mib, extract_dir )

    else:
        add_mib_to_site_mibs( mib_context, out, local_mib )



def download_install_mib( mib_context, out, mibfile_url="", REQUEST=None ):
    if mibfile_url == "":
        return

    try:
        local_mib= download_mib( mibfile_url, download_dir )
        process_mib_package( mib_context, out, local_mib )

    except:
         mib_context.write( out, "Oops!  Problems downloading the MIB from %s: %s" % ( mibfile_url, sys.exc_info()[1] ) )




def download_install_MIBs( self, mib_urls="", context=None, REQUEST=None ):
    """Download and install MIBs from the list of URLs.

       NB: We need to make sure that the form that sends us our
           mib_file has the enctype attribute in the 'form' element:

     <form ... enctype="multipart/form-data" >
           ...
     </form>
"""

    #
    # Quick sanity check
    #
    urls= []
    for url in mib_urls.split():
        url.strip()
        if url != "":
            urls.append( url )
    
    if( len( urls ) == 0 ):
        return

    #
    # Because this routine doesn't "belong" to a class
    # (in this case, 'Mibs') we need to call other scripts
    # from the correct context in order to make this work.
    #
    mib_context= self.dmd.Mibs

    if REQUEST:
        REQUEST['cmd'] = ''
        #
        # Sigh, more magic.  commandOutputTemplate.pt is a Zope Page Template
        # that we load and then split into two parts: everything up to the
        # point that we want to start outputting our command text, and then
        # rest to compose a syntactically correct HTML page.  Inside of the
        # middle of commandOutputTemplate.pt is the text 'OUTPUT_TOKEN',
        # which is used to delineate the top (header) from the bottom (footer).
        #
        header, footer = mib_context.commandOutputTemplate().split('OUTPUT_TOKEN')
        REQUEST.RESPONSE.write(str(header))
        out = REQUEST.RESPONSE
    else:
        out = None
    
    tFile = None
    try:  
        for url in urls:
            mib_context.write( out, "Downloading %s..." % url )
            download_install_mib( mib_context, out, url )

    except:
        mib_context.write(out, 'Error loading MIBs.')
        mib_context.write( out, 'type: %s  value: %s' % tuple(sys.exc_info()[:2]))
        mib_context.write(out, '')

    mib_context.write(out, '')
    mib_context.write(out, 'Done loading MIB.')

    #
    # NB: At this point we should consider cleaning up the files we
    #     uploaded to the server, but we're going to leave them around
    #     because they shouldn't take up much room and we can't generate
    #     these files from what we've stored in Zenoss.
    #
    if REQUEST:
        REQUEST.RESPONSE.write(footer)
    


#
# NB: We need to make sure that the form that sends us our
#     mib_file has the enctype attribute in the 'form' element:
#
#     <form ... enctype="multipart/form-data" >
#           ...
#     </form>
#
def upload_installMIB(self, mib_file=None, REQUEST=None):
    """Installs mib_file, which is a file upload from the browser.

       NB: We need to make sure that the form that sends us our
           mib_file has the enctype attribute in the 'form' element:

     <form ... enctype="multipart/form-data" >
           ...
     </form>
    """
       
    #
    # Because this routine doesn't "belong" to a class
    # (in this case, 'Mibs') we need to call other scripts
    # from the correct context in order to make this work.
    #
    mib_context= self.dmd.Mibs

    if REQUEST:
        REQUEST['cmd'] = ''
        #
        # Sigh, more magic.  commandOutputTemplate.pt is a Zope Page Template
        # that we load and then split into two parts: everything up to the
        # point that we want to start outputting our command text, and then
        # rest to compose a syntactically correct HTML page.  Inside of the
        # middle of commandOutputTemplate.pt is the text 'OUTPUT_TOKEN',
        # which is used to delineate the top (header) from the bottom (footer).
        #
        header, footer = mib_context.commandOutputTemplate().split('OUTPUT_TOKEN')
        REQUEST.RESPONSE.write(str(header))
        out = REQUEST.RESPONSE
    else:
        out = None
    
    tFile = None
    try:
        # Write the MIB to the filesystem                
        tDir = tempfile.gettempdir()
        local_mib = open(os.path.join(tDir, mib_file.filename), 'wb')
        local_mib.write( mib_file.read() )
        local_mib.close()

        process_mib_package( mib_context, out, local_mib.name )

    except:
        mib_context.write(out, 'Error loading MIB.')
        mib_context.write( out, 'type: %s  value: %s' % tuple(sys.exc_info()[:2]))
        mib_context.write(out, '')

    mib_context.write(out, '')
    mib_context.write(out, 'Done loading MIB.')
    if REQUEST:
        REQUEST.RESPONSE.write(footer)



def dump_proc_output2xml( xml_file, cmd ):
    """Execute a command and write the output to a file.

   The XML will appear as:

 <command> </command>
 <stdout> </stdout>
 <stderr> </stderr>
"""

    #
    # TODO: Kill the command if it hangs
    #
    xml_file.write( """<command>%s</command>""" % quote( cmd ) )
    proc= Popen( cmd, shell=True, stdout=PIPE, stderr=PIPE )

    #
    # Check to make sure that we don't have any hangups in
    # executing our smidump
    #
    if not proc.stdout:
        xml_file.write( """<stdout></stdout>
<stderr>Couldn't open pipe to stdout for %s</stderr>""", quote( cmd ) )
        return

    if not proc.stderr:
        xml_file.write( """<stdout></stdout>
<stderr>Couldn't open pipe to stderr for %s</stderr>""", quote( cmd ) )
        return

    #
    # Dump out standard output...
    #
    output= quote( "".join( proc.stdout.read() ) )
    xml_file.write( """<stdout>%s</stdout>""" % output )

    #
    # Dump out standard error...
    #
    output= quote( "".join( proc.stderr.read() ) )
    xml_file.write( """<stderr>%s</stderr>""" % output )



def oid_translate2xml( self, oid="", REQUEST=None ):
    """Wrapper around the command-line utility snmptranslate.
  This translates an OID from names to numbers or numbers to
  names, and also provides more information about the OID."""

    #
    # Create our XML "file" and headers...
    #
    xml_output= StringIO()

    xml_output.write( """<?xml version="1.0" encoding="ISO-8859-1" standalone="yes" ?>
<output>
""" )

    #
    # Sanity checks....
    #
    if oid == "":
        xml_output.write( """Given an empty OID to translate!</output>""" )
        tree= parseString( xml_output.getvalue() )
        pretty= tree.toprettyxml( "    ", "" )
        pretty= re.sub( r'<\?.*\?>', '', pretty, 1 )
        return pretty

    #
    # Discard unexpected characters
    #
    oid= re.sub( r'[^-a-zA-Z_\.0-9:]+', '', oid )

    #
    #
    # Run the command...
    #
    cmd= "snmptranslate -M +%s -Td -Ln -Ofn %s" % ( mymib_dir, oid )
    dump_proc_output2xml( xml_output, cmd )
    xml_output.write( """</output>""" )


    #
    # Take the resulting string and XML-ize it
    #
    tree= parseString( xml_output.getvalue() )
    pretty= tree.toprettyxml( "    ", "" )

    #
    # Strip out the XML header as the XML header 
    # will be supplied by showOID2XML.
    #
    pretty= re.sub( r'<\?.*\?>', '', pretty, 1 )

    return pretty



def snmpwalk( self, device="", oid="", community="", REQUEST=None ):
    """Use the snmpwalk command to walk the device's MIB
       starting from the given oid.  Currently just uses the
       SNMP v1 style authentication, so only community is supported.
"""
    mib_context= self.dmd.Mibs

    if REQUEST:
        REQUEST['cmd'] = ''
        #header, footer = mib_context.commandOutputTemplate().split('OUTPUT_TOKEN')
        header, footer = mib_context.undecoratedCommandOutputTemplate().split('OUTPUT_TOKEN')
        REQUEST.RESPONSE.write(str(header))
        out = REQUEST.RESPONSE
    else:
        out = None

    try:
        cmd= "snmpwalk -v1 -c %s %s %s" % ( community, device, oid )
        dump_command_output( mib_context, out, cmd )

    except:
        mib_context.write(out, 'Error invoking snmpwalk.')
        mib_context.write( out, 'type: %s  value: %s' % tuple(sys.exc_info()[:2]))
        mib_context.write(out, '')

    mib_context.write(out, '')
    mib_context.write(out, 'Done SNMP walking the OID %s' % oid )
    if REQUEST:
        REQUEST.RESPONSE.write(footer)



def add_MIB_node( self, id="", oid="", nodetype="", access="", status="", description="", REQUEST=None ):
    """Add, depending on the nodetype, either a MIB node or trap."""
    #
    # Attempt to resolve the path into an object
    #

    #
    # We need to change our path depending on whether we are
    # going to process a node or a trap.
    #
    path= '/'.join( REQUEST[ 'PATH_INFO' ].split( '/' )[:-3] )
    if nodetype == "notification":
        path += "/notifications"
    else:
        path += "/nodes"

    try:
        zport_class= self.dmd.unrestrictedTraverse( path )    
    except:
        return "It blew up!"

    #
    # Okay, add the MIB node
    #
    unpacked_description= unquote( description )
    if nodetype == "notification":
        mib_node= zport_class.createMibNotification( id, oid=oid, nodetype=nodetype, status=status, access=access, description=unpacked_description )

    else:
        mib_node= zport_class.createMibNode( id, oid=oid, nodetype=nodetype, status=status, access=access, description=unpacked_description )

#
# --------------------------------------------------
#   Add global functions to Zope
# --------------------------------------------------
#
from Products.ZenModel.ZentinelPortal import ZentinelPortal
ZentinelPortal.show_xml= show_xml
ZentinelPortal.mib2xml= mib2xml
ZentinelPortal.download_install_MIBs= download_install_MIBs
ZentinelPortal.upload_installMIB= upload_installMIB
ZentinelPortal.oid_translate2xml= oid_translate2xml
ZentinelPortal.snmpwalk= snmpwalk
ZentinelPortal.add_MIB_node= add_MIB_node
