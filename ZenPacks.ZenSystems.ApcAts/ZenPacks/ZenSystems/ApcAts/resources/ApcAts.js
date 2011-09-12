(function(){

var ZC = Ext.ns('Zenoss.component');


function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.ApcAtsInputPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'ApcAtsInput',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'inputType'},
                {name: 'inputName'},
                {name: 'inputFrequency'},
                {name: 'inputVoltage'},
                {name: 'statusSelectedSource'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'statusSelectedSource',
                dataIndex: 'statusSelectedSource',
                header: _t('Currently Selected Source'),
                width: 200,
                sortable: true,
            },{
                id: 'inputType',
                dataIndex: 'inputType',
                header: _t('Input Type'),
                width: 200,
                sortable: true,
            },{
                id: 'inputName',
                dataIndex: 'inputName',
                header: _t('Input Name'),
                width: 200,
                sortable: true
            },{
                id: 'inputFrequency',
                dataIndex: 'inputFrequency',
                header: _t('Input Frequency'),
                sortable: true,
            },{
                id: 'inputVoltage',
                dataIndex: 'inputVoltage',
                header: _t('Input Voltage'),
                sortable: true,
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name')
            }]
        });
        ZC.ApcAtsInputPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('ApcAtsInputPanel', ZC.ApcAtsInputPanel);
ZC.registerName('ApcAtsInput', _t('APC ATS Input / Output'), _t('APC ATS Inputs / Outputs'));

})();


