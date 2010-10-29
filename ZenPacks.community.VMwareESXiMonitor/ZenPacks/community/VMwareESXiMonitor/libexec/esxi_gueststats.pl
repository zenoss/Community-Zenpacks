#!/usr/bin/perl

use strict;
use warnings;
use VMware::VIRuntime;

Opts::parse();
Opts::validate();

Util::connect();

my $host_view = Vim::find_entity_views(
	view_type => 'HostSystem'
);

my $host = @$host_view[0];

my $cpuspeed = ($host->summary->hardware->cpuMhz * $host->summary->hardware->numCpuCores) * 1000000;
my $cpuusage = $host->summary->quickStats->overallCpuUsage * 1000000;
my $memorysize = $host->summary->hardware->memorySize;
my $memoryusage = $host->summary->quickStats->overallMemoryUsage * 1048576;

#foreach my $host (@$host_view) {
#	print "Stop here"
#}

print "STATUS OK|CPUSpeed=".$cpuspeed." CPUUsage=".$cpuusage." MemorySize=".$memorysize." MemoryUsage=".$memoryusage."\n";


Util::disconnect();
