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

Opts::parse();
Opts::validate();

Util::connect();

my $vm_views = Vim::find_entity_views(
	view_type => 'VirtualMachine'
);

foreach my $vm (@$vm_views)
{
	#my $name = $vm->guest->hostName;
	#if (!$name)
	#{
	#	$name = $vm->name;
	#}
	my $name = $vm->name;
	my $memory = $vm->config->hardware->memoryMB;
	my $os = $vm->config->guestFullName;
	my $powerStatus = $vm->runtime->powerState->val;
	my $status = $vm->summary->overallStatus->val;

	print $name . ";" . $memory . ";" . $os . ";" . $powerStatus . ";" . $status . "\n";
}

Util::disconnect();
