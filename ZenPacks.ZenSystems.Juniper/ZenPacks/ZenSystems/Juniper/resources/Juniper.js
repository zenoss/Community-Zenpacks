(function(){

var ZC = Ext.ns('Zenoss.component');


function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.JuniperContentsPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'JuniperContents',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'containerIndex'},
                {name: 'containerDescr'},
                {name: 'containerParentIndex'},
                {name: 'containerParentDescr'},
                {name: 'contentsType'},
                {name: 'contentsDescr'},
                {name: 'contentsSerialNo'},
                {name: 'contentsRevision'},
                {name: 'contentsPartNo'},
                {name: 'contentsChassisId'},
                {name: 'contentsChassisDescr'},
                {name: 'contentsChassisCLEI'},
                {name: 'contentsCPU'},
                {name: 'contentsTemp'},
                {name: 'contentsState'},
                {name: 'contentsUpTime'},
                {name: 'contentsMemory'},
                {name: 'manufacturer'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'contentsDescr',
                dataIndex: 'contentsDescr',
                header: _t('Description'),
                width: 200,
                sortable: true,
            },{
                id: 'containerIndex',
                dataIndex: 'containerIndex',
                header: _t('Container Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerDescr',
                dataIndex: 'containerDescr',
                header: _t('Container Descr'),
                width: 150,
                sortable: true,
            },{
                id: 'containerParentIndex',
                dataIndex: 'containerParentIndex',
                header: _t('Parent Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerParentDescr',
                dataIndex: 'containerParentDescr',
                header: _t('Parent Descr'),
                width: 150,
                sortable: true,
            },{
                id: 'contentsSerialNo',
                dataIndex: 'contentsSerialNo',
                header: _t('SerialNo'),
                width: 90,
                sortable: true,
            },{
                id: 'contentsRevision',
                dataIndex: 'contentsRevision',
                header: _t('Revision'),
                width: 60,
                sortable: true,
            },{
                id: 'contentsPartNo',
                dataIndex: 'contentsPartNo',
                header: _t('PartNo'),
                width: 80,
                sortable: true,
            },{
                id: 'contentsChassisCLEI',
                dataIndex: 'contentsChassisCLEI',
                header: _t('Chassis CLEI.'),
                width: 80,
                sortable: true,
            },{
                id: 'contentsState',
                dataIndex: 'contentsState',
                header: _t('State'),
                width: 60,
                sortable: true,
            },{
                id: 'contentsUpTime',
                dataIndex: 'contentsUpTime',
                header: _t('UpTime (Days)'),
                width: 60,
                sortable: true,
            },{
                id: 'contentsMemory',
                dataIndex: 'contentsMemory',
                header: _t('Memory (MB)'),
                width: 70,
                sortable: true,
            },{
                id: 'contentsType',
                dataIndex: 'contentsType',
                header: _t('Type'),
                width: 200,
                sortable: true,
            },{
                id: 'contentsChassisId',
                dataIndex: 'contentsChassisId',
                header: _t('ChassisId'),
                width: 40,
                sortable: true,
            },{
                id: 'contentsChassisDescr',
                dataIndex: 'contentsChassisDescr',
                header: _t('Chassis Descr.'),
                width: 80,
                sortable: true,
            },{
                id: 'contentsCPU',
                dataIndex: 'contentsCPU',
                header: _t('CPU %'),
                width: 60,
                sortable: true,
            },{
                id: 'contentsTemp',
                dataIndex: 'contentsTemp',
                header: _t('Temp.C'),
                width: 50,
                sortable: true,
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name'),
                width: 200,
                sortable: true,
            },{
                id: 'manufacturer',
                dataIndex: 'manufacturer',
                header: _t('Manufacturer'),
                renderer: render_link,
                width: 10,
                sortable: true,
            }]
        });
        ZC.JuniperContentsPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperContentsPanel', ZC.JuniperContentsPanel);
ZC.registerName('JuniperContents', _t('Contents'), _t('Contents'));

