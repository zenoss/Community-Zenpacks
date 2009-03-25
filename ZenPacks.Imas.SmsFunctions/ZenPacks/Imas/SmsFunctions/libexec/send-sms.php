#!/usr/bin/php -q
<?php


$DB_Server="localhost";
$mysql_user="zenoss";
$mysql_passwd="zenoss";
$logfile="send-sms.log";



$ZENHOME=getenv('ZENHOME');



$verbose=0;
$logfile="$ZENHOME/log/$logfile";
$fh = fopen($logfile, 'a');

// Connect to the database
mysql_connect("$DB_Server", "$mysql_user", "$mysql_passwd") or die(mysql_error());

// include the command line parser class file
include ("Getopt.php");
// initialize object
$cg = new Console_Getopt();
// define list of allowed options
$allowedShortOptions = "v"; 
$allowedLongOptions = array("verbose", "component==" ,"action=", "sendsms=", "sendsms1=", "sendto=", "sendto1=", "monitortime=", "monitortime1=", "manageip=", "id=", "evid=" , "summary=="); 
// read the command line
$args = $cg->readPHPArgv(); 
// get the options
$ret = $cg->getopt($args, $allowedShortOptions, $allowedLongOptions); 
// check for errors and die with an error message if there was a problem
if (PEAR::isError($ret)) {
    die ("Error in command line: " . $ret->getMessage() . "\n");
}

// now parse the options array
$opts = $ret[0];
if (sizeof($opts) > 0) {
    // if at least one option is present
    // iterate over option list
    // assign option values to PHP variables
    foreach ($opts as $o) {
        switch ($o[0]) {
            case '--action':
                $action = $o[1];
                break;
            case '--sendsms':
                $cSend_sms = $o[1];
                break;
            case '--sendsms1':
                $cSend_sms_1 = $o[1];
                break;
            case '--sendto':
                $cSMS_Send_To = $o[1];
                break;
            case '--sendto1':
                $cSMS_Send_To_1 = $o[1];
		break;
	    case '--component':
		$component = $o[1];
                break;
            case '--monitortime':
                $cMonitor_Time = $o[1];
                break;
            case '--monitortime1':
                $cMonitor_Time_1 = $o[1];
                break;
            case '--manageip':
                $dev_manageIp = $o[1];
                break;
            case '--id':
                $dev_id = $o[1];
                break;
            case '--evid':
                $evt_evid = $o[1];
                break;
            case '--summary':
                $evt_summary = $o[1];
                break;
	    case 'v':
  		$verbose=1;
		break;
        }
    }
}
else {
    die("Error: No arguments supplied use --help to see the values\n");
} 






//let's look up which mobile to use for contact 0
$result = mysql_query("select * from `smsd`.`$cSMS_Send_To` WHERE Oncall='1'");

if ( $result == "" ) {
    $system="Direct Phone";
    $number=$cSMS_Send_To;
    $name = "Unknown";
    $result = mysql_query("select * from `smsd`.`mobiles` WHERE Number='$cSMS_Send_To'");
    while($row = mysql_fetch_array($result)){
        $name=$row['Name'];
    }

}
else
{
    while($row = mysql_fetch_array($result)){
	$system="$cSMS_Send_To";
        $name=$row['Name'];
        $number=$row['Number'];
    }
}


//let's look up which mobile to use for contact 1
$result = mysql_query("select * from `smsd`.`$cSMS_Send_To_1` WHERE Oncall='1'");

if ( $result == "" ) {
    $system1="Direct Phone";
    $number1=$cSMS_Send_To_1;
    $name1 = "Unknown";
    $result = mysql_query("select * from `smsd`.`mobiles` WHERE Number='$cSMS_Send_To_1'");
    while($row = mysql_fetch_array($result)){
        $name1=$row['Name'];
    }

}
else
{
    while($row = mysql_fetch_array($result)){
        $system1="$cSMS_Send_To_1";
        $name1=$row['Name'];
        $number1=$row['Number'];
    }
}





