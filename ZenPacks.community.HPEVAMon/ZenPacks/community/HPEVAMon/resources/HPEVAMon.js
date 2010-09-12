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

ZC.HPEVADiskDrivePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'HPEVADiskDrive',
            autoExpandColumn: 'product',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'enclosure'},
                {name: 'storagePool'},
                {name: 'bay'},
                {name: 'diskType'},
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
                header: _t('Name'),
                sortable: true
            },{
                id: 'enclosure',
                dataIndex: 'enclosure',
                header: _t('Enclosure'),
                sortable: true,
                renderer: Zenoss.render.default_uid_renderer
            },{
                id: 'bay',
                dataIndex: 'bay',
                header: _t('Bay'),
                sortable: true
            },{
                id: 'storagePool',
                dataIndex: 'storagePool',
                header: _t('Disk Group'),
                sortable: true,
                renderer: Zenoss.render.default_uid_renderer
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
                width: 160,
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
        ZC.HPEVADiskDrivePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('HPEVADiskDrivePanel', ZC.HPEVADiskDrivePanel);
ZC.registerName('HPEVADiskDrivePanel', _t('Hard Disk'), _t('Hard Disks'));

ZC.HPEVAFCPortPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'HPEVAFCPort',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'controller'},
                {name: 'wwn'},
                {name: 'networkAddresses'},
                {name: 'linkTechnology'},
                {name: 'type'},
                {name: 'speed'},
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
                id: 'controller',
                dataIndex: 'controller',
                header: _t('Controller'),
                sortable: true,
                renderer: Zenoss.render.default_uid_renderer
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Interface Name'),
                sortable: true
            },{
                id: 'wwn',
                dataIndex: 'wwn',
                header: _t('WWN'),
                sortable: true,
                width: 160,
            },{
                id: 'networkAddresses',
                dataIndex: 'networkAddresses',
                sortable: true,
                header: _t('Network'),
            },{
                id: 'linkTechnology',
                dataIndex: 'linkTechnology',
                header: _t('Link Technology'),
            },{
                id: 'type',
                dataIndex: 'type',
                header: _t('Type'),
            },{
                id: 'speed',
                dataIndex: 'speed',
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
        ZC.HPEVAFCPortPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('HPEVAFCPortPanel', ZC.HPEVAFCPortPanel);
ZC.registerName('HPEVAFCPortPanel', _t('FC Port'), _t('FC Ports'));

ZC.HPEVAStorageDiskEnclosurePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'HPEVAStorageDiskEnclosure',
            autoExpandColumn: 'product',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'manufacturer'},
                {name: 'product'},
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
                header: _t('ID'),
                width: 20,
                sortable: true
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
        ZC.HPEVAStorageDiskEnclosurePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('HPEVAStorageDiskEnclosurePanel', ZC.HPEVAStorageDiskEnclosurePanel);
ZC.registerName('HPEVAStorageDiskEnclosurePanel', _t('Storage Enclosure'), _t('Storage Enclosures'));

ZC.HPEVAStoragePoolPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'HPEVAStoragePool',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'totalDisks'},
                {name: 'diskGroupType'},
                {name: 'diskType'},
                {name: 'protLevel'},
                {name: 'totalBytesString'},
                {name: 'usedBytesString'},
                {name: 'availBytesString'},
                {name: 'capacity'},
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
                header: _t('Name'),
                sortable: true
            },{
                id: 'totalDisks',
                dataIndex: 'totalDisks',
                header: _t('Total Disks')
            },{
                id: 'diskGroupType',
                dataIndex: 'diskGroupType',
                header: _t('Disk Group Type')
            },{
                id: 'diskType',
                dataIndex: 'diskType',
                header: _t('Disk Type')
            },{
                id: 'protLevel',
                dataIndex: 'protLevel',
                header: _t('Protection Level')
            },{
                id: 'totalBytesString',
                dataIndex: 'totalBytesString',
                header: _t('Total bytes')
            },{
                id: 'usedBytesString',
                dataIndex: 'usedBytesString',
                header: _t('Used bytes')
            },{
                id: 'availBytesString',
                dataIndex: 'availBytesString',
                header: _t('Free bytes')
            },{
                id: 'capacity',
                dataIndex: 'capacity',
                header: _t('% Util')
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
        ZC.HPEVAStoragePoolPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('HPEVAStoragePoolPanel', ZC.HPEVAStoragePoolPanel);
ZC.registerName('HPEVAStoragePoolPanel', _t('Disk Group'), _t('Disk Groups'));

ZC.HPEVAStorageProcessorCardPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'HPEVAStorageProcessorCard',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'slot'},
                {name: 'manufacturer'},
                {name: 'product'},
                {name: 'serialNumber'},
                {name: 'uptime'},
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
                header: _t('Slot'),
                sortable: true
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
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
                header: _t('Serial #'),
                width: 120
            },{
                id: 'uptime',
                dataIndex: 'uptime',
                header: _t('Uptime'),
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
        ZC.HPEVAStorageProcessorCardPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('HPEVAStorageProcessorCardPanel', ZC.HPEVAStorageProcessorCardPanel);
ZC.registerName('HPEVAStorageProcessorCardPanel', _t('Controller'), _t('Controllers'));

ZC.HPEVAStorageVolumePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'HPEVAStorageVolume',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'storagePool'},
                {name: 'diskType'},
                {name: 'raidType'},
                {name: 'preferredPath'},
                {name: 'accessType'},
                {name: 'totalBytesString'},
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
                header: _t('Name'),
                sortable: true
            },{
                id: 'storagePool',
                dataIndex: 'storagePool',
                header: _t('Disk Group'),
                sortable: true,
                renderer: Zenoss.render.default_uid_renderer
            },{
                id: 'diskType',
                dataIndex: 'diskType',
                header: _t('Disk Type')
            },{
                id: 'raidType',
                dataIndex: 'raidType',
                header: _t('RAID Level')
            },{
                id: 'preferredPath',
                dataIndex: 'preferredPath',
                header: _t('Preferred Path')
            },{
                id: 'accessType',
                dataIndex: 'accessType',
                header: _t('Access')
            },{
                id: 'totalBytesString',
                dataIndex: 'totalBytesString',
                header: _t('Size')
            },{
                id: 'totalBytesString',
                dataIndex: 'totalBytesString',
                header: _t('Size')
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
        ZC.HPEVAStorageVolumePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('HPEVAStorageVolumePanel', ZC.HPEVAStorageVolumePanel);
ZC.registerName('HPEVAStorageVolumePanel', _t('Virtual Disk'), _t('Virtual Disks'));
})();
