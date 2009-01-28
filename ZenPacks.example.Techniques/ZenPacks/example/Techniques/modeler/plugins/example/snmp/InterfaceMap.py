import re
from Products.DataCollector.plugins.zenoss.snmp.InterfaceMap \
    import InterfaceMap as Base

class InterfaceMap(Base):
    def process(self, device, results, log):
        for ifidx, data in ifalias.items():
            if not iftable.has_key(ifidx): continue
            match =  re.search("Customer:[^\s]+", data.get('description'))
            if match:
                iftable[ifdx]['setCustomerInfo'] = match.groups()[0]
        return Base.process(self, device, results, log)
