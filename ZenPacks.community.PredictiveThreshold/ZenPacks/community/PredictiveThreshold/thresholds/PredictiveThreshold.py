__doc__= """PredictiveThreshold
"""

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
from Products.ZenModel.GraphDefinition import GraphDefinition
from ZenPacks.community.PredictiveThreshold.HoltData import ApplyHoltData
import logging
log = logging.getLogger('zen.PredictiveThreshold')

from Products.ZenUtils.Utils import unused
import types
import re

def rpneval(value, rpn):
    """
    Simulate RPN evaluation: only handles simple arithmetic
    """
    if value is None: return value
    operators = ('+','-','*','/')
    rpn = rpn.split(',')
    rpn.reverse()
    stack = [value]
    while rpn:
        next = rpn.pop()
        if next in operators:
            first = stack.pop()
            second = stack.pop()
            try:
                value = eval('%s %s %s' % (second, next, first))
            except ZeroDivisionError:
                value = 0
            stack.append(value)
        elif next.upper() == 'ABS':
            stack.append(abs(float(stack.pop())))
        else:
            stack.append(float(next))
    return stack[0]


class PredictiveThreshold(ThresholdClass):
    """
    Threshold class that can evaluate RPNs and Python expressions
    """

    eventClass = Perf_Snmp
    severity = 3
    escalateCount = 0

    # Holt Winters Parameters
    alpha = 0.1  # 0-1  , value closer to 1 means more recent observation carries more weight, baseling
    beta = 0.0035   # 0-1  , value closer to 1 means more recent observation carries more weight, linear trend
    gamma = 0.1  # 0-1  ,  value closer to 1 means more recent observation carries more weight, seasonal trend
    rows = 1440  # rows >=season, 5days, 300second_intervals * 1440 points
    season = 288  # 1day,  288points * 300second_intervals
    window = 6 # window length ..
    threshold = 3 # number of periods it has to fail in a window before alert sent ..
    delta = 2 # deviations

    predcolor = '#000000FF' # Prediction Line Color
    cbcolor = '#000080B2'  # Confidence Band Color
    tkcolor = '#ffffa0'  # Tick Color

    _properties = ThresholdClass._properties + (
        {'id':'pointval',        'type':'string',  'mode':'w'},
        {'id':'eventClass',    'type':'string',  'mode':'w'},
        {'id':'severity',      'type':'int',     'mode':'w'},
        {'id':'escalateCount', 'type':'int',     'mode':'w'},
        {'id':'alpha', 'type':'string',     'mode':'w'},
        {'id':'beta', 'type':'string',     'mode':'w'},
        {'id':'gamma', 'type':'string',     'mode':'w'},
        {'id':'rows', 'type':'string',     'mode':'w'},
        {'id':'season', 'type':'string',     'mode':'w'},
        {'id':'window', 'type':'string',     'mode':'w'},
        {'id':'threshold', 'type':'string',     'mode':'w'},
        {'id':'delta', 'type':'string',     'mode':'w'},
        {'id':'predcolor', 'type':'string',     'mode':'w'},
        {'id':'cbcolor', 'type':'string',     'mode':'w'},
        {'id':'tkcolor', 'type':'string',     'mode':'w'},
        )

    factory_type_information = (
        {
        'immediate_view' : 'editRRDPredictiveThreshold',
        'actions'        :
        (
        { 'id'            : 'edit'
          , 'name'          : 'Predictive Threshold'
          , 'action'        : 'editRRDPredictiveThreshold'
          , 'permissions'   : ( Permissions.view, )
          },
        )
        },
        )


# Update for 4 variables
    def createThresholdInstance(self, context):
        """Return the config used by the collector to process point
        thresholds. (id, pointval, severity, escalateCount)
        """
        pti = PredictiveThresholdInstance(self.id,
                                      ThresholdContext(context),
                                      self.dsnames,
                                      eventClass=self.eventClass,
                                      severity=self.severity,
                                      escalateCount=self.escalateCount,
                                      alpha=self.alpha,
                                      beta=self.beta,
                                      gamma=self.gamma,
                                      rows=self.rows,
                                      season=self.season,
                                      window=self.window,
                                      threshold=self.threshold,
                                      delta=self.delta,
                                      predcolor=self.predcolor,
                                      cbcolor=self.cbcolor,
                                      tkcolor=self.tkcolor
                                      )
        return pti