ZC.JuniperFanPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'Fan',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'fanContainerIndex'},
                {name: 'fanDescr'},
                {name: 'fanType'},
                {name: 'fanSerialNo'},
                {name: 'fanRevision'},
                {name: 'fanChassisId'},
                {name: 'fanState'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'fanDescr',
                dataIndex: 'fanDescr',
                header: _t('Description'),
                width: 200,
                sortable: true,
            },{
                id: 'fanState',
                dataIndex: 'fanState',
                header: _t('State'),
                width: 200,
                sortable: true,
            },{
/*
                id: 'fanContainerIndex',
                dataIndex: 'fanContainerIndex',
                header: _t('Container Index'),
                width: 40,
                sortable: true,
            },{
                id: 'fanType',
                dataIndex: 'fanType',
                header: _t('Type'),
                width: 200,
                sortable: true,
            },{
                id: 'fanSerialNo',
                dataIndex: 'fanSerialNo',
                header: _t('SerialNo'),
                width: 90,
                sortable: true,
            },{
                id: 'fanRevision',
                dataIndex: 'fanRevision',
                header: _t('Revision'),
                width: 60,
                sortable: true,
            },{
                id: 'fanChassisId',
                dataIndex: 'fanChassisId',
                header: _t('ChassisId'),
                width: 40,
                sortable: true,
            },{
*/
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name')
            }]
        });
        ZC.JuniperFanPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperFanPanel', ZC.JuniperFanPanel);
ZC.registerName('JuniperFan', _t('Fan'), _t('Fans'));

ZC.JuniperPowerSupplyPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'PowerSupply',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'powerSupplyContainerIndex'},
                {name: 'powerSupplyDescr'},
                {name: 'powerSupplyType'},
                {name: 'powerSupplySerialNo'},
                {name: 'powerSupplyPartNo'},
                {name: 'powerSupplyRevision'},
                {name: 'powerSupplyChassisId'},
                {name: 'powerSupplyState'},
                {name: 'powerSupplyTemp'},
                {name: 'powerSupplyCPU'},
                {name: 'powerSupplyMemory'},
                {name: 'powerSupplyUpTime'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'powerSupplyDescr',
                dataIndex: 'powerSupplyDescr',
                header: _t('Description'),
                width: 200,
                sortable: true,
            },{
                id: 'powerSupplyRevision',
                dataIndex: 'powerSupplyRevision',
                header: _t('Revision'),
                width: 60,
                sortable: true,
            },{
                id: 'powerSupplySerialNo',
                dataIndex: 'powerSupplySerialNo',
                header: _t('SerialNo'),
                width: 90,
                sortable: true,
            },{
                id: 'powerSupplyPartNo',
                dataIndex: 'powerSupplyPartNo',
                header: _t('Part No'),
                width: 90,
                sortable: true,
            },{
                id: 'powerSupplyState',
                dataIndex: 'powerSupplyState',
                header: _t('State'),
                width: 60,
                sortable: true,
            },{
                id: 'powerSupplyUpTime',
                dataIndex: 'powerSupplyUpTime',
                header: _t('Up Time (days)'),
                width: 100,
                sortable: true,
            },{
/*
                id: 'powerSupplyTemp',
                dataIndex: 'powerSupplyTemp',
                header: _t('Temp'),
                width: 60,
                sortable: true,
            },{
                id: 'powerSupplyCPU',
                dataIndex: 'powerSupplyCPU',
                header: _t('CPU'),
                width: 60,
                sortable: true,
            },{
                id: 'powerSupplyMemory',
                dataIndex: 'powerSupplyMemory',
                header: _t('Memory'),
                width: 60,
                sortable: true,
            },{
                id: 'powerSupplyContainerIndex',
                dataIndex: 'powerSupplyContainerIndex',
                header: _t('Container Index'),
                width: 40,
                sortable: true,
            },{
                id: 'powerSupplyType',
                dataIndex: 'powerSupplyType',
                header: _t('Type'),
                width: 200,
                sortable: true,
            },{
                id: 'powerSupplyChassisId',
                dataIndex: 'powerSupplyChassisId',
                header: _t('ChassisId'),
                width: 40,
                sortable: true,
            },{
*/
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name')
            }]
        });
        ZC.JuniperPowerSupplyPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperPowerSupplyPanel', ZC.JuniperPowerSupplyPanel);
ZC.registerName('JuniperPowerSupply', _t('PowerSupply'), _t('Power Supplies'));

