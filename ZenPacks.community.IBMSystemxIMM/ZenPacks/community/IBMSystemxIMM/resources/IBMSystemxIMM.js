(function(){

var ZC = Ext.ns('Zenoss.component');

function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.IMMFwVpdPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'IMMFwVpd',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'immVpdIndex'},
                {name: 'immVpdType'},
                {name: 'immVpdVersionString'},
                {name: 'immVpdReleaseDate'},
            ],
            /* These are the columns that will appear in the 3.0-style Component details panel (i.e. ComponentGridPanel)
               Note: there seems to be a requirement for a column with id: 'name'; the table will not display without it.  Must be a key of some kind.
               Still, seems odd, since we don't have to actually DISPLAY the data in that variable (dataIndex can point to something else, that is).
            */
            // Column designated here will take up remaining field width in the table.  Appears to be 'name' by default.
            // Making the last column in the table the autoexpand essentially left-justifies the columns, seems to be a good practice.
            autoExpandColumn: 'immVpdReleaseDate',
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'immVpdIndex',
                dataIndex: 'immVpdIndex',
                header: _t('ID'),
                sortable: true,
                width: 50
            },{
//              id: 'immVpdType',
                id: 'name',
                dataIndex: 'immVpdType',
                header: _t('Firmware Type'),
                sortable: true,
            },{
                id: 'immVpdVersionString',
                dataIndex: 'immVpdVersionString',
                header: _t('Version'),
                sortable: true,
            },{
                id: 'immVpdReleaseDate',
                dataIndex: 'immVpdReleaseDate',
                header: _t('Release Date'),
                sortable: true,
//          },{
//              id: 'renderTest1',
//              dataIndex: 'immVpdType',
//              header: _t('Render function test 1'),
//              sortable: true,
//              width: 200,
//              // Most basic example of renderer...
//              renderer: function(arbitraryVarName) {
//                  return "Embed a value like: " + arbitraryVarName + " in a fmt string";
//              },  
//          },{
//              id: 'renderTest2',
//              dataIndex: 'immVpdType',
//              header: _t('Render function test 2'),
//              sortable: true,
//              width: 200,
//              // Renderer with a conditional...
//              renderer: function(immVpdType) {
//					if (immVpdType=='IMM') {
////                    return "The IMM FW";
//       				return Zenoss.render.pingStatus('up');
//					} else {
////	                return "NOT the IMM FW";
//  	      			return Zenoss.render.pingStatus('down');
//					}
//              },  
//          },{
//              // Not sure about this one...
//              id: 'renderTest3',
//              dataIndex: 'name',
//              header: _t('Render function test 3'),
//              sortable: true,
//              width: 200,
//              renderer: function(obj) {
//         		return Zenoss.render.DeviceClass(obj.uid, obj.name);
//              },  
//          },{
//              id: 'name',
//              dataIndex: 'name',
//              header: _t('Name'),
//              width: 50,
//              sortable: true,
            }]
        });
        ZC.IMMFwVpdPanel.superclass.constructor.call(this, config);
    }
});
// Register the above grid panel...
Ext.reg('IMMFwVpdPanel', ZC.IMMFwVpdPanel);
// The registered name (field 1) must match the value of: portal_type = meta_type = 'xxxx' in the Component's object class.
// The remaining fields determine the label that appears in the UI under Components heading when single or multiple objects are found, respectively.
ZC.registerName('IMMFwVpd', _t('IMM Firmware VPD'), _t('IMM Firmware VPD'));

ZC.IMMCpuVpdPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'IMMCpuVpd',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'cpuVpdIndex'},
                {name: 'cpuVpdDescription'},
                {name: 'cpuVpdSpeed'},
                {name: 'cpuVpdIdentifier'},
                {name: 'cpuVpdType'},
                {name: 'cpuVpdFamily'},
                {name: 'cpuVpdCores'},
                {name: 'cpuVpdThreads'},
                {name: 'cpuVpdVoltage'},
                {name: 'cpuVpdDataWidth'},
            ],
            autoExpandColumn: 'cpuVpdDataWidth',
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'cpuVpdIndex',
                dataIndex: 'cpuVpdIndex',
                header: _t('ID'),
                sortable: true,
                width: 50
            },{
//              id: 'cpuVpdDescription',
                id: 'name',
                dataIndex: 'cpuVpdDescription',
                header: _t('Description'),
                sortable: true,
            },{
                id: 'cpuVpdSpeed',
                dataIndex: 'cpuVpdSpeed',
//              header: _t('Speed (MHz)'),
                header: _t('Speed'),
                sortable: true,
                renderer: function(arbitraryVarName) {
            		return arbitraryVarName + " MHz";
            	},  
            },{
                id: 'cpuVpdIdentifier',
                dataIndex: 'cpuVpdIdentifier',
                header: _t('Identifier'),
                sortable: true,
            },{
                id: 'cpuVpdType',
                dataIndex: 'cpuVpdType',
                header: _t('Type'),
                sortable: true,
            },{
                id: 'cpuVpdFamily',
                dataIndex: 'cpuVpdFamily',
                header: _t('Family'),
                sortable: true,
            },{
                id: 'cpuVpdCores',
                dataIndex: 'cpuVpdCores',
                header: _t('Cores'),
                sortable: true,
            },{
                id: 'cpuVpdThreads',
                dataIndex: 'cpuVpdThreads',
                header: _t('Threads'),
                sortable: true,
            },{
                id: 'cpuVpdVoltage',
                dataIndex: 'cpuVpdVoltage',
                header: _t('Voltage'),
                sortable: true,
            },{
                id: 'cpuVpdDataWidth',
                dataIndex: 'cpuVpdDataWidth',
                header: _t('Data Width'),
                sortable: true,
//          },{
//              id: 'name',
//              dataIndex: 'name',
//              header: _t('Name'),
//              width: 50,
//              sortable: true,
            }]
        });
        ZC.IMMCpuVpdPanel.superclass.constructor.call(this, config);
    }
});
Ext.reg('IMMCpuVpdPanel', ZC.IMMCpuVpdPanel);
ZC.registerName('IMMCpuVpd', _t('IMM CPU VPD'), _t('IMM CPU VPD'));

