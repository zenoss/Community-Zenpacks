######################################################################
#
# ZenPacks.TwoNMS.PrinterMIB PrinterMap modeler plugin
#
######################################################################

__doc__=""" PrinterMap

PrinterMib maps Printer Supplies on ZenPacks.TwoNMS.PrinterMIB.Printer objects

$Id: $"""

__version__ = '$Revision: $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap, GetMap
from Products.DataCollector.plugins.DataMaps import ObjectMap

class PrinterMap(SnmpPlugin):
    
    relname = "printermibsupply"
    modname = "ZenPacks.TwoNMS.PrinterMIB.PrinterSupply"

#    compname = ""
    
    # New classification stuff uses weight to help it determine what class a
    # device should be in. Higher weight pushes the device to towards the
    # class were this plugin is defined.
    weight = 15
    
    prtMarkerSupplies_columns = {
         #'.3': 'prtMarkerSuppliesColorantIndex', # snmp index
         '.5.1': 'PrtMarkerSuppliesTypeTC', # see cartType
         '.6.1': 'prtMarkerSuppliesDescription',  # "ex. "Black Toner Cartridge HP Q6000A""
         '.7.1': 'PrtMarkerSuppliesSupplyUnitTC', # see cartUnit
         '.8.1': 'prtMarkerSuppliesMaxCapacity',  # Max level
         '.9.1': 'prtMarkerSuppliesLevel', # current level
         }
    
    prtMarkerColorant_columns = {
        '.2.1': 'prtMarkerColorantIndex', #snmp index
        '.4.1': 'prtMarkerColorantValue', # color ex. "black"
        }

# RFC3805
    cartType = {
         '1': 'other',
         '2': 'unknown',
         '3': 'toner',
         '4': 'wasteToner',
         '5': 'ink',
         '6': 'inkCartridge',
         '7': 'inkRibbon',
         '8': 'wasteInk',
         '9': 'opc',
         '10': 'developer',
         '11': 'fuserOil',
         '12': 'solidWax',
         '13': 'ribbonWax',
         '14': 'wasteWax',
         '15': 'fuser',
         '16': 'coronaWire',
         '17': 'fuserOilWick',
         '18': 'cleanerUnit',
         '19': 'fuserCleaningPad',
         '20': 'transferUnit',
         '21': 'tonerCartridge',
         '22': 'fuserOiler',
         }
    
    cartUnit = {
         '1': 'other',
         '2': 'unknown',
         '3': 'tenThousandthsOfInches',
         '4': 'micrometers',
         '7': 'impressions',
         '8': 'sheets',
         '11': 'hours',
         '12': 'thousandthsOfOunces',
         '13': 'tenthsOfGrams',
         '14': 'hundrethsOfFluidOunces',
         '15': 'tenthsOfMilliliters',
         '16': 'feet',
         '17': 'meters',
         }
    
    snmpGetTableMaps = (
        GetTableMap('prtMarkerSupplies', '.1.3.6.1.2.1.43.11.1.1', prtMarkerSupplies_columns),
        GetTableMap('prtMarkerColorant', '.1.3.6.1.2.1.43.12.1.1', prtMarkerColorant_columns),
    )

    rgbColorCodes = {
        'other': 'CC0000',
        'unknown': 'CC0000',
        'white': 'FFFFFF',
        'red': 'CC3333',
        'green': '339933',
        'blue': '336699',
        'cyan': '00E6E6',
        'magenta': 'E600E6',
        'yellow': 'E6E600',
        'black': '000000',
    }
    
    def process(self, device, results, log):
        
        log.info('processing %s for device %s', self.name(), device.id)
        log.debug('-- RESULTS --')
        log.debug('results')
        
        getdata, tabledata = results

        # Uncomment next 2 lines for debugging when modeling
        #log.warn( "Get Data= %s", getdata )
        #log.warn( "Table Data= %s", tabledata )
        
        supplies = tabledata.get("prtMarkerSupplies")
        colors = tabledata.get("prtMarkerColorant")

        #log.info('-- SUPPLIES & INFO --')
        #log.info(supplies)
        #log.info(colors)

        # If no data returned then simply return
        if not supplies:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            return
        
        if not colors:
            log.warn( 'No SNMP response from %s for the %s plugin', device.id, self.name() )
            return
        
        rm = self.relMap()
        
        for oid,data in supplies.iteritems():
            omsupply = self.objectMap(data)
            omcolor = self.objectMap(colors[oid])
            omsupply.id = self.prepId(omcolor.prtMarkerColorantValue)
            omsupply.snmpindex = omcolor.prtMarkerColorantIndex
            omsupply.prtMarkerColorantValue = omcolor.prtMarkerColorantValue
            omsupply.prtMarkerColorantIndex = omcolor.prtMarkerColorantIndex

            try:
                omsupply.PrtMarkerSuppliesTypeTC = self.cartType[str(omsupply.PrtMarkerSuppliesTypeTC)]
                omsupply.PrtMarkerSuppliesSupplyUnitTC = self.cartUnit[str(omsupply.PrtMarkerSuppliesSupplyUnitTC)]
                omsupply.rgbColorCode = self.rgbColorCodes[omcolor.prtMarkerColorantValue]
            except KeyError:
                log.error("error occurred " )
                omsupply.rgbColorCode = self.rgbColorCodes['unknown']

            rm.append(omsupply)

        return rm

