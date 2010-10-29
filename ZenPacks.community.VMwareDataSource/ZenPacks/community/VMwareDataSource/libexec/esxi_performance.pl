#!/usr/bin/perl -w
#
# License: GPL
# Author: Eric Enns
#

use strict;
use warnings;
use VMware::VIRuntime;

my %opts = (
	vmname => {
		type => "=s",
		variable => "VI_VMNAME",
		help => "The name of the virtual machine",
		required => 0,
	},
	host => {
		type => "=s",
		variable => "VI_HOST",
		help => "The name of the host",
		required => 0,
	},
	options => {
		type => "=s",
        variable => "VI_OPTIONS",
        help => "Query Options",
        required => 1,
	},
);

Opts::add_options(%opts);
Opts::parse();
Opts::validate();

Util::connect();

my $options = Opts::get_option('options');

my $output = "Unknown ERROR!";
my $values;

eval
{
	Util::connect();

	if ($options =~ /^guestperf:(.*)$/)
	{
		my $vmname = $1;
		my $memUsage = vm_info($vmname, 'mem', 'usage', 'minimum');
		my $memOverhead = vm_info($vmname, 'mem', 'overhead', 'minimum');
		my $memConsumed = vm_info($vmname, 'mem', 'consumed', 'minimum');
        my $diskUsage = vm_info($vmname, 'disk', 'usage', 'average');
		my $cpuUsageMin = vm_info($vmname, 'cpu', 'usage', 'minimum');
        my $cpuUsageMax = vm_info($vmname, 'cpu', 'usage', 'maximum');
		my $cpuUsageAvg = vm_info($vmname, 'cpu', 'usage', 'average');
        my $cpuUsage = vm_info($vmname, 'cpu', 'usagemhz', 'average');

		print "guestperf|memUsage=".$memUsage." memOverhead=".$memOverhead." memConsumed=".$memConsumed." diskUsage=".$diskUsage." cpuUsageMin=".$cpuUsageMin." cpuUsageMax=".$cpuUsageMax." cpuUsageAvg=".$cpuUsageAvg." cpuUsage=".$cpuUsage."\n";
	}
	elsif ($options =~ /^hostperf:(.*)$/)
	{
		my $esxi = {name => $1};
		my $sysUpTime = host_info('sys', 'uptime', 'latest',$esxi) * 100;
        my $memSwapused = host_info('mem', 'swapused', 'maximum', $esxi);
        my $memGranted = host_info('mem', 'granted', 'maximum', $esxi);
        my $memActive = host_info('mem', 'active', 'maximum', $esxi);
        my $diskUsage = host_info('disk', 'usage', 'average', $esxi);
        my $cpuUsagemhz = host_info('cpu', 'usagemhz', 'average', $esxi);
        my $cpuUsage = host_info('cpu', 'usage', 'average', $esxi);
        my $cpuReservedcapacity = host_info('cpu', 'reservedCapacity', 'average', $esxi);

		print "hostperf|sysUpTime=".$sysUpTime." memSwapused=".$memSwapused." memGranted=".$memGranted." memActive=".$memActive." diskUsage=".$diskUsage." cpuUsagemhz=".$cpuUsagemhz." cpuUsage=".$cpuUsage." cpuReservedcapacity=".$cpuReservedcapacity."\n";
	}
	#if (defined($vmname))
	#{
	#	$output = vm_info($vmname, $group_type, $counter, $rollup_type);
	#}
	#elsif (defined($host))
	#{
	#	my $esxi = {name => $host};
	#	$output = host_info($group_type, $counter, $rollup_type, $esxi);
	#}
};

Util::disconnect();

###############################################################################

sub get_key_metrices
{
	my ($perfmgr_view, $group, @names) = @_;
	my $perfCounterInfo = $perfmgr_view->perfCounter;
	my @counters;

	foreach (@$perfCounterInfo)
	{
		if ($_->groupInfo->key eq $group)
		{
			my $cur_name = $_->nameInfo->key . "." . $_->rollupType->val;
			foreach my $index (0..@names-1)
			{
				if ($names[$index] =~ /$cur_name/)
				{
					$names[$index] =~ /(\w+).(\w+):*(.*)/;
					$counters[$index] = PerfMetricId->new(counterId => $_->key, instance => $3);
				}
			}
		}
	}

	return \@counters;
}

sub get_performance_values
{
	my ($views, $group, @list) = @_;
	my $counter = 0;
	my @values = ();
	my $amount = @list;
	eval
	{
		my $perfMgr = Vim::get_view(mo_ref => Vim::get_service_content()->perfManager, properties => [ 'perfCounter' ]);
		my $metrices = get_key_metrices($perfMgr, $group, @list);
		
		my @perf_query_spec = ();
		push(@perf_query_spec, PerfQuerySpec->new(entity => $_, metricId => $metrices, format => 'csv', intervalId => 20, maxSample => 1)) foreach (@$views);
		my $perf_data = $perfMgr->QueryPerf(querySpec => \@perf_query_spec);
		$amount *= @$perf_data;

		while (@$perf_data)
		{
			my $unsorted = shift(@$perf_data)->value;
			my @host_values = ();
			
			foreach my $id (@$unsorted)
			{
				foreach my $index (0..@$metrices-1)
				{
					if ($id->id->counterId == $$metrices[$index]->counterId)
					{
						$counter++ if (!defined($host_values[$index]));
						$host_values[$index] = $id;
					}
				}
			}

			push(@values, \@host_values);
		}
	};
	return undef if ($@ || $counter != $amount);
	return \@values;
}

sub get_vm_performance_values
{
	my $values;
	my $vmname = shift(@_);
	my $vm_view = Vim::find_entity_views(view_type => 'VirtualMachine', filter => {name => $vmname}, properties => [ 'name', 'runtime.powerState' ]);
	die "Runtime error\n" if (!defined($vm_view));
	die "VMware machine \"" . $vmname . "\" does not exist\n" if (!@$vm_view);
	die "VMware machine \"" . $vmname . "\" is not running. Current state is \"" . $$vm_view[0]->get_property('runtime.powerState')->val . "\"\n" if ($$vm_view[0]->get_property('runtime.powerState')->val ne "poweredOn");
	$values = get_performance_values($vm_view, @_);

	return $@ if ($@);
	return $values;
}

sub get_host_performance_values
{
	my $values;
	my $host_name = shift(@_);
	my $host_view = Vim::find_entity_views(view_type => 'HostSystem', filter => $host_name, properties => [ 'name' ]); # Added properties named argument.
	die "Runtime error\n" if (!defined($host_view));
	die "Host \"" . $$host_name{"name"} . "\" does not exist\n" if (!@$host_view);
	$values = get_performance_values($host_view, @_);
	return undef if ($@);
	return $values;
}

#====================================| VM |===================================#

sub vm_info
{
	my ($vmname, $group_type, $counter, $rollup_type) = @_;
	
	$values = get_vm_performance_values($vmname, $group_type, ($counter.".".$rollup_type));
	if (defined($values))
	{
		my ( $t ) = split(/,/, $$values[0][0]->value);
        return $t;
	}
}

#===================================| Host |==================================#

sub host_info
{
	my ($group_type, $counter, $rollup_type, $host) = @_;

        $values = get_host_performance_values($host, $group_type, ($counter.".".$rollup_type));
        if (defined($values))
        {
				my ( $t ) = split(/,/, $$values[0][0]->value);
                return $t;
        }
}

