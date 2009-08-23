#! /usr/bin/perl
$what = shift(@ARGV);
$community = shift(@ARGV);
$verP = shift(@ARGV);
$host = shift(@ARGV);
$baseoid = "1.3.6.1.4.1.9.9.42.1.2.10.1";
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

        $tmp=`snmpwalk -c$community -$verP $host -O vq $baseoid.1.$id`;
        $response="rttMonLatestRttOperCompletionTime=$tmp";

        $tmpB=`snmpwalk -c$community -$verP $host -O vq $baseoid.2.$id `;
        $response="$response rttMonLatestRttOperSense=$tmpB";

        $tmpC=`snmpwalk -c$community -$verP $host -O vq $baseoid.3.$id`;
        $response=" $response rttMonLatestRttOperApplSpecificSense=$tmpC";

        $tmpD=`snmpwalk -c$community -$verP $host -O vqt $baseoid.5.$id`;
        $response=" $response rttMonLatestRttOperTime=$tmpD";

        $response=~ s/\n//g;
        $response=~ s/  //g;

        print "OK| $response\n";
        exit();
}

sub CallTimer
{
sleep $timeout;
}
