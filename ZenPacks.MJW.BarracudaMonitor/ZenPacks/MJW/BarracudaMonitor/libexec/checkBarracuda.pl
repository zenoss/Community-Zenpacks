#!/usr/bin/perl

use warnings;
use strict;
use LWP::Simple;
use XML::Simple;
use lib $ENV{ZENHOME}."/libexec";
use utils qw(%ERRORS usage);
use Getopt::Long;

my $host;
GetOptions("hostname|H=s" => \$host);
if (!$host) {
	usage "Hostname/address not specified.\n"; 
	exit;
}

# Get statistics XML from the Barracuda
my $url = "https://$host/cgi-mod/stats.cgi";
my $content = get($url);
die "Unable to get content: $url" unless (defined($content));

# Parse the XML
my $xml = new XML::Simple->XMLin($content);
die "Unable to parse XML." unless (defined($xml));

my @attrs = ('spams', 'bad_recipients', 'viruses',
	'quarantined', 'tagged', 'allowed', 'rate_control');
my %stats;

# Set all statistics to 0
foreach my $attr (@attrs) { $stats{$attr} = 0; }

# Total each statistic for the last 24 hours
foreach my $hour (keys(%{$xml->{hourly}})) {
	foreach my $attr (@attrs) {
		$stats{$attr} += $xml->{hourly}->{$hour}->{$attr}
			if(defined($xml->{hourly}->{$hour}->{$attr}));
	}
}

my $prtstr = "Barracuda-$host OK |";
$prtstr .= " inqueue=$xml->{performance}->{inbound_queue_size};";
$prtstr .= " outqueue=$xml->{performance}->{outbound_queue_size};";
foreach my $attr (@attrs) {
	$prtstr .= " $attr=$stats{$attr};";
}

print "$prtstr\n";

exit $ERRORS{'OK'};