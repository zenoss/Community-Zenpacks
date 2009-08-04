################################################################################
#
# This program is part of the deviceAdvDetail Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__= """StatusThreshold
Make threshold comparisons dynamic by using objects statusmap property,
rather than just number bounds checking.

$Id: HWStatus.py,v 1.3 2009/07/17 21:36:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

import rrdtool
from AccessControl import Permissions

from Globals import InitializeClass
from Products.ZenModel.ThresholdClass import ThresholdClass
from Products.ZenModel.ThresholdInstance import ThresholdInstance, ThresholdContext
from Products.ZenEvents import Event
from Products.ZenEvents.ZenEventClasses import Perf_Snmp
from Products.ZenUtils.ZenTales import talesEval, talesEvalStr
from Products.ZenEvents.Exceptions import pythonThresholdException, \
        rpnThresholdException

import logging
log = logging.getLogger('zen.StatusThreshold')

from Products.ZenUtils.Utils import unused
import types


class StatusThreshold(ThresholdClass):
    """
    Threshold class that can evaluate RPNs and Python expressions
    """

    escalateCount = 0

    _properties = ThresholdClass._properties + (
        {'id':'escalateCount', 'type':'int',     'mode':'w'},
        )

    factory_type_information = (
        { 
        'immediate_view' : 'editRRDStatusThreshold',
        'actions'        :
        ( 
        { 'id'            : 'edit'
          , 'name'          : 'Status Threshold'
          , 'action'        : 'editRRDStatusThreshold'
          , 'permissions'   : ( Permissions.view, )
          },
        )
        },
        )

    def createThresholdInstance(self, context):
        """Return the config used by the collector to process point
        thresholds. (id, escalateCount)
        """
        mmt = StatusThresholdInstance(self.id,
                                      ThresholdContext(context),
                                      self.dsnames,
                                      self.escalateCount,
                                      context.statusmap,)
        return mmt


InitializeClass(StatusThreshold)
StatusThresholdClass = StatusThreshold



class StatusThresholdInstance(ThresholdInstance):
    # Not strictly necessary, but helps when restoring instances from
    # pickle files that were not constructed with a count member.
    count = {}
    statusmap = ''

    def __init__(self, id, context, dpNames, escalateCount, statusmap):
        self.count = {}
        self._context = context
        self.id = id
        self.escalateCount = escalateCount
        self.dataPointNames = dpNames
        self._rrdInfoCache = {}
        self.statusmap = statusmap

    def name(self):
        "return the name of this threshold (from the ThresholdClass)"
        return self.id

    def context(self):
        "Return an identifying context (device, or device and component)"
        return self._context

    def dataPoints(self):
        "Returns the names of the datapoints used to compute the threshold"
        return self.dataPointNames

    def rrdInfoCache(self, dp):
        if dp in self._rrdInfoCache:
            return self._rrdInfoCache[dp]
        data = rrdtool.info(self.context().path(dp))
        # handle both old and new style RRD versions   
        try:
            # old style 1.2.x
            value = data['step'], data['ds']['ds0']['type']
        except KeyError: 
            # new style 1.3.x
            value = data['step'], data['ds[ds0].type']
        self._rrdInfoCache[dp] = value
        return value

    def countKey(self, dp):
        return(':'.join(self.context().key()) + ':' + dp)
        
    def getCount(self, dp):
        countKey = self.countKey(dp)
        if not self.count.has_key(countKey):
            return None
        return self.count[countKey]

    def incrementCount(self, dp):
        countKey = self.countKey(dp)
        if not self.count.has_key(countKey):
            self.resetCount(dp)
        self.count[countKey] += 1
        return self.count[countKey]

    def resetCount(self, dp):
        self.count[self.countKey(dp)] = 0
    
    def fetchLastValue(self, dp, cycleTime):
        """
        Fetch the most recent value for a data point from the RRD file.
        """
        startStop, names, values = rrdtool.fetch(self.context().path(dp),
            'AVERAGE', '-s', 'now-%d' % (cycleTime*2), '-e', 'now')
        values = [ v[0] for v in values if v[0] is not None ]
        if values: return values[-1]

    def check(self, dataPoint):
        """The given datapoints have been updated, so re-evaluate.
        returns events or an empty sequence"""
        unused(dataPoint)
        result = []
        for dp in self.dataPointNames:
            cycleTime, rrdType = self.rrdInfoCache(dp)
            result.extend(self.checkStatus(
                dp, self.fetchLastValue(dp, cycleTime)))
        return result

    def checkRaw(self, dataPoint, timeOf, value):
        """A new datapoint has been collected, use the given _raw_
        value to re-evalue the threshold."""
        unused(timeOf)
        result = []
        if value is None: return result
        try:
            cycleTime, rrdType = self.rrdInfoCache(dataPoint)
        except Exception:
            log.exception('Unable to read RRD file for %s' % dataPoint)
            return result
        if rrdType != 'GAUGE' and value is None:
            value = self.fetchLastValue(dataPoint, cycleTime)
        result.extend(self.checkStatus(dataPoint, value))
        return result

    def checkStatus(self, dp, value):
        'Check the value for point thresholds'
        log.debug("Checking %s %s in %s", dp, value, self.statusmap)
        if value is None:
            return []
        if type(value) in types.StringTypes:
            value = int(value)
        try:
            status = self.statusmap.get(value, None)
        except: return []
        if not status: return []
        msg = 'threshold of %s exceeded: current value %.2f' %(self.name(), value)
        return [dict(device=self.context().deviceName,
                    summary=msg,
                    eventKey=self.id,
                    eventClass='/Change/Set/Status',
                    component=self.context().componentName,
                    severity=status[1])]
        

    def getGraphElements(self, template, context, gopts, namespace, color,
                         legend, relatedGps):
        """Produce a visual indication on the graph of where the
        threshold applies."""
        unused(template, namespace)
        return gopts


    def getNames(self, relatedGps):
        legends = [ getattr(gp, 'legend', gp) for gp in relatedGps.values() ] 
        return ', '.join(legends) 

from twisted.spread import pb
pb.setUnjellyableForClass(StatusThresholdInstance, StatusThresholdInstance)