$time=date("H:i");
$now=date("U");



// Split up the monitor times 
$element = explode(" ",$cMonitor_Time);
$time0_from = $element[0];
$time0_to = $element[2];

$element = explode(" ",$cMonitor_Time_1);
$time1_from = $element[0];
$time1_to = $element[2];

$sms_txt=addslashes("$action: $dev_id summery: $evt_summary component: $component");



//
$today=date("D M j G:i:s T Y");
if ($verbose) { echo "$today : Got triggered for event $evt_evid \n"; }
fwrite($fh, "$today : Got triggered for event $evt_evid \n");




// Look if we are in time to send the sms for the first contact
if ($verbose) {echo "First contact:\n";}
fwrite($fh, "First contact:\n");
if ( strtotime($time) < strtotime($time0_to) and strtotime($time) > strtotime($time0_from) and $cSend_sms == "True" ) {
  if ($verbose) {echo "-- Insert SMS in database\n";}
  if ($verbose) {echo "---- Type	: $system\n";}
  if ($verbose) {echo "---- Sended to	: $name\n";}
  if ($verbose) {echo "---- Number	: $number\n";}
  if ($verbose) {echo "---- Text	: $sms_txt\n\n";}
  fwrite($fh, "-- Insert SMS in database\n---- Type       : $system\n---- Sended to  : $name\n---- Number     : $number\n---- Text       : $sms_txt\n\n");

  $insertlog = mysql_query("INSERT INTO `gammu`.`outbox` ( `DestinationNumber` , `Coding` , `TextDecoded` , `CreatorID`) VALUES ( '$number', 'Default_No_Compression',  '$sms_txt', '$evt_evid' ) ")
  or die(mysql_error());
  //fwrite($fh, "$system;$name;$number;$sms_txt;$now\n");
}
else {
  if ($cSend_sms != "True") {
    if ($verbose) {echo "-- Sms not enabled\n\n";}
    fwrite($fh, "-- Sms not enabled\n\n");
  }
  else { 
    if ($verbose) { echo "-- not in time to send SMS\n\n";}
    fwrite($fh, "-- not in time to send SMS\n\n");
  }
}


// Look if we are in time to send the sms for the second contact
if ($verbose) { echo "Second contact:\n";}
fwrite($fh, "Second contact:\n");


if ( strtotime($time) < strtotime($time1_to) and strtotime($time) > strtotime($time1_from) and $cSend_sms_1 == "True"  ) {
  if ($verbose) { echo "-- Insert SMS in database\n";}
  if ($verbose) { echo "---- Type       : $system1\n";}
  if ($verbose) { echo "---- Sended to  : $name1\n";}
  if ($verbose) { echo "---- Number     : $number1\n";}
  if ($verbose) { echo "---- Text       : $sms_txt\n\n";}
  fwrite($fh, "-- Insert SMS in database\n---- Type       : $system1\n---- Sended to  : $name1\n---- Number     : $number1\n---- Text       : $sms_txt\n\n");

  $insertlog = mysql_query("INSERT INTO `gammu`.`outbox` ( `DestinationNumber` , `Coding` , `TextDecoded` , `CreatorID`) VALUES ( '$number1', 'Default_No_Compression',  '$sms_txt', '$evt_evid' ) ")
  or die(mysql_error());
  //fwrite($fh, "$system1;$name1;$number1;$sms_txt;$now\n");
}
else {
  if ($cSend_sms_1 != "True") {
    if ($verbose) { echo "-- Sms not enabled\n\n";}
    fwrite($fh, "-- Sms not enabled\n\n");
  }
  else {
    if ($verbose) { echo "-- not in time to send SMS\n\n";}
    fwrite($fh, "-- not in time to send SMS\n\n");
  }
}


fclose($fh);

?>