# End Update for 4 variables
    def zmanage_editProperties(self, REQUEST=None, redirect=False):
        """Edit a ZenModel object and return its proper page template
        """
        CreateCmdAppendStr = "\nRRA:HWPREDICT:%s:%s:%s:%s" % (\
                            self.rows,\
                            self.gamma,\
                            self.beta,\
                            self.season\
                            )
        collector = self.getDmdRoot('Monitors').Performance.localhost
        defaultCreateCmd = collector.getDefaultRRDCreateCommand()
        log.debug("DefaultCreateCmd is %s" % defaultCreateCmd)
        template = self.getPrimaryParent().getPrimaryParent()
        for dsname in self.dsnames:
            dsn, dpn = dsname.split('_', 1)
            dp = template.datasources._getOb(dsn).datapoints._getOb(dpn)
            if not re.search(CreateCmdAppendStr,dp.createCmd, re.I):
                if dp.createCmd:
                    dp.createCmd = dp.createCmd + CreateCmdAppendStr
                else:
                    dp.createCmd = defaultCreateCmd + CreateCmdAppendStr
            log.debug("Updating Create Cmd for %s to be %s" % (dp.name(), dp.createCmd))


#        'add some validation'
#        if REQUEST:
#            # rows >= season
##            rows = int(REQUEST.get('rows', ''))
#            season = int(REQUEST.get('season', ''))
#            if rows and season:
#                REQUEST.form['rows'] = rows
#                REQUEST.form['season'] = season
##                except ValueError:
#                    messaging.IMessageSender(self).sendToBrowser(
#                        'Invalid rows',
#                        "%s is an invalid OID." % oid,
#                        priority=messaging.WARNING
#                    )
#                    return self.callZenScreen(REQUEST)
#
        return ThresholdClass.zmanage_editProperties(self, REQUEST, redirect)

InitializeClass(PredictiveThreshold)
PredictiveThresholdClass = PredictiveThreshold

