#!/usr/bin/env python

import rrdtool
import re
import shutil
import getopt
import sys
import os

def RemoveHoltData(filename = None):
    if not filename:
        return

    # Assign names for files
    old_rrd = filename
    old_rrd_renamed=old_rrd + ".old"
    new_rrd=old_rrd

    # Regexs to be used later
    dssearch = re.compile('^ds\[(\S+)\]\.type')
    rrasearch = re.compile('^rra\[(\d+)\]\.(\S+)')
    datasearch = re.compile('(AVERAGE|MIN|MAX|LAST)')
    holtsearch = re.compile('(HWPREDICT|SEASONAL|DEVSEASONAL|DEVPREDICT|FAILURES)')
    ds_type_search = re.compile('(GAUGE|COUNTER|DERIVE|ABSOLUTE)')

    datasources=[]
    data_rras=[]
    holt_rra={}
    rra=[]

    try:
        data = rrdtool.info(old_rrd)
    except:
        return

    start = rrdtool.first(old_rrd)
    step = data['step']

    HOLTWINTERS = holtsearch.search(str(data))
    if not HOLTWINTERS:
        print "Holt Winters Data Not found.  Skipping...."
        return

    # Move the old file out of the way
    shutil.move(old_rrd,old_rrd_renamed)
    sorted_keys=data.keys()
    sorted_keys.sort()
    for key in sorted_keys:
        value=data[key]
        name_match = dssearch.search(key)
        if name_match:
            name=name_match.groups()[0]
            datasources.append(name)
        else:
            rra_match=rrasearch.search(key)
            if rra_match:
                rranum,rraprop=rra_match.groups()
                if rraprop == 'cf':
                    data_match = datasearch.search(value)
                    if data_match:
                        data_rras.append(rranum)
                    else:
                        holt_match = holtsearch.search(value)
                        if holt_match:
                            holt_rra[value]=rranum


    for key in datasources:
        type_str = "ds[%s].type" % key
        min_str = "ds[%s].min" % key
        max_str = "ds[%s].max" % key
        minimal_heartbeat_str = "ds[%s].minimal_heartbeat" % key
        type = data[type_str]
        type_match=ds_type_search.search(type)
        if type_match:
            min_str = "ds[%s].min" % key
            min = data[min_str]
            if not min:
                min = 'U'

            max_str = "ds[%s].max" % key
            max = data[max_str]
            if not max:
                max = 'U'

            minimal_heartbeat_str = "ds[%s].minimal_heartbeat" % key
            minimal_heartbeat = data[minimal_heartbeat_str]
            args = "%s:%s:%s" % (minimal_heartbeat,min,max)
        elif type == 'COMPUTE':
            cdef_str = "ds[%s].cdef" % key
            args = cdef_str
        else:
            continue

        ds_string='DS:%s:%s:%s' % (key,type,args)

    for key in data_rras:
        cf_string = "rra[%s].cf" % key
        xff_string = "rra[%s].xff" % key
        pdp_per_row_string = "rra[%s].pdp_per_row" % key
        rows_string = "rra[%s].rows" % key
        rra.append('RRA:%s:%s:%s:%s' % (data[cf_string], data[xff_string], \
            data[pdp_per_row_string], data[rows_string]))

    # New Basic holt winters setup .. based on assumption we will tune
    # parameters later
    #rra.append('RRA:HWPREDICT:1440:0.1:0.0035:288')

    args=['foo.rrd','--start',str(start),'--step',str(step),' '.join(datasources),\
        ' '.join(rra)]

    rra_string=', '.join(rra)
    rrdtool.create(new_rrd,
        "--start",  str(start),
        "--step",  str(step),
        ds_string,
        *rra_string.split()
    )


    # Copy the data into the new file
    startStop, names, values = rrdtool.fetch(old_rrd_renamed,'AVERAGE','--start',str(start))
    #print startStop[0]
    time=start
    #print step, time
    for value in values:
        time += step
        if value[0]:
            data_fmt = "%s:%s" % (time, value[0])
            print data_fmt
            rrdtool.update(new_rrd, data_fmt )
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "n:")
    for file in args:
        if os.path.exists(file) and os.path.isfile(file):
            print "Removing Holt Winters Data from %s" % str(file)
            RemoveHoltData(file)
