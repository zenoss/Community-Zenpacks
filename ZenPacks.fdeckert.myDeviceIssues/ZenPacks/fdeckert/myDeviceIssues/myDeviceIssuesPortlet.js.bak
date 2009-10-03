var myDeviceIssuesPortlet = Subclass.create(YAHOO.zenoss.portlet.Portlet);
myDeviceIssuesPortlet.prototype = {
    __class__:"YAHOO.zenoss.portlet.myDeviceIssuesPortlet",
    __init__: function(args) {
        args = args || {};
        id = 'id' in args? args.id : getUID('mydevissues');
        datasource = 'datasource' in args? args.datasource :
            new YAHOO.zenoss.portlet.TableDatasource({

                            // Query string will never be that long, so GET
                            // is appropriate here
                            method:'GET',

                            // Here's where you call the back end method
                            url:'/zport/getmyDeviceIssuesJSON',

                            // Set up the path argument and set a default ReportClass
                            queryArguments: {'path':'/Devices'}
                        });
        bodyHeight = 'bodyHeight' in args? args.bodyHeight :
            200;
        title = 'title' in args? args.title:"my Device Issues";
        refreshTime = 'refreshTime' in args? args.refreshTime : 60;
        this.superclass.__init__(
            {id:id, title:title, 
             datasource:datasource, 
             refreshTime: refreshTime,
             bodyHeight:bodyHeight}
        );
        this.buildSettingsPane();
    },
    buildSettingsPane: function() {
        s = this.settingsSlot;
        this.locsearch = new YAHOO.zenoss.zenautocomplete.DevAndEventObjectSearch(
            'Zenoss Objects', s);
        addElementClass(this.locsearch.container, 'portlet-settings-control');
    },
    submitSettings: function(e, settings) {
                    // Get your ReportClass value and put it in the datasource
                    var mypath = this.locsearch.input.value;
                    this.datasource.queryArguments.path = mypath;

                    this.titleInput.value="my Device Issues " + mypath;

                    // Call Portlet's submitSettings
                    this.superclass.submitSettings(e, {'queryArguments':
                        {'path': mypath} 
                    }); 
    }
}
YAHOO.zenoss.portlet.myDeviceIssuesPortlet = myDeviceIssuesPortlet;
