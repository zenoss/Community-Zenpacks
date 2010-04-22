
import Globals
import os.path
import os

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

# Create a simlink to the configuration file. This is so the config can be 
# accessed from the Settings > Daemons page
from Products.ZenUtils.Utils import zenPath
import sys

# The full path to emailping.py is passed as sys.argv[0]. First, we use the
# filename to see if the symlink exists
epFileName = os.path.basename( sys.argv[0] )

# strip '.py' add '.conf'
configFileName = epFileName[:-3] + '.conf'
configFilePath = zenPath( 'etc', configFileName )

# if the file doesn't exist, create it
if not os.path.exists( configFilePath ):
    file = open( configFilePath, 'a' )
    file.close()
    # zenpackRootDir = os.path.dirname( sys.argv[0] )
    # configFile = os.path.join( zenpackRootDir, 'etc', configFileName )
    # if os.path.exists( configFile ):
        # try:
            # cmd = 'ln -s %s %s' % ( configFile, linkFile )
            # os.system( cmd )
        # except:
            # pass



from Products.ZenModel.ZenPack import ZenPackBase
class ZenPack(ZenPackBase):
    
    def install( self, app ):
    
        # create the config file when the zenpack is installed
        super( ZenPack, self ).install( app )
        configFileName = zenPath( 'etc', 'emailping.conf' )
        file = open( configFileName, 'a' )
        file.close()
    
    def remove(self, app, leaveObjects=False):

        super( ZenPack, self ).remove( app, leaveObjects )
        if not leaveObjects:
            self.removeEmailPingObjects()        
        
    def removeEmailPingObjects( self ):
    
        template = self.dmd.Monitors.rrdTemplates.PerformanceConf
        
        # remove config files
        import glob
        configFiles = glob.glob( 
            os.path.join( zenPath( 'etc' ), 'emailping*' ) )
        for configFile in configFiles:
            try:
                os.remove( configFile )
            except:
                pass
            
        # remove $ZENHOME/bin shortcuts
        # daemonLinks = glob.glob( 
            # os.path.join( zenPath( 'emailping' ), 'emailping*' ) )
        # for daemonLink in daemonLinks:
            # try:
                # os.remove( daemonLink )
            # except:
                # pass
            
        # remove cycleTime graph points
        graph = template.graphDefs._getOb( 'Cycle Times' )
        emailpingGraphPoints = []
        for graphPoint in graph.graphPoints.objectIds():
            if graphPoint.startswith( 'emailping' ):
                emailpingGraphPoints.append( graphPoint )
        for graphPoint in emailpingGraphPoints:
            try:
                graph.graphPoints._delObject( graphPoint )
            except:
                pass
        
        # remove Queue Length and Transit Time graphs
        graphNames = ['EmailPing Queue Lengths', 'EmailPing Transit Times']
        for graphName in graphNames:
            try:
                template.graphDefs._delObject( graphName )
            except:
                pass
                
        # remove datasources
        emailpingDatasources = []
        for datasource in template.datasources.objectIds():
            if datasource.startswith( 'emailping' ):
                emailpingDatasources.append( datasource )
        try:
            template.manage_deleteRRDDataSources( tuple( emailpingDatasources ) )
        except:
            pass
        
        import transaction
        transaction.commit()

    # These two methods have to be overridden because Products.ZenUtils.ZenPack
    # bypasses them and doesn't do anything.
    def stopDaemons(self):
        """
        Stop all the daemons provided by this pack.
        Called before an upgrade or a removal of the pack.
        """
        for d in self.getDaemonNames():
            self.About.doDaemonAction(d, 'stop')


    def startDaemons(self):
        """
        Start all the daemons provided by this pack.
        Called after an upgrade or an install of the pack.
        """
        # for d in self.getDaemonNames():
            # self.About.doDaemonAction(d, 'start')
        
        # since emailping needs to be configured before it can be run, we bypass
        # the start function (just in case the developers turn this back on)
        pass
