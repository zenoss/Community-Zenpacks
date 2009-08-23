var _getAllReportOrganizers = function(callback) {
    var payload=[];
    var cur;
    function getReportOrganizer(newpayload) {
	var d = loadJSONDoc('/zport/dmd/Reports/getOrganizerNames');
        d.addCallback (function (p) {
	    for (var i = 0; i < p.length; i++){ 
                path=p[i];
	        var d1 = loadJSONDoc('/zport/getJSONReportList?path='+path);
		d1.addCallback (function (path, p) {
			for (var i = 0; i < p.length; i++){
				payload.push (path+"/"+p[i]);
			}
		}, path
		);
	    } 
            payload.sort();
            callback(payload);
        });
    }
    getReportOrganizer([]);
}

YAHOO.zenoss.zenautocomplete.Reports = Subclass.create(
    YAHOO.zenoss.zenautocomplete.ZenAutoComplete);
YAHOO.zenoss.zenautocomplete.Reports.prototype = {
    __init__: function(label, container) {
        bindMethods(this);
        this.target = $(container);
        this.label = label;
        this.setup();
        _getAllReportOrganizers(this.makeAutoCompleter);
    }
}
YAHOO.register('zenautocompletereports', YAHOO.zenoss.zenautocomplete.Reports, {});

YAHOO.zenoss.portlet.StaticDatasource.Table = Subclass.create(
    YAHOO.zenoss.portlet.StaticDatasource);
YAHOO.zenoss.portlet.StaticDatasource.Table.prototype = {
    __class__: "YAHOO.zenoss.portlet.StaticDatasource.Table",
    __init__: function(settings) {
        this.postContent = settings.postContent;
        this.superclass.__init__(
            {settings:settings,
             html:settings.html
            });
    }
} 
YAHOO.register('staticdatasourcetable', YAHOO.zenoss.portlet.StaticDatasource.Table, {});

var FavoriteReportsPortlet = YAHOO.zenoss.Subclass.create(
                YAHOO.zenoss.portlet.Portlet);
    FavoriteReportsPortlet.prototype = {
    __class__:"YAHOO.zenoss.portlet.FavoriteReportsPortlet",
    __init__: function(args) {
        args = args || {};
        id = 'id' in args? args.id : getUID('FavoriteReports');
        title = 'title' in args? args.title: "Favorite Reports",
	b=args.datasource;
        datasource = 'datasource' in args? args.datasource : new YAHOO.zenoss.portlet.StaticDatasource.Table (
		{html:'', postContent: [] }
		);
        bodyHeight = 'bodyHeight' in args? args.bodyHeight:200;
        refreshTime = 'refreshTime' in args? args.refreshTime: 60;
        this.superclass.__init__(
            {id:id,
             title:title,
             datasource:datasource,
             refreshTime: refreshTime,
             bodyHeight: bodyHeight
            }
        );
        this.buildSettingsPane();
    },
    buildSettingsPane: function() {
        s = this.settingsSlot;
        loc = new YAHOO.zenoss.zenautocomplete.Reports('Zenoss Reports', s);
        this.locsearch = loc;
        addElementClass(this.locsearch.container, 'portlet-settings-control');
    },
    submitSettings: function(e, settings) {
        var postContent = settings?settings.postContent:
                          this.datasource.postContent;
        var newob = this.locsearch.input.value;
        if (findValue(postContent, newob)<0) {
            if (newob.length>0) postContent.push(newob);
            this.superclass.submitSettings(e, {'postContent':postContent});
        }
        this.locsearch.input.value = '';
    },
    fillTable: function(contents) {
        var columnDefs = contents.columnDefs;
        var dataSource = contents.dataSource;
        i=0;
        forEach(dataSource.liveData, bind(function(x){
            var removelink = "<a id='"+this.id+"_row_"+i+
                         "' class='removerowlink'"+
                         " title='Stop watching this object'>" +
                         "X</a>";
            x['Object'] = removelink + x['Object'];
            i++;
        }, this));
        var oConfigs = {};
        addElementClass(this.body, 'yui-skin-sam');
        if (this.dataTable) {
            this.dataTable.initializeTable(dataSource.liveData);
        } else {
            var myDataTable = new YAHOO.widget.DataTable(
                this.body, columnDefs, dataSource, oConfigs);
            this.dataTable = myDataTable;
        }
        forEach(this.dataTable.getRecordSet().getRecords(), bind(function(x){
            var row = this.dataTable.getTrEl(x);
            var link = getElementsByTagAndClassName('a','removerowlink',row)[0];
            connect(link, "onclick", method(this,
                function(){this.deleteRow(x);}));
        }, this));
    },
    fill: function(contents) {
        if (this.body) { 
            if (contents.responseText) {
                contents = contents.responseText;
            }
        var oConfigs = {};
        addElementClass(this.body, 'yui-skin-sam');
	var columnDefs = [ {key:"name", label:"Reports"}, ];
	var data=Array();
        for (var i = 0; i < this.datasource.postContent.length; i++){
                url=escape("/zport/dmd/Reports"+this.datasource.postContent[i]);
                parts=this.datasource.postContent[i].split("/");
                removelink="<a id='reports_row_"+i+
                         "' class='removerowlink'"+
                         " title='Remove this favorite'>" +
                         "X</a>";
                short=parts[parts.length-1];
		data[i] = Array (removelink+"<a class=\"prettylink\" href=\""+url+"\" title=\""+this.datasource.postContent[i]+"\">"+short+"</a>");
	}

	
        if ('dataSource' in this) {
		this.dataSource.liveData = data;
        } else {
		var dataSource = new YAHOO.util.DataSource(data);
		dataSource.responseSchema = {fields:["name"]}; 
		dataSource.responseType = YAHOO.util.DataSource.TYPE_JSARRAY;
		this.dataSource = dataSource;
        }

/*
        if (this.dataTable) {
            this.dataTable.initializeTable(this.dataSource.liveData);
        } else {
*/
            var myDataTable = new YAHOO.widget.DataTable(this.body, columnDefs, this.dataSource, oConfigs);
            this.dataTable = myDataTable;
/*
	}
*/

        forEach(this.dataTable.getRecordSet().getRecords(), 
		bind(function(x){
			var row;
			if (x._nCount == 0)
				row = this.dataTable.getTrEl(0);
			else
				row = this.dataTable.getTrEl(x);

			if (row != null) {
				var link = getElementsByTagAndClassName('a','removerowlink',row)[0];
				connect(link, "onclick", method(this,
					function(){ this.deleteRow(x); })
					);
			}
        		}, this
		)
	);

        }
    },  
    deleteRow: function(record) {
        var data = record.getData().name;
        var regex = /title="(.*)"/;
        var name = data.match(regex);
        var myarray = this.datasource.postContent;
        myarray.splice(findValue(myarray, name[1]), 1);
        this.submitSettings(null, {'postContent':myarray});
    }
}
YAHOO.zenoss.portlet.FavoriteReportsPortlet = FavoriteReportsPortlet;
