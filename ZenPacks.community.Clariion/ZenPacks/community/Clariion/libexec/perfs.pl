#! /usr/bin/perl -w
#*=============================================================================
#* San supervising
#*=============================================================================
#* Script: getPerfs.pl
#* Created: 07/22/2010
#* Author: Richard Esteve
#* Company: Iron Mountain
#*=============================================================================
#* How to use it: 
#* 	./perfs.pl [ip] [user] [pass] [type] [id]*
#*	type = disk | lun | mirror | rlp | sp
#*	* disk = [name] - mirror = [name]
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
#* Name    : checkDisk
#* Purpose : Check hard/soft read/write errors and read/write requests/Kb
#* Inputs  : Nothing
#* Print   : hrer hwer srer swer rere wrre kbre kbwr
#*=============================================================================
sub checkDisk
{
	# get disk
	die("\n") unless($id);
	open(FIC, "$navicli -Timeout 20 -user $user -password $pass -scope 0 -address $ip getdisk $id 2>/dev/null|") or die("Unknown|results\n");
	my @lines = <FIC>;
	die("Unknown|results\n") unless(@lines);
	die("Unknown|No Response\n") unless($lines[0] !~ m/^Could not connect to the specified host/);
	
	# hard read error
	my @words = split( /\W+/, $lines[15]);
	my $hrer  = $words[-1];
	
	# hard write error
	@words   = split( /\W+/, $lines[16]);
	my $hwer = $words[-1];
	
	# soft read error
	@words   = split( /\W+/, $lines[17]);
	my $srer = $words[-1];
	
	# soft write error
	@words   = split( /\W+/, $lines[18]);
	my $swer = $words[-1];

	# read requests
	@words   = split( /\W+/, $lines[28]);
	my $rere = $words[-1];
	
	# write requests
	@words   = split( /\W+/, $lines[29]);
	my $wrre = $words[-1];
	
	# kbytes read
	@words   = split( /\W+/, $lines[30]);
	my $kbre = $words[-1];
	
	# kbytes written
	@words   = split( /\W+/, $lines[31]);
	my $kbwr = $words[-1];
	
	# get file
	my $secs = time;
	my ($t, $a, $b, $c, $d) = (0, 0, 0, 0, 0);
	
	# if(open(FIC, ".DiskSave"))
	# {
	#	my @cont = split( /\W+/, <FIC>);
	#	$t = $secs - $cont[0];
	#	$a = ($rere - $cont[1]) / $t if($cont[1] lt $rere);
	#	$b = ($wrre - $cont[2]) / $t if($cont[2] lt $wrre);
	#	$c = ($kbre - $cont[3]) / $t if($cont[3] lt $kbre);
	#	$d = ($kbwr - $cont[4]) / $t if($cont[4] lt $kbwr);
	# }

	# print results
	# open(FIC, "echo $secs $rere $wrre $kbre $kbwr > .DiskSave|") or die("Unknown|results\n");
	# print("OK|hrer=$hrer hwer=$hwer srer=$srer swer=$swer rere=$a wrre=$b kbre=$c kbwr=$d\n");
	print("OK|hrer=$hrer hwer=$hwer srer=$srer swer=$swer rere=$rere wrre=$wrre kbre=$kbre kbwr=$kbwr\n");
}


#*=============================================================================
#* Name    : checkLun
#* Purpose : Check total number, unallocated, Used (Gb) and % used of lun pool
#* Inputs  : Nothing
#* Print   : totalLun nbUnallocated usedLun percentUsed
#*=============================================================================
sub checkLun
{
	# get lunpool
	open(FIC, "$navicli -Timeout 20 -user $user -password $pass -scope 0 -address $ip reserved -lunpool -list 2>/dev/null|") or die("Unknown|results\n");
	my @lines = <FIC>;
	die("Unknown|results\n") unless(@lines);
	die("Unknown|No response\n") unless($lines[0] !~ m/^Could not connect to the specified host/);
	
	# total number of lun in pool
	my @words = split( /\W+/, $lines[1]);
	my $ttln  = $words[-1];
	
	# number of unallocated lun in pool
	@words    = split( /\W+/, $lines[2]);
	my $nbun  = $words[-1];
	
	# used of lun pool
	@words    = split( /\W+/, $lines[6]);
	my $used  = "$words[-2].$words[-1]";
	
	# % used of lun pool
	@words    = split( /\W+/, $lines[7]);
	my $perc  = "$words[-2].$words[-1]";
	
	# print results
	print("OK|totalLun=$ttln nbUnallocated=$nbun usedLun=$used percentUsed=$perc\n");
}


#*=============================================================================
#* Name    : checkMirror
#* Purpose : Check synchronizing progress and time since last update (min)
#* Inputs  : Nothing
#* Print   : synchroProgress timeUpdate
#*=============================================================================
sub checkMirror
{
	# get mirror
	die("\n") unless($id);
	open(FIC, "$navicli -Timeout 20 -user $user -password $pass -scope 0 -address $ip mirror -async -list -name $id 2>/dev/null|") or die("Unknown|results\n");
	my @lines = <FIC>;
	die("Unknown|results\n") unless(@lines);
	die("Unknown|No response\n") unless($lines[0] !~ m/^Could not connect to the specified host/);
	
	# synchronizing progress
	my @words = split( /\W+/, $lines[27]);
	my $sync  = $words[-1];
	
	# time since previous update
	@words    = split( /\W+/, $lines[30]);
	my $time  = $words[-1];
	
	# print result
	print("OK|synchroProgess=$sync | timeUpdate=$time\n");
}


