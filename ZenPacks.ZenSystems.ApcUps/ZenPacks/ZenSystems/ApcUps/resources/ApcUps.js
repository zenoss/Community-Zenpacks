(function(){

var ZC = Ext.ns('Zenoss.component');


function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.ApcUpsBatteryPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'ApcUpsBattery',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'batteryStatus'},
                {name: 'batteryStatusText'},
                {name: 'timeOnBattery'},
                {name: 'batteryLastReplacementDate'},
                {name: 'batteryReplaceIndicator'},
                {name: 'batteryReplaceIndicatorText'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'batteryStatus',
                dataIndex: 'batteryStatus',
                header: _t('Battery Status'),
                sortable: true,
                renderer: Zenoss.render.severity,
                width: 120,
            },{
                id: 'batteryStatusText',
                dataIndex: 'batteryStatusText',
                header: _t('Battery Status'),
                sortable: true,
                width: 150,
            },{
                id: 'timeOnBattery',
                dataIndex: 'timeOnBattery',
                header: _t('Time on Battery (mins)'),
                sortable: true,
                width: 200,
            },{
                id: 'batteryLastReplacementDate',
                dataIndex: 'batteryLastReplacementDate',
                header: _t('Last replacement date'),
                sortable: true,
                width: 200,
            },{
                id: 'batteryReplaceIndicator',
                dataIndex: 'batteryReplaceIndicator',
                header: _t('Battery Replacement Indicator'),
                sortable: true,
                renderer: Zenoss.render.severity,
                width: 180,
            },{
                id: 'batteryReplaceIndicatorText',
                dataIndex: 'batteryReplaceIndicatorText',
                header: _t('Battery Replacement Indicator'),
                sortable: true,
                width: 180,
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name')
            }]
        });
        ZC.ApcUpsBatteryPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('ApcUpsBatteryPanel', ZC.ApcUpsBatteryPanel);
ZC.registerName('ApcUpsBattery', _t('APC UPS Battery'), _t('APC UPS Batteries'));

})();


