#!/usr/bin/perl

# script to get assp statistics
#
# please edit the username - passwd - ip address before you use it.
#
#

use LWP;
use HTTP::Cookies;
$| = 1;
my $ua = new LWP::UserAgent;
#
#
# Modify these 3 lines for your system.
$username = "USERNAME";
$passwd = "password";
$ipaddress = "192.168.0.203";

$ua->agent("Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)");
#$ua->proxy('http','http://:8080/');
$cookie_jar = new HTTP::Cookies;
$cookie_jar->{'hide_cookie2'} = 1;
$cookie_jar->{'set_version'} = 0;
$ua->cookie_jar($cookie_jar);

#print "getting url\n";
$starturl = 'http://'.$username.':'.$passwd.'@'. $ipaddress.':55555/infostats';
$request = new HTTP::Request('GET', $starturl);
$response = $ua->request($request);
@pagelines = $response->content =~ /(.*\n?)/g;
$nr = 0;
foreach $line (@pagelines) {
  chomp($line);
  $line =~ s/\r//g;
  if ($line =~ /SMTP Connections Accepted:/i) {
     $line2 = $pagelines[$nr+2];
     if ($line2 =~ /2">(\d+)<\/td/i) {
       $smtpAcc = $1;
     }
  }
  elsif ($line =~ /SMTP Connections Rejected:/i) {
        $line2 = $pagelines[$nr+2];
        if ($line2 =~ /2">(\d+)<\/td/i) {
          $smtpDrop = $1;
        }
}

  elsif ($line =~ /Messages Rejected:/i) {
     $line2 = $pagelines[$nr+2];
     if ($line2 =~ /2">(\d+)<\/td/i) {
       $rejmess = $1;
     }
  }
  elsif ($line =~ /Messages Passed:/i) {
     $line2 = $pagelines[$nr+2];
     if ($line2 =~ /2">(\d+)<\/td/i) {
       $passmail = $1;
     }
  }
 elsif ($line =~ /By IP Frequency Limits:/i) {
        $line2 = $pagelines[$nr+2];
        if ($line2 =~ /2">(\d+)<\/td/i) {
          $freqip = $1;
        }
  }
elsif ($line =~ /Penalty Box:/i) {
        $line2 = $pagelines[$nr+2];
        if ($line2 =~ /2">(\d+)<\/td/i) {
          $penaltybx = $1;
        }
  }
elsif ($line =~ /SPF Failures:/i) {
        $line2 = $pagelines[$nr+2];
        if ($line2 =~ /2">(\d+)<\/td/i) {
          $spf = $1;
        }
  }
elsif ($line =~ /RBL Failures:/i) {
        $line2 = $pagelines[$nr+2];
        if ($line2 =~ /2">(\d+)<\/td/i) {
          $rbl = $1;
        }
  }
elsif ($line =~ /URIBL Failures:/i) {
        $line2 = $pagelines[$nr+2];
        if ($line2 =~ /2">(\d+)<\/td/i) {
          $uribl = $1;
        }
  }
  $nr++;
}

print "smtpAcc:$smtpAcc smtpDrop:$smtpDrop MSGrejected:$rejmess MSGpass:$passmail IpFreqLimit:$freqip PenatyBox:$penaltybx SpfFail:$spf Rbl:$rbl Uribl:$uribl ";
