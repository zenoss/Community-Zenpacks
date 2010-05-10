import re
from datetime import date, datetime, time

from Products.ZenUtils.Utils import prepId
from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

#parse '11/8/09 9:17 PM'
def parse_date(odt):
    "Parse the date and convert to YYYY/MM/DD HH:MM:SS"
    #nuts, Python 2.5 only, bring back for Zenoss 3.0
    #dt = datetime.strptime(odt, "%m/%d/%y %I:%M %p")
    #get the date
    mm, dd, yy = odt.split()[0].split('/')
    #if the year is 0-40, assume post-2000
    if int(yy) < 40:
        yy = '20'+yy
    else:
        yy = '19'+yy
    odate = date(int(yy), int(mm), int(dd))
    #get the time
    odtime = odt.split(None, 1)[1]
    otstr, pm = odtime.split()
    hh, mm = otstr.split(':')
    if (hh == '12'):
        hh = '0'
    if pm == 'PM':
        hh = int(hh)+12
    otime = time(int(hh), int(mm))
    dt = datetime.combine(odate, otime)
    moddate = dt.strftime("%Y/%m/%d %H:%M")
    return moddate

#parse '4.1, Copyright Apple Inc. 2002-2007'
def parse_manufacturer(info):
    "Parse the info and pull out the manufacturer"
    #strip out all permutations of "all rights reserved" and the last character
    info = re.sub('(?i)all rights reserved+', '', info).strip()
    info = re.sub('(?i)incorporated|(?i)inc.', '', info).strip()
    info = re.sub('(?i), ltd', '', info).strip()
    info = re.sub('(?i) s\.a\.', '', info).strip()
    #remove copyright dates
    info = re.sub('\d{4}-\d{4}|\d{4} - \d{4}|\d{4}', '', info).strip()
    manufacturer = 'Unknown'
    #check for standard entries
    if re.search('Apple', info):
        return 'Apple'
    elif re.search('Microsoft', info):
        return 'Microsoft'
    elif re.search('Hewlett-Packard', info):
        return 'HP'
    elif re.search('Firefox|Thunderbird', info):
        return 'Mozilla'
    elif re.search('Python Software Foundation', info):
        return 'Python'
    #check for copyright dates
    elif re.search('\(c\)', info):
        manufacturer = info.split('(c)')[1].strip()
    elif re.search('\(C\)', info):
        manufacturer = info.split('(C)')[1].strip()
    elif re.search('Copyright', info):
        manufacturer = info.split('Copyright')[1].strip()
    manufacturer = re.sub('\.$', '', manufacturer).strip()
    manufacturer = re.sub('\.$', '', manufacturer).strip() #twice is intentional
    manufacturer = re.sub(',', '', manufacturer).strip()
    manufacturer = manufacturer.title()
    #if manufacturer != 'Unknown': print manufacturer #debug line for matches
    return manufacturer

class software(CommandPlugin):
    """
    system_profiler SPApplicationsDataType | sed '/Kind:/d' | sed '/64-Bit (Intel):/d' | sed '/^$/d' | sed 's/\©/\(c\)/g'
    """

    command = "system_profiler SPApplicationsDataType | sed '/Kind:/d' | sed '/64-Bit (Intel):/d' | sed '/^$/d' | sed 's/\©/\(c\)/g'"
    compname = "os"
    relname = "software"
    modname = "Products.ZenModel.Software"

    #  Applications:
    #     Address Book:
    #       Version: 4.1.2
    #       Last Modified: 11/8/09 9:17 PM
    #       Kind: Universal
    #       Get Info String: 4.1, Copyright Apple Inc. 2002-2007
    #       Location: /Applications/Address Book.app
    #     Adium:
    #       Version: 1.3.8
    #       Last Modified: 11/8/09 9:00 PM
    #       Kind: Universal
    #       Get Info String: 1.3.8, Copyright 2001-2009 The Adium Team
    #       Location: /Applications/Adium.app

    def process(self, device, results, log):
        log.info('Collecting Software Installed for device %s' % device.id)
        rm = self.relMap()

        #split on "Location" to get discrete packages
        for package in results.split('Location:'):
            om = self.objectMap()
            lines = package.split('\n')
            version = manufacturer = ''
            #second line is the software package
            om.id = prepId(lines[1].split(':')[0].strip())
            for line in package.split('\n'):
                key = value = ''
                if re.search(':', line):
                    key, value = line.split(':',1)
                    key = key.strip()
                if key == "Version":
                    version = value.strip()
                #the assumption is made that Modified Date is an appropriate
                #equivalent to Install date
                if key == "Last Modified":
                    om.setInstallDate = parse_date(value.strip())
                if key == "Get Info String":
                    manufacturer = parse_manufacturer(value.strip())
            if not manufacturer:
                manufacturer = "Unknown"
            om.setProductKey = MultiArgs(om.id,manufacturer)
            if om.id:
                rm.append(om)

        log.debug(rm)
        return rm