ZC.JuniperFPCPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'JuniperFPC',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'containerIndex'},
                {name: 'containerDescr'},
                {name: 'containerParentIndex'},
                {name: 'containerParentDescr'},
                {name: 'FPCType'},
                {name: 'FPCDescr'},
                {name: 'FPCSerialNo'},
                {name: 'FPCRevision'},
                {name: 'FPCPartNo'},
                {name: 'FPCChassisId'},
                {name: 'FPCChassisDescr'},
                {name: 'FPCChassisCLEI'},
                {name: 'FPCCPU'},
                {name: 'FPCTemp'},
                {name: 'FPCState'},
                {name: 'FPCUpTime'},
                {name: 'FPCMemory'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'FPCDescr',
                dataIndex: 'FPCDescr',
                header: _t('Description'),
                width: 200,
                sortable: true,
            },{
                id: 'FPCRevision',
                dataIndex: 'FPCRevision',
                header: _t('Revision'),
                width: 60,
                sortable: true,
            },{
                id: 'FPCSerialNo',
                dataIndex: 'FPCSerialNo',
                header: _t('SerialNo'),
                width: 90,
                sortable: true,
            },{
                id: 'FPCPartNo',
                dataIndex: 'FPCPartNo',
                header: _t('PartNo'),
                width: 80,
                sortable: true,
            },{
                id: 'FPCState',
                dataIndex: 'FPCState',
                header: _t('State'),
                width: 60,
                sortable: true,
            },{
                id: 'FPCUpTime',
                dataIndex: 'FPCUpTime',
                header: _t('UpTime (Days)'),
                width: 60,
                sortable: true,
            },{
/*
                id: 'FPCChassisCLEI',
                dataIndex: 'FPCChassisCLEI',
                header: _t('Chassis CLEI.'),
                width: 80,
                sortable: true,
            },{
                id: 'FPCType',
                dataIndex: 'FPCType',
                header: _t('Type'),
                width: 200,
                sortable: true,
            },{
                id: 'FPCChassisId',
                dataIndex: 'FPCChassisId',
                header: _t('ChassisId'),
                width: 40,
                sortable: true,
            },{
                id: 'FPCChassisDescr',
                dataIndex: 'FPCChassisDescr',
                header: _t('Chassis Descr.'),
                width: 80,
                sortable: true,
            },{
                id: 'FPCCPU',
                dataIndex: 'FPCCPU',
                header: _t('CPU %'),
                width: 60,
                sortable: true,
            },{
                id: 'FPCMemory',
                dataIndex: 'FPCMemory',
                header: _t('Memory (MB)'),
                width: 70,
                sortable: true,
            },{
                id: 'FPCTemp',
                dataIndex: 'FPCTemp',
                header: _t('Temp.C'),
                width: 50,
                sortable: true,
            },{
                id: 'containerIndex',
                dataIndex: 'containerIndex',
                header: _t('Container Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerDescr',
                dataIndex: 'containerDescr',
                header: _t('Container Descr'),
                width: 150,
                sortable: true,
            },{
                id: 'containerParentIndex',
                dataIndex: 'containerParentIndex',
                header: _t('Parent Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerParentDescr',
                dataIndex: 'containerParentDescr',
                header: _t('Parent Descr'),
                width: 150,
                sortable: true,
            },{
*/
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name'),
                width: 200,
                sortable: true,
            }]
        });
        ZC.JuniperFPCPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperFPCPanel', ZC.JuniperFPCPanel);
ZC.registerName('JuniperFPC', _t('FPC'), _t('FPCs'));

