var ShowGraphPortlet = YAHOO.zenoss.Subclass.create(
                YAHOO.zenoss.portlet.Portlet);
            ShowGraphPortlet.prototype = {

                // Define the class name for serialization
                __class__:"YAHOO.zenoss.portlet.ShowGraphPortlet",

                // __init__ is run on instantiation (feature of Class object)
                __init__: function(args) {

                    // args comprises the attributes of this portlet, restored
                    // from serialization. Take them if they're defined,
                    // otherwise provide sensible defaults.
                    args = args || {};
                    id = 'id' in args? args.id : getUID('ShowGraph');
                    title = 'title' in args? args.title: "Graphs";
                    bodyHeight = 'bodyHeight' in args? args.bodyHeight:200;

                    // You don't need a refresh time for this portlet. In case
                    // someone wants one, it's available, but default is 0
                    refreshTime = 'refreshTime' in args? args.refreshTime: 60;

                    // The datasource has already been restored from
                    // serialization, but if not make a new one.
                    datasource = 'datasource' in args? args.datasource :
                        new YAHOO.zenoss.portlet.TableDatasource({

                            // Query string will never be that long, so GET
                            // is appropriate here
                            method:'GET',

                            // Here's where you call the back end method
                            url:'/zport/getJSONGraphList',

                            // Set up the path argument and set a default ReportClass
//                            queryArguments: {'path':'/Device Reports'} 
			    queryArguments: {'path':'/Device Reports' , 'report':'test'} 
                        });


                    // Call Portlet's __init__ method with your new args
                    this.superclass.__init__(
                        {id:id, 
                         title:title,
                         datasource:datasource,
                         refreshTime: refreshTime,
                         bodyHeight: bodyHeight
                        }
                    );

                    // Create the settings pane for the portlet
                    this.buildSettingsPane();
                },

                // buildSettingsPane creates the DOM elements that populate the
                // settings pane.
                buildSettingsPane: function() {

                    // settingsSlot is the div that holds the elements
                    var s = this.settingsSlot;

                    // Make a function that, given a string, creates an option
                    // element that is either selected or not based on the
                    // settings you've already got.
                    var getopt = method(this, function(x) { 
                        opts = {'value':x};
                        path = this.datasource.queryArguments.path;
                        if (path==x) opts['selected']=true;
                        return OPTION(opts, x); });
		    var getopt2 = method(this, function(x) { 
                        opts = {'value':x};
                        report = this.datasource.queryArguments.report;
                        if (report==x) opts['selected']=true;
                        return OPTION(opts, x); });


                    // Create the select element
		    this.pathselect = SELECT(null, null);
		    connect(this.pathselect,'onchange',update_select);
		    this.graphselect = SELECT(null,null);
		    path = this.datasource.queryArguments.path;

                    // A function to create the option elements from a list of
                    // strings
                    var createOptions = method(this, function(jsondoc) {
                        forEach(jsondoc, method(this, function(x) {
                            opt = getopt(x);
                            appendChildNodes(this.pathselect, opt);
                        }));
                    });
		    var createOptions2 = method(this, function(jsondoc) {
                        forEach(jsondoc, method(this, function(x) {
                            opt = getopt2(x);
                            appendChildNodes(this.graphselect, opt);
                        }));
                    });



                    // Wrap these elements in a DIV with the right CSS class,
                    // and give it a label, so it looks pretty
                    mycontrol = DIV({'class':'portlet-settings-control'}, [
                            DIV({'class':'control-label'}, 'Report Class'),
                             this.pathselect
                           ],[
                            DIV({'class':'control-label'}, 'Reports'),
                             this.graphselect
			   ]);

                    // Put the thing in the settings pane
                    appendChildNodes(s, mycontrol);

                    // Go get the strings that will populate your select element.
                    d = loadJSONDoc('/zport/dmd/Reports/getOrganizerNames');
                    d.addCallback(method(this, createOptions));
                    d1 = loadJSONDoc('/zport/getJSONReportList?path='+path);
                    d1.addCallback(method(this, createOptions2));
		    var graphselect2;
		    var graphselect=this.graphselect;
		    function update_select()
		    {
		        var childs=new Array;
		        var path=this.value;
		        var createOptions3 = method(this, function(jsondoc) {
                        forEach(jsondoc, method(this, function(x) {
                            opt = getopt2(x);
			    childs.push(opt);
                        })
			);
			replaceChildNodes(graphselect,childs);
                    });
                    	d1 = loadJSONDoc('/zport/getJSONReportList?path='+path);
                    	d1.addCallback(method(this, createOptions3));
		    }
                },

                // submitSettings puts the current values of the elements in
                // the settingsPane into their proper places.
                submitSettings: function(e, settings) {

                    // Get your ReportClass value and put it in the datasource
                    var mypath = this.pathselect.value;
                    var myreport = this.graphselect.value;
                    this.datasource.queryArguments.path = mypath;
                    this.datasource.queryArguments.report = myreport;

                    // Call Portlet's submitSettings
                    this.superclass.submitSettings(e, {'queryArguments':
                        {'path': mypath, 'report': myreport}
                    });
                }
            }
            YAHOO.zenoss.portlet.ShowGraphPortlet = ShowGraphPortlet;
