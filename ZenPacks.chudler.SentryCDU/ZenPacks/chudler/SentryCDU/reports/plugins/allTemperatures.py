import Globals
from Products.ZenReports import Utilization
from Products.ZenModel.GraphPoint import GraphPoint
import os

class allTemperatures:
    cFunc = "AVERAGE"
    collector = None
    
    def run(self, dmd, args):
        # This allows us to easily use the common start/end/consolidation
        # parameters that you'd typically want for graphs.
        summary = Utilization.getSummaryArgs(dmd, args)
        
        self.cFunc = summary['function']
        # FIXME 16APR09:  will this work with distributed collectors?
        self.collector = dmd.Monitors.Performance.localhost
        
        # Setup basic graph properties.
        graph = [
            '-F', '-E',
            '--height=250', '--width=600', '--lower-limit=0',
            '--vertical-label=Temperature',
            '--start=%d' % (int(summary['start']),),
            '--end=%d' % (int(summary['end']),)
            ]
        
        # This is the workhorse method that goes and generates the real data in
        # the graph.
        graph.extend(self.getTemperatures( dmd.Devices.Power.SentryCDU.getSubDevices()))
        
        # Do some post-processing to get a proper URL for the graph image.
        graph = self.collector._fullPerformancePath(graph)
        url = self.collector.buildGraphUrlFromCommands(graph, summary['end'] - summary['start'])
        
        # This is done to prevent "None" from appearing in the legend.
        return url + "&comment=All CDU/PDU Temperature Sensors"
    
    def getTemperatures(self, cdus):
        graph = []
        
        dataCount = 0
        for cdu in cdus:

            # Creating a graph point so we can make use of the getColor method
            # to automatically rotate colors.
            gp = GraphPoint(cdu.id)
            gp.color = ""
            for sensor in cdu.sentrysensors():
                tempRrd = os.path.join(sensor.rrdPath(), 'temperature_temp' + '.rrd')
                if not tempRrd: continue
                name = cdu.id + '-' + sensor.id
                graph.append("DEF:temperature%d=%s:%s:%s" % (dataCount, tempRrd, "ds0", self.cFunc))
                graph.append("LINE1:temperature%d%s:%s" % (dataCount, gp.getColor(dataCount), name))
                dataCount += 1
        return graph