ZC.JuniperPICPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'JuniperPIC',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'containerIndex'},
                {name: 'containerDescr'},
                {name: 'containerParentIndex'},
                {name: 'containerParentDescr'},
                {name: 'PICType'},
                {name: 'PICDescr'},
                {name: 'PICSerialNo'},
                {name: 'PICRevision'},
                {name: 'PICPartNo'},
                {name: 'PICChassisId'},
                {name: 'PICChassisDescr'},
                {name: 'PICChassisCLEI'},
                {name: 'PICCPU'},
                {name: 'PICTemp'},
                {name: 'PICState'},
                {name: 'PICUpTime'},
                {name: 'PICMemory'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'PICDescr',
                dataIndex: 'PICDescr',
                header: _t('Description'),
                width: 200,
                sortable: true,
            },{
                id: 'PICState',
                dataIndex: 'PICState',
                header: _t('State'),
                width: 60,
                sortable: true,
            },{
/*
                id: 'PICRevision',
                dataIndex: 'PICRevision',
                header: _t('Revision'),
                width: 60,
                sortable: true,
            },{
                id: 'PICSerialNo',
                dataIndex: 'PICSerialNo',
                header: _t('SerialNo'),
                width: 90,
                sortable: true,
            },{
                id: 'PICPartNo',
                dataIndex: 'PICPartNo',
                header: _t('PartNo'),
                width: 80,
                sortable: true,
            },{
                id: 'PICUpTime',
                dataIndex: 'PICUpTime',
                header: _t('UpTime (Days)'),
                width: 60,
                sortable: true,
            },{
                id: 'PICChassisCLEI',
                dataIndex: 'PICChassisCLEI',
                header: _t('Chassis CLEI.'),
                width: 80,
                sortable: true,
            },{
                id: 'PICType',
                dataIndex: 'PICType',
                header: _t('Type'),
                width: 200,
                sortable: true,
            },{
                id: 'PICChassisId',
                dataIndex: 'PICChassisId',
                header: _t('ChassisId'),
                width: 40,
                sortable: true,
            },{
                id: 'PICChassisDescr',
                dataIndex: 'PICChassisDescr',
                header: _t('Chassis Descr.'),
                width: 80,
                sortable: true,
            },{
                id: 'PICCPU',
                dataIndex: 'PICCPU',
                header: _t('CPU %'),
                width: 60,
                sortable: true,
            },{
                id: 'PICMemory',
                dataIndex: 'PICMemory',
                header: _t('Memory (MB)'),
                width: 70,
                sortable: true,
            },{
                id: 'PICTemp',
                dataIndex: 'PICTemp',
                header: _t('Temp.C'),
                width: 50,
                sortable: true,
            },{
                id: 'containerIndex',
                dataIndex: 'containerIndex',
                header: _t('Container Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerDescr',
                dataIndex: 'containerDescr',
                header: _t('Container Descr'),
                width: 150,
                sortable: true,
            },{
                id: 'containerParentIndex',
                dataIndex: 'containerParentIndex',
                header: _t('Parent Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerParentDescr',
                dataIndex: 'containerParentDescr',
                header: _t('Parent Descr'),
                width: 150,
                sortable: true,
            },{
*/
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name'),
                width: 200,
                sortable: true,
            }]
        });
        ZC.JuniperPICPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperPICPanel', ZC.JuniperPICPanel);
ZC.registerName('JuniperPIC', _t('PIC'), _t('PICs'));

ZC.JuniperMICPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'JuniperMIC',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'containerIndex'},
                {name: 'containerDescr'},
                {name: 'containerParentIndex'},
                {name: 'containerParentDescr'},
                {name: 'MICType'},
                {name: 'MICDescr'},
                {name: 'MICSerialNo'},
                {name: 'MICRevision'},
                {name: 'MICPartNo'},
                {name: 'MICChassisId'},
                {name: 'MICChassisDescr'},
                {name: 'MICChassisCLEI'},
                {name: 'MICCPU'},
                {name: 'MICTemp'},
                {name: 'MICState'},
                {name: 'MICUpTime'},
                {name: 'MICMemory'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'MICDescr',
                dataIndex: 'MICDescr',
                header: _t('Description'),
                width: 200,
                sortable: true,
            },{
                id: 'MICState',
                dataIndex: 'MICState',
                header: _t('State'),
                width: 60,
                sortable: true,
            },{
/*
                id: 'MICRevision',
                dataIndex: 'MICRevision',
                header: _t('Revision'),
                width: 60,
                sortable: true,
            },{
                id: 'MICSerialNo',
                dataIndex: 'MICSerialNo',
                header: _t('SerialNo'),
                width: 90,
                sortable: true,
            },{
                id: 'MICPartNo',
                dataIndex: 'MICPartNo',
                header: _t('PartNo'),
                width: 80,
                sortable: true,
            },{
                id: 'MICUpTime',
                dataIndex: 'MICUpTime',
                header: _t('UpTime (Days)'),
                width: 60,
                sortable: true,
            },{
                id: 'MICChassisCLEI',
                dataIndex: 'MICChassisCLEI',
                header: _t('Chassis CLEI.'),
                width: 80,
                sortable: true,
            },{
                id: 'MICType',
                dataIndex: 'MICType',
                header: _t('Type'),
                width: 200,
                sortable: true,
            },{
                id: 'MICChassisId',
                dataIndex: 'MICChassisId',
                header: _t('ChassisId'),
                width: 40,
                sortable: true,
            },{
                id: 'MICChassisDescr',
                dataIndex: 'MICChassisDescr',
                header: _t('Chassis Descr.'),
                width: 80,
                sortable: true,
            },{
                id: 'MICCPU',
                dataIndex: 'MICCPU',
                header: _t('CPU %'),
                width: 60,
                sortable: true,
            },{
                id: 'MICMemory',
                dataIndex: 'MICMemory',
                header: _t('Memory (MB)'),
                width: 70,
                sortable: true,
            },{
                id: 'MICTemp',
                dataIndex: 'MICTemp',
                header: _t('Temp.C'),
                width: 50,
                sortable: true,
            },{
                id: 'containerIndex',
                dataIndex: 'containerIndex',
                header: _t('Container Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerDescr',
                dataIndex: 'containerDescr',
                header: _t('Container Descr'),
                width: 150,
                sortable: true,
            },{
                id: 'containerParentIndex',
                dataIndex: 'containerParentIndex',
                header: _t('Parent Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerParentDescr',
                dataIndex: 'containerParentDescr',
                header: _t('Parent Descr'),
                width: 150,
                sortable: true,
            },{
*/
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name'),
                width: 200,
                sortable: true,
            }]
        });
        ZC.JuniperMICPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperMICPanel', ZC.JuniperMICPanel);
