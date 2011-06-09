function start_oid_lookup() {
 var info= document.getElementById( "oid_lookup" );
 var oid= info.value;

 if( ! oid ) {
    return;
 }

 var oid_lookup_url= "/zport/showOID2XML?oid=" + oid;
 var req= getXMLHttpRequest();
 req.open( "GET", oid_lookup_url, true );
 sendXMLHttpRequest( req ).addCallback( process_XML_OID_lookup_response );
}



process_XML_OID_lookup_response= function(req) {
 var xml= req.responseXML;
 var output= xml.getElementsByTagName("stdout")[0];

 if( output ) {
    document.getElementById( "oid_result" ).value= unescape( output.textContent );

 } else {
    alert( "\nUnable to parse out 'stdout' element from server response\nTruncated XML response=\n" + req.responseText );
 }
}

