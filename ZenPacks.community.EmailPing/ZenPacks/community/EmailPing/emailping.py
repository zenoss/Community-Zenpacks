###########################################################################
# This daemon is designed to monitor your email alerting mechanism.
# The design is based on the assumption that an internal email server
# is being used to send SMS alerts via an Internet connection. If any
# device along the alerting path ceases to function, alerts will not be
# received, but how do you know if something has failed? 
#
# That is what EmailPing is for. It uses the mail configuration within 
# Zenoss to send test email messages to an external email address. It
# also checks for those same messages via a POP server. If messages
# are not received at the specified interval, Events are generated. 
###########################################################################
import Globals
from Products.ZenHub.PBDaemon import PBDaemon
from Products.ZenUtils import Utils
from Products.ZenUtils.Driver import drive, driveLater
from twisted.internet import defer
from Products.ZenEvents import Event
from email.MIMEText import MIMEText
from ZenPacks.community.EmailPing.EmailPingStats import EmailPingStats

import sys
import poplib
import email
import email.Utils
import re
import time
from datetime import datetime, timedelta

POP_LOGIN_TYPE_CLEARTEXT = 'cleartext'
DEFAULT_POP3_CLEARTEXT_PORT = 110

POP_LOGIN_TYPE_SSL = 'ssl'
DEFAULT_POP3_SSL_PORT = 995

POP_LOGIN_TYPES = {
    POP_LOGIN_TYPE_CLEARTEXT: DEFAULT_POP3_CLEARTEXT_PORT,
    POP_LOGIN_TYPE_SSL: DEFAULT_POP3_SSL_PORT }

QUEUE_LENGTH_GRAPH_NAME = 'EmailPing Queue Lengths'
TRANSIT_TIME_GRAPH_NAME = 'EmailPing Transit Times'
RECEIVED_MAIL_GRAPH_NAME = 'EmailPing Received Mail Count'
GRAPH_NAMES = [QUEUE_LENGTH_GRAPH_NAME, TRANSIT_TIME_GRAPH_NAME,
               RECEIVED_MAIL_GRAPH_NAME]

MAX_EMAIL_CHUNK = 10
MAX_INT = sys.maxint

GRAPH_COLORS = [ '0000FF',  #blue
                 'FF7F00',  #orange
                 '00FF00',  #green
                 'FF0000',  #red
                 'FF00FF',  #magenta
                 '00FFFF',  #cyan
                 '00FF7F' ] #light green
                 
class Email( object ):
    
    def __init__( self, timeStamp ):
        self.timeStamp = timeStamp
        self.retrieved = False
        self.transitTime = 0
        self.age = 0
        
    def _computeTransitTime( self, message ):
        """
        Compute the number of seconds between when the mail was sent and when
        it was received
        """
        receivedList = message.get_all( 'Received', None )
        if not receivedList: 
            msg = 'Could not compute TransitTime. No \'Received\' values.'
            self.log.warning( msg )
            return 0
        
        try:        
            start = receivedList[-1].split( ';' )[-1].strip()
            startTuple = email.Utils.parsedate_tz( start )
            startTime = time.mktime( startTuple[:9] )
            if startTuple[9]:
                startTime += startTuple[9]
                
            end = receivedList[0].split( ';' )[-1].strip()
            endTuple = email.Utils.parsedate_tz( end )
            endTime = time.mktime( endTuple[:9] )
            if endTuple[9]:
                endTime += endTuple[9]
            
            difference = endTime - startTime
        except:
            return 0
            
        return difference

    def markRetrieved( self, message ):
        """
        Mark this email as one that has been received
        """
        self.retrieved = True
        self.transitTime = self._computeTransitTime( message )
    
    def ageEmail( self ):
        self.age += 1
        
