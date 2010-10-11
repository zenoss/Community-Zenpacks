/*
################################################################################
#
# This program is part of the RDBMS Zenpack for Zenoss.
# Copyright (C) 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################
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

ZC.DatabasePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'Database',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'dbSrvInst'},
                {name: 'name'},
                {name: 'type'},
                {name: 'totalBytesString'},
                {name: 'usedBytesString'},
                {name: 'capacity'},
                {name: 'locking'},
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
                id: 'dbSrvInst',
                dataIndex: 'dbSrvInst',
                header: _t('Instance'),
                sortable: true,
                renderer: Zenoss.render.default_uid_renderer
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'type',
                dataIndex: 'type',
                header: _t('Database Type')
            },{
                id: 'totalBytesString',
                dataIndex: 'totalBytesString',
                header: _t('Total Bytes')
            },{
                id: 'usedBytesString',
                dataIndex: 'usedBytesString',
                header: _t('Used Bytes')
            },{
                id: 'capacity',
                dataIndex: 'capacity',
                header: _t('% Util'),
                width: 50
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
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 60
            }]
        });
        ZC.DatabasePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('DatabasePanel', ZC.DatabasePanel);
ZC.registerName('Database', _t('Database'), _t('Databases'));

ZC.DBSrvInstPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'DBSrvInst',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'status'},
                {name: 'name'},
                {name: 'manufacturer'},
                {name: 'product'},
                {name: 'locking'},
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
                id: 'manufacturer',
                dataIndex: 'manufacturer',
                header: _t('Manufacturer'),
                renderer: render_link
            },{
                id: 'product',
                dataIndex: 'product',
                header: _t('Product'),
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
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 60
            }]
        });
        ZC.DBSrvInstPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('DBSrvInstPanel', ZC.DBSrvInstPanel);
ZC.registerName('DBSrvInst', _t('DB Server Instance'), _t('DB Server Instances'));

})();