ZC.registerName('JuniperMIC', _t('MIC'), _t('MICs'));

ZC.JuniperBaseCompPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'JuniperBaseComp',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'containerIndex'},
                {name: 'containerDescr'},
                {name: 'containerParentIndex'},
                {name: 'containerParentDescr'},
                {name: 'BaseCompType'},
                {name: 'BaseCompDescr'},
                {name: 'BaseCompSerialNo'},
                {name: 'BaseCompRevision'},
                {name: 'BaseCompPartNo'},
                {name: 'BaseCompChassisId'},
                {name: 'BaseCompChassisDescr'},
                {name: 'BaseCompChassisCLEI'},
                {name: 'BaseCompCPU'},
                {name: 'BaseCompTemp'},
                {name: 'BaseCompState'},
                {name: 'BaseCompUpTime'},
                {name: 'BaseCompMemory'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'BaseCompDescr',
                dataIndex: 'BaseCompDescr',
                header: _t('Description'),
                width: 200,
                sortable: true,
            },{
                id: 'BaseCompState',
                dataIndex: 'BaseCompState',
                header: _t('State'),
                width: 60,
                sortable: true,
            },{
/*
                id: 'BaseCompRevision',
                dataIndex: 'BaseCompRevision',
                header: _t('Revision'),
                width: 60,
                sortable: true,
            },{
                id: 'BaseCompSerialNo',
                dataIndex: 'BaseCompSerialNo',
                header: _t('SerialNo'),
                width: 90,
                sortable: true,
            },{
                id: 'BaseCompPartNo',
                dataIndex: 'BaseCompPartNo',
                header: _t('PartNo'),
                width: 80,
                sortable: true,
            },{
                id: 'BaseCompUpTime',
                dataIndex: 'BaseCompUpTime',
                header: _t('UpTime (Days)'),
                width: 60,
                sortable: true,
            },{
                id: 'BaseCompChassisCLEI',
                dataIndex: 'BaseCompChassisCLEI',
                header: _t('Chassis CLEI.'),
                width: 80,
                sortable: true,
            },{
                id: 'BaseCompType',
                dataIndex: 'BaseCompType',
                header: _t('Type'),
                width: 200,
                sortable: true,
            },{
                id: 'BaseCompChassisId',
                dataIndex: 'BaseCompChassisId',
                header: _t('ChassisId'),
                width: 40,
                sortable: true,
            },{
                id: 'BaseCompChassisDescr',
                dataIndex: 'BaseCompChassisDescr',
                header: _t('Chassis Descr.'),
                width: 80,
                sortable: true,
            },{
                id: 'BaseCompCPU',
                dataIndex: 'BaseCompCPU',
                header: _t('CPU %'),
                width: 60,
                sortable: true,
            },{
                id: 'BaseCompMemory',
                dataIndex: 'BaseCompMemory',
                header: _t('Memory (MB)'),
                width: 70,
                sortable: true,
            },{
                id: 'BaseCompTemp',
                dataIndex: 'BaseCompTemp',
                header: _t('Temp.C'),
                width: 50,
                sortable: true,
            },{
                id: 'containerIndex',
                dataIndex: 'containerIndex',
                header: _t('Container Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerDescr',
                dataIndex: 'containerDescr',
                header: _t('Container Descr'),
                width: 150,
                sortable: true,
            },{
                id: 'containerParentIndex',
                dataIndex: 'containerParentIndex',
                header: _t('Parent Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerParentDescr',
                dataIndex: 'containerParentDescr',
                header: _t('Parent Descr'),
                width: 150,
                sortable: true,
            },{
*/
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name'),
                width: 200,
                sortable: true,
            }]
        });
        ZC.JuniperBaseCompPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperBaseCompPanel', ZC.JuniperBaseCompPanel);