class EmailManager( object ):
    """
    A EmailManager object is used to manage a group of EMail
    objects. Each "EmailManager" possesses an emails dictionary in order
    to track the emails that have been sent to that address.
    """
    
    def __init__( self, address, log, maxQueueLength ):
        self.address = address
        self.log = log
        self.maxQueueLength = maxQueueLength
        
        self.retrievedEmailCount = 0 # number of retrieved emails in this cycle
        self.subjects = []           # a list of the subject lines from the emails in the queue
        self.emails = {}             # the queue { subject: Email object }
        self.receiveFailure = False  # tracks errors between cycles
        self.sendFailure = False     # tracks errors between cycles
        
    def add( self, subject, timeStamp ):
        """
        Insert a new email into the queue
        """
        # if queue is full, delete oldest email
        if self.emailsInQueue() == self.maxQueueLength:
            msg = 'Email queue for %s is full' % self.address
            self.log.debug( msg )
            self._delete( self.subjects[0] )
        
        self.subjects.append( subject )
        self.emails[subject] = Email( timeStamp )
        
        msg = 'Added email \'%s\', timeStamp: %d, to queue: %s' % \
            ( subject, timeStamp, self.address )
        self.log.debug( msg )
        
    def _delete( self, subject ):
        """
        Remove an email from dictionaries and lists
        """
        del self.emails[subject]
        del self.subjects[self.subjects.index( subject )]
        
    def ageEmails( self ):
        """
        
        """
        for subject in self.subjects:
            email = self.emails[subject]
            # must drop old emails because rrd only waits so long before it
            # assumes that a value is lost
            if email.age >= self.maxQueueLength-1: 
                msg = '%s: aging out email \'%s\'' % ( self.address, subject )
                self.log.debug( msg )
                self._delete( subject )
            else:
                email.ageEmail()

    def clearRetrievedMail( self ):
        """
        Remove retrieved mail from dictionaries and lists
        """
        
        self.retrievedEmailCount = 0
        while self.emailsInQueue() > 0:
            subject = self.subjects[0]
            email = self.emails[subject]
            if email.retrieved: 
                self._delete( subject )
            else:
                break
        
    def emailsInQueue( self ):
        """
        Return the number of objects in the queue
        """
        return len( self.subjects )
    
    def emailsNotRetrievedCount( self ):
        """
        Return the number of emails that have not been marked retrieved
        """
        count = 0
        for email in self.emails.values():
            if not email.retrieved: count += 1
            
        return count
        
    def getTransitTimes( self ):
        """
        Return a tuple of tuples ((timeStamp, transitTime), (timeStamp, transitTime))
        """
        retVal = ()
        for subject in self.subjects:
            email = self.emails[subject]
            if not email.retrieved: break
            retVal += ( ( email.timeStamp, email.transitTime ), )
            
        return retVal
            
    def markMailRetrieved( self, message ):
        """
        Search queue for matching message. If found, mark it, save statistics, 
        return True. If not found, return false.
        """
        subject = message['Subject']
        
        if not str(subject) in self.subjects:
            msg = 'Email \'%s\' to %s is not in the queue' % ( subject, self.address )
            self.log.debug( msg )
            return False
        
        email = self.emails[subject]
        email.markRetrieved( message )
        self.retrievedEmailCount += 1
        
        msg = 'Email \'%s\' to %s was found in the queue at index %d' % \
            ( subject, self.address, self.subjects.index( subject ) )
        self.log.debug( msg )
        
        return True
        
    def subjectsWithStatus( self ):
        """
        Return a list of the subjects in the queue with (R) appended to 
        those that have been received but are still in the queue
        """
        subjects = []
        for subject in self.subjects:
            email = self.emails[subject]
            subjects.append( subject + '(R)' if email.retrieved else subject )
            
        return subjects
        
        
    # def retrievedEmailCount( self ):
        # """
        # Returns the number of emails retrieved in this cycle
        # """
        # count = 0
        # for email in self.emails.values():
            # if email.retrieved and email.age == 0: count += 1
        
        # return count
                
class EmailManagerCollection( object ):
    
    managers = {}
    
    def __init__( self, log, queueLength ):
        self.log = log
        self.queueLength = queueLength
        
    def __call__( self, address=None ):
        """
        If called, return either a list of all managers or a specific manager
        """
        if not address:
            return self.managers.values()
        elif address in self.managers.keys():
            return self.managers[address]
        else:
            return None
            
    def add( self, address ):
        self.managers[address] = EmailManager( address, self.log, self.queueLength )
        return self.managers[address]
        
    def addresses( self ):
        return self.managers.keys()

