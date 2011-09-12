(function(){

var ZC = Ext.ns('Zenoss.component');


function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.ApcPduOutletPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'ApcPduOutlet',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'outNumber'},
                {name: 'outName'},
                {name: 'outState'},
                {name: 'outBank'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'outNumber',
                dataIndex: 'outNumber',
                header: _t('Outlet Number'),
                sortable: true,
            },{
                id: 'outName',
                dataIndex: 'outName',
                header: _t('Outlet Name'),
                width: 200,
                sortable: true
            },{
                id: 'outState',
                dataIndex: 'outState',
                header: _t('Outlet State'),
                renderer: function(oS) {
                        if (oS=='On') {
                          return Zenoss.render.pingStatus('up');
                        } else {
                          return Zenoss.render.pingStatus('down');
                        }
                },
                sortable: true,
            },{
                id: 'outBank',
                dataIndex: 'outBank',
                header: _t('Outlet Bank'),
                sortable: true,
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name')
            }]
        });
        ZC.ApcPduOutletPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('ApcPduOutletPanel', ZC.ApcPduOutletPanel);
ZC.registerName('ApcPduOutlet', _t('APC PDU Outlet'), _t('APC PDU Outlets'));

ZC.ApcPduBankPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'ApcPduBank',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'bankNumber'},
                {name: 'bankState'},
                {name: 'bankStateText'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'bankNumber',
                dataIndex: 'bankNumber',
                header: _t('Bank Number'),
                sortable: true,
            },{
                id: 'bankStateText',
                dataIndex: 'bankStateText',
                header: _t('Bank State Status'),
/*            
                renderer: function(tS) {
                        if (tS==0) return 'Load: Normal';
                        else if (tS==2) return 'Load: Low';
                             else if (tS==4) return 'Load: Near Overload';
                                  else if (tS==5) return 'Load: Overload';
                                       else return 'Load: Unknown';
                        } ,
*/
                width: 200,
                sortable: true,
            },{
                id: 'bankStateStatus',
                dataIndex: 'bankState',
                header: _t('Bank State Status'),
                renderer: Zenoss.render.severity,
                width: 120,
                sortable: true,
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name')
            }]
        });
        ZC.ApcPduBankPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('ApcPduBankPanel', ZC.ApcPduBankPanel);
ZC.registerName('ApcPduBank', _t('APC PDU Bank'), _t('APC PDU Banks'));

ZC.ApcPduPSPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'ApcPduPS',
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'hasMonitor'},
                {name: 'monitor'},
                {name: 'supply1Status'},
                {name: 'supply2Status'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'supply1StatusDot',
                dataIndex: 'supply1Status',
                header: _t('Power Supply 1 Status'),
                renderer: function(pS1) {
                        if (pS1=='OK') {
                          return Zenoss.render.pingStatus('up');
                        } else {
                          return Zenoss.render.pingStatus('down');
                        }
                },
                width: 120,
                sortable: true,
            },{
                id: 'supply2StatusDot',
                dataIndex: 'supply2Status',
                header: _t('Power Supply 2 Status'),
                renderer: function(pS2) {
                        if (pS2=='OK') {
                          return Zenoss.render.pingStatus('up');
                        } else {
                          return Zenoss.render.pingStatus('down');
                        }
                },
                width: 120,
                sortable: true,
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Object Name')
            }]
        });
        ZC.ApcPduPSPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('ApcPduPSPanel', ZC.ApcPduPSPanel);
ZC.registerName('ApcPduPS', _t('APC PDU Power Supply'), _t('APC PDU Power Supplies'));
})();


