from Products.ZenRRD.ComponentCommandParser import ComponentCommandParser

class ifconfig(ComponentCommandParser):

    # Regex that will split the cmd output into its components
    # In this case eth entries are split by two carriage returns
    componentSplit = '\n\n'

    # Regex that will find for example eth0 at the begining 
    # of the component string created from the split above
    # and save it to the component variable
    componentScanner = '^(?P<component>[aA-zZ:0-9]+)'

    componentScanValue = 'interfaceName'

    # scanners that use regex's to pick out values in a string and save
    # them to a variable for example ifInUcastPackets is saved from
    # RX Packets:12352234
    scanners = [
        r'RX packets:(?P<ifInUcastPackets>\d+) +errors:(?P<ifInErrors>\d+) +',
        r'TX packets:(?P<ifOutUcastPackets>\d+) +errors:(?P<ifOutErrors>\d+) +',
        r'RX bytes:(?P<ifInOctets>\d+) +\(\d+\.\d+ \w+\) +TX bytes:(?P<ifOutOctets>\d+) +',
        ]

