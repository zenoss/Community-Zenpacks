var ZenOLGeoMap = YAHOO.zenoss.Class.create();

var GLOB_MARKERS = [];
 
ZenOLGeoMap.prototype = {
    __init__: function(container){
        this.lock = new DeferredLock();
        OpenLayers.ImgPath = 'oltheme/';
        this.map = new OpenLayers.Map(container,
                    {   //maxResolution: 0.703125, 
                        controls: [
                            new OpenLayers.Control.PanZoom(),
                            new OpenLayers.Control.MouseDefaults(),
                            //new OpenLayers.Control.Navigation(),
                            //new OpenLayers.Control.NavToolbar(), 
                            //new OpenLayers.Control.PanZoomBar(),
                            //new OpenLayers.Control.MouseToolbar(),
                            //new OpenLayers.Control.LayerSwitcher({'ascending':false}),
                            //new OpenLayers.Control.Permalink(),
                            //new OpenLayers.Control.ScaleLine(),
                            //new OpenLayers.Control.Permalink('permalink'),
                            new OpenLayers.Control.MousePosition(),
                            //new OpenLayers.Control.OverviewMap(),
                            new OpenLayers.Control.KeyboardDefaults()
                        ],
                        theme: 'oltheme/style.css',
                        'maxZoomLevel': 18
                    }
        );
        OpenLayers.Tile.Image.prototype.checkImgURL  = function() {}
        OpenLayers.Util.onImageLoadError = function() {  
        this.style.display = "";
        this.src="nodata.png";
        } 

        //var baseMapLayer = new OpenLayers.Layer.WMS( "NASA Global Mosaic", "http://t1.hypercube.telascience.org/cgi-bin/landsat7", 
        //                                         {layers: "landsat7"});
        //this.map.addLayer(baseMapLayer);
  

        //var bgMapLayer  = new OpenLayers.Layer.MapServer( "OpenLayers WMS", 
        //            "http://10.10.210.200/cgi-bin/vmap",
        //            {
        //                layers: 'countries, bg',  
        //                format: 'image/png', 
                        //transparent: 'TRUE',
                        //resolutions: [0.703125,0.3515625,0.17578125,0.087890625,0.0439453125]
        //            },
        //            {
        //                'numZoomLevels': 18
        //            } 
                    //{reproject:false, isBaseLayer: false}
        //); 
        //this.map.addLayer(bgMapLayer);


        // var sofiaMapLayer  = new OpenLayers.Layer.WMS( "sfmap", 
                    // "http://10.10.210.200/cgi-bin/tilecache.cgi?", {
                        // layers: 'sfmap', 
                        // format: 'image/png', 
                        //transparent: 'TRUE'
                    // },
                    // {
                        // isBaseLayer: false
                    // }); 
 
        // this.map.addLayer(sofiaMapLayer);

        //var world = new OpenLayers.Layer.WMS(
        //         "World Map",
        //         "http://world.freemap.in/cgi-bin/mapserv",
        //         {
        //            map: '/www/freemap.in/world/map/factbooktrans.map',
        //            transparent: 'TRUE',
        //            layers: 'factbook',
        //           resolutions: [0.703125,0.3515625,0.17578125]
        //         }//,
        //         {
        //                isBaseLayer: false
        //         }
        //    );
        //this.map.addLayer(world);

        var ol_wms = new OpenLayers.Layer.WMS(
                "OpenLayers WMS",
                "http://labs.metacarta.com/wms/vmap0",
                {layers: 'basic'}
        );

        this.map.addLayer(ol_wms);



        this.vectorLayer = new OpenLayers.Layer.Vector("Connections");
        this.map.addLayer(this.vectorLayer);
        
        this.markers = new OpenLayers.Layer.Markers("markers");
        this.map.addLayer(this.markers);
        
        bindMethods(this);
    },
    clearAll: function() {
        for(var n in GLOB_MARKERS) {
            this.markers.removeMarker(GLOB_MARKERS[n]);               
        }

        for (var i = (this.map.popups.length-1); i >= 0; --i) {
            this.map.removePopup(this.map.popups[i]);
        }

        this.vectorLayer.destroyFeatures();

        GLOB_MARKERS = [];
    },
    parseLonLat: function(address) {
        var lon = 0;
        var lat = 0;
        
        var data = address.split(",")
        
        if(data[0] && data[1]) 
        {
            lat = parseFloat(data[0]);
            lon = parseFloat(data[1]);
        }
        return new OpenLayers.LonLat(lon,lat); 
    },
    Dot: function(p, color) {
        var colors = ['green', 'grey', 'blue', 'yellow', 'orange', 'red'];
        var severity = findValue(colors, color);
        var newsize = 16 + severity;

        var icon_size = new OpenLayers.Size(newsize,newsize);
        var calculateOffset = function(size) {
                        return new OpenLayers.Pixel(-(size.w/2), -(size.h/2)); };
        var icon = new OpenLayers.Icon("img/"+color+"_dot.png", 
                                       icon_size, null, calculateOffset);
        return new OpenLayers.Marker(p, icon);
    },
    addPolyline: function(addresses) {
        var addys = addresses[0];
        var severity = addresses[1];
        var colors = ['#00ff00', '#888888', '#0000ff', '#ffd700', 
                      '#ff8c00', '#ff0000']
        var color = colors[severity];
        var style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);        
        style.strokeColor = color; 
        style.fillColor = color; 
        var points = []
        var lock = new DeferredLock();
        var lock2 = new DeferredLock();
        var addadd = bind(function(address){
            var d = lock.acquire();
            d.addCallback(bind(function(p){
                        var latlon = this.parseLonLat(address);
                        var point = new OpenLayers.Geometry.Point(latlon.lon, latlon.lat);
                        points.push(point);
                        if(points.length==addys.length){
                            if (lock2.locked) lock2.release();
                        }
                        lock.release();   
            }, this));
        }, this);
        var e = lock2.acquire();
        e.addCallback(bind(function(){
            for(var p in addys)
            {
                addadd(addys[p]);
            }
        }, this));
        var f = lock2.acquire();
        f.addCallback(bind(function(p){
            var lineFeature = new OpenLayers.Feature.Vector(
                                    new OpenLayers.Geometry.LineString(points),null,style);
            this.vectorLayer.addFeatures([lineFeature]);
            lineFeature.layer.drawFeature(lineFeature);
            lock2.release();
        }, this));
    },
    addMarkers: function(nodedata){
        var ready_markers = [];
        var nummarkers = 0;
        var nodelen = nodedata.length;

        function makeMarker(node) {
            var address = node[0];
            var color = node[1];
            var clicklink = node[2].replace(
                'locationGeoMap',
                'OLGeoMap'
            );
            var summarytext = node[3];

            if (address) 
            {
                var lonlat = this.parseLonLat(address); 
                var marker = this.Dot(lonlat, color);
                nummarkers += 1;
                
                marker.events.register('mousedown', marker, function(evt) {
                                if (clicklink.search('GeoMap')>0){
                                    location.href = clicklink;
                                } else {
                                    currentWindow().parent.location.href = clicklink;
                                }
                                OpenLayers.Event.stop(evt); });
            
                var feature = new OpenLayers.Feature(this.markers, lonlat); 
                feature.popupClass = OpenLayers.Popup.Anchored;
                feature.data.popupContentHTML = summarytext;
                
                marker.events.register('mouseover', feature, function (evt) {
                        var popup = this.createPopup(false);
                        popup.size = new OpenLayers.Size(320,100);
                        this.layer.map.addPopup(popup,true);
                        this.popup.show();
                        OpenLayers.Event.stop(evt);
                });

                marker.events.register('mouseout', feature, function (evt) {
                        this.popup.hide();
                        OpenLayers.Event.stop(evt);
                });
                
                ready_markers.push(marker);
                GLOB_MARKERS.push(marker);
            } else { nummarkers += 1 }
        }
        var makeMarker = method(this, makeMarker);
        
        for ( var cnt in nodedata )
        {
            makeMarker(nodedata[cnt]); 
        }
        
        function checkMarkers() 
        {
            if (nodelen == nummarkers) 
            {   
                for ( var cnt in ready_markers )
                {
                    this.markers.addMarker(ready_markers[cnt]); 
                }
            } 
            else
            {
                try {this.markerchecking.cancel()}catch(e){noop();}
                this.markerchecking = callLater(0.2, checkMarkers);
            }
        }
        var checkMarkers = method(this, checkMarkers);
        checkMarkers();
    },
    doDraw: function(results) {
        var nodedata = results.nodedata;
        var linkdata = results.linkdata;

        this.clearAll();

        this.addMarkers(nodedata);

        for (var j=0;j<linkdata.length;j++) {
            this.addPolyline(linkdata[j]);
        }
        
        this.map.zoomToExtent(this.markers.getDataExtent());
    },
    refresh: function() {
        var results = {
            'nodedata':[],
            'linkdata':[]
        };
        var myd = loadJSONDoc('getChildGeomapData');
        myd.addCallback(function(x){results['nodedata']=x});
        var myd2 = loadJSONDoc('getChildLinks');
        myd2.addCallback(function(x){results['linkdata']=x});
        var bigd = new DeferredList([myd, myd2], false, false, true);
        bigd.addCallback(method(this, function(){this.doDraw(results)}));
    }
}

function olgeomap_initialize(){

    var x = new ZenOLGeoMap($('olgeomapcontainer'));
    connect(currentWindow(), 'onunload', x.map.destroy);

    addElementClass($('olgeomapcontainer'), "yui-skin-sam");

    x.refresh();
}

addLoadEvent(function() {
    var loader = YAHOO.zenoss.getLoader(); //New since 2.2.3
    loader.require("container");
    loader.insert({onSuccess:olgeomap_initialize})
});

