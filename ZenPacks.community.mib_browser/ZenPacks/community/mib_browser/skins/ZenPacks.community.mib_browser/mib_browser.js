//window.onload = initAll;
//YAHOO.util.Event.addListener( window, "load", initAll );
//YAHOO.util.Event.onAvailable( "mib_browser", initAll );
// YAHOO.util.Event.onAvailable( "mib_browser", mib_browser );
var isie= false;

/*
  Map of YAHOO.widget.TextNode instances in the TreeView instance.
 */

var oTextNodeMap= {};

/*
  The YAHOO.widget.TextNode instance whose "contextmenu"
  DOM event triggered the display of the
  ContextMenu instance.
*/
var oCurrentTextNode= null;
var oContextMenu= null;

var oTreeView= false;

/*
 * The following are XML document links to specific portions of the oid_detail iframe
 */
var oid_window= false;
var oid_form_action= false;
var oid_name= false;
var oid_access= false;
var oid_status= false;
var oid_node_type= false;
var oid_description= false;
var oid_number= false;

var mib_url= "";


/*
 * ===================================================================
 *    Function declarations
 */
function open_oid_window() {
 var start_x= screen.availHeight - 100;
 var start_y= 0;

 /* 
  * Open up a child window to store the OID info
  * but only if the window isn't already opened.

  *
  * TODO: Find out why this code doesn't actually detect issues.  Maybe register for a close event on the child window?
  *

  */
 if( ! oid_window || oid_window.closed ) {
     oid_window= window.open( "oid_details", "oid_details", "location=yes,scrollbars=yes,toolbar=no,status=no,resizable=no,width=250,height=275,left=" + start_x + ",top=" + start_y ); 

     oid_window.onload= find_oid_detail_xml_frags;
 }
}



function find_oid_detail_xml_frags() {
 var oid_page= oid_window.document;

 oid_name= oid_page.getElementById( "oid_name" );
 oid_access= oid_page.getElementById( "oid_access" );
 oid_status= oid_page.getElementById( "oid_status" );
 oid_node_type= oid_page.getElementById( "oid_node_type" );
 oid_description= oid_page.getElementById( "oid_description" );
 oid_number= oid_page.getElementById( "oid_number" );
 oid_form_action= oid_page.getElementById( "form_save_oid" );
}



function initAll() {
 var mib_info= document.getElementById("mib_id");
 mib_name= mib_info.getAttribute( "name" );
 mib_url= mib_info.getAttribute( "value" );

 var req= getXMLHttpRequest();
 //req.overrideMimeType( "text/xml" );
 req.open( "GET", mib_url, true );
 sendXMLHttpRequest( req ).addCallback( process_XML_MIB_response );

 if( window.ActiveXObject ) {
    // Start the browser-specific hacks here...
    isie= true;
 }

 open_oid_window();
}



function trim( text ) {
 return( text.replace( /(^\s*|\s*$)/, "" ) );
}



// Creates a TextNode instance and appends it to the TreeView
function build_tree_from_nodes( root_node, xml_nodes ) {
 var i, oid_value, node;
 var seen_nodes= { };
 var description= "";

 if( ! xml_nodes ) {
    return;
 }

 var node_list= xml_nodes.getElementsByTagName( "node" );
 for( i= 0; node_list[i] ; i++ ) {
     if( node_list[i].nodeType == 1 ) { // Ignore whitespace nodes
        next;
     }

     try {
       description= trim( unescape( node_list[i].getElementsByTagName( "description" )[0].firstChild.nodeValue ) );
     } catch(e) {
       description= "";
     }

     var node_data= {
             label: node_list[i].getAttribute( "name" ),
             // Tooltip will use the title attribute
             title: description,
             style: "mib_treeview_label"
     };

     oid_value= node_list[i].getAttribute( "oid" );

     var oid_array= oid_value.split( '.' );
     oid_array.pop();
     var prev_oid= oid_array.join('.');
     if( prev_oid in seen_nodes ) { // Found an exact match
         node = new YAHOO.widget.TextNode( node_data, seen_nodes[ prev_oid ], false);
         seen_nodes[ oid_value ]= node;

     } else {
         while( oid_array.length > 0 ) { // Look for sub-matches
            oid_array.pop();
            prev_oid= oid_array.join('.');
            if( prev_oid in seen_nodes ) {
                node = new YAHOO.widget.TextNode( node_data, seen_nodes[ prev_oid ], false);
                seen_nodes[ oid_value ]= node;
                break;
            }
         }
         if( oid_array.length == 0 ) { // no match at all (possibly first entry)
             node = new YAHOO.widget.TextNode( node_data, root_node, false);
             seen_nodes[ oid_value ]= node;
         }
     }

     node.data= node_list[i];
     oTextNodeMap[ node.labelElId ] = node;
 }

}



