import Globals
import re
from Products.ZenReports import Utils, Utilization
from Products.ZenReports.AliasPlugin import AliasPlugin, Column, \
                                            PythonColumnHandler, \
                                            RRDColumnHandler

class PrinterMIBInventory( AliasPlugin ):
    """The PrinterMIB Inventory report"""

    def getComponentPath(self):
        return 'printermibsupply'
    
    def _getComponents(self, device, componentPath):
        components=[]
        try:
             for i in device.printermibsupply():
                 #if not i.monitored(): continue
                 #if i.snmpIgnore(): continue
                 components.append(i)
        except AttributeError: 
             pass
        return components
    
    def getColumns(self):
        return [
                Column('deviceName', PythonColumnHandler( 'device.titleOrId()' )),
                Column('color', PythonColumnHandler( 'component.name()' )),
                Column('description', PythonColumnHandler('component.prtMarkerSuppliesDescription')),
                Column('type', PythonColumnHandler('component.PrtMarkerSuppliesTypeTC')),
                Column('maxinkusage', PythonColumnHandler('component.prtMarkerSuppliesMaxCapacity')),
                Column('currinkusage', PythonColumnHandler('component.prtMarkerSuppliesLevel')),
                ]

    def getCompositeColumns(self):
        return [
                Column('inkused', PythonColumnHandler('(currinkusage * 100) / maxinkusage')),
               ]