class PredictiveThresholdInstance(ThresholdInstance):
    # Not strictly necessary, but helps when restoring instances from
    # pickle files that were not constructed with a count member.
    count = {}

    def __init__(self, id, context, dpNames,
                  eventClass, severity, escalateCount,alpha,
                  beta,gamma,rows,season,window,threshold,delta,
                  predcolor,cbcolor,tkcolor
                  ):
        self.count = {}
        self._context = context
        self.id = id
        self.eventClass = eventClass
        self.severity = severity
        self.escalateCount = escalateCount
        self.dataPointNames = dpNames
        self._rrdInfoCache = {}
        self.alpha=alpha
        self.beta=beta
        self.gamma=gamma
        self.rows=rows
        self.season=season
        self.window=window
        self.threshold=threshold
        self.delta=delta
        self.predcolor=predcolor
        self.cbcolor=cbcolor
        self.tkcolor=tkcolor

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

    def TuneHoltData(self, dp):
        # Alpha
        rrdtool.tune(self.context().path(dp),'--alpha',str(self.alpha))

        # Beta
        rrdtool.tune(self.context().path(dp),'--beta',str(self.beta))

        # Gamma
        rrdtool.tune(self.context().path(dp),'--gamma',str(self.gamma))
        rrdtool.tune(self.context().path(dp),'--gamma-deviation',str(self.gamma))

        # Delta
        rrdtool.tune(self.context().path(dp),'--deltapos',str(self.delta))
        rrdtool.tune(self.context().path(dp),'--deltaneg',str(self.delta))


        # Check that these actually changed otherwise we will reset
        # violation counts to 0
        data = rrdtool.info(self.context().path(dp))
        rrasearch = re.compile('^rra\[(\d+)\]\.(\S+)')
        sorted_keys=data.keys()
        sorted_keys.sort()
        for key in sorted_keys:
            value=data[key]
            rra_match=rrasearch.search(key)
            if rra_match:
                rranum,rraprop=rra_match.groups()

                # Failure Threshold
                if rraprop == 'failure_threshold' and value != self.threshold:
                    rrdtool.tune(self.context().path(dp),'--failure-threshold',str(self.threshold))

                # Window Length
                if rraprop == 'window_length' and value != self.window:
                    rrdtool.tune(self.context().path(dp),'--window-length',str(self.window))
        #[--deltapos scale-value] # confidence band used internally
        #[--deltaneg scale-value]   # confidence band used internally 
        #[--failure-threshold failure-threshold]  # number of failures in a window 
        #[--window-length window-length]   # < 28 
        #[--alpha adaption-parameter] 0-1
        #[--beta adaption-parameter]  0-1
        #[--gamma adaption-parameter] 0-1
        #[--gamma-deviation adaption-parameter]  0-1
        #[--smoothing-window fraction-of-season]          0-1
        #[--smoothing-window-deviation fraction-of-season] 0-1

    def fetchLastValue(self, dp, cycleTime):
        """
        Fetch the most recent value for a data point from the RRD file.
        """
        startStop, names, values = rrdtool.fetch(self.context().path(dp),
            'AVERAGE', '-s', 'now-%d' % (cycleTime*2), '-e', 'now')
        values = [ v[0] for v in values if v[0] is not None ]
        if values: return values[-1]

    def fetchLastFailureValue(self, dp, cycleTime):
        """
        Fetch the most recent value for Failures from the RRD file.
        """
        # Convert the rrd to a Holt-Winters if it hasn't already been done
        ApplyHoltData(self.context().path(dp))

        # Retune the dp rrd file
        try:
            self.TuneHoltData(dp)
        except:
            pass

        startStop, names, values = rrdtool.fetch(self.context().path(dp),
            'FAILURES', '-s', 'now-%d' % (cycleTime*2), '-e', 'now')
        values = [ v[0] for v in values if v[0] is not None ]
        if values: return values[-1]

    def check(self, dataPoints):
        """The given datapoints have been updated, so re-evaluate.
        returns events or an empty sequence"""
        unused(dataPoints)
        result = []
        for dp in self.dataPointNames:
            cycleTime, rrdType = self.rrdInfoCache(dp)
            result.extend(self.checkPredictive(
                dp, self.fetchLastFailureValue(dp, cycleTime)))
        return result

    def checkRaw(self, dataPoint, timeOf, value):
        """A new datapoint has been collected, use the given _raw_
        value to re-evalue the threshold. Really this is the same as check"""

        unused(timeOf)
        unused(value)
        result = []
        try:
            cycleTime, rrdType = self.rrdInfoCache(dataPoint)
        except Exception:
            log.exception('Unable to read RRD file for %s' % dataPoint)
            return result
        result.extend(self.checkPredictive( dataPoint,
            self.fetchLastFailureValue(dataPoint, cycleTime)))
        return result
        #if value is None: return result
        #try:
        #    cycleTime, rrdType = self.rrdInfoCache(dataPoint)
        #except Exception:
        #    log.exception('Unable to read RRD file for %s' % dataPoint)
        #    return result
        #if rrdType != 'GAUGE' and value is None:
        #    value = self.fetchLastFailureValue(dataPoint, cycleTime)
        ##result.extend(self.checkPredictive(dataPoint, value))
        #result.extend(self.checkPredictive(dataPoint,
        #    self.fetchLastFailureValue(dataPoint, cycleTime)))
        #return result


    # Extend to support out of band calculations and throwning a warning
    def checkPredictive(self, dp, value):
        'Check the value for predictive thresholds'

        log.debug("Checking Predictive Threshold %s %s", dp, value)
        if value is None:
            return []
        if type(value) in types.StringTypes:
            value = float(value)
        thresh = None
        if value == 1:
            thresh = 1
            how = 'triggered'
        if thresh is not None:
            severity = self.severity
            count = self.incrementCount(dp)
            if self.escalateCount and count >= self.escalateCount:
                severity = min(severity + 1, 5)
            summary = 'Predictive Threshold of %s %s' % ( self.name(), how )
            log.debug(summary)
            return [dict(device=self.context().deviceName,
                         summary=summary,
                         eventKey=self.id,
                         eventClass=self.eventClass,
                         component=self.context().componentName,
                         severity=severity)]
        else:
            count = self.getCount(dp)
            if count is None or count > 0:
                summary = 'Predictive Threshold of %s restored' % ( self.name())
                self.resetCount(dp)
                log.debug(summary)
                return [dict(device=self.context().deviceName,
                             summary=summary,
                             eventKey=self.id,
                             eventClass=self.eventClass,
                             component=self.context().componentName,
                             severity=Event.Clear)]
        return []


    def raiseRPNExc( self ):
        """
        Raise an RPN exception, taking care to log all details.
        """
        msg= "The following RPN exception is from user-supplied code."
        log.exception( msg )
        raise rpnThresholdException(msg)

    # Add Graph Elements for Confidence Bands and Prediction
    def getGraphElements(self, template, context, gopts, namespace, color,
                         legend, relatedGps):
        """Produce a visual indication on the graph of where the
        threshold applies."""
        unused(template, namespace)

        if not color.startswith('#'):
            color = '#%s' % color
        if not self.dataPointNames:
            return gopts
        gp = relatedGps[self.dataPointNames[0]]

        # Attempt any RPN expressions
        rpn = getattr(gp, 'rpn', None)
        if rpn:
            try:
                rpn = talesEvalStr(rpn, context)
            except:
                self.raiseRPNExc()
                return gopts

        result = []
        for dp in self.dataPointNames:
            # Convert the rrd to a Holt-Winters if it hasn't already been done
            ApplyHoltData(self.context().path(dp))

            # Retune the dp rrd file
            try:
                self.TuneHoltData(dp)
            except:
                pass

            result += [ "DEF:%sa=%s:ds0:AVERAGE" % (dp, self.context().path(dp)) ]
            result += [ "DEF:%sb=%s:ds0:HWPREDICT" % (dp, self.context().path(dp)) ]
            result += [ "DEF:%sc=%s:ds0:DEVPREDICT" % (dp, self.context().path(dp)) ]
            result += [ "DEF:%sd=%s:ds0:FAILURES" % (dp, self.context().path(dp)) ]
            result += [ "CDEF:%scdefc=%sb,%sc,%s,*,+" % (dp,dp,dp,self.delta) ]
            result += [ "CDEF:%scdefd=%sb,%sc,%s,*,-" % (dp,dp,dp,self.delta) ]
            result += [ "TICK:%sd%s:1.0:%s Failures\j" %
                    (dp,self.tkcolor,legend) ]
            result += [ "LINE3:%sb%s:%s HwPredict\j" %
                    (dp,self.predcolor,legend) ]
            result += [ "LINE2:%scdefc%s:%s Confidence Band\j" %
                    (dp,self.cbcolor,legend) ] # Upper confidence Band
            result += [ "LINE2:%scdefd%s:" % (dp,self.cbcolor) ] # Lower confidence band
            result += [ "LINE1:%sd#000000FF:" % dp ]
        return gopts + result

    def getNames(self, relatedGps):
        legends = [ getattr(gp, 'legend', gp) for gp in relatedGps.values() ]
        return ', '.join(legends)

    def setPower(self, number):
        powers = ("k", "M", "G")
        if number < 1000: return number
        for power in powers:
            number = number / 1000.0
            if number < 1000:
                return "%0.2f%s" % (number, power)
        return "%.2f%s" % (number, powers[-1])

from twisted.spread import pb
pb.setUnjellyableForClass(PredictiveThresholdInstance, PredictiveThresholdInstance)
