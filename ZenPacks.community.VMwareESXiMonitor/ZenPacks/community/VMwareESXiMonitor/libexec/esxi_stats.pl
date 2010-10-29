#!/usr/bin/perl
################################################################################
#
# This program is part of the VMwareESXiMonitor Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

use strict;
use warnings;
use VMware::VIRuntime;

my %opts = (
	vmname => {
		type => "=s",
		variable => "VI_VMNAME",
		help => "The name of the virtual machine",
		required => 1,
	},
);

Opts::add_options(%opts);
Opts::parse();
Opts::validate();

Util::connect();

my $vmname = Opts::get_option('vmname');

my $cpuspeed;
my $cpuusage;
my $memorysize;
my $activememory;
my $cachedmemory;


if( !($vmname eq Opts::get_option('server')) )
{
	my $vm = Vim::find_entity_view(
		view_type => 'VirtualMachine',
		filter => { 'name' => Opts::get_option('vmname') }
	);

	$cpuspeed = $vm->runtime->maxCpuUsage * 1000000;
    $cpuusage = $vm->summary->quickStats->overallCpuUsage * 1000000;
    $memorysize = $vm->runtime->maxMemoryUsage * 1048576;
    $activememory = $vm->summary->quickStats->guestMemoryUsage * 1048576;
	$cachedmemory = $vm->summary->quickStats->hostMemoryUsage * 1048576;
}
else
{
	my $host_view = Vim::find_entity_views(
		view_type => 'HostSystem'
	);

	my $host = @$host_view[0];

	$cpuspeed = ($host->summary->hardware->cpuMhz * $host->summary->hardware->numCpuCores) * 1000000;
	$cpuusage = $host->summary->quickStats->overallCpuUsage * 1000000;
	$memorysize = $host->summary->hardware->memorySize;
	$activememory = $host->summary->quickStats->overallMemoryUsage * 1048576;
	$cachedmemory = 0
}

print "STATUS OK|CPUSpeed=".$cpuspeed." CPUUsage=".$cpuusage." MemorySize=".$memorysize." ActiveMemory=".$activememory." CachedMemory=".$cachedmemory."\n";

Util::disconnect();
