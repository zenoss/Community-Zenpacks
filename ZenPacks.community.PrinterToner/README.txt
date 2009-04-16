PrinterToner Zenpack
--------------------

This Zenpack consists of a modeller which will model printers, using SNMP, 
and determine their toner cartridges.  The modeller then passes these
values back to Zenoss.  


Printers that have been tested are HP, Brother, Canon and Xerox.  The results
vary and there is 100% support for HP and Brother printers and only 80%
success on cannon and xerox printers.

You will need to associate the community.snmp.PrinterTonerMap with the
/Printers/Laser zCollectorPlugins


A new tab is added to the Device details for printers - called Printer Toner.
Under this new tab, the detail per cartridge can be obtained.
Perf data is calculated as a percentage and alerts can be set of these values.

