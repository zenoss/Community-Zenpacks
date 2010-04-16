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

MAX_EMAIL_CHUNK = 10
MAX_INT = sys.maxint
    
class ToAddress( object ):
    
    def __init__( self, address ):
        self.address = address
        self.mailFound = True
        self.receiveFailure = False
        self.sendFailure = False
        self.subjects = []
        self.transitTimes = {}
        
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

    isFirstCycle = True
    lastCycleTime = 0
    
    popReceiveFailure = False
    popConnectionFailure = False
    recordPerformanceData = True
    
    """
    Method Sequence: 
    
    EmailPing.__init__()
        PBDaemon.__init__()
            ZenDaemon.__init__()
                CmdBase.__init__()                  
    PBDaemon.run()
        EmailPing.connected()
            connected() creates a deferred that spawns periodic calls from the
            reactor to emailCycle() and 
    """
    
    def __init__( self ):
        
        self.name = 'emailping'
    
        super( EmailPing, self ).__init__( keeproot=True )

        # get a connection to the DMD
        from Products.ZenUtils.ZCmdBase import ZCmdBase
        zcmdbase = ZCmdBase( noopts=True )
        self.dmd = zcmdbase.dmd
        
        # seed the number used for a subject line
        from random import random
        self.emailNumber = int( random() * MAX_INT )

    def connected( self ):
        
        if not self.validateOptions():
            self.stop()
            return
                        
        self.log.info( 'Starting EmailPing. Instance: %s' % self.name )
        self.configureOptions()
        deferred = drive( self.configurePerformanceData )
        deferred.addErrback( self.logError )
        deferred.addCallback( self.startClearMailbox )
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
            
        # create ToAddress objects for each address
        self.toAddresses = {}
        for address in self.options.toaddress:
            self.toAddresses[address] = ToAddress( address )
        
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
        
    def configurePerformanceData( self, driver ):
        
        cyclesPerHour = int( 60*60 / self.options.emailcycleinterval )
        cyclesPerDay = int( 24*60*60 / self.options.emailcycleinterval )
        # 14 days of raw data are stored
        # Next, 4 hours are compressed into 1 datapoint, leaving 6 datapoints
        # per day * 90 days.
        createCommand = ( 
            'RRA:AVERAGE:0.5:1:%d' % int( cyclesPerDay * 14 ), 
            'RRA:MAX:0.5:%d:%d' % ( int( cyclesPerHour * 4 ), int( 6 * 90 ) ) )
            
        self.rrdStats.config( self.options.monitor, self.name, [], createCommand )
        
        #set up all the data points in the default PerformanceConf
        try:
            self.changedZope = False
            template = self.dmd.Monitors.rrdTemplates.PerformanceConf
            dataSource = self.configureDataSource( template )
            self.configureDataPoints( dataSource )
            self.configureGraphs( template )
            self.configureGraphPoints( dataSource )
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
    
        if 'cycleTime' not in datasource.datapoints.objectIds():
            datasource.manage_addRRDDataPoint( 'cycleTime' )
            msg = 'Added data point cycleTime to data source %s' % self.name
            self.log.info( msg )
            self.changedZope = True

        for address in self.toAddresses:
            name = '%s_ql' % address
            if name not in datasource.datapoints.objectIds():
                datasource.manage_addRRDDataPoint( name )
                msg = 'Added data point %s to data source %s' % ( name, self.name )
                self.log.info( msg )
                self.changedZope = True
            name = '%s_tt' % address
            if name not in datasource.datapoints.objectIds():
                datasource.manage_addRRDDataPoint( name )
                msg = 'Added data point %s to data source %s' % ( name, self.name )
                self.log.info( msg )
                self.changedZope = True
                
    def configureGraphs( self, template ):
    
        if not QUEUE_LENGTH_GRAPH_NAME in template.graphDefs.objectIds():
            graph = template.manage_addGraphDefinition( QUEUE_LENGTH_GRAPH_NAME )
            graph.units = 'emails'
            
        if not TRANSIT_TIME_GRAPH_NAME in template.graphDefs.objectIds():
            graph = template.manage_addGraphDefinition( TRANSIT_TIME_GRAPH_NAME )
            graph.units = 'seconds'
        
        
    def configureGraphPoints( self, template ):
    
        from Products.ZenModel.DataPointGraphPoint import DataPointGraphPoint
        
        graph = template.graphDefs._getOb( 'Cycle Times' )
        if not self.name in graph.graphPoints.objectIds():
            graphPoint = graph.createGraphPoint( DataPointGraphPoint, self.name )
            graphPoint.dpName = '%s_cycleTime' % self.name
            self.log.info( 'Added graph point %s to graph \'Cycle Times\'' )
            self.changedZope = True
        
        graphQL = template.graphDefs._getOb( QUEUE_LENGTH_GRAPH_NAME )
        graphTT = template.graphDefs._getOb( TRANSIT_TIME_GRAPH_NAME )
        for address in self.toAddresses:
            if not address in graphQL.graphPoints.objectIds():
                graphPoint = graphQL.createGraphPoint( DataPointGraphPoint, address )
                graphPoint.dpName = '%s_%s_ql' % ( self.name, address )
                msg = 'Added graph point %s to graph \'EmailPing Queue Lengths\'' % address
                self.log.info( msg )
                self.changedZope = True
                
            if not address in graphTT.graphPoints.objectIds():
                graphPoint = graphTT.createGraphPoint( DataPointGraphPoint, address )
                graphPoint.dpName = '%s_%s_tt' % ( self.name, address )
                msg = 'Added graph point %s to graph \'EmailPing Transit Times\'' % address
                self.log.info( msg )
                self.changedZope = True
                
    def logError( self, error ):
    
        self.log.exception( error.getErrorMessage() )
    
    def startClearMailbox( self, ignored = None ):
    
        deferred = drive( self.clearMailbox )
        deferred.addErrback( self.logError )
        
    def clearMailbox( self, driver ):
    
        """
        Connect to a POP mailbox and delete all existing messages
        
        @param driver: a Driver object that walks this generator function
        @type driver: Driver object
        """
        
        yield defer.succeed( self.openPopConnection() )
        connection = driver.next()
        
        if connection is None:
            raise StopIteration()
        
        yield defer.succeed( self.eraseAllMessagesInMailbox( connection ) )
        driver.next()
        
        yield defer.succeed( self.closePopConnection( connection ) )
        driver.next()
    
    def startEmailCycle( self, ignored = None ):
    
        deferred = drive( self.emailCycle )
        deferred.addErrback( self.logError )
        
        if not self.options.cycle:
            deferred.addBoth( lambda unused: self.stop() )
            
    def emailCycle( self, driver ):
        
        """
        Main function of this daemon. 
        
        Step 1: Retrieve emails from POP mailbox
        Step 2: Send new mail
        Step 3: Record performance data
        """
        
        self.heartbeat()
        
        startTime = time.time()
        
        if self.options.cycle:
            deferred = driveLater( self.options.emailcycleinterval, 
                                   self.emailCycle )
            deferred.addErrback( self.logError )
        
        # How many emails have been sent but not retrieved?
        yield defer.succeed( self.getEmailsInFlight() )
        sentMail = driver.next()
        
        # if one or more, try and get them
        if sentMail:
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
                        
                # analyze the mail that was received and determine
                # if we need to send any events
                yield defer.succeed( self.sendRetrievedEvents( retrievedEmailCount ) )
                driver.next()
        
        # send new email messages
        yield defer.succeed( self.sendEmail() )
        driver.next()
        
        # update performance data
        self.lastCycleTime = time.time() - startTime
        if self.isFirstCycle:
            self.isFirstCycle = False
        else:
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
        
        sentMail = False
        subject = str( self.emailNumber )
        
        # loop thru each "to" address
        for address in self.toAddresses:
            
            # Check to see if this "to" address queue is full. If so,
            # delete the oldest from the queue
            if len( self.toAddresses[address].subjects ) == \
                    self.options.queuesize:
                self.log.warning( 'Email queue %s full.' % address )
                del self.toAddresses[address].subjects[0]
            
            # set up new mail message
            emsg = MIMEText('')
            emsg['From'] = self.dmd.getEmailFrom()
            emsg['Subject'] = subject
            emsg['To'] = address

            # send it
            result, errorMsg = Utils.sendEmail( emsg, 
                                                self.dmd.smtpHost,
                                                self.dmd.smtpPort, 
                                                self.dmd.smtpUseTLS, 
                                                self.dmd.smtpUser,
                                                self.dmd.smtpPass )
            # if successful send
            if result:
                msg = "Sent email \'%s\' to %s" % ( subject, address )
                self.log.info( msg )
                self.toAddresses[address].subjects.append( subject )
                sentMail = True
                # If this address was previously flagged with a failure, but
                # now succeeded, send event
                if self.toAddresses[address].sendFailure:
                    msg = 'Sent email to %s' % address
                    self.sendEmailPingEvent( 'epSendClear', address, msg )
                    self.toAddresses[address].sendFailure = False
            
            # if not successful send
            else:
                msg = "Failed to send email \'%s\' to %s" % ( subject, address )
                self.log.warning( msg )
                msg = 'Failed to send email to %s' % address
                self.sendEmailPingEvent( 'epSendFailure', address, msg )
                self.toAddresses[address].sendFailure = True
       
        if sentMail:
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
    
    def getEmailsInFlight( self ):
    
        sentCount = 0

        # If this is the first cycle, no messages have been sent, so just
        # return 0.
        if self.isFirstCycle:
            return 0
        
        for address in self.toAddresses:
            sentCount += len( self.toAddresses[address].subjects )
            
        if sentCount == 0:
            self.log.warning( 'No emails in queue to retrieve' )
        else:
            msg = 'The queues contain %d emails to be retrieved' % sentCount 
            self.log.debug( msg )
        
        return sentCount
        
    def retrieveEmail( self, connection, newMailCount ):
    
        msg = 'Retrieving email. Host: %s Account: %s' % \
              ( self.options.pophost, self.options.popusername )
        self.log.debug( msg )
        
        retrievedEmailCount = 0
        maxIndexes = {}
        
        for address in self.toAddresses:
            maxIndexes[address] = 0
            self.toAddresses[address].mailFound = False

            
        # loop thru each email in the inbox and match with emails sent
        for messageIndex in range( 1, newMailCount + 1 ):
        
            # only check MAX_EMAIL_CHUNK mails at a time so as not to hog the CPU
            if messageIndex % MAX_EMAIL_CHUNK == 0:
                yield 0
            
            message = self.getEmailMessage( connection, messageIndex )
            connection.dele( messageIndex )        
            
            if message is None: break
            
            self.log.debug( 'TO string: %s' % message['To'] )
            
            # retrieve the To address 
            addressPatterns = [r'.*<(?P<address>[^>]+).*',  # "My Name" <myname@domain.com>
                               r'(?P<address>.+@.+\..+)']    # myname@domain.com
            for pattern in addressPatterns:
                match = re.match( pattern , message['To'] )
                if match: break
                    
            if match is None: continue
            
            # if "to" address is not one of ours, skip
            address = match.group('address')
            if not address in self.toAddresses: 
                continue
            toAddress = self.toAddresses[address]
            
            # if the subject of the email is not one we sent, skip to next email
            if not message['Subject'] in toAddress.subjects: 
                continue

            # record state of email from this address and overall number
            # of emails retrieved (matched to ones we know we sent) during
            # this cycle
            toAddress.mailFound = True
            retrievedEmailCount += 1
            
            # If this is the most recent message retreived, save it's position
            # in the subjects list. Later we will remove [:maxindex] entries
            index = toAddress.subjects.index( message['Subject'] )
            if index > maxIndexes[address]:
                maxIndexes[address] = index
            
            # save the round trip time of this email for statistics
            transmitTime = self.getTransmitTime( message )
            toAddress.transitTimes[index] = transmitTime
            msg = 'Transmit time for message \'%s\' to %s was %d' % \
                  ( message['Subject'], address, transmitTime )
            self.log.debug( msg )
            
        # Delete subject lines from the queue
        # We delete from the most recent message retrieved back to the oldest
        # one sent.
        for address in maxIndexes:
            index = maxIndexes[address] + 1
            del self.toAddresses[address].subjects[:index]
            
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
    
    def getTransmitTime( self, message ):
    
        receivedList = message.get_all( 'Received', None )
        if not receivedList: 
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
        for address in self.toAddresses:
            if not self.toAddresses[address].mailFound:
                self.toAddresses[address].receiveFailure = True
                self.sendEmailPingEvent( 'epAccountReceiveFailure',
                                          address,
                                         '0 messages received from %s' % address )
                self.log.warning( 'Did not receive mail from %s' % address )
            else:
                if self.toAddresses[address].receiveFailure:
                    self.sendEmailPingEvent( 'epAccountReceiveClear',
                                              address,
                                             'Message(s) received from %s' % address )
                self.log.info( 'Received mail from %s' % address )

    def updatePerformanceData( self ):
        
        # write the queue length and transmit time data
        for address in self.toAddresses:
            toAddress = self.toAddresses[address]
            
            # queue length
            datapoint = '%s_ql' % address
            self.rrdStats.gauge( datapoint,
                                 self.options.emailcycleinterval,
                                 len( toAddress.subjects ) )

            # transmit time
            if len( toAddress.transitTimes ) == 0: 
                continue
            keys = toAddress.transitTimes.keys()
            keys.sort()
            for key in keys:
                datapoint = '%s_tt' % address 
                self.rrdStats.gauge( datapoint,
                                     self.options.emailcycleinterval,
                                     toAddress.transitTimes[key] )
            toAddress.transitTimes = {}
        
            
        # write the last cycle time
        self.rrdStats.gauge( 'cycleTime',
                             self.options.emailcycleinterval,
                             self.lastCycleTime )
                             
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
            '--queuesize',
            dest='queuesize',
            type='int',
            help='Maximum number of emails (per address) to store in ' \
                 'memory for comparison to Inbox' )
        self.parser.set_defaults( queuesize=5 )
        
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
                 'Value 0 uses default port for selected poplogintype' )
        self.parser.set_defaults( popport=0 )

        self.parser.add_option(
            '--emailcycleinterval',
            dest='emailcycleinterval',
            type='int',
            help='Number of seconds between sending/checking emails. ' \
                 'Default = 180 seconds' )
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