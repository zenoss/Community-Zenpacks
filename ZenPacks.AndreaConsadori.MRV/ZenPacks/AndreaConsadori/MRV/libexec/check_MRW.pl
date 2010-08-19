#!/opt/perl/bin/perl
$ip       = $ARGV[0];
$passwd   = $ARGV[1];
die ("IP must be passed as an argument. $!\n") unless defined($ip);
use Net::Telnet ();
$handle = new Net::Telnet (Timeout => 10, Prompt => '/.*(#|>|\))\s*$/');
$handle->open("$ip");
$handle->login("admin",$passwd);
#$handle->cmd("terminal length 0");
@lines = $handle->cmd("show station");
print "@lines";
#system("sleep 30");
$handle->cmd(exit);
$handle->close;