ZC.IMMMemVpdPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'IMMMemVpd',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'memoryVpdIndex'},
                {name: 'memoryVpdDescription'},
                {name: 'memoryVpdPartNumber'},
                {name: 'memoryVpdFRUSerialNumber'},
                {name: 'memoryVpdManufactureDate'},
                {name: 'memoryVpdType'},
                {name: 'memoryVpdSize'},
            ],
            autoExpandColumn: 'memoryVpdSize',
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'memoryVpdIndex',
                dataIndex: 'memoryVpdIndex',
                header: _t('ID'),
                sortable: true,
                width: 50
            },{
//              id: 'memoryVpdDescription',
                id: 'name',
                dataIndex: 'memoryVpdDescription',
                header: _t('Description'),
                sortable: true,
            },{
                id: 'memoryVpdPartNumber',
                dataIndex: 'memoryVpdPartNumber',
                header: _t('Part Number'),
                sortable: true,
                width: 150
            },{
                id: 'memoryVpdFRUSerialNumber',
                dataIndex: 'memoryVpdFRUSerialNumber',
                header: _t('Serial Number'),
                sortable: true,
            },{
                id: 'memoryVpdManufactureDate',
                dataIndex: 'memoryVpdManufactureDate',
                header: _t('Manufacture Date'),
                sortable: true,
            },{
                id: 'memoryVpdType',
                dataIndex: 'memoryVpdType',
                header: _t('Type'),
                sortable: true,
            },{
                id: 'memoryVpdSize',
                dataIndex: 'memoryVpdSize',
                header: _t('Size'),
                sortable: true,
                renderer: function(arbitraryVarName) {
                	return arbitraryVarName + " GB";
            	},  
//          },{
//              id: 'name',
//              dataIndex: 'name',
//              header: _t('Name'),
//              width: 50,
//              sortable: true,
            }]
        });
        ZC.IMMMemVpdPanel.superclass.constructor.call(this, config);
    }
});
Ext.reg('IMMMemVpdPanel', ZC.IMMMemVpdPanel);
ZC.registerName('IMMMemVpd', _t('IMM Memory VPD'), _t('IMM Memory VPD'));

ZC.IMMComponentVpdPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'IMMComponentVpd',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'componentLevelVpdIndex'},
                {name: 'componentLevelVpdFruNumber'},
                {name: 'componentLevelVpdFruName'},
                {name: 'componentLevelVpdSerialNumber'},
                {name: 'componentLevelVpdManufacturingId'},
            ],
            autoExpandColumn: 'componentLevelVpdManufacturingId',
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'componentLevelVpdIndex',
                dataIndex: 'componentLevelVpdIndex',
                header: _t('ID'),
                sortable: true,
                width: 50
            },{
                id: 'componentLevelVpdFruNumber',
                dataIndex: 'componentLevelVpdFruNumber',
                header: _t('FRU Number'),
                sortable: true,
            },{
//              id: 'componentLevelVpdFruName',
                id: 'name',
                dataIndex: 'componentLevelVpdFruName',
                header: _t('FRU Name'),
                sortable: true,
                width: 150
            },{
                id: 'componentLevelVpdSerialNumber',
                dataIndex: 'componentLevelVpdSerialNumber',
                header: _t('Serial Number'),
                sortable: true,
            },{
                id: 'componentLevelVpdManufacturingId',
                dataIndex: 'componentLevelVpdManufacturingId',
                header: _t('Manufacturer'),
                sortable: true,
            }]
        });
        ZC.IMMComponentVpdPanel.superclass.constructor.call(this, config);
    }
});
Ext.reg('IMMComponentVpdPanel', ZC.IMMComponentVpdPanel);
ZC.registerName('IMMComponentVpd', _t('IMM Chassis Component VPD'), _t('IMM Chassis Component VPD'));

