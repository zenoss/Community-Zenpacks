(function(){

var ZC = Ext.ns('Zenoss.component');


function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.DellUpsBatteryPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'DellUpsBattery',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'batteryABMStatus'},
                {name: 'batteryABMStatusText'},
                {name: 'batteryTestStatus'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'batteryABMStatus',
                dataIndex: 'batteryABMStatus',
                header: _t('Advanced Battery Monitoring Status'),
                sortable: true,
                renderer: Zenoss.render.severity,
                width: 200,
            },{
                id: 'batteryTestStatus',
                dataIndex: 'batteryTestStatus',
                header: _t('Battery Test Status'),
                sortable: true,
                width: 120,
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name')
            }]
        });
        ZC.DellUpsBatteryPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('DellUpsBatteryPanel', ZC.DellUpsBatteryPanel);
ZC.registerName('DellUpsBattery', _t('Dell UPS Battery'), _t('Dell UPS Batteries'));

})();


