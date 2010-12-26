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

ZC.CiscoExpansionCardPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CiscoExpansionCard',
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
        ZC.CiscoExpansionCardPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CiscoExpansionCardPanel', ZC.CiscoExpansionCardPanel);
ZC.registerName('CiscoExpansionCard', _t('Expansion Card'), _t('Expansion Cards'));

ZC.CiscoFanPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CiscoFan',
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
        ZC.CiscoFanPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CiscoFanPanel', ZC.CiscoFanPanel);
ZC.registerName('CiscoFan', _t('Fan'), _t('Fans'));

ZC.CiscoTemperatureSensorPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CiscoTemperatureSensor',
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
        ZC.CiscoTemperatureSensorPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CiscoTemperatureSensorPanel', ZC.CiscoTemperatureSensorPanel);
ZC.registerName('CiscoTemperatureSensor', _t('Temperature Sensor'), _t('Temperature Sensors'));

ZC.CiscoPowerSupplyPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'CiscoPowerSupply',
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
        ZC.CiscoPowerSupplyPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('CiscoPowerSupplyPanel', ZC.CiscoPowerSupplyPanel);
ZC.registerName('CiscoPowerSupply', _t('Power Supply'), _t('Power Supplies'));

})();
