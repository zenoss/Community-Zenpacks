from Products.ZenRRD.ComponentCommandParser import ComponentCommandParser
import re
from pprint import pformat
import logging
from Products.ZenUtils.Utils import prepId as globalPrepId

log = logging.getLogger("zen.ComponentCommandParser")

class puppetlast(ComponentCommandParser):
    componentSplit = '\n'
    componentScanner = '^(?P<component>\S+)'
    componentScanValue = 'id'
    scanners = [
	r'^\S+ checked in (?P<pcLastUpdateTime>[0-9]+) minutes ago',
	r'^\S+ cached expired, checked in (?P<pcLastUpdateTime>[0-9]+) minutes ago',
    ]

#    def dataForParser(self, context, dp):
#        return dict(componentScanValue = getattr(context, self.componentScanValue))
#
#    def processResults(self, cmd, result):
#
#        # Map datapoints by data you can find in the command output
#        ifs = {}
#        for dp in cmd.points:
#            points = ifs.setdefault(dp.data['componentScanValue'], {})
#            points[dp.id] = dp
#
#        # split data into component blocks
#        parts = cmd.result.output.split(self.componentSplit)
#
#        for part in parts:
#            # find the component match
#            match = re.search(self.componentScanner, part)
#            if not match: continue
#            component = match.groupdict()['component'].strip()
#            if self.componentScanValue == 'id': component = self.prepId(component)
#            points = ifs.get(component, None)
#            if not points: continue
#
#            # find any datapoints
#            for search in self.scanners:
#                match = re.search(search, part)
#                if match:
#                    for name, value in match.groupdict().items():
#                        dp = points.get(name, None)
#                        if dp is not None:
#                            if value in ('-', ''): value = 0
#                            result.values.append( (dp, value ) )
#			    #log.debug('value='+value+' float(value)='+float(value))
#
#	log.debug('Finished with result set')
#        log.debug(pformat(result))
#        return result