class EmailPing( PBDaemon ):
    """
    EmailPing is designed to monitor the state of an email server and/or
    Internet connection. The basic cycle is as follows:
    1. Check a POP mailbox for new messages.
    2. Compare any new messages with ones that we know we sent. If
       no matching messages received, report an error.
    3. Send more messages.
    
    Numerous error conditions are monitored and generate events:
    epSendFailure            Error while sending messages
    epSendClear
    epPopConnectionFailure   Unable to connect to the POP server
    epPopConnectionClear
    epPopReceiveFailure      No messages received from POP account during this cycle
    epPopReceiveClear
    epAccountReceiveFailure  No messages received from a specific "to" 
                             address during this cycle
    """

    lastCycleTime = 0
    
    popConnectionFailure = False
    popReceiveFailure = False
    recordPerformanceData = True
    
    name = 'emailping'
    """
    Method Sequence: 
    
    EmailPing.__init__()
        PBDaemon.__init__()
            ZenDaemon.__init__()
                CmdBase.__init__()                  
    PBDaemon.run()
        EmailPing.connected()
            connected() creates a deferred that spawns periodic calls from the
            reactor to emailCycle()
    """
    
    def __init__( self ):
        
        super( EmailPing, self ).__init__( keeproot=True )
        
        # get a connection to the DMD
        from Products.ZenUtils.ZCmdBase import ZCmdBase
        zcmdbase = ZCmdBase( noopts=True )
        self.dmd = zcmdbase.dmd
        
        # seed the number used for a subject line
        from random import random
        self.emailNumber = int( random() * MAX_INT )
        
        self.rrdStats = EmailPingStats()

    def connected( self ):
        
        if not self.validateOptions():
            self.stop()
            return
        
        # For some reason that I can't figure out, the severity level does not
        # get set in the Products.ZenUtils.CmdBase setupLogging method.
        # It always starts at the INFO level. I have to manually set the
        # logging level here.
        try:
            loglevel = int(self.options.logseverity)
        except ValueError:
            loglevel = getattr(logging, self.options.logseverity.upper(), logging.INFO)
        self.log.setLevel(loglevel)
        
        self.log.info( 'Starting EmailPing. Instance: %s' % self.name )
        self.configureOptions()
        deferred = drive( self.configurePerformanceData )
        deferred.addErrback( self.logError )
        deferred.addCallback( self.startEmailCycle )
        # NOTE: Last addCallback deferred must have the following line on it
        # to terminate the deferred
        # deferred.addBoth(lambda unused: self.stop())
    
    def validateOptions( self ):
    
        if not self.options.toaddress:
            msg = 'Attempting to start EmailPing without ' \
                  'defining --toaddress option.'
            self.log.error( 'Attempting to start EmailPing without ' \
                                'defining --toaddress option.' )
            return False
                             
        # split the toaddress option into a list of addresses
        self.options.toaddress = \
            [address.strip() for address in self.options.toaddress.split( ';' )]
        
        # verify address takes the xxx@yyy.zzz form
        for address in self.options.toaddress:
            if not re.match( r'.+@.+\..+', address ):
                self.log.error( 'Address \'%s\' is invalid.' % address )
                return False
        
        return True
                             
    def configureOptions( self ):

        # TODO: add code for multiple instances
        # if we had to change the instance name, notify the user in the log
        # if getattr( self.options, 'original_instancename', None ):
            # msg = 'Option --instancename cannot contain the \'_\' character. ' \
                  # 'Modifying to: %s' % self.options.instancename
            # self.log.warning( msg )
            # delattr( self.options, 'original_instancename' )
        # self.name = self.options.instancename.lower()
            
        # create EmailManager object for each address
        self.emailManagers = EmailManagerCollection( self.log, self.options.emailqueuelength )
        for address in self.options.toaddress:
            self.emailManagers.add( address )
        
        # if popport not specified, use the default
        if self.options.popport == 0:
            self.options.popport = POP_LOGIN_TYPES[self.options.poplogintype]
                
        # self.popaccount is used as the component in some error messages.
        # If user name takes the form xxx@yyy.zzz, just use that, otherwise
        # put the username and pophost together as username@pophost
        if re.match( r'.+@.+\..+', self.options.popusername ):
            self.popaccount = self.options.popusername
        else:
            self.popaccount = '%s@%s' % ( self.options.popusername, 
                                          self.options.pophost )

        # Daemons cycle a little longer than the cycle interval on each cycle.
        # Since we want to keep our cycles aligned with rrd data slots, we use
        # a mechanism to realign every 24 hours
        self.alignmentInterval = int(24*60*60 / self.options.emailcycleinterval) * \
            self.options.emailcycleinterval

    def configurePerformanceData( self, driver ):
            
        self.rrdStats.config( self.log, 
                              self.name, 
                              self.options.monitor, 
                              self.options.emailcycleinterval )
        
        #set up all the data points in the default PerformanceConf
        try:
            self.changedZope = False
            template = self.dmd.Monitors.rrdTemplates.PerformanceConf
            dataSource = self.configureDataSource( template )
            yield defer.succeed( self.configureDataPoints( dataSource ) )
            driver.next()
            yield defer.succeed( self.configureGraphs( template ) )
            driver.next()
            yield defer.succeed( self.configureGraphPoints( dataSource ) )
            driver.next()
            if self.changedZope:
                import transaction
                transaction.commit()
                self.log.debug( 'Zope updated' )
            else:
                self.log.debug( 'Zope up to date. No changes committed.' )
            delattr( self, 'changedZope' )
        except Exception, e:
            msg = 'Error configuring performance templates: %s' % e.args
            self.log.warning( msg )
            self.recordPerformanceData = False
            
        yield defer.succeed(0)
        driver.next()
    
    def configureDataSource( self, template ):
    
        if self.name in template.datasources.objectIds():
            return template.datasources._getOb( self.name )
        
        DS_OPTION = 'BuiltInDS.Built-In'
        datasource = template.manage_addRRDDataSource( self.name, DS_OPTION )
        self.log.info( 'Created new data source: %s' % self.name )
        self.changedZope = True
        return datasource
        
    def configureDataPoints( self, datasource ):
        cyclesPerHour = 3600 / self.options.emailcycleinterval
        rras = []

        # 2 days of raw data
        # 5 days of data @ 1 data point / 1 hour
        # 83 days of data @ 1 data point / 6 hours
        # 450 days of data @ 1 data point / day
        rras += ['--step', str( self.options.emailcycleinterval )]
        rras.append( 'DS:ds0:GAUGE:%s:U:U' % \
            str( self.options.emailcycleinterval * 
            (self.options.emailqueuelength + 2) ) )
        rras.append( 'RRA:AVERAGE:0.5:1:%d' % ( 48 * cyclesPerHour ) )
        rras.append( 'RRA:MAX:0.5:%d:120' % cyclesPerHour )
        rras.append( 'RRA:MAX:0.5:%d:332' % ( cyclesPerHour * 6 ) )
        rras.append( 'RRA:MAX:0.5:%d:450' % ( cyclesPerHour * 24 ) )
        RRD_CREATE_COMMAND_AVG = rras    
        
        # same data points, but save MAX value, not average
        rras = []
        rras += ['--step', str( self.options.emailcycleinterval )]
        rras.append( 'DS:ds0:GAUGE:%s:U:U' % \
            str( self.options.emailcycleinterval * 
            (self.options.emailqueuelength + 2) ) )
        rras.append( 'RRA:MAX:0.5:1:%d' % ( 48 * cyclesPerHour ) )
        rras.append( 'RRA:MAX:0.5:%d:120' % cyclesPerHour )
        rras.append( 'RRA:MAX:0.5:%d:332' % ( cyclesPerHour * 6 ) )
        rras.append( 'RRA:MAX:0.5:%d:450' % ( cyclesPerHour * 24 ) )
        RRD_CREATE_COMMAND_MAX = rras    

        # cycle time must be configured the same as the other data points on the
        # cycle time graph, so we use defaults
        performanceConf = self.dmd.Monitors.Performance._getOb( 
            self.options.monitor )
        
        rras = []
        rras += ['--step', str( performanceConf.perfsnmpCycleInterval )]
        rras.append( 'DS:ds0:GAUGE:%s:U:U' % \
            str( performanceConf.perfsnmpCycleInterval * 3 ) )
        rras += performanceConf.defaultRRDCreateCommand
        RRD_CREATE_COMMAND_CT = rras    # rrd for cycle times
        
        
        # add cycleTime data source
        usedDataPointIds = ['cycleTime']
        self.rrdStats.createRRDFile( 'cycleTime', RRD_CREATE_COMMAND_CT )
        if 'cycleTime' not in datasource.datapoints.objectIds():
            datasource.manage_addRRDDataPoint( 'cycleTime' )
            msg = 'Added data point cycleTime to data source %s' % self.name
            self.log.info( msg )
            self.changedZope = True

        # add unknown_rec data source
        usedDataPointIds.append( 'unknown_rec' )
        self.rrdStats.createRRDFile( 'unknown_rec', RRD_CREATE_COMMAND_MAX )
        if 'unknown_rec' not in datasource.datapoints.objectIds():
            datasource.manage_addRRDDataPoint( 'unknown_rec' )
            msg = 'Added data point unknown_rec to data source %s' % self.name
            self.log.info( msg )
            self.changedZope = True
        
        # add address_ql, address_tt, address_rec data sources for each "toaddress"
        for address in self.emailManagers.addresses():
            name = '%s_ql' % address
            usedDataPointIds.append( name )
            self.rrdStats.createRRDFile( name, RRD_CREATE_COMMAND_MAX )
            if name not in datasource.datapoints.objectIds():
                datasource.manage_addRRDDataPoint( name )
                msg = 'Added data point %s to data source %s' % ( name, self.name )
                self.log.info( msg )
                self.changedZope = True
                
            name = '%s_rec' % address
            usedDataPointIds.append( name )
            self.rrdStats.createRRDFile( name, RRD_CREATE_COMMAND_MAX )
            if name not in datasource.datapoints.objectIds():
                datasource.manage_addRRDDataPoint( name )
                msg = 'Added data point %s to data source %s' % ( name, self.name )
                self.log.info( msg )
                self.changedZope = True
                
            name = '%s_tt' % address
            usedDataPointIds.append( name )
            self.rrdStats.createRRDFile( name, RRD_CREATE_COMMAND_AVG )
            if name not in datasource.datapoints.objectIds():
                datasource.manage_addRRDDataPoint( name )
                msg = 'Added data point %s to data source %s' % ( name, self.name )
                self.log.info( msg )
                self.changedZope = True
                
        # remove unused data points
        for datapointId in datasource.datapoints.objectIds():
            if datapointId not in usedDataPointIds:
                datasource.datapoints._delObject( datapointId, suppress_events=True )
                msg = 'Removed datapoint %s from datasource %s' % ( datapointId, self.name )
                self.log.info( msg )
                self.changedZope = True
        
    def configureGraphs( self, template ):
    
        if not QUEUE_LENGTH_GRAPH_NAME in template.graphDefs.objectIds():
            graph = template.manage_addGraphDefinition( QUEUE_LENGTH_GRAPH_NAME )
            graph.units = 'emails'
            msg = 'Created graph %s' % QUEUE_LENGTH_GRAPH_NAME
            self.log.info( msg )
            
        if not TRANSIT_TIME_GRAPH_NAME in template.graphDefs.objectIds():
            graph = template.manage_addGraphDefinition( TRANSIT_TIME_GRAPH_NAME )
            graph.units = 'seconds'
            msg = 'Created graph %s' % TRANSIT_TIME_GRAPH_NAME
            self.log.info( msg )
        
        if not RECEIVED_MAIL_GRAPH_NAME in template.graphDefs.objectIds():
            graph = template.manage_addGraphDefinition( RECEIVED_MAIL_GRAPH_NAME )
            graph.units = 'emails'
            msg = 'Created graph %s' % RECEIVED_MAIL_GRAPH_NAME
            self.log.info( msg )
        
    def configureGraphPoints( self, template ):
    
        from Products.ZenModel.DataPointGraphPoint import DataPointGraphPoint
        
        graph = template.graphDefs._getOb( 'Cycle Times' )
        if not self.name in graph.graphPoints.objectIds():
            graphPoint = graph.createGraphPoint( DataPointGraphPoint, self.name )
            graphPoint.dpName = '%s_cycleTime' % self.name
            self.log.info( 'Added graph point %s to graph \'Cycle Times\'' % self.name )
            self.changedZope = True
        
        graphQL = template.graphDefs._getOb( QUEUE_LENGTH_GRAPH_NAME )
        graphTT = template.graphDefs._getOb( TRANSIT_TIME_GRAPH_NAME )
        graphREC = template.graphDefs._getOb( RECEIVED_MAIL_GRAPH_NAME )
        
        if not 'unknown' in graphREC.graphPoints.objectIds():
            graphPoint = graphREC.createGraphPoint( DataPointGraphPoint, 'unknown' )
            graphPoint.dpName = '%s_unknown_rec' % self.name
            graphPoint.cFunc = 'MAX'
            graphPoint.lineType = 'AREA'
            graphPoint.stacked = True
            graphPoint.color = 'BABABA' #gray
            graphPoint.sequence = 40
            self.log.info( 'Added graph point unknown to graph \'%s\'' % RECEIVED_MAIL_GRAPH_NAME )
            self.changedZope = True

        # used to make all the graphs consistent
        class graphPointData():
            def __init__( self, sequence, color ):
                self.sequence = sequence
                self.color = color
        
        graphPoints = {}
        sequence = 0
        for address in self.emailManagers.addresses():
            graphPoints[address] = graphPointData( sequence, GRAPH_COLORS[sequence] )
            sequence += 1

        # make sure each current address has a graph point.
        for address in self.emailManagers.addresses():
            if not address in graphQL.graphPoints.objectIds():
                graphPoint = graphQL.createGraphPoint( DataPointGraphPoint, address )
                graphPoint.dpName = '%s_%s_ql' % ( self.name, address )
                graphPoint.cFunc = 'MAX'
                graphPoint.sequence = graphPoints[address].sequence
                graphPoint.color = graphPoints[address].color
                msg = 'Added graph point %s to graph \'%s\'' % \
                    ( address, QUEUE_LENGTH_GRAPH_NAME )
                self.log.info( msg )
                self.changedZope = True
            else:
                graphPoint = graphQL.graphPoints._getOb( address )
                if graphPoint.sequence != graphPoints[address].sequence:
                    graphPoint.sequence = graphPoints[address].sequence
                    graphPoint.color = graphPoints[address].color
                    self.changedZope = True
                
            if not address in graphTT.graphPoints.objectIds():
                graphPoint = graphTT.createGraphPoint( DataPointGraphPoint, address )
                graphPoint.dpName = '%s_%s_tt' % ( self.name, address )
                graphPoint.sequence = graphPoints[address].sequence
                graphPoint.color = graphPoints[address].color
                msg = 'Added graph point %s to graph \'%s\'' % \
                    ( address, TRANSIT_TIME_GRAPH_NAME )
                self.log.info( msg )
                self.changedZope = True
            else:
                graphPoint = graphTT.graphPoints._getOb( address )
                if graphPoint.sequence != graphPoints[address].sequence:
                    graphPoint.sequence = graphPoints[address].sequence
                    graphPoint.color = graphPoints[address].color
                    self.changedZope = True
        
            if not address in graphREC.graphPoints.objectIds():
                graphPoint = graphREC.createGraphPoint( DataPointGraphPoint, address )
                graphPoint.dpName = '%s_%s_rec' % ( self.name, address )
                graphPoint.cFunc = 'MAX'
                graphPoint.lineType = 'AREA'
                graphPoint.stacked = True
                graphPoint.sequence = graphPoints[address].sequence
                graphPoint.color = graphPoints[address].color
                msg = 'Added graph point %s to graph \'%s\'' % \
                    ( address, RECEIVED_MAIL_GRAPH_NAME )
                self.log.info( msg )
            else:
                graphPoint = graphREC.graphPoints._getOb( address )
                if graphPoint.sequence != graphPoints[address].sequence:
                    graphPoint.sequence = graphPoints[address].sequence
                    graphPoint.color = graphPoints[address].color
                    self.changedZope = True
                self.changedZope = True
        
        # remove unused graph points 
        for graphPointId in graphQL.graphPoints.objectIds():
            if graphPointId not in self.emailManagers.addresses():
                graphQL.graphPoints._delObject( graphPointId, suppress_events=True )
                msg = 'Removed graphpoint %s from graph \'%s\'' % \
                    ( graphPointId, QUEUE_LENGTH_GRAPH_NAME )
                self.log.info( msg )
                self.changedZope = True
                
        for graphPointId in graphTT.graphPoints.objectIds():
            if graphPointId not in self.emailManagers.addresses():
                graphTT.graphPoints._delObject( graphPointId, suppress_events=True )
                msg = 'Removed graphpoint %s from graph \'%s\'' % \
                    ( graphPointId, TRANSIT_TIME_GRAPH_NAME )
                self.log.info( msg )
                self.changedZope = True
        
        usedGraphPointIds = self.emailManagers.addresses() + ['unknown']
        for graphPointId in graphREC.graphPoints.objectIds():
            if graphPointId not in usedGraphPointIds:
                graphREC.graphPoints._delObject( graphPointId, suppress_events=True )
                msg = 'Removed graphpoint %s from graph \'%s\'' % \
                    ( graphPointId, RECEIVED_MAIL_GRAPH_NAME )
                self.log.info( msg )
                self.changedZope = True

                
    def logError( self, error ):
    
        self.log.exception( error.getErrorMessage() )
            
    def clearMailbox( self ):
    
        """
        Connect to a POP mailbox and delete all existing messages
        
        @param driver: a Driver object that walks this generator function
        @type driver: Driver object
        """
        
        connection = self.openPopConnection()
        if connection is None: return
        
        self.eraseAllMessagesInMailbox( connection )
        self.closePopConnection( connection )
    
    def startEmailCycle( self, ignored = None ):
    
        self.log.info( 'Beginning emailping cycle' )
            
        # retrieve the timeStamp for this cycle
        self.cycleTimeStamp = self.rrdStats.getCurrentTimeStamp( 
            '%s_ql' % self.emailManagers.addresses()[0] )
        self.log.debug( 'TimeStamp for this cycle is %d' % self.cycleTimeStamp )
        
        self.nextAlignmentTimeStamp = self.cycleTimeStamp + self.alignmentInterval
        
        # If we are less than 20 seconds from the next rrd aligned time cycle,
        # just use that as the current cycle time stamp. Run the next cycle
        # at one interval + difference + 10 seconds
        nextCycleTimeStamp = self.cycleTimeStamp + self.options.emailcycleinterval
        if nextCycleTimeStamp - time.time() < 20:
            self.cycleTimeStamp = nextCycleTimeStamp
            nextCycleInterval = nextCycleTimeStamp - time.time() + \
                self.options.emailcycleinterval + 10
        else:
            nextCycleInterval = nextCycleTimeStamp - time.time() + 10
            
        if self.options.cycle:
            deferred = driveLater( nextCycleInterval, self.emailCycle )
            deferred.addErrback( self.logError )
                    
        # erase all messages in mailbox
        self.clearMailbox()
        
        # send out emails
        self.sendEmail()
        
        if not self.options.cycle:
            self.stop()
        
    def emailCycle( self, driver ):
        
        """
        Main function of this daemon. 
        
        Step 1: Retrieve emails from POP mailbox
        Step 2: Send new mail
        Step 3: Record performance data
        """
        
        # retrieve the timeStamp for this cycle
        self.cycleTimeStamp = self.rrdStats.getCurrentTimeStamp( 
            '%s_ql' % self.emailManagers.addresses()[0] )
            
        if self.cycleTimeStamp == self.nextAlignmentTimeStamp:
            offset = self.cycleTimeStamp + 10 - time.time()
            self.log.info( 'Aligning cycle by %f seconds.' % offset )
            
            nextCycleInterval = self.cycleTimeStamp + \
                self.options.emailcycleinterval + 10 - time.time()
            self.nextAlignmentTimeStamp = self.cycleTimeStamp + self.alignmentInterval
        else:
            nextCycleInterval = self.options.emailcycleinterval
            
        deferred = driveLater( nextCycleInterval, self.emailCycle )
        deferred.addErrback( self.logError )
        self.log.info( '' )
        self.log.info( 'Beginning emailping cycle' )
        
        startTime = time.time()
        self.unknownEmailCount = 0
        self.heartbeat()

        # How many emails have been sent but not retrieved?
        yield defer.succeed( self.getEmailsNotRetrievedCount() )
        emailsNotRetrievedCount = driver.next()

        # if one or more, try and get them
        if emailsNotRetrievedCount:
            msg = 'The queues contain %d emails to be retrieved' % emailsNotRetrievedCount
            self.log.debug( msg )
            
            # age all outstanding emails by one cycle
            self.ageEmails()
            
            yield defer.succeed( self.openPopConnection() )
            connection = driver.next()
            
            # continue if successfully connected to POP server
            if not connection is None:
                yield defer.succeed( self.getNewMailCount( connection ) )
                newMailCount = driver.next()
                
                # if there are new messages in the inbox, process 
                # MAX_EMAIL_CHUNK at a time, yielding in between
                retrievedEmailCount = 0
                if newMailCount:
                    generator = self.retrieveEmail( connection, newMailCount )
                    try:
                        while True:
                            yield defer.succeed( generator.next() )
                            retrievedEmailCount = driver.next()
                    except StopIteration:
                        self.closePopConnection( connection )
                
                self.unknownEmailCount = newMailCount - retrievedEmailCount
                
                # analyze the mail that was received and determine
                # if we need to send any events
                yield defer.succeed( self.sendRetrievedEvents( retrievedEmailCount ) )
                driver.next()
        else:
            self.log.warning( 'No emails in queue(s) to retrieve' )
            
        # send new email messages
        yield defer.succeed( self.sendEmail() )
        driver.next()
        
        # update performance data
        self.lastCycleTime = time.time() - startTime
        
        if self.recordPerformanceData:
            self.updatePerformanceData()
                
        yield defer.succeed( 0 )
        driver.next()
        
    def heartbeat( self ):
        """
        Send a heartbeat event for this monitor.
        """
        
        # set heartbeat to timeout at 3x email cycle
        timeout = self.options.emailcycleinterval * 3
        evt = Event.EventHeartbeat( self.options.monitor, 
                                    self.name, 
                                    timeout )
        self.eventQueue.append( evt )
        
        # if a watchdog was configured for this daemon, talk to it
        self.niceDoggie(self.options.emailcycleinterval) 
        
    def getNewMailCount( self, connection ):
        """
        Retrieves the number of messages in the POP Inbox
        """
        
        try:
            newMailCount = len( connection.list()[1] )
            if newMailCount == 0:
                self.log.info( 'No messages in Inbox.' )
            else:
                msg = 'There are %d messages in the mailbox.' % newMailCount
                self.log.debug( msg )
                
            return newMailCount
            
        except Exception, e:
            self.log.error( 'Error while retrieving messages: %s' % e.args )
            return 0
     
    def sendEmail( self ):
        """
        Sends an email using the email account configured in Zenoss Settings
        One email is sent to each --toaddress. The subject line is a number
        that is saved until the email has been received.
        """
        
        subject = str( self.emailNumber )
        
        msg = 'Sending email \'%s\', timeStamp: %d to %s' % \
            ( subject, self.cycleTimeStamp, '; '.join( self.emailManagers.addresses() ) )
        self.log.info( msg )
        
        # loop thru each "to" address
        for emailManager in self.emailManagers():
                        
            # set up new mail message
            emsg = MIMEText('')
            emsg['From'] = self.dmd.getEmailFrom()
            emsg['Subject'] = subject
            emsg['To'] = emailManager.address

            # send it
            result, errorMsg = Utils.sendEmail( emsg, 
                                                self.dmd.smtpHost,
                                                self.dmd.smtpPort, 
                                                self.dmd.smtpUseTLS, 
                                                self.dmd.smtpUser,
                                                self.dmd.smtpPass )
            # if successful send
            if result:
                emailManager.add( subject, self.cycleTimeStamp )
                # If this address was previously flagged with a failure, but
                # now succeeded, send clear event
                if emailManager.sendFailure:
                    msg = 'Sent email to %s' % emailManager.address
                    self.sendEmailPingEvent( 'epSendClear', emailManager.address, msg )
                    emailManager.sendFailure = False
            
            # if send failed
            else:
                msg = "Failed to send email \'%s\' to %s" % ( subject, emailManager.address )
                self.log.warning( msg )
                msg = 'Failed to send email to %s' % emailManager.address
                self.sendEmailPingEvent( 'epSendFailure', emailManager.address, msg )
                emailManager.sendFailure = True
       
        self.incrementEmailNumber()
        
    def incrementEmailNumber( self ):
    
        if self.emailNumber == MAX_INT:
            self.emailNumber = 1
        else:
            self.emailNumber += 1
    
    def sendEmailPingEvent( self, eventClassKey, component, summary, **kwargs ):
    
        fields = { 'agent': self.name,
                   'component': component,
                   'device': self.options.monitor,
                   'eventClassKey': eventClassKey,
                   'manager': self.fqdn,
                   'monitor': self.options.monitor,
                   'severity': 3,
                   'summary': summary }
        if kwargs:
            fields.update( kwargs )
        
        evt = Event.buildEventFromDict( fields )
        self.eventQueue.append( evt )
        
    def openPopConnection( self ):
    
        """
        Retrieve a connection to a POP server
        
        @return: object representing a connection to a POP server
        @rtype: POP3 object
        """
        
        connection = None
        
        try:
            if self.options.poplogintype == POP_LOGIN_TYPE_CLEARTEXT:
                connection = poplib.POP3( self.options.pophost, 
                                          self.options.popport )
            else:
                connection = poplib.POP3_SSL( self.options.pophost, 
                                              self.options.popport )
                                              
            connection.user( self.options.popusername )
            connection.pass_( self.options.poppassword )
            
        except Exception, e:
            # Track the state of a connection failure so we can send failure
            # and clear events
            self.popConnectionFailure = True
            
            summary = 'Failed to connect to POP server %s on port %d via %s.' % \
                      ( self.options.pophost, self.options.popport,
                        self.options.poplogintype )
            self.log.error( '%s Error message: %s' % ( summary, e.args ) )
            self.sendEmailPingEvent( 'epPopConnectionFailure', 
                                      self.options.pophost, summary )
                                      
            try:
                if connection:
                    connection.quit()
            except:
                pass
            
            return None
        
        # POP connection successful
        msg = 'Connected to POP server %s on port %d via %s' % \
                  ( self.options.pophost, self.options.popport, 
                    self.options.poplogintype )
        self.log.debug( msg )
        
        # Clear a previous failure
        if self.popConnectionFailure:
            self.sendEmailPingEvent( 'epPopConnectionClear', 
                                      self.options.pophost, msg )
            self.popConnectionFailure = False
             
        return connection
        
    def closePopConnection( self, connection ):
    
        try:
            connection.quit()
            msg = 'Closed connection to POP server %s' % self.options.pophost
            self.log.debug( msg )
        except:
            msg = 'Error while closing connection to POP server %s.' % \
                   self.options.pophost
            self.log.warning( msg )

    def eraseAllMessagesInMailbox( self, connection ):
    
        try:
            messageCount = len( connection.list()[1] )

            for messageIndex in range( messageCount ):
                connection.dele( messageIndex + 1 )
            
            msg = 'All emails in %s have been erased.' % self.popaccount
            self.log.info( msg )
        except Exception, e:
            msg = 'Unable to clear mailbox: %s' % ( e.args )
            self.log.error( msg )
    
    def getEmailsNotRetrievedCount( self ):
    
        notRetrievedCount = 0
       
        for emailManager in self.emailManagers():
            self.log.debug( 'EmailManager %s has %d items in the queue: %s' % \
                ( emailManager.address, 
                  emailManager.emailsInQueue(),
                  ', '.join( emailManager.subjectsWithStatus() ) ) )
            notRetrievedCount += emailManager.emailsNotRetrievedCount()
            
        return notRetrievedCount
        
    def ageEmails( self ):
        for emailManager in self.emailManagers():
            emailManager.ageEmails()
            
    def retrieveEmail( self, connection, newMailCount ):
    
        retrievedEmailCount = 0
        
        msg = 'Retrieving email. Host: %s Account: %s' % \
              ( self.options.pophost, self.options.popusername )
        self.log.debug( msg )
        
        addressPatterns = [r'.*<(?P<address>[^>]+).*',  # "My Name" <myname@domain.com>
                           r'(?P<address>.+@.+\..+)']   # myname@domain.com
                           
        # loop thru each email in the inbox and match with emails sent
        for messageIndex in range( 1, newMailCount + 1 ):
        
            # only check MAX_EMAIL_CHUNK mails at a time so as not to hog the CPU
            if messageIndex % MAX_EMAIL_CHUNK == 0:
                yield 0
            
            message = self.getEmailMessage( connection, messageIndex )
            connection.dele( messageIndex )        
            
            if message is None: break
            
            # retrieve the To address 
            for pattern in addressPatterns:
                match = re.match( pattern , message['To'] )
                if match: break
                    
            if match is None: 
                msg = 'Could not match TO field \'%s\' to an email address type' % message['To']
                self.log.warning( msg )
                continue
            
            # if "to" address is not one of ours, skip
            address = match.group( 'address' )
            if not address in self.emailManagers.addresses(): 
                msg = 'Received email from unknown sender: %s' % address
                self.log.info( msg )
                continue
            
            emailManager = self.emailManagers( address )
            
            # if the subject of the email is not one we sent, skip to next email
            if not emailManager.markMailRetrieved( message ): continue

            retrievedEmailCount += 1
            
        self.log.info( 'Retrieved %d sent messages.' % retrievedEmailCount )
            
        yield retrievedEmailCount
    
    def getEmailMessage( self, connection, messageIndex ):
    
        try:
            message = connection.retr( messageIndex )
            message = '\n'.join( message[1] )
            message = email.message_from_string( message )
            return message
        except Exception, e:
            self.log.error( 'Error while retrieving messages: %s' % e.args )
            return None
    
    def sendRetrievedEvents( self, retrievedEmailCount ):

        # if no new messages recevied, create an alarm event
        if retrievedEmailCount == 0:
            self.popReceiveFailure = True
            msg = '0 new email in POP mailbox %s' % self.popaccount
            self.sendEmailPingEvent( 'epPopReceiveFailure', self.popaccount, msg )
            return
            
        # if there were messages received and there was an active
        # alarm event, send a clear event
        elif self.popReceiveFailure:
            self.popReceiveFailure = False
            msg = 'Mail received in POP mailbox %s' % self.popaccount
            self.sendEmailPingEvent( 'epPopReceiveClear', self.popaccount, msg )
        
        # If no messages received from a "to" address, send alarm event.
        # Conversely, if "to" address flagged with alarm state and mail was
        # received, send clear event
        for emailManager in self.emailManagers():
            if emailManager.retrievedEmailCount == 0:
                emailManager.receiveFailure = True
                self.sendEmailPingEvent( 'epAccountReceiveFailure',
                                          emailManager.address,
                                         '0 messages received from %s' % emailManager.address )
                self.log.warning( 'Did not receive mail from %s' % emailManager.address )
            else:
                if emailManager.receiveFailure:
                    emailManager.receiveFailure = False
                    self.sendEmailPingEvent( 'epAccountReceiveClear',
                                              emailManager.address,
                                             'Message(s) received from %s' % emailManager.address )

    def updatePerformanceData( self ):
        
        for emailManager in self.emailManagers():

            # record number of emails received in this cycle
            datapoint = '%s_rec' % emailManager.address
            self.rrdStats.write( datapoint, 
                                 float( emailManager.retrievedEmailCount ), 
                                 self.cycleTimeStamp )
                                 
            # transit times must be written to rrd in chronological order. If
            # emails arrive out of order, must wait and record the oldest first.
            datapoint = '%s_tt' % emailManager.address
            for timeStamp, transitTime in emailManager.getTransitTimes():
                self.rrdStats.write( datapoint, float( transitTime ), timeStamp )
                
            # now that transit times on retrieved emails have been recorded,
            # they can finally be disposed of
            emailManager.clearRetrievedMail()
            
            # Record number of emails that have yet to be retrieved. 
            datapoint = '%s_ql' % emailManager.address
            self.rrdStats.write( datapoint, 
                                 float( emailManager.emailsNotRetrievedCount() ),
                                 self.cycleTimeStamp )
            
        # write the last cycle time
        self.rrdStats.write( 'cycleTime', self.lastCycleTime )
        
        # record the number of emails received that couldn't be matched
        self.rrdStats.write( 'unknown_rec', 
                             float( self.unknownEmailCount ), 
                             self.cycleTimeStamp )
    
    #TODO: Allow emailping to run multiple instances
    # def setupLogging(self):
    
        # """
        # Override CmdBase.py so that we can create unique log files for
        # each instance of EmailPing
        # """
        
        # #instancename cannot contain the '_' character since performance 
        # #templates use it as a delimiter between the datasource and point name
        # if self.options.instancename.find('_') != -1:
            # name = ''.join( self.options.instancename.split( '_' ) )
            # self.options.original_instancename = self.options.instancename
            # self.options.instancename = name
            
        # import logging
        # import os

        # rootLog = logging.getLogger()
        # rootLog.setLevel( logging.WARN )
        
        # logname = 'zen.%s' % self.options.instancename
        # self.log = logging.getLogger( logname )
        # self.log.setLevel( self.options.logseverity )
        
        # filename = '%s.log' % self.options.instancename.lower()
        # logdir = self.checkLogpath()
        # if not logdir:
            # logdir = Utils.zenPath( 'log' )
        # logfile = os.path.join( logdir, filename )
        # maxBytes = self.options.maxLogKiloBytes * 1024
        # backupCount = self.options.maxBackupLogs
        # logHandler = logging.handlers.RotatingFileHandler( 
            # logfile, 'a', maxBytes, backupCount )
        # logHandler.setFormatter( logging.Formatter(
            # "%(asctime)s %(levelname)s %(name)s: %(message)s" ) )
        # self.log.addHandler( logHandler )
    
    def buildOptions( self ):
        
        super( EmailPing, self ).buildOptions()

        self.parser.add_option(
            '--toaddress',
            type='string',
            dest='toaddress', 
            help='Email address(es) where mail is to be sent to. Separate ' \
                 'multiple addresses with the \';\' character.' )
        self.parser.set_defaults( toaddress=None )
        
        self.parser.add_option(
            '--emailqueuelength',
            dest='emailqueuelength',
            type='int',
            help='Maximum number of emails (per address) to store in ' \
                 'memory for comparison to Inbox' )
        self.parser.set_defaults( emailqueuelength=5 )
        
        self.parser.add_option(
            '--pophost',
            dest='pophost',
            help='FQDN of the POP server' )
        self.parser.set_defaults( pophost='localhost' )
        
        self.parser.add_option(
            '--popusername',
            dest='popusername',
            help='User name for the POP account' )
        self.parser.set_defaults( popusername='zenoss' )
        
        self.parser.add_option(
            '--poppassword',
            dest='poppassword',
            help='Password for the POP account' )
        self.parser.set_defaults( poppassword='zenosspw' )
        
        self.parser.add_option(
            '--poplogintype',
            dest='poplogintype',
            help='Method used to login to pop server. ' \
                 'Available options: %s' % ', '.join( POP_LOGIN_TYPES.keys() ) )
        self.parser.set_defaults( poplogintype=POP_LOGIN_TYPE_CLEARTEXT )
        
        self.parser.add_option(
            '--popport',
            dest='popport',
            type='int',
            help='Port number to use for logging into pop server. ' \
                 'Value 0 uses default port for selected poplogintype ' \
                 '(cleartext=110, ssl=995)' )
        self.parser.set_defaults( popport=0 )

        self.parser.add_option(
            '--emailcycleinterval',
            dest='emailcycleinterval',
            type='int',
            help='Number of seconds between sending/checking emails. ' )
        self.parser.set_defaults( emailcycleinterval = 180 )

        #TODO: Allow emailping to run multiple instances
        # self.parser.add_option(
            # '--instancename',
            # dest='instancename',
            # help='Name of this instance of EmailPing' )
        # self.parser.set_defaults( instancename='EmailPing' )
            
if __name__ == '__main__':
    emailping = EmailPing()
    emailping.run()