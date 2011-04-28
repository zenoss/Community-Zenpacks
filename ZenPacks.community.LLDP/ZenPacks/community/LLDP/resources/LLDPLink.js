(function() {

var ZC = Ext.ns('Zenoss.component');
function render_link(ob) {
    if (ob && ob.uid) {
        /* we also need a name! */
        if (ob.name) {
            name = ob.name;
        } else {
            /* extract from object */
            var parts = ob.uid.split('/');
            name = parts[parts.length-1];
        }
        return Zenoss.render.link(ob.uid,null,name);
    } else {
        return ob;
    }
}
 


ZC.LLDPLinkPanel = Ext.extend(ZC.ComponentGridPanel, {
	constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'LLDPLink',
            autoExpandColumn: 'remoteInterface',
            fields: [
                {name: 'uid'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locPortDesc'},
                {name: 'remSysName'},
                {name: 'remPortDesc'},
                {name: 'remMgmtAddr'},
                {name: 'localInterface'},
                {name: 'remoteInterface'},
                {name: 'remoteDevice'},
            ],
            columns: [{
                id: 'localInterface',
                dataIndex: 'localInterface',
                header: _t('localInterface'),
		width: 150,
		renderer: render_link
            },{
                id: 'remoteDevice',
                dataIndex: 'remoteDevice',
                header: _t('remoteDevice'),
		width: 150,
		renderer: render_link
            },{
                id: 'remoteInterface',
                dataIndex: 'remoteInterface',
                header: _t('remoteInterface'),
		renderer: render_link
            }]
        });
        ZC.LLDPLinkPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('LLDPLinkPanel', ZC.LLDPLinkPanel);


}());
