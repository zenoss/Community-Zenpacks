/*
###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
*/

(function(){

var ZC = Ext.ns('Zenoss.component');

function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.MemoryModulePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'MemoryModule',
            autoExpandColumn: 'product',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'manufacturer'},
                {name: 'product'},
                {name: 'size'},
                {name: 'hasMonitor'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Slot')
            },{
                id: 'manufacturer',
                dataIndex: 'manufacturer',
                header: _t('Manufacturer'),
                renderer: render_link
            },{
                id: 'product',
                dataIndex: 'product',
                header: _t('Model'),
                renderer: render_link
            },{
                id: 'size',
                dataIndex: 'size',
                header: _t('Size'),
                renderer: Zenoss.render.bytesString,
                width: 70
            },{
                id: 'monitor',
                dataIndex: 'monitor',
                header: _t('Monitored'),
                renderer: Zenoss.render.monitor,
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.MemoryModulePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('MemoryModulePanel', ZC.MemoryModulePanel);
ZC.registerName('MemoryModule', _t('Memory Module'), _t('Memory Modules'));

ZC.LogicalDiskPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'LogicalDisk',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'description'},
                {name: 'diskType'},
                {name: 'stripesize'},
                {name: 'size'},
                {name: 'hasMonitor'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name')
            },{
                id: 'description',
                dataIndex: 'description',
                header: _t('OS Name')
            },{
                id: 'diskType',
                dataIndex: 'diskType',
                header: _t('Type')
            },{
                id: 'stripesize',
                dataIndex: 'stripesize',
                header: _t('Stripe Size'),
                renderer: Zenoss.render.bytesString,
                width: 70
            },{
                id: 'size',
                dataIndex: 'size',
                header: _t('Size'),
                renderer: Zenoss.render.bytesString,
                width: 70
            },{
                id: 'monitor',
                dataIndex: 'monitor',
                header: _t('Monitored'),
                renderer: Zenoss.render.monitor,
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.LogicalDiskPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('LogicalDiskPanel', ZC.LogicalDiskPanel);
ZC.registerName('LogicalDisk', _t('Logical Disk'), _t('Logical Disks'));

ZC.HardDiskPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'HardDisk',
            autoExpandColumn: 'product',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'bay'},
                {name: 'diskType'},
                {name: 'rpm'},
                {name: 'size'},
                {name: 'manufacturer'},
                {name: 'product'},
                {name: 'serialNumber'},
                {name: 'hasMonitor'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name')
            },{
                id: 'bay',
                dataIndex: 'bay',
                header: _t('Bay')
            },{
                id: 'manufacturer',
                dataIndex: 'manufacturer',
                header: _t('Manufacturer'),
                renderer: render_link
            },{
                id: 'product',
                dataIndex: 'product',
                header: _t('Model'),
                renderer: render_link
            },{
                id: 'diskType',
                dataIndex: 'diskType',
                header: _t('Type'),
                width: 70,
            },{
                id: 'rpm',
                dataIndex: 'rpm',
                header: _t('RPM'),
                width: 70,
            },{
                id: 'size',
                dataIndex: 'size',
                header: _t('Size'),
                renderer: Zenoss.render.bytesString,
            },{
                id: 'monitor',
                dataIndex: 'monitor',
                header: _t('Monitored'),
                renderer: Zenoss.render.monitor,
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.HardDiskPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('HardDiskPanel', ZC.HardDiskPanel);
ZC.registerName('HardDisk', _t('Hard Disk'), _t('Hard Disks'));

ZC.ExpansionCardPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'ExpansionCard',
            autoExpandColumn: 'product',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'slot'},
                {name: 'name'},
                {name: 'manufacturer'},
                {name: 'product'},
                {name: 'serialNumber'},
                {name: 'hasMonitor'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'slot',
                dataIndex: 'slot',
                header: _t('Slot')
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name')
            },{
                id: 'manufacturer',
                dataIndex: 'manufacturer',
                header: _t('Manufacturer'),
                renderer: render_link
            },{
                id: 'product',
                dataIndex: 'product',
                header: _t('Model'),
                renderer: render_link
            },{
                id: 'serialNumber',
                dataIndex: 'serialNumber',
                header: _t('Serial #')
            },{
                id: 'monitor',
                dataIndex: 'monitor',
                header: _t('Monitored'),
                renderer: Zenoss.render.monitor,
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.ExpansionCardPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('ExpansionCardPanel', ZC.ExpansionCardPanel);
ZC.registerName('ExpansionCard', _t('Expansion Card'), _t('Expansion Cards'));

ZC.FanPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'Fan',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'rpmString'},
                {name: 'hasMonitor'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name')
            },{
                id: 'rpmString',
                dataIndex: 'rpmString',
                header: _t('Speed')
            },{
                id: 'monitor',
                dataIndex: 'monitor',
                header: _t('Monitored'),
                renderer: Zenoss.render.monitor,
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.FanPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('FanPanel', ZC.FanPanel);
ZC.registerName('Fan', _t('Fan'), _t('Fans'));

ZC.TemperatureSensorPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'TemperatureSensor',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'tempString'},
                {name: 'hasMonitor'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name')
            },{
                id: 'tempString',
                dataIndex: 'tempString',
                header: _t('Temperature')
            },{
                id: 'monitor',
                dataIndex: 'monitor',
                header: _t('Monitored'),
                renderer: Zenoss.render.monitor,
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.TemperatureSensorPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('TemperatureSensorPanel', ZC.TemperatureSensorPanel);
ZC.registerName('TemperatureSensor', _t('Temperature Sensor'), _t('Temperature Sensors'));

ZC.PowerSupplyPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'PowerSupply',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'type'},
                {name: 'wattsString'},
                {name: 'millivoltsString'},
                {name: 'hasMonitor'},
                {name: 'monitor'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name')
            },{
                id: 'type',
                dataIndex: 'type',
                header: _t('Type')
            },{
                id: 'wattsString',
                dataIndex: 'wattsString',
                header: _t('Watts')
            },{
                id: 'millivoltsString',
                dataIndex: 'millivoltsString',
                header: _t('Voltage')
            },{
                id: 'monitor',
                dataIndex: 'monitor',
                header: _t('Monitored'),
                renderer: Zenoss.render.monitor,
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                width: 60
            }]
        });
        ZC.PowerSupplyPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('PowerSupplyPanel', ZC.PowerSupplyPanel);
ZC.registerName('PowerSupply', _t('Power Supply'), _t('Power Supplies'));

})();