#*=============================================================================
#* Name    : checkRLP
#* Purpose : Check Reserved Lun Pool state
#* Inputs  : Nothing
#* Print   : totallun freelun totalsize unusedsize usedsize percentused
#*=============================================================================
sub checkRLP
{
	# get RLP
	open(FIC, "$navicli -Timeout 20 -user $user -password $pass -scope 0 -address $ip reserved -lunpool -list 2>/dev/null|") or die("Unknown|results\n");
	my @lines = <FIC>;
	die("Unknown|results\n") unless(@lines);
	die("Unknown|No response\n") unless($lines[0] !~ m/^Could not connect to the specified host/);
	die("Unknown|No response\n") unless($lines[0] !~ m/^Invalid server certificate/);
	
	# tluns (total lun)
	my @words = split( /\W+/, $lines[1]);
	my $tluns  = "$words[-1]";
	
	# fluns (free lun)
	@words = split( /\W+/, $lines[2]);
	my $fluns = "$words[-1]";
	
	# uluns (used lun)
	my $uluns = $tluns-$fluns;
	
	# tsize (Total size)
	@words = split( /\W+/, $lines[4]);
	my $tsize = "$words[-2].$words[-1]";
	
	# fsize (Unused size)
	@words = split( /\W+/, $lines[5]);
	my $fsize = "$words[-2].$words[-1]";
	
	# usize (Used size)
	@words = split( /\W+/, $lines[6]);
	my $usize = "$words[-2].$words[-1]";
	
	# psize (Percent pool size used
	@words = split( /\W+/, $lines[7]);
	my $psize = "$words[-2].$words[-1]";
	
	print("OK|totallun=$tluns freelun=$fluns usedlun=$uluns totalsize=$tsize unusedsize=$fsize usedsize=$usize percentused=$psize\n");
	
}

#*=============================================================================
#* Name    : checkSP
#* Purpose : Check busy/idle percent of sp and dirty/owned pages of cache
#* Inputs  : Nothing
#* Print   : busy idle dirty owned
#*=============================================================================
sub checkSP
{
	# get control
	open(FIC, "$navicli -Timeout 20 -User $user -password $pass -scope 0 -address $ip getcontrol 2>/dev/null|") or die("Unknown|results\n");
	my @lines = <FIC>;
	die("Unknown|results\n") unless(@lines);
	die("Unknown|No response\n") unless($lines[0] !~ m/^Could not connect to the specified host/);
	die("Unknown|No response\n") unless($lines[0] !~ m/^Invalid server certificate/);
	
	# prct busy
	my @words = split( /\W+/, $lines[9]);
	my $busy  = "$words[-2].$words[-1]";

	# prct idle
	@words    = split( /\W+/, $lines[10]);
	my $idle  = "$words[-2].$words[-1]";
	
	# total blocks read
	@words    = split( /\W+/, $lines[16]);
	my $bread = $words[-1];
	
	# total blocks writen
	@words    = split( /\W+/, $lines[17]);
	my $bwriten = $words[-1];	
	
	# get cache
	open(FIC, "$navicli -Timeout 20 -user $user -password $pass -scope 0 -address $ip getcache 2>/dev/null|") or die("Unknown|results\n");
	@lines    = <FIC>;
	die("Unknown|results\n") unless(@lines);
	die("Unknown|No response\n") unless($lines[0] !~ m/^Could not connect to the specified host/);
	
	# prct dirty
	@words    = split( /\W+/, $lines[11]);
	my $dirt  = $words[-1];
	
	# prct owned
	@words    = split( /\W+/, $lines[12]);
	my $owne  = $words[-1];
	
	# get file
	my $secs = time;
	my ($t, $a, $b) = (0, 0, 0);
	
	#if(open(FIC, ".save"))
	#{
	#	my @cont = split( /\W+/, <FIC>);
	#	$t = $secs - $cont[0];
	#	$a = ($bread - $cont[1]) / $t if($cont[1] lt $bread);
	#	$b = ($bwriten - $cont[2]) / $t if($cont[2] lt $bwriten);
	#}
	
	# print result
	#open(FIC, "echo $secs $bread $bwriten > .save|") or die("Unknown|results\n");
	print("OK|busy=$busy idle=$idle dirty=$dirt owned=$owne bread=$bread bwriten=$bwriten\n");
}


#*=============================================================================
#* Main
#*=============================================================================
die("\n")   unless($type);
die("\n")   unless($type eq "disk" || $type eq "lun" || $type eq "mirror" || $type eq "rlp" || $type eq "sp");
checkDisk   if($type eq "disk");
checkLun    if($type eq "lun");
checkMirror if($type eq "mirror");
checkRLP	if($type eq "rlp");
checkSP     if($type eq "sp");