ZC.registerName('JuniperBaseComp', _t('Base Component'), _t('Base Components'));

ZC.JuniperRoutingEnginePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'JuniperRoutingEngine',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'containerIndex'},
                {name: 'containerDescr'},
                {name: 'containerParentIndex'},
                {name: 'containerParentDescr'},
                {name: 'RoutingEngineType'},
                {name: 'RoutingEngineDescr'},
                {name: 'RoutingEngineSerialNo'},
                {name: 'RoutingEngineRevision'},
                {name: 'RoutingEnginePartNo'},
                {name: 'RoutingEngineChassisId'},
                {name: 'RoutingEngineChassisDescr'},
                {name: 'RoutingEngineChassisCLEI'},
                {name: 'RoutingEngineCPU'},
                {name: 'RoutingEngineTemp'},
                {name: 'RoutingEngineState'},
                {name: 'RoutingEngineUpTime'},
                {name: 'RoutingEngineMemory'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'RoutingEngineDescr',
                dataIndex: 'RoutingEngineDescr',
                header: _t('Description'),
                width: 200,
                sortable: true,
            },{
                id: 'RoutingEngineRevision',
                dataIndex: 'RoutingEngineRevision',
                header: _t('Revision'),
                width: 80,
                sortable: true,
            },{
                id: 'RoutingEngineSerialNo',
                dataIndex: 'RoutingEngineSerialNo',
                header: _t('SerialNo'),
                width: 100,
                sortable: true,
            },{
                id: 'RoutingEnginePartNo',
                dataIndex: 'RoutingEnginePartNo',
                header: _t('PartNo'),
                width: 100,
                sortable: true,
            },{
                id: 'RoutingEngineState',
                dataIndex: 'RoutingEngineState',
                header: _t('State'),
                width: 100,
                sortable: true,
            },{
/*
                id: 'RoutingEngineUpTime',
                dataIndex: 'RoutingEngineUpTime',
                header: _t('UpTime (Days)'),
                width: 100,
                sortable: true,
            },{
                id: 'RoutingEngineChassisCLEI',
                dataIndex: 'RoutingEngineChassisCLEI',
                header: _t('Chassis CLEI.'),
                width: 80,
                sortable: true,
            },{
                id: 'RoutingEngineType',
                dataIndex: 'RoutingEngineType',
                header: _t('Type'),
                width: 200,
                sortable: true,
            },{
                id: 'RoutingEngineChassisId',
                dataIndex: 'RoutingEngineChassisId',
                header: _t('ChassisId'),
                width: 40,
                sortable: true,
            },{
                id: 'RoutingEngineChassisDescr',
                dataIndex: 'RoutingEngineChassisDescr',
                header: _t('Chassis Descr.'),
                width: 80,
                sortable: true,
            },{
                id: 'RoutingEngineCPU',
                dataIndex: 'RoutingEngineCPU',
                header: _t('CPU %'),
                width: 60,
                sortable: true,
            },{
                id: 'RoutingEngineMemory',
                dataIndex: 'RoutingEngineMemory',
                header: _t('Memory (MB)'),
                width: 70,
                sortable: true,
            },{
                id: 'RoutingEngineTemp',
                dataIndex: 'RoutingEngineTemp',
                header: _t('Temp.C'),
                width: 50,
                sortable: true,
            },{
                id: 'containerIndex',
                dataIndex: 'containerIndex',
                header: _t('Container Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerDescr',
                dataIndex: 'containerDescr',
                header: _t('Container Descr'),
                width: 150,
                sortable: true,
            },{
                id: 'containerParentIndex',
                dataIndex: 'containerParentIndex',
                header: _t('Parent Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerParentDescr',
                dataIndex: 'containerParentDescr',
                header: _t('Parent Descr'),
                width: 150,
                sortable: true,
            },{
*/
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name'),
                width: 200,
                sortable: true,
            }]
        });
        ZC.JuniperRoutingEnginePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperRoutingEnginePanel', ZC.JuniperRoutingEnginePanel);
