from Products.ZenRRD.CommandParser import CommandParser
import re
#dladm show-link -s
#SET minf mjf xcal  intr ithr  csw icsw migr smtx  srw syscl  usr sys  wt idl sze
#  0    9   0    0   329  102   88    0    3    1    0   229    4   0   0 96 2
#'foo': dict(ssCpuUser=12000,
#             ssCpuSystem=0.48,
#             ssCpuIdle=0.45,
#             ssCpuInterrupt=0.18)}
def average(list):
    total = 0.0
    for number in list:
        total += int(number)
    average = total/len(list)
    return average

class mpstat_a(CommandParser):

    def processResults(self, cmd, result):
        """
        Parse the results of the mpstat command to get sysUptime and load
        averages.
        """
        output = cmd.result.output.split('\n')[1:]
        dps = dict([(dp.id, dp) for dp in cmd.points])
        sscpuint=[]
        sscpuusr=[]
        sscpusys=[]
        sscpuidl=[]
        for line in output:
            if line.startswith('SET'): continue
            data=line.split()
            if len(data) >12:
                sscpuint.append(data[4])
                sscpuusr.append(data[12])
                sscpusys.append(data[13])
                sscpuidl.append(data[15])

        if len( sscpuint) == 1:
            result.values.append( (dps['ssCpuInterrupt'], int(sscpuint[0]) ) )
            result.values.append( (dps['ssCpuUser'],  int(sscpuusr[0]) ) )
            result.values.append( (dps['ssCpuSystem'],  int(sscpusys[0]) ) )
            result.values.append( (dps['ssCpuIdle'],  int(sscpuidl[0]) ) )
        else:
            # Skip the first value as it usually is erroneous to system averages
            sscpuint=sscpuint[1:]
            sscpuusr=sscpuusr[1:]
            sscpusys=sscpusys[1:]
            sscpuidl=sscpuidl[1:]
            result.values.append( (dps['ssCpuInterrupt'], average(sscpuint) ) )
            result.values.append( (dps['ssCpuUser'],  average(sscpuusr) ) )
            result.values.append( (dps['ssCpuSystem'],  average(sscpusys) ) )
            result.values.append( (dps['ssCpuIdle'],  average(sscpuidl) ) )

        return result
