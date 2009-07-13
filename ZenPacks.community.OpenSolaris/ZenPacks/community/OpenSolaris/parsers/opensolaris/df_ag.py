from Products.ZenRRD.CommandParser import CommandParser
import re
from pprint import pformat
import logging
from Products.ZenUtils.Utils import prepId as globalPrepId
log = logging.getLogger("zen.ComponentCommandParser")

#/                  (rpool/ROOT/opensolaris-1):   131072 block size #512 frag size\n20514816 total blocks    8146535 free blocks  8146535
#available        8327314 total files\n 8146535 free files     47775746
#filesys id\n     zfs fstype       0x00000004 flag             255 filename
#length\n\n/


def prepId(id, subchar='_'):
    """Return the global prep ID
    """
    # TODO: document what this means and why we care
    return globalPrepId(id, subchar)

class df_ag(CommandParser):
    componentScanValue = 'id'
    componentSplit = '\n\n'
    componentScanner = '^(?P<component>[\w\/]+)\s*'
    scanners = [
            '(?P<availBlocks>\d+) free blocks',
            '(?P<totalBlocks>\d+) total blocks',
            '(?P<availInodes>\d+) free files',
            '(?P<totalInodes>\d+) total files',
            ]

    def dataForParser(self, context, dp):
        return dict(componentScanValue = getattr(context, self.componentScanValue))

    def processResults(self, cmd, result):

        # Map datapoints by data you can find in the command output
        ifs = {}
        for dp in cmd.points:
            points = ifs.setdefault(dp.data['componentScanValue'], {})
            points[dp.id] = dp
        # split data into component blocks
        parts = cmd.result.output.split(self.componentSplit)

        for part in parts:
            # find the component match
            match = re.search(self.componentScanner, part)
            if not match: continue
            component = match.groupdict()['component'].strip()
            points = ifs.get(prepId(component), None)
            if not points: continue

            availBlocks=None
            totalBlocks=None
            usedBlocks=None
            availInodes=None
            totalInodes=None
            usedInodes=None
            percentInodesUsed=None

            # find any datapoints
            for search in self.scanners:
                match = re.search(search, part)
                if match:
                    for name, value in match.groupdict().items():
                        if name == 'availBlocks': availBlocks = long(value)/2
                        if name == 'totalBlocks': totalBlocks = long(value)/2
                        if name == 'availInodes': availInodes = long(value)
                        if name == 'totalInodes': totalInodes = long(value)
                        dp = points.get(name, None)
                        if dp is not None:
                            if value in ('-', ''): value = 0
                            result.values.append( (dp, float(value) ) )
                        if availBlocks and totalBlocks and not usedBlocks:
                            usedBlocks = totalBlocks - availBlocks
                            log.debug(totalBlocks)
                            log.debug(availBlocks)
                            log.debug(usedBlocks)
                            dp = points.get('usedBlocks', None)
                            if dp is not None:
                                if usedBlocks in ('-', ''): usedBlocks = 0
                                result.values.append( (dp, float(usedBlocks) ) )
                        if availInodes and totalInodes and not usedInodes:
                            usedInodes = totalInodes - availInodes
                            dp = points.get('usedInodes', None)
                            if dp is not None:
                                if usedInodes in ('-', ''): usedInodes = 0
                                result.values.append( (dp, float(usedInodes) ) )
                        if usedInodes and totalInodes and not percentInodesUsed:
                            percentInodesUsed = usedInodes/totalInodes * 100
                            dp = points.get('percentInodesUsed', None)
                            if dp is not None:
                                if percentInodesUsed in ('-', ''): percentInodesUsed = 0
                                result.values.append( (dp, float(percentInodesUsed) ) )
        log.debug(pformat(result))
        return result