ZC.registerName('JuniperRoutingEngine', _t('RoutingEngine'), _t('Routing Engines'));

ZC.JuniperBGPPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'JuniperBGP',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'bgpLocalAddress'},
                {name: 'bgpRemoteAddress'},
                {name: 'bgpRemoteASN'},
                {name: 'bgpStateInt'},
                {name: 'bgpStateText'},
                {name: 'bgpLastUpDown'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'bgpRemoteAddress',
                dataIndex: 'bgpRemoteAddress',
                header: _t('Remote address'),
                width: 120,
                sortable: true,
            },{
                id: 'bgpRemoteASN',
                dataIndex: 'bgpRemoteASN',
                header: _t('Remote ASN'),
                width: 80,
                sortable: true,
            },{
                id: 'bgpStateText',
                dataIndex: 'bgpStateText',
                header: _t('State'),
                width: 100,
                sortable: true,
            },{
                id: 'bgpLastUpDown',
                dataIndex: 'bgpLastUpDown',
                header: _t('Last Up/Down (days)'),
                width: 120,
                sortable: true,
            },{
/*
                id: 'bgpStateInt',
                dataIndex: 'bgpStateInt',
                header: _t('State (int)'),
                width: 60,
                sortable: true,
            },{
*/
                id: 'bgpLocalAddress',
                dataIndex: 'bgpLocalAddress',
                header: _t('Local address'),
                width: 120,
                sortable: true,
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name'),
                width: 200,
                sortable: true,
            }]
        });
        ZC.JuniperBGPPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperBGPPanel', ZC.JuniperBGPPanel);
ZC.registerName('JuniperBGP', _t('BGP'), _t('BGPs'));

ZC.JuniperComponentsPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'JuniperComponents',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'containerIndex'},
                {name: 'containerDescr'},
                {name: 'containerParentIndex'},
                {name: 'containerParentDescr'},
                {name: 'containerType'},
                {name: 'containerLevel'},
                {name: 'containerNextLevel'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'containerParentIndex',
                dataIndex: 'containerParentIndex',
                header: _t('Parent Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerParentDescr',
                dataIndex: 'containerParentDescr',
                header: _t('Parent Descr'),
                width: 150,
                sortable: true,
            },{
                id: 'containerIndex',
                dataIndex: 'containerIndex',
                header: _t('Container Index'),
                width: 40,
                sortable: true,
            },{
                id: 'containerDescr',
                dataIndex: 'containerDescr',
                header: _t('Descr'),
                width: 200,
                sortable: true,
            },{
                id: 'containerLevel',
                dataIndex: 'containerLevel',
                header: _t('Level'),
                width: 60,
                sortable: true,
            },{
                id: 'containerNextLevel',
                dataIndex: 'containerNextLevel',
                header: _t('Next Level'),
                width: 60,
                sortable: true,
            },{
                id: 'containerType',
                dataIndex: 'containerType',
                header: _t('Type'),
                width: 200,
                sortable: true,
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name')
            }]
        });
        ZC.JuniperComponentsPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperComponentsPanel', ZC.JuniperComponentsPanel);
ZC.registerName('JuniperComponents', _t('Container'), _t('Containers'));

ZC.JuniperIpSecVPNPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'JuniperIpSecVPN',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'vpnPhase1LocalGwAddr'},
                {name: 'vpnPhase1LocalIdValue'},
                {name: 'vpnPhase1RemoteIdValue'},
                {name: 'vpnPhase1State'},
                {name: 'vpnPhase2LocalGwAddr'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'vpnPhase1LocalGwAddr',
                dataIndex: 'vpnPhase1LocalGwAddr',
                header: _t('Phase 1 Local G/w'),
                width: 120,
                sortable: true,
            },{
                id: 'vpnPhase1LocalIdValue',
                dataIndex: 'vpnPhase1LocalIdValue',
                header: _t('Phase 1 Local Id'),
                width: 100,
                sortable: true,
            },{
                id: 'vpnPhase1RemoteIdValue',
                dataIndex: 'vpnPhase1RemoteIdValue',
                header: _t('Phase 1 Remote Id'),
                width: 100,
                sortable: true,
            },{
                id: 'vpnPhase1State',
                dataIndex: 'vpnPhase1State',
                header: _t('Phase 1 State'),
                width: 80,
                sortable: true,
           },{
                id: 'vpnPhase2LocalGwAddr',
                dataIndex: 'vpnPhase2LocalGwAddr',
                header: _t('Phase 2 Local G/w'),
                width: 120,
                sortable: true,
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name'),
                width: 200,
                sortable: true,
            }]
        });
        ZC.JuniperIpSecVPNPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperIpSecVPNPanel', ZC.JuniperIpSecVPNPanel);
