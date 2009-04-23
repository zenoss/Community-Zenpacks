var SiteWindowDatasource = Class.create();

SiteWindowDatasource.prototype = {
    __class__ : "YAHOO.zenoss.portlet.SiteWindowDatasource",
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
YAHOO.zenoss.portlet.SiteWindowDatasource = SiteWindowDatasource;

var myEventViewsPortlet = YAHOO.zenoss.Subclass.create(
    YAHOO.zenoss.portlet.Portlet);
myEventViewsPortlet.prototype = {
    __class__: "YAHOO.zenoss.portlet.myEventViewsPortlet",
    __init__: function(args) {
        args = args || {};
        id = 'id' in args? args.id : getUID('myeventviews');
        baseLoc = 'zport/dmd/ZenPackManager/packs/ZenPacks.fdeckert.myeventviews/myEventViews'
        bodyHeight = 'bodyHeight' in args? args.bodyHeight : 400;
        title = 'title' in args? args.title: "myEventViews";
        refreshTime = 'refreshTime' in args? args.refreshTime : 60;
	miscthing = 'miscthing' in args? args.miscthing: "miscthing";
        this.mapobject = null;
        var datasource = 'datasource' in args? 
            args.datasource:
            new YAHOO.zenoss.portlet.SiteWindowDatasource(
                {'baseLoc':baseLoc?baseLoc:''});
        this.superclass.__init__(
            {id:id, title:title, refreshTime:refreshTime, miscthing:miscthing,
            datasource:datasource, bodyHeight:bodyHeight}
        );
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
YAHOO.zenoss.portlet.myEventViewsPortlet = myEventViewsPortlet;
