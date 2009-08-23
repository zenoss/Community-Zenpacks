#! /usr/bin/perl
$what = shift(@ARGV);
$community = shift(@ARGV);
$verP = shift(@ARGV);
$host = shift(@ARGV);
$baseoid = "1.3.6.1.4.1.9.9.42.1.5.2.1";
$timeout=5;

use threads;
use threads::shared;
use Thread::Exit;

my $done;

$child_thread=threads->new(\&Call_Doit);
$child_thread->detach();

CallTimer();

sub Call_Doit
{

        $name=`snmpwalk -c$community -$verP $host -O qv 1.3.6.1.4.1.9.9.42.1.2.1.1.3 | grep -m 1 -w '$what'`;
        $id=`snmpwalk -c$community -$verP $host -O nqa 1.3.6.1.4.1.9.9.42.1.2.1.1.3 | grep -m 1 -w '$what'`;
        $name=~ s/"//g;
        $id=~s/"//g;
        $id=~s/.1.3.6.1.4.1.9.9.42.1.2.1.1.3.//g;
        $id=~s/$name//g;

        $tmp=`snmpwalk -c$community -$verP $host -O vq $baseoid.46.$id`;
        $response="rttMonLatestJitterOperAvgJitter=$tmp";

        $tmpB=`snmpwalk -c$community -$verP $host -O vq $baseoid.42.$id `;
        $response="$response rttMonLatestJitterOperMOS=$tmpB";

        $tmpC=`snmpwalk -c$community -$verP $host -O vq $baseoid.43.$id `;
        $response="$response rttMonLatestJitterOperICPIF=$tmpC";

        $tmpD=`snmpwalk -c$community -$verP $host -O vq $baseoid.44.$id `;
        $response="$response rttMonLatestJitterOperIAJOut=$tmpD";

        $tmpE=`snmpwalk -c$community -$verP $host -O vq $baseoid.45.$id `;
        $response="$response rttMonLatestJitterOperIAJIn=$tmpE";

        $response=~ s/\n//g;
        $response=~ s/  //g;

        print "OK| $response\n";
        exit();
}

sub CallTimer
{
sleep $timeout;
}