/*
  Adds a new TextNode as a child of the TextNode instance
  that was the target of the "contextmenu" event that
  triggered the display of the ContextMenu instance.
*/
function addNode() {
 var sLabel= window.prompt( "Enter a label for the new node: ", ""), oChildNode;

 if( sLabel && sLabel.length > 0 ) {                       
    oChildNode= new YAHOO.widget.TextNode( sLabel, oCurrentTextNode, false );

    oCurrentTextNode.refresh();
    oCurrentTextNode.expand();

    oTextNodeMap[ oChildNode.labelElId ]= oChildNode;
 }
}



/*
  Deletes the TextNode that was the target of the "contextmenu"
  event that triggered the display of the ContextMenu instance.
*/
function deleteNode() {
 var menu_oid= oCurrentTextNode.labelElId;
 if( menu_oid == "Nodes" || menu_oid == "Traps" ) {
    return;
 }

 delete oTextNodeMap[ oCurrentTextNode.labelElId ];

 oTreeView.removeNode( oCurrentTextNode );
 oTreeView.draw();
}



function snmpwalk_oid() {
  var menu_oid;
  var device, community, snmpVer;

 if( oCurrentTextNode ) {
    menu_oid= oCurrentTextNode.data.getAttribute( 'oid' );
 } else {
    return;
 }

 if( menu_oid == "Nodes" || menu_oid == "Traps" ) {
    return;
 }

 device= document.getElementById( "test_device" ).value;
 community= document.getElementById( "test_community" ).value;
//  This doesn't work - don't know why - JC
//snmpVer= document.getElementById( "test_snmp_ver" ).value;

 if( device == "" || community == "" ) {
    alert( "Need to define a test server and community string!" );
    /*
     * Ideally, there should be a way to set the focus to the
     * test settings tab so that the user has to do the minimum
     * amount of work.
     * TODO: reset focus to test settings tab
     */
    return;
 }

 var url= "/zport/snmpwalk?device=" + device + "&oid=" + menu_oid + "&community=" + community ;
// This doesn't work - don't know why - JC
// var url= "/zport/snmpwalk?device=" + device + "&oid=" + menu_oid + "&community=" + community + "&snmpVer=" + snmpVer;

 snmpwalk_window= window.open( url, oCurrentTextNode.label, "location=yes,scrollbars=yes,toolbar=no,status=no,resizable=yes,width=600,height=400" ); 
}



/*
  "contextmenu" event handler for the element(s) that
  triggered the display of the ContextMenu instance - used
  to set a reference to the TextNode instance that triggered
  the display of the ContextMenu instance.
*/
function onTriggerContextMenu( p_oEvent ) {
 var oTarget= this.contextEventTarget;

 if( oTarget.className == "mib_treeview_label" ) {
    oCurrentTextNode= oTextNodeMap[ oTarget.id ];

 } else { // Cancel the display of the ContextMenu instance.
    this.cancel();
 }
}



function add_root( root_label, root_description, xml_doc ) {
 var root_node= false;
 var o= {
        label: root_label,
        // Tooltip will use the title attribute
        title: root_description,
        style: "mib_treeview_label"
 };
 root_node= new YAHOO.widget.TextNode(o, oTreeView.getRoot(), false);

 /*
   Add the TextNode instance to the map, using its
   HTML id as the key.
  */
 oTextNodeMap[ root_node.labelElId ]= root_node;                   

 try {
   build_tree_from_nodes( root_node, xml_doc );
 } catch(e) {
   alert( "Failed to create tree for " + root_label + " because " + e.message );
 }
}