ZC.registerName('JuniperIpSecVPN', _t('IpSecVPN'), _t('IpSecVPNs'));

ZC.JuniperIpSecNATPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'JuniperIpSecNAT',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'natId'},
                {name: 'natNumPorts'},
                {name: 'natNumSess'},
                {name: 'natPoolType'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'natId',
                dataIndex: 'natId',
                header: _t('NAT Id'),
                width: 200,
                sortable: true,
            },{
                id: 'natNumPorts',
                dataIndex: 'natNumPorts',
                header: _t('Num. of Ports'),
                width: 100,
                sortable: true,
            },{
                id: 'natNumSess',
                dataIndex: 'natNumSess',
                header: _t('Num. of Sessions'),
                width: 100,
                sortable: true,
            },{
                id: 'natPoolType',
                dataIndex: 'natPoolType',
                header: _t('Pool Type'),
                width: 80,
                sortable: true,
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name'),
                width: 200,
                sortable: true,
            }]
        });
        ZC.JuniperIpSecNATPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperIpSecNATPanel', ZC.JuniperIpSecNATPanel);
ZC.registerName('JuniperIpSecNAT', _t('IpSecNAT'), _t('IpSecNATs'));


ZC.JuniperIpSecPolicyPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'JuniperIpSecPolicy',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'policyId'},
                {name: 'policyAction'},
                {name: 'policyState'},
                {name: 'policyFromZone'},
                {name: 'policyToZone'},
                {name: 'policyName'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'policyId',
                dataIndex: 'policyId',
                header: _t('Policy Id'),
                width: 250,
                sortable: true,
            },{
                id: 'policyFromZone',
                dataIndex: 'policyFromZone',
                header: _t('Policy From Zone'),
                width: 100,
                sortable: true,
            },{
                id: 'policyToZone',
                dataIndex: 'policyToZone',
                header: _t('Policy To Zone'),
                width: 100,
                sortable: true,
            },{
                id: 'policyName',
                dataIndex: 'policyName',
                header: _t('Policy Name'),
                width: 250,
                sortable: true,
            },{
                id: 'policyAction',
                dataIndex: 'policyAction',
                header: _t('Policy Action'),
                width: 100,
                sortable: true,
            },{
                id: 'policyState',
                dataIndex: 'policyState',
                header: _t('Policy State'),
                width: 100,
                sortable: true,
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name'),
                width: 200,
                sortable: true,
            }]
        });
        ZC.JuniperIpSecPolicyPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperIpSecPolicyPanel', ZC.JuniperIpSecPolicyPanel);
ZC.registerName('JuniperIpSecPolicy', _t('IpSecPolicy'), _t('IpSecPolicys'));

ZC.JuniperVlanPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'JuniperVlan',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'vlanName'},
                {name: 'vlanType'},
                {name: 'vlanTag'},
                {name: 'vlanPortGroup'},
                {name: 'vlanInterfaceInfo'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'vlanName',
                dataIndex: 'vlanName',
                header: _t('VLAN Name'),
                width: 120,
                sortable: true,
            },{
                id: 'vlanType',
                dataIndex: 'vlanType',
                header: _t('VLAN Type'),
                width: 100,
                sortable: true,
            },{
                id: 'vlanTag',
                dataIndex: 'vlanTag',
                header: _t('VLAN Tag'),
                width: 60,
                sortable: true,
            },{
/*
                id: 'vlanPortGroup',
                dataIndex: 'vlanPortGroup',
                header: _t('VLAN Port Group'),
                width: 120,
                sortable: true,
            },{
*/
                id: 'vlanInterfaceInfo',
                dataIndex: 'vlanInterfaceInfo',
                header: _t('VLAN Interface Info'),
                width: 950,
                sortable: true,
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name'),
                width: 200,
                sortable: true,
            }]
        });
        ZC.JuniperVlanPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('JuniperVlanPanel', ZC.JuniperVlanPanel);
ZC.registerName('JuniperVlan', _t('Vlan'), _t('Vlans'));

})();