ZC.IMMComponentLogPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'IMMComponentLog',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'componentLevelVpdTrackingIndex'},
                {name: 'componentLevelVpdTrackingFruNumber'},
                {name: 'componentLevelVpdTrackingFruName'},
                {name: 'componentLevelVpdTrackingSerialNumber'},
                {name: 'componentLevelVpdTrackingManufacturingId'},
                {name: 'componentLevelVpdTrackingAction'},
                {name: 'componentLevelVpdTrackingTimestamp'},
            ],
            autoExpandColumn: 'componentLevelVpdTrackingTimestamp',
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'componentLevelVpdTrackingIndex',
                dataIndex: 'componentLevelVpdTrackingIndex',
                header: _t('ID'),
                sortable: true,
                width: 50
            },{
                id: 'componentLevelVpdTrackingFruNumber',
                dataIndex: 'componentLevelVpdTrackingFruNumber',
                header: _t('FRU Number'),
                sortable: true,
            },{
//              id: 'componentLevelVpdTrackingFruName',
                id: 'name',
                dataIndex: 'componentLevelVpdTrackingFruName',
                header: _t('FRU Name'),
                sortable: true,
                width: 150
            },{
                id: 'componentLevelVpdTrackingSerialNumber',
                dataIndex: 'componentLevelVpdTrackingSerialNumber',
                header: _t('Serial Number'),
                sortable: true,
            },{
                id: 'componentLevelVpdTrackingManufacturingId',
                dataIndex: 'componentLevelVpdTrackingManufacturingId',
                header: _t('Manufacturer'),
                sortable: true,
            },{
                id: 'componentLevelVpdTrackingAction',
                dataIndex: 'componentLevelVpdTrackingAction',
                header: _t('Action'),
                sortable: true,
            },{
                id: 'componentLevelVpdTrackingTimestamp',
                dataIndex: 'componentLevelVpdTrackingTimestamp',
                header: _t('Timestamp'),
                sortable: true,
            }]
        });
        ZC.IMMComponentLogPanel.superclass.constructor.call(this, config);
    }
});
Ext.reg('IMMComponentLogPanel', ZC.IMMComponentLogPanel);
ZC.registerName('IMMComponentLog', _t('IMM Chassis Component Log'), _t('IMM Chassis Component Log'));

ZC.IMMFanMonPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'IMMFanMon',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'fanIndex'},
                {name: 'fanDescr'},
                {name: 'fanSpeed'},
                {name: 'fanCritLimitLow'},
            ],
            autoExpandColumn: 'fanCritLimitLow',
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'fanIndex',
                dataIndex: 'fanIndex',
                header: _t('ID'),
                sortable: true,
                width: 50
            },{
//              id: 'fanDescr',
                id: 'name',
                dataIndex: 'fanDescr',
                header: _t('Description'),
                sortable: true,
                width: 150
            },{
                id: 'fanSpeed',
                dataIndex: 'fanSpeed',
                header: _t('Fan Speed'),
                sortable: true,
            },{
                id: 'fanCritLimitLow',
                dataIndex: 'fanCritLimitLow',
                header: _t('Critical Low Limit'),
                sortable: true,
            }]
        });
        ZC.IMMFanMonPanel.superclass.constructor.call(this, config);
    }
});
Ext.reg('IMMFanMonPanel', ZC.IMMFanMonPanel);
ZC.registerName('IMMFanMon', _t('IMM Fan Monitor'), _t('IMM Fan Monitors'));

ZC.IMMVoltMonPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'IMMVoltMon',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'voltIndex'},
                {name: 'voltDescr'},
                {name: 'voltReading'},
                {name: 'voltNominalReading'},
                {name: 'voltCritLimitHigh'},
                {name: 'voltCritLimitLow'},
            ],
            autoExpandColumn: 'voltCritLimitLow',
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'voltIndex',
                dataIndex: 'voltIndex',
                header: _t('ID'),
                sortable: true,
                width: 50
            },{
//              id: 'voltDescr',
                id: 'name',
                dataIndex: 'voltDescr',
                header: _t('Description'),
                sortable: true,
                width: 150
            },{
                id: 'voltReading',
                dataIndex: 'voltReading',
                header: _t('Current Reading'),
                sortable: true,
            },{
                id: 'voltNominalReading',
                dataIndex: 'voltNominalReading',
                header: _t('Nominal Reading'),
                sortable: true,
            },{
                id: 'voltCritLimitHigh',
                dataIndex: 'voltCritLimitHigh',
                header: _t('Critical High Limit'),
                sortable: true,
            },{
                id: 'voltCritLimitLow',
                dataIndex: 'voltCritLimitLow',
                header: _t('Critical Low Limit'),
                sortable: true,
            }]
        });
        ZC.IMMVoltMonPanel.superclass.constructor.call(this, config);
    }
});
Ext.reg('IMMVoltMonPanel', ZC.IMMVoltMonPanel);
ZC.registerName('IMMVoltMon', _t('IMM Voltage Monitor'), _t('IMM Voltage Monitors'));

})();