function display_oid_data( node ) {
 var this_node= node.data;
 var temp;
 var oid_save_url= "";

 /* ...  Just in case the user closed it... ... */
 open_oid_window();

 /*
  * IE7 doesn't deal with onload events properly
  */
 find_oid_detail_xml_frags();
 oid_name.value= node.label;
 oid_number.value= this_node.getAttribute( 'oid' );
 temp= this_node.getAttribute( 'access' );
 if( ! temp ) {
    oid_access.value= "";
 } else {
    oid_access.value= temp;
 }

 temp= this_node.getAttribute( 'status' );
 if( ! temp ) {
    oid_status.value= "";
 } else {
    oid_status.value= temp;
 }

 temp= this_node.getAttribute( 'type' );
 if( ! temp ) {
    oid_node_type.value= "";
 } else {
    oid_node_type.value= temp;

   /*
    * At this point we can determine the path to use in
    * order to invoke zmanage_ediProperties
    */
   if( temp == "notification" ) {
      oid_save_url= mib_url.replace( /showMibasXML/, "notifications/" + node.label  );
      oid_form_action.setAttribute( "action", oid_save_url );
   } else {
      oid_save_url= mib_url.replace( /showMibasXML/, "nodes/" + node.label  );
      oid_form_action.setAttribute( "action", oid_save_url );
   }
 }

 try {
   oid_description.value= trim( unescape( this_node.getElementsByTagName("description")[0].firstChild.nodeValue ) );
 } catch(e) {
   oid_description.value= "";
 }

 oid_window.focus();
}


function mib_browser( xml_doc ) {
 // Create a TreeView instance
 oTreeView= new YAHOO.widget.TreeView( "mib_browser" );
 var nodes, traps;

 nodes= xml_doc.getElementsByTagName( "nodes" )[0];
 add_root( "Nodes", "Root of the MIB", nodes );

 traps= xml_doc.getElementsByTagName( "notifications" )[0];
 add_root( "Traps", "Notifications sent from the MIB agent", traps );

 oTreeView.draw();

 var context_menu_options= {
       trigger: "mib_browser",
       lazyload: true,
       itemdata: [
                  { text: "snmpwalk", onclick: { fn: snmpwalk_oid } }
                  //{ text: "Add Child Node", onclick: { fn: addNode } },
                  //{ text: "Delete Node", onclick: { fn: deleteNode } }
                  ] 
 };

 /*
   Instantiate a ContextMenu:  The first argument passed to
   the constructor is the id of the element to be created; the
   second is an object literal of configuration properties.
  */
 oContextMenu= new YAHOO.widget.ContextMenu( "mytreecontextmenu", context_menu_options );

 oContextMenu.subscribe( "triggerContextMenu", onTriggerContextMenu);

 /* ...  Hack to make things appear properly on IE7  ... */
 oContextMenu.cfg.setProperty( "zindex", 10 );


 /*
  *  Subscribe to the onlick event so that we get called whenever someone clicks on an item
  */
 oTreeView.subscribe( "labelClick", display_oid_data );
}





function display_MIB( doc ) {
 var module= false;

 module= doc.getElementsByTagName("module")[0];
 try {
       document.getElementById("mib_name").value= module.getAttribute( "name" );
 } catch(e) {}

 try {
       document.getElementById("language").value= module.getAttribute( "language" );
 } catch(e) {}

 try {
       document.getElementById("contact").value= trim( unescape(module.getElementsByTagName("contact")[0].firstChild.nodeValue ));
 } catch(e) {}

 try {
       document.getElementById("description").value= trim( unescape( module.getElementsByTagName("description")[0].firstChild.nodeValue ) );
 } catch(e) {}

 mib_browser( doc )
}



process_XML_MIB_response= function(req) {

 var xml= req.responseXML;
 var nodelist= xml.getElementsByTagName("smi")[0];

 if( nodelist ) {
    display_MIB( nodelist );

 } else {
    alert( "\nUnable to parse out 'smi' element from server response\nTruncated XML response=\n" + req.responseText );
 }
}

