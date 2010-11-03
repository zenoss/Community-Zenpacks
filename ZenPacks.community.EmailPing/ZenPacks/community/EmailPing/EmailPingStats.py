###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2007, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
import Globals
from Products.ZenUtils.Utils import zenPath

import rrdtool
import os
import time

class EmailPingStats( object ):
    "Utility for a daemon to write out internal performance statistics"

    name = ""
    monitor = ""

    def config( self, log, name, monitor, cycleTime ):
        """Initialize the object.  We could do this in __init__, but
        that would delay creation to after configuration time, which
        may run asynchronously with collection or heartbeats.  By
        deferring initialization, this object implements the Null
        Object pattern until the application is ready to start writing
        real statistics.
        """
        self.log = log
        self.daemonName = name
        self.monitor = monitor
        self.cycleTime = cycleTime

    def createRRDFile( self, dataPointName, rrdCreateCommand ):
        """
        Create an RRD file if it does not exist or if the step value has changed.
        Returns the basename of the rrdFile, suitable for checking thresholds.
        """
        self.log.debug( 'Checking RRD File for %s' % dataPointName )
        
        if not self.daemonName: 
            return
        
        directory = zenPath( 'perf', 'Daemons', self.monitor )
        if not os.path.exists( directory ):
            self.log.debug( 'Creating directory: %s' % directory )
            os.makedirs( directory )
            
        fileName = '%s_%s.rrd' % ( self.daemonName, dataPointName )
        filePath = zenPath( directory, fileName )
        step = rrdCreateCommand[rrdCreateCommand.index('--step')+1]
        if not os.path.exists( filePath ) or \
                self._hasStepTimeChanged( filePath, step ):
            import getpass
            self.log.debug( 'Creating RRD file %s as user %s with options %s' % 
                ( filePath, getpass.getuser(), rrdCreateCommand ) )
            rrdtool.create( filePath, *rrdCreateCommand )
        else:
            self.log.debug( 'RRD file already exists' )

    def _hasStepTimeChanged( self, filePath, step ):
        try:
            retVal = rrdtool.info( filePath )['step'] != int(step)
        except:
            retVal = True
        return retVal
    
    def write( self, dataPointName, value, timestamp='N' ):
        """
        Write timestamped values to the rrd file
        """
        value = str(value)
        timestamp = str(timestamp)
        fileName = zenPath( 'perf', 'Daemons', self.monitor, 
            '%s_%s' % ( self.daemonName, dataPointName + '.rrd' ) )
        try:
            self.log.debug( 'Writing to: %s, timestamp: %s, value:%s' % 
                ( fileName, timestamp, value ) )
            rrdtool.update( fileName, '%s:%s' % ( timestamp, value ) )
        except rrdtool.error, err:
            self.log.error( 'rrdtool reported error %s %s', err, fileName )
    
    def getCurrentTimeStamp( self, dataPointName ):
        """
        Return timestamp in rrd file for this moment
        """
        fileName = zenPath( 'perf', 'Daemons', self.monitor, 
            '%s_%s' % ( self.daemonName, dataPointName + '.rrd' ) )
        firstTime = rrdtool.first( fileName )
        timestamp = int((time.time() - firstTime) / self.cycleTime) * self.cycleTime + firstTime
        return timestamp
