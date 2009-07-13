from Products.ZenRRD.ComponentCommandParser import ComponentCommandParser
import re
#dladm show-link -s
#LINK            IPACKETS   RBYTES   IERRORS    OPACKETS     OBYTES       OERRORS
#e1000g0         54581      4371217  0          23929        4124567      0

class dladm(ComponentCommandParser):
    componentScanValue = 'id'
    componentSplit = '\n'
    componentScanner = '^(?P<component>\w+)'
    scanners = [
            '\w+\s+(?P<ifInUcastPackets>\d+)\s+(?P<ifInOctets>\d+)\s+(?P<ifInErrors>\d+)\s+(?P<ifOutUcastPackets>\d+)\s+(?P<ifOutOctets>\d+)\s+(?P<ifOutErrors>\d+)'
            ]
