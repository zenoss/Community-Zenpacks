#! /usr/bin/perl -w
#*=============================================================================
#* San supervising
#*=============================================================================
#* Script: getStates.pl
#* Created: 07/21/2010
#* Author: Richard Esteve
#* Company: Iron Mountain
#*=============================================================================
#* How to use it: 
#* 	./states.pl [ip] [user] [pass] [type] [id]*
#*	type = cache | disk | fault | mirror | sp
#*	* cache=read|write - disk=[name] - fault=all - mirror=[name] - sp=etat|busy
#*=============================================================================
use strict;
use warnings;

my $navicli = "/opt/Navisphere/bin/naviseccli";

my $ip 	 = $ARGV[0];
my $user = $ARGV[1];
my $pass = $ARGV[2];
my $type = $ARGV[3];
my $id	 = $ARGV[4];


#*=============================================================================
#* Name    : checkCache
#* Purpose : Check read/write caches states
#* Inputs  : Nothing
#* Returns : 0 = good, 1 = warning, 2 = critical, 3 = error
#*=============================================================================
sub checkCache
{
	# get cache
	open(FIC, "$navicli -Timeout 20-User $user -Password $pass -Scope 0 -Address $ip getcache -state 2>> .statesErrors|") or exit 3;
	my @lines = <FIC>;
	exit 3 unless(@lines);
	exit 3 unless($lines[0] !~ m/^Could not connect to the specified host/);
	
	# read cache state
	if($id eq "read")
	{
		my @words = split( /\W+/, $lines[0]);
		exit 2 if($words[-1] eq "Disabled");
		exit 1 if($words[-1] eq "Disabling");
		exit 0 if($words[-1] eq "Enabled");
		exit 3;
	}
	
	# write cache state
	if($id eq "write")
	{
		my @words = split( /\W+/, $lines[1]);
		exit 2 if($words[-1] eq "Disabled");
		exit 2 if($words[-1] eq "Disabling");
		exit 2 if($words[-1] eq "Dumping");
		exit 0 if($words[-1] eq "Enabled");
		exit 0 if($words[-1] eq "Enabling");
		exit 2 if($words[-1] eq "Frozen");
		exit 0 if($words[-1] eq "Initializing");
		exit 3;
	}
	exit 3;
}


#*=============================================================================
#* Name    : checkDisk
#* Purpose : Check [id] disk state
#* Inputs  : Nothing
#* Returns : 0 = good, 1 = warning, 2 = critical, 3 = error
#*=============================================================================
sub checkDisk
{
	# get disk
	open(FIC, "$navicli -Timeout 20-User $user -Password $pass -Scope 0 -Address $ip getdisk $id -state 2>> .statesErrors|") or exit 3;
	my @lines = <FIC>;
	exit 3 unless(@lines);
	exit 3 unless($lines[0] !~ m/^Could not connect to the specified host/);
	
	# disk state
	my @words = split( /\W+/, $lines[1]);
	exit 0 if($words[-1] eq "Binding");
	exit 1 if($words[-1] eq "Empty");
	exit 0 if($words[-1] eq "Enabled");
	exit 1 if($words[-1] eq "Equalizing");
	exit 2 if($words[-1] eq "Failed");
	exit 1 if($words[-1] eq "Formatting");
	exit 2 if($words[-1] eq "Off");
	exit 0 if($words[-1] eq "Powering Up");
	exit 0 if($words[-1] eq "Ready");
	exit 1 if($words[-1] eq "Rebuilding");
	exit 2 if($words[-1] eq "Removed");
	exit 0 if($words[-1] eq "Hot Spare Ready");
	exit 0 if($words[-1] eq "Unbound");
	exit 3;
}


#*=============================================================================
#* Name    : checkFault
#* Purpose : Check all faults states
#* Inputs  : Nothing
#* Returns : 0 = good, 1 = warning, 2 = critical, 3 = error
#*=============================================================================
sub checkFault
{
	# get faults
	open(FIC, "$navicli -Timeout 20-User $user -Password $pass -Scope 0 -Address $ip faults -list 2>> .statesErrors|") or exit 3;
	my @lines = <FIC>;
	exit 3 unless(@lines);
	exit 3 unless($lines[0] !~ m/^Could not connect to the specified host/);
	
	# faults state
	if($id eq "all")
	{
		exit 0 if($lines[0] eq "The array is operating normally.\n");
		exit 2 if($lines[0] ne "The array is operating normally.\n");
	}
	exit 3;
}


#*=============================================================================
#* Name    : checkMirror
#* Purpose : Check [id] mirror state
#* Inputs  : Nothing
#* Returns : 0 = good, 1 = warning, 2 = critical, 3 = error
#*=============================================================================
sub checkMirror
{
	# get mirror
	open(FIC, "$navicli -Timeout 20-User $user -Password $pass -Scope 0 -Address $ip mirror -async -list -name $id -state 2>> .statesErrors|") or exit 3;
	my @lines = <FIC>;
	exit 3 unless(@lines);
	exit 3 unless($lines[0] !~ m/^Could not connect to the specified host/);
	
	# mirror state
	my @words = split( /\W+/, $lines[1]);
	exit 2 if($words[-1] ne "Active");
}


#*=============================================================================
#* Name    : checkSP
#* Purpose : Check all SP states
#* Inputs  : Nothing
#* Returns : 0 = good, 1 = warning, 2 = critical, 3 = error
#*=============================================================================
sub checkSP
{
	# get control
	open(FIC, "$navicli -Timeout 20-User $user -Password $pass -Scope 0 -Address $ip getcontrol 2>> .statesErrors|") or exit 3;
	my @lines = <FIC>;
	exit 3 unless(@lines);
	exit 3 unless($lines[0] !~ m/^Could not connect to the specified host/);
	
	# sp state
	if($id eq "state")
	{
		my @words = split( /\W+/, $lines[0]);
		exit 0 if($words[-1] eq "OFF");
		exit 2 if($words[-1] eq "ON");
		exit 3;
	}
	
	# busy state
	if($id eq "busy")
	{
		my @words = split( /\W+/, $lines[9]);
		exit 0 if("$words[-2].$words[-1]" le "70.00");
		exit 1 if("$words[-2].$words[-1]" le "90.00");
		exit 2 if("$words[-2].$words[-1]" le "100.00");
		exit 3;
	}
	exit 3;
}


#*=============================================================================
#* Main
#*=============================================================================
print("ok\n");
exit 3      unless($id);
exit 3      unless($type eq "cache" || $type eq "disk" || $type eq "fault" || $type eq "mirror" || $type eq "sp");
checkCache  if($type eq "cache");
checkDisk   if($type eq "disk");
checkFault  if($type eq "fault");
checkMirror if($type eq "mirror");
checkSP     if($type eq "sp");
