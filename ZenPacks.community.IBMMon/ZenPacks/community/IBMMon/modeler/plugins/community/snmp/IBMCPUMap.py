################################################################################
#
# This program is part of the IBMMon Zenpack for Zenoss.
# Copyright (C) 2009 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""IBMCPUMap

IBMCPUMap maps the ibmSystemProcessor table to cpu objects

$Id: IBMCPUMap.py,v 1.0 2009/07/12 23:08:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class IBMCPUMap(SnmpPlugin):
    """Map IBM Director cpu table to model."""

    maptype = "IBMCPUMap"
    modname = "ZenPacks.community.IBMMon.IBMCPU"
    relname = "cpus"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('hrProcessorTable',
	            '.1.3.6.1.2.1.25.3.3.1',
		    {
		        '.1': '_cpuidx',
		    }
	),
        GetTableMap('cpuTable',
	            '.1.3.6.1.4.1.2.6.159.1.1.140.1.1',
		    {
                        '.1': 'id',
                        '.2': '_manuf',
                        '.3': '_family',
                        '.6': 'clockspeed',
		    }
	),
    )


    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        cputable = tabledata.get("cpuTable")
        if not cputable: return
        rm = self.relMap()
        for oid, cpu in cputable.iteritems():
            om = self.objectMap(cpu)
            model = self.families.get(getattr(om, '_family', 1), "Unknown")
            if not model.startswith(getattr(om, '_manuf')):
                model = "%s %s" %(getattr(om, '_manuf'), model)
            om.setProductKey = MultiArgs(model, getattr(om, '_manuf')) 
            om.socket = om.id[3:]
            om.id = self.prepId(om.id)
            om.cores = len(tabledata.get("hrProcessorTable")) / len(cputable)
            if om.cores == 0: om.cores = 1
            rm.append(om)
        return rm


    families = {1: "Other",
                2: "Unknown",
                3: "8086",
                4: "80286",
                5: "80386",
                6: "80486",
                7: "8087",
                8: "80287",
                9: "80387",
                10: "80487", 
                11: "Pentium(R) brand",
                12: "Pentium(R) Pro",
                13: "Pentium(R) II",
                14: "Pentium(R) processor with MMX(TM) technology",
                15: "Celeron(TM)",
                16: "Pentium(R) II Xeon(TM)",
                17: "Pentium(R) III",
                18: "M1 Family",
                19: "M2 Family", 
                24: "K5 Family",
                25: "K6 Family",
                26: "K6-2",
                27: "K6-3",
                28: "Athlon(TM) Processor",
                29: "Duron(TM) Processor",
                30: "AMD29000", 
                31: "K6-2+",
                32: "Power PC",
                33: "Power PC 601",
                34: "Power PC 603",
                35: "Power PC 603+",
                36: "Power PC 604",
                37: "Power PC 620",
                38: "Power PC X704",
                39: "Power PC 750", 
                48: "Alpha",
                49: "Alpha 21064",
                50: "Alpha 21066",
                51: "Alpha 21164",
                52: "Alpha 21164PC",
                53: "Alpha 21164a",
                54: "Alpha 21264",
                55: "Alpha 21364", 
                64: "MIPS",
                65: "MIPS R4000",
                66: "MIPS R4200",
                67: "MIPS R4400",
                68: "MIPS R4600",
                69: "MIPS R10000", 
                80: "SPARC",
                81: "SuperSPARC",
                82: "microSPARC II",
                83: "microSPARC IIep",
                84: "UltraSPARC",
                85: "UltraSPARC II",
                86: "UltraSPARC IIi",
                87: "UltraSPARC III",
                88: "UltraSPARC IIIi", 
                96: "68040",
                97: "68xxx",
                98: "68000",
                99: "68010",
                100: "68020",
                101: "68030", 
                112: "Hobbit",
                120: "Crusoe(TM) TM5000",
                121: "Crusoe(TM) TM3000",
                128: "Weitek",
                130: "Itanium(TM) Processor",
                131: "Athlon(TM) 64 Processor",
                132: "Opteron(TM) Processor", 
                144: "PA-RISC Family",
                145: "PA-RISC 8500",
                146: "PA-RISC 8000",
                147: "PA-RISC 7300LC",
                148: "PA-RISC 7200",
                149: "PA-RISC 7100LC",
                150: "PA-RISC 7100", 
                160: "V30 Family",
                176: "Pentium(R) III Xeon(TM)",
                177: "Pentium(R) III Processor with Intel(R) SpeedStep(TM) Technology", 
                178: "Pentium(R) 4",
                179: "Xeon(TM)", 
                180: "AS400 Family",
                181: "Xeon(TM) processor MP",
                182: "Athlon(TM) XP",
                183: "Athlon(TM) MP",
                184: "Itanium(R) 2",
                185: "Pentium(R) M processor", 
                190: "K7", 
                200: "S/390 and zSeries",
                201: "ESA/390 G4",
                202: "ESA/390 G5",
                203: "ESA/390 G6",
                204: "z/Architectur base", 
                250: "i860",
                251: "i960",
                260: "SH-3",
                261: "SH-4",
                280: "ARM",
                281: "StrongARM", 
                300: "6x86",
                301: "MediaGX",
                302: "MII",
                320: "WinChip",
                350: "DSP",
                500: "Video Processor",
                }

