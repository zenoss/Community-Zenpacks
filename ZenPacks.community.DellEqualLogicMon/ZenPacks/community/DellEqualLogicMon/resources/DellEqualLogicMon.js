(function(){

var ZC = Ext.ns('Zenoss.component');

function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.DellEqualLogicStoragePoolPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'DellEqualLogicStoragePool',
            fields: [
                {name: 'uid'},
                {name: 'status'},
                {name: 'name'},
				{name: 'totalBytesString'},
				{name: 'usedBytesString'}
            ],
            columns: [{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true
            },{
                id: 'totalBytesString',
                dataIndex: 'totalBytesString',
                header: _t('Total bytes')
            },{
                id: 'usedBytesString',
                dataIndex: 'usedBytesString',
                header: _t('Used bytes')
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
        ZC.DellEqualLogicStoragePoolPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('DellEqualLogicStoragePoolPanel', ZC.DellEqualLogicStoragePoolPanel);
ZC.registerName('DellEqualLogicStoragePool', _t('StoragePool'), _t('Storage Pools'));

ZC.DellEqualLogicVolumePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
	config = Ext.applyIf(config||{}, {
	    componentType: 'Volume',
	    fields: [
		{name: 'uid'},
		{name: 'status'},
		{name: 'name'},
		{name: 'provisionedSizeString'},
		{name: 'reservedSizeString'},
		{name: 'isThinProvisioned'}
	    ],
	    columns: [{
		id: 'name',
		dataIndex: 'name',
		header: _t('Name'),
		sortable: true
	    },{
		id: 'provisionedSizeString',
		dataIndex: 'provisionedSizeString',
		header: _t('Provisioned Size')
	    },{
		id: 'reservedSizeString',
		dataIndex: 'reservedSizeString',
		header: _t('Reserved Size')
	    },{
		id: 'isThinProvisioned',
		dataIndex: 'isThinProvisioned',
		header: _t('Thin Provisioned')
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
        ZC.DellEqualLogicVolumePanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('DellEqualLogicVolumePanel', ZC.DellEqualLogicVolumePanel);
ZC.registerName('DellEqualLogicVolume', _t('Volume'), _t('Volumes'));

})();
