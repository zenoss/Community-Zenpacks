import Globals
from Products.ZenReports import Utilization
from Products.ZenModel.GraphPoint import GraphPoint
import os

class clusterRequests:
    cFunc = "AVERAGE"
    collector = None
    
    def run(self, dmd, args):
        # This allows us to easily use the common start/end/consolidation
        # parameters that you'd typically want for graphs.
        summary = Utilization.getSummaryArgs(dmd, args)
        
        self.cFunc = summary['function']
        self.collector = dmd.Monitors.Performance.localhost
        
        # Setup basic graph properties.
        graph = [
            '-F', '-E',
            '--height=250', '--width=600', '--lower-limit=0',
            '--vertical-label=requests/s',
            '--start=%d' % (int(summary['start']),),
            '--end=%d' % (int(summary['end']),),
            "COMMENT:\\s",
            "COMMENT:     Current",
            "COMMENT:     Average",
            "COMMENT:     Maximum\\l",
            ]
        
        # This is the workhorse method that goes and generates the real data in
        # the graph.
        graph.extend(self.getClusterRequests(
            dmd.Devices.Server.Linux.Web.children()))
        
        # Do some post-processing to get a proper URL for the graph image.
        graph = self.collector._fullPerformancePath(graph)
        url = self.collector.buildGraphUrlFromCommands(graph,
            summary['end'] - summary['start'])
        
        # This is done to prevent "None" from appearing in the legend.
        return url + "&comment="
        
    
    def getClusterRequests(self, clusters):
        dpname = "requestsPerSecond_requestsPerSecond"
        graph = []
        
        cluster_cdefs = []
        for i, cluster in enumerate(clusters):
            
            # Creating a graph point so we can make use of the getColor method
            # to automatically rotate colors.
            gp = GraphPoint(cluster.id)
            gp.color = ""
            
            # Pull in all of the individual RRD files for each device within
            # the collector.
            count = 0
            for device in cluster.getSubDevices():
                dp = device.primaryAq().getRRDDataPoint(dpname)
                if not dp: continue
                
                rrdFile = os.path.join(device.rrdPath(), dpname + '.rrd')
                graph.append("DEF:rps%d_%d=%s:%s:%s" % (
                    i, count, rrdFile, "ds0", self.cFunc))
                count += 1
            
            # Do the aggregation.
            if count > 0:
                cdef = "CDEF:rps%d_total=%s" % (i, ','.join(
                    [ "rps%d_%d" % (i, n) for n in range(count) ]))
                if count > 1:
                    cdef += "," + ','.join([ 'ADDNAN' for n in range(count-1)])
                
                graph.append(cdef)
                graph.append("GPRINT:rps%d_total:LAST:      %%5.2lf%%s" % i)
                graph.append("GPRINT:rps%d_total:AVERAGE:      %%5.2lf%%s" % i)
                graph.append("GPRINT:rps%d_total:MAX:      %%5.2lf%%s" % i)
                graph.append("AREA:rps%d_total%s:%s\\l:STACK" % (
                    i, gp.getColor(i), cluster.id))
                
                cluster_cdefs.append("rps%d_total" % i)
            
        # Do an additional summarization of all of the clusters.
        if cluster_cdefs:
            cdef = "CDEF:rps_total=%s" % (','.join(cluster_cdefs))
            if len(cluster_cdefs) > 1:
                cdef += "," + ",".join(
                    [ 'ADDNAN' for n in range(len(cluster_cdefs)-1) ])
            
            graph.append("COMMENT:\\s")
            graph.append(cdef)
            graph.append("GPRINT:rps_total:LAST:      %5.2lf%s")
            graph.append("GPRINT:rps_total:AVERAGE:      %5.2lf%s")
            graph.append("GPRINT:rps_total:MAX:      %5.2lf%s")
            graph.append("LINE2:rps_total#333333:Total\\l")
        
        return graph
