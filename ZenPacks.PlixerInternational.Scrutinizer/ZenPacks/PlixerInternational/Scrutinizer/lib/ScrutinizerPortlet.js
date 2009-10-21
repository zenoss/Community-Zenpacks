var ScrutinizerDatasource = Class.create();

ScrutinizerDatasource.prototype = {
    __class__ : "YAHOO.zenoss.portlet.ScrutinizerDatasource",
    __init__: function(settings) {
        this.baseLoc = settings.baseLoc;
    },
    get: function(callback) {
        this.callback = callback;
		var url = this.baseLoc;
        html = '<iframe src="' + url + '" ' +
               'style="border:medium none;margin:0;padding:0;'+
               'width:100%;height:100%;"/>';
        callback({responseText:html});
    }
}
YAHOO.zenoss.portlet.ScrutinizerDatasource = ScrutinizerDatasource;

var ScrutinizerPortlet = YAHOO.zenoss.Subclass.create(
    YAHOO.zenoss.portlet.Portlet);
ScrutinizerPortlet.prototype = {
    __class__: "YAHOO.zenoss.portlet.ScrutinizerPortlet",
    __init__: function(args) {
        args = args || {};
        id = 'id' in args? args.id : getUID('Scrutinizer');
        baseLoc = 'baseLoc' in args? args.baseLoc : "http://scrutinizer.plixer.com/gadgets/scrut_nba_volume.cgi?standalone=1";
        bodyHeight = 'bodyHeight' in args? args.bodyHeight : 400;
        title = 'title' in args? args.title: "Site Window";
        refreshTime = 'refreshTime' in args? args.refreshTime : 60;
	miscthing = 'miscthing' in args? args.miscthing: "miscthing";
        this.mapobject = null;
        var datasource = 'datasource' in args? 
            args.datasource:
            new YAHOO.zenoss.portlet.ScrutinizerDatasource(
                {'baseLoc':baseLoc?baseLoc:''});
        this.superclass.__init__(
            {id:id, title:title, refreshTime:refreshTime, miscthing:miscthing,
            datasource:datasource, bodyHeight:bodyHeight}
        );
        this.buildSettingsPane();
    },
    buildSettingsPane: function() {
        s = this.settingsSlot;
        this.locsearch = YAHOO.zenoss.zenautocomplete.LocationSearch(
            'URL (http://scrutinizer.plixer.com/gadgets/scrut_nba_volume.cgi?standalone=1)', s);
        addElementClass(this.locsearch.container, 
                        'portlet-settings-control');
    },
    submitSettings: function(e, settings) {
        baseLoc = this.locsearch.input.value;
        if (baseLoc.length<1) baseLoc = this.datasource.baseLoc;
        this.locsearch.input.value = '';
        this.superclass.submitSettings(e, {'baseLoc':baseLoc});
    },
    startRefresh: function(firsttime) {
        if (!firsttime) this.mapobject.refresh();
        if (this.refreshTime>0)
            this.calllater = callLater(this.refreshTime, this.startRefresh);
    }

}
YAHOO.zenoss.portlet.ScrutinizerPortlet = ScrutinizerPortlet;
