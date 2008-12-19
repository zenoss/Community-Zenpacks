#!/usr/bin/perl -w
# vim:ts=4
#
# vmware_monitor v2.4
# Steve S 2005,2006
#
# Generate a directory filled with .rrd files for usage stats of virtual
# machines, plus mrtg .cfg file for their display.
#
# Usage:
# vmware_monitor -c cachefile -d rrddirectory -m mrtg.cfg 
#                -C community -H vmwarehost
# default rrddir is .
# default cachefile is <rrddir>/cache
# default mrtg file is <rrddir>/vmware.cfg
# default community is public
# default hostname is localhost
#
# This requires SNMP to be running on the ESX server with the VMWARE agent.
# Also, you should have the vmware-stats script in /etc/snmp and the
# line added to the /etc/snmp/snmpd.conf file


use strict;
use Net::SNMP;
use Getopt::Std;
use RRDs;

my($STATEFILE) = '';
my($RRDDIR) = '';
my($CFGFILE) = '';
my($CFGFILES) = '/u01/mrtg/conf';
my($VMOID) = "1.3.6.1.4.1.6876";
my($UCDOID) = "1.3.6.1.4.1.2021.1000.10"; # OID of the vmware-stats script
my($DEBUG) = 0;
my($TIMEOUT) = 5;
my($PFX) = "";
my($snmp,$resp,$snmperr);
my($hostname) = '';
my($community) = 'public'; # Default community string
my($MSG) = '';
my(%lookup) = ();
my($readvmids) = 0;
my(%states) = ();
my(%tmpnet) = ();
my(%vhosts) = (); # location of their rrd, etc
my(%proc) = ();
my($maxrrd) = 0;
my(@list) = ();
my($maxcpu,$maxmem);
my($vh);
my(%vmware) = ();

use vars qw($opt_t $opt_C $opt_H $opt_h $opt_c $opt_d $opt_m $opt_D $opt_t);

sub dohelp {
	print "Usage: vmware_monitor [-d][-h] -H host [-C community] [-D directory] [-c cachefile]\n";
	print "                      [-m mrtgfile] [-t timeout]\n";

	exit 0;
}

sub clean($) { # remove any characters that are dodgy in filesystems
	my($x) = $_[0];
	$x =~ s/[:\\\/\[\]#!\*&\?\(\)\s]/-/g;
	return $x;
}

sub readstate {
	return if(! -r $STATEFILE);
	open STATE, "<$STATEFILE";
	flock STATE,1; # read lock
	while( <STATE> ) { $states{$1}=$2 if( /^(\S.*)\s*=\s*(.*)/ and $2 ); }
	flock STATE,8; # unlock
	close STATE;
}
sub writestate {
	open STATE, ">$STATEFILE"; 
#	foreach ( keys %states ) { print STATE "$_=".$states{$_}."\n" ; }
	foreach ( keys %vhosts ) {
		next if(!$_ or !$vhosts{$_}{rrd});
		print STATE "vhost-$_=".$vhosts{$_}{rrd}."\n";
		print STATE "ifname-$_=".(join " ",(keys %{$vhosts{$_}{net}}))."\n"
			if(defined $vhosts{$_}{net});
		print STATE "hbaname-$_=".(join " ",(keys %{$vhosts{$_}{hba}}))."\n"
			if(defined $vhosts{$_}{hba});
		print STATE "cpus-$_=".$vmware{"vhost-".$lookup{$_}."-cpu-max"}."\n" 
			if($lookup{$_} and $vmware{"vhost-".$lookup{$_}."-cpu-max"});
		print STATE "maxmem-$_=".$vmware{"vhost-".$lookup{$_}."-mem-max"}."\n" 
			if($lookup{$_} and $vmware{"vhost-".$lookup{$_}."-mem-max"});
	}
	close STATE;
}
sub dooutput { print "$MSG\n"; }

# Create all RRD files for the given vhost
sub createrrd($) {
	my($rrd) = $_[0];
    my($err);

	print "Creating RRD #$rrd\n" if($DEBUG);

    RRDs::create( "$RRDDIR/$rrd-cpu.rrd",
                qw/RRA:AVERAGE:0.5:1:800 RRA:AVERAGE:0.25:6:800 RRA:AVERAGE:0.25:24:800 RRA:AVERAGE:0.25:288:800 RRA:MAX:0.5:1:800 RRA:MAX:0.25:6:800 RRA:MAX:0.25:24:800 RRA:MAX:0.25:288:800/,
                qw/DS:ds0:COUNTER:600:0:32 DS:ds1:COUNTER:600:0:32/ );
   $err = RRDs::error; if($err) { print "RRD Error: $err\n"; return 1; }
    RRDs::create( "$RRDDIR/$rrd-mem.rrd",    # actv/total
                qw/RRA:AVERAGE:0.5:1:800 RRA:AVERAGE:0.25:6:800 RRA:AVERAGE:0.25:24:800 RRA:AVERAGE:0.25:288:800 RRA:MAX:0.5:1:800 RRA:MAX:0.25:6:800 RRA:MAX:0.25:24:800 RRA:MAX:0.25:288:800/,
                qw/DS:ds0:GAUGE:600:0:1024000000000 DS:ds1:GAUGE:600:0:1024000000000/ );
   $err = RRDs::error; if($err) { print "RRD Error: $err\n"; return 1; }
    RRDs::create( "$RRDDIR/$rrd-mem-ps.rrd", # pvt/shr
                qw/RRA:AVERAGE:0.5:1:800 RRA:AVERAGE:0.25:6:800 RRA:AVERAGE:0.25:24:800 RRA:AVERAGE:0.25:288:800 RRA:MAX:0.5:1:800 RRA:MAX:0.25:6:800 RRA:MAX:0.25:24:800 RRA:MAX:0.25:288:800/,
                qw/DS:ds0:GAUGE:600:0:1024000000000 DS:ds1:GAUGE:600:0:1024000000000/ );
   $err = RRDs::error; if($err) { print "RRD Error: $err\n"; return 1; }
    RRDs::create( "$RRDDIR/$rrd-mem-bs.rrd", # bal/swp
                qw/RRA:AVERAGE:0.5:1:800 RRA:AVERAGE:0.25:6:800 RRA:AVERAGE:0.25:24:800 RRA:AVERAGE:0.25:288:800 RRA:MAX:0.5:1:800 RRA:MAX:0.25:6:800 RRA:MAX:0.25:24:800 RRA:MAX:0.25:288:800/,
                qw/DS:ds0:GAUGE:600:0:1024000000000 DS:ds1:GAUGE:600:0:1024000000000/ );
   $err = RRDs::error; if($err) { print "RRD Error: $err\n"; return 1; }
	return 0;
}
sub createrrdx($$) {
	my($rrdno,$ifname) = @_;
    my($err);
	my($rrd) = "$rrdno-x-".clean($ifname);

	print "Creating RRD #$rrd\n" if($DEBUG);
    RRDs::create( "$RRDDIR/$rrd.rrd",
                qw/RRA:AVERAGE:0.5:1:800 RRA:AVERAGE:0.25:6:800 RRA:AVERAGE:0.25:24:800 RRA:AVERAGE:0.25:288:800 RRA:MAX:0.5:1:800 RRA:MAX:0.25:6:800 RRA:MAX:0.25:24:800 RRA:MAX:0.25:288:800/,
                qw/DS:ds0:COUNTER:600:0:10240000 DS:ds1:COUNTER:600:0:10240000/ );
   $err = RRDs::error; if($err) { print "RRD Error: $err\n"; return 1; }
	return 0;
}

# Update the RRD files as per the data held in %vhosts
sub updaterrd {
	my($err,$vh,$id,$vhid,$T);
	foreach $vh ( keys %vhosts ) {
		next if(!$vh);
		next if(!$vhosts{$vh}{rrd});
		$vhid = $lookup{$vh};
		print "Updating vhost=$vh #".$vhosts{$vh}{rrd}."\n" if($DEBUG);
		if(!$vhid) {
			print "Guest '$vh' no longer defined, or down\n";
		} else {  # IE, this guest is running
		$T = $vmware{"time"};
		print "Time is: $T\n" if($DEBUG);
		RRDs::update ( "$RRDDIR/".$vhosts{$vh}{rrd}."-cpu.rrd",
			"--template", "ds0:ds1",
			"$T:" .int($vmware{"vhost-$vhid-cpu-used-count"}).":"
				.int($vmware{"vhost-$vhid-cpu-ready-count"}) )
			if(defined $vmware{"vhost-$vhid-cpu-used-count"});
		print "Updating CPU to ".int($vmware{"vhost-$vhid-cpu-used-count"})."/"
				.int($vmware{"vhost-$vhid-cpu-ready-count"})."\n"
			if(defined $vmware{"vhost-$vhid-cpu-used-count"} and $DEBUG);
   $err = RRDs::error; if($err) { print "RRD Error: $err\n"; return; }
		RRDs::update ( "$RRDDIR/".$vhosts{$vh}{rrd}."-mem.rrd",
			"--template", "ds0:ds1",
			"$T:".$vmware{"vhost-$vhid-mem-used"}.":".$vmware{"vhost-$vhid-mem-active"} )
			if(defined $vmware{"vhost-$vhid-mem-active"} );
		print "Updating MEM to ".$vmware{"vhost-$vhid-mem-active"}."\n"
			if(defined $vmware{"vhost-$vhid-mem-active"} and $DEBUG);

   $err = RRDs::error; if($err) { print "RRD Error: $err\n"; return; }
		RRDs::update ( "$RRDDIR/".$vhosts{$vh}{rrd}."-mem-ps.rrd",
			"--template", "ds0:ds1",
			"$T:".$vmware{"vhost-$vhid-mem-private"}.":".$vmware{"vhost-$vhid-mem-shared"} )
			if(defined $vmware{"vhost-$vhid-mem-private"});
		print "Updating MEM-PS to ".$vmware{"vhost-$vhid-mem-private"}."/".$vmware{"vhost-$vhid-mem-shared"}."\n"
			if(defined $vmware{"vhost-$vhid-mem-private"} and $DEBUG);

   $err = RRDs::error; if($err) { print "RRD Error: $err\n"; return; }
		RRDs::update ( "$RRDDIR/".$vhosts{$vh}{rrd}."-mem-bs.rrd",
			"--template", "ds0:ds1",
			"$T:".$vmware{"vhost-$vhid-mem-balloon"}.":".$vmware{"vhost-$vhid-mem-swap"} )
			if(defined $vmware{"vhost-$vhid-mem-balloon"});
		print "Updating MEM-BS to ".$vmware{"vhost-$vhid-mem-balloon"}."/".$vmware{"vhost-$vhid-mem-swap"}."\n"
			if(defined $vmware{"vhost-$vhid-mem-balloon"} and $DEBUG);
   $err = RRDs::error; if($err) { print "RRD Error: $err\n"; return; }

		} # vhid set (ie, running)

		foreach $id ( keys %{$vhosts{$vh}{net}} ) {
			next if( !defined $vhosts{$vh}{net}{$id}{in} );
			RRDs::update ( "$RRDDIR/".$vhosts{$vh}{rrd}."-x-".clean($id).".rrd",
				"--template", "ds0:ds1",
				"N:".$vhosts{$vh}{net}{$id}{in}.":"
					.$vhosts{$vh}{net}{$id}{out} );
			print "Updating NET:$id to ".$vhosts{$vh}{net}{$id}{in}
				.":".$vhosts{$vh}{net}{$id}{out}."\n" if($DEBUG);
  			$err = RRDs::error; if($err) { print "RRD Error: $err\n"; return; }
		}
		foreach $id ( keys %{$vhosts{$vh}{hba}} ) {
			next if( !defined $vhosts{$vh}{hba}{$id}{in} );
			RRDs::update ( "$RRDDIR/".$vhosts{$vh}{rrd}."-x-".clean($id).".rrd",
				"--template", "ds0:ds1",
				"N:".$vhosts{$vh}{hba}{$id}{in}.":"
					.$vhosts{$vh}{hba}{$id}{out} );
			print "Updating HBA:$id to ".$vhosts{$vh}{hba}{$id}{in}
				.":".$vhosts{$vh}{hba}{$id}{out}."\n" if($DEBUG);
  			$err = RRDs::error; if($err) { print "RRD Error: $err\n"; return; }
		}
	}
}

# Write the corresponding MRTG configuration file.
sub writecfg {
	my( $vhname, $vhid, $vhseq, $vhno, $id, $ifseq, $hbaid );
	my($down, $target, $f, $ff,$sufx,$mymaxcpu,$mymaxmem);
	$ifseq = "";

	$CFGFILES = $CFGFILE; $CFGFILES =~ s/\/[^\/]+\/[^\/]+$//;
	open CFG,">$CFGFILE" or do { print "$CFGFILE: $!\n"; return; };

	print CFG "BREAK\n";
	print CFG "# routers2 configuration for host $hostname\n";
	print CFG "# THIS FILE IS AUTOGENERATED! Do not change it!\n\n";

	print CFG "# NOT FOR USE IN MRTG: The data is colected by the vmgather process.\n# This is only for routers2/14all/mrtg-rrd display rules\n\n";

	print CFG "Workdir: $RRDDIR\nLogformat: rrdtool\nOptions[_]: growright\n";
	print CFG "routers.cgi*ShortDesc: $hostname\n";
	print CFG "routers.cgi*Description: VMWare server $hostname VHosts\n";
	print CFG "routers.cgi*RoutingTable: no\n";
	print CFG "routers.cgi*Icon: vmware-sm.gif\n";
	print CFG "routers.cgi*NoCache: yes\n";
	print CFG "EnableIPv6: no\n";
	print CFG "routers.cgi*Extension: Management http://$hostname/ cog-sm.gif _new noopts\n\n";
	
	# the various per-vhost graphs
	foreach $vhname ( keys %vhosts ) {
		if( defined $lookup{$vhname} ) {
			$vhid = $lookup{$vhname};
		} else {
			$vhid = -999;
		}
		$vhno = $vhosts{$vhname}{rrd};
		next if(!$vhno);
		if( $vhid == -999 ) {
			$vhseq = 9999;
			$vhid = 9999;
			$down = " (Undefined)";
		} elsif( $vhid < 0) {
			$vhseq = 8888;
			$vhid = 8888;
			$down = " (DOWN)";
		} else {
			$vhseq = $lookup{$vhid};
			$down = "";
		}
		$mymaxcpu = $vmware{"vhost-$vhid-cpu-max"};
		$mymaxmem = $vmware{"vhost-$vhid-mem-max"};
		$mymaxcpu = $states{"cpus-$vhname"} if(!$mymaxcpu);
		$mymaxmem = $states{"maxmem-$vhname"} if(!$mymaxmem);

		print CFG "\n#########################################\n";
		print CFG   "# VHost: $vhname $down\n";
		print CFG   "#########################################\n\n";

		if( $mymaxcpu ) {
		print CFG "# CPU: percentage of allocated CPU in use\n";
		print CFG "# maxcpu=$mymaxcpu\n";
#		print CFG "# CPU usage: u/s/r/w = "
#			.$vmware{"vhost-$vhid-cpu-used-pc"}."%/"
#			.$vmware{"vhost-$vhid-cpu-sys-pc"}."%/"
#			.$vmware{"vhost-$vhid-cpu-ready-pc"}."%/"
#			.$vmware{"vhost-$vhid-cpu-wait-pc"}."%"
#			."\n";
		print CFG "Target[$vhno-cpu]: $VMOID.3.1.2.1.3.$vhid&$VMOID.3.1.2.1.3.$vhid:$community\@$hostname\n";
		print CFG "Title[$vhno-cpu]: Allocated CPU usage on $vhname\[$mymaxcpu\] $down\n";
		print CFG "routers.cgi*ShortName[$vhno-cpu]: $vhname CPUs\n";
		print CFG "MaxBytes[$vhno-cpu]: $mymaxcpu\n";
		print CFG "Factor[$vhno-cpu]: ".(100/$mymaxcpu)."\n";
		print CFG "Options[$vhno-cpu]: growright \n";
		print CFG "Legend1[$vhno-cpu]: CPU usage\n";
		print CFG "Legend2[$vhno-cpu]: CPU ready\n";
		print CFG "Legend3[$vhno-cpu]: Max CPU usage\n";
		print CFG "Legend4[$vhno-cpu]: Max CPU ready\n";
		print CFG "YLegend[$vhno-cpu]: percent\n";
		print CFG "ShortLegend[$vhno-cpu]: %\n";
		print CFG "LegendI[$vhno-cpu]: active:\n";
		print CFG "LegendO[$vhno-cpu]: ready :\n";
		print CFG "routers.cgi*InMenu[$vhno-cpu]: no\n";
		print CFG "routers.cgi*InOut[$vhno-cpu]: no\n";
		print CFG "routers.cgi*InSummary[$vhno-cpu]: no\n";
		print CFG "routers.cgi*InCompact[$vhno-cpu]: no\n";
		print CFG "routers.cgi*Options[$vhno-cpu]: nopercent scaled fixunit nototal\n";
		print CFG "routers.cgi*Mode[$vhno-cpu]: generic\n";
		print CFG "routers.cgi*Graph[$vhno-cpu]: $PFX-CPU noo active\n";
		print CFG "routers.cgi*Graph[$vhno-cpu]: $PFX-CPUrdy noi active\n";
		print CFG "routers.cgi*Graph[$vhno-cpu]: $PFX-runningCPU noo active\n"
			."routers.cgi*Graph[$vhno-cpu]: $PFX-runningCPUrdy noi active\n"
			if($vhid < 8888);
#		print CFG "routers.cgi*Graph[$vhno-cpu]: $PFX-definedCPU  noo\n"
#			."routers.cgi*Graph[$vhno-cpu]: $PFX-definedCPUrdy  noi\n"
#			if($vhid < 9999);
		} else {
			print CFG "# Cannot add CPU graph as no max-cpu for vhost\n";
		}

		if( $mymaxmem ) {
#		print CFG "# Memory usage (current: u/a = "
#			.$vmware{"vhost-$vhid-mem-used"}."/"
#			.$vmware{"vhost-$vhid-mem-active"}
#			.")\n";
		print CFG "Target[$vhno-mem]: vhost-$vhid-mem:$community\@$hostname\n";
		print CFG "Title[$vhno-mem]: Memory in use on $vhname $down\n";
		print CFG "routers.cgi*ShortName[$vhno-mem]: $vhname Memory\n";
		print CFG "MaxBytes[$vhno-mem]: $mymaxmem\n";
		print CFG "Options[$vhno-mem]: growright gauge\n";
		print CFG "Legend1[$vhno-mem]: Memory usage\n";
		print CFG "Legend2[$vhno-mem]: Memory active\n";
		print CFG "Legend3[$vhno-mem]: Max memory usage\n";
		print CFG "Legend4[$vhno-mem]: Max memory active\n";
		print CFG "YLegend[$vhno-mem]: Bytes\n";
		print CFG "ShortLegend[$vhno-mem]: B\n";
		print CFG "LegendI[$vhno-mem]: used  :\n";
		print CFG "LegendO[$vhno-mem]: active:\n";
		print CFG "routers.cgi*InMenu[$vhno-mem]: no\n";
		print CFG "routers.cgi*InOut[$vhno-mem]: no\n";
		print CFG "routers.cgi*InSummary[$vhno-mem]: no\n";
		print CFG "routers.cgi*InCompact[$vhno-mem]: no\n";
		print CFG "routers.cgi*Options[$vhno-mem]: scaled bytes \n";
		print CFG "routers.cgi*Graph[$vhno-mem]: $PFX-MEM noo active\n";
		print CFG "routers.cgi*Graph[$vhno-mem]: $PFX-MEMactive total noi active\n";
		print CFG "routers.cgi*Graph[$vhno-mem]: $PFX-runningMEM noo active\n"
			."routers.cgi*Graph[$vhno-mem]: $PFX-runningMEMactive total noi active\n"
			if($vhid < 8888);
#		print CFG "routers.cgi*Graph[$vhno-mem]: $PFX-definedMEM total noo\n"
#			."routers.cgi*Graph[$vhno-mem]: $PFX-definedMEMactive total noi\n"
#			if($vhid < 9999);
		print CFG "# Memory breakdown\n";
#		print CFG "# (current: "
#			.$vmware{"vhost-$vhid-mem-private"}."/"
#			.$vmware{"vhost-$vhid-mem-shared"}."/"
#			.$vmware{"vhost-$vhid-mem-balloon"}."/"
#			.$vmware{"vhost-$vhid-mem-swap"}
#			.")\n";
		print CFG "Target[$vhno-mem-ps]: vhost-$vhid-mem-ps:$community\@$hostname\n";
		print CFG "Title[$vhno-mem-ps]: Memory in use on $vhname $down (private, shared)\n";
		print CFG "routers.cgi*ShortName[$vhno-mem-ps]: $vhname Memory\n";
		print CFG "MaxBytes[$vhno-mem-ps]: $mymaxmem\n";
		print CFG "Options[$vhno-mem-ps]: growright gauge\n";
		print CFG "Legend1[$vhno-mem-ps]: Private memory\n";
		print CFG "Legend2[$vhno-mem-ps]: Shared memory\n";
		print CFG "Legend3[$vhno-mem-ps]: Max private\n";
		print CFG "Legend4[$vhno-mem-ps]: Max shared\n";
		print CFG "YLegend[$vhno-mem-ps]: Bytes\n";
		print CFG "ShortLegend[$vhno-mem-ps]: B\n";
		print CFG "LegendI[$vhno-mem-ps]: private:\n";
		print CFG "LegendO[$vhno-mem-ps]: shared :\n";
		print CFG "routers.cgi*InMenu[$vhno-mem-ps]: no\n";
		print CFG "routers.cgi*InOut[$vhno-mem-ps]: no\n";
		print CFG "routers.cgi*InSummary[$vhno-mem-ps]: no\n";
		print CFG "routers.cgi*InCompact[$vhno-mem-ps]: no\n";
		print CFG "routers.cgi*Options[$vhno-mem-ps]: scaled bytes \n";
		print CFG "routers.cgi*Graph[$vhno-mem-ps]: $PFX-memsplit$vhno  active\n";

		print CFG "Target[$vhno-mem-bs]: vhost-$vhid-mem-bs:$community\@$hostname\n";
		print CFG "Title[$vhno-mem-bs]: Memory in use on $vhname $down (swapped, balloon)\n";
		print CFG "routers.cgi*ShortName[$vhno-mem-bs]: $vhname Memory\n";
		print CFG "MaxBytes[$vhno-mem-bs]: $mymaxmem\n";
		print CFG "Options[$vhno-mem-bs]: growright gauge\n";
		print CFG "Legend2[$vhno-mem-bs]: Swapped memory\n";
		print CFG "Legend1[$vhno-mem-bs]: Balloon memory\n";
		print CFG "Legend4[$vhno-mem-bs]: Max swapped\n";
		print CFG "Legend3[$vhno-mem-bs]: Max balloon\n";
		print CFG "YLegend[$vhno-mem-bs]: Bytes\n";
		print CFG "ShortLegend[$vhno-mem-bs]: b\n";
		print CFG "LegendO[$vhno-mem-bs]: swapped:\n";
		print CFG "LegendI[$vhno-mem-bs]: balloon:\n";
		print CFG "routers.cgi*InMenu[$vhno-mem-bs]: no\n";
		print CFG "routers.cgi*InOut[$vhno-mem-bs]: no\n";
		print CFG "routers.cgi*InSummary[$vhno-mem-bs]: no\n";
		print CFG "routers.cgi*InCompact[$vhno-mem-bs]: no\n";
		print CFG "routers.cgi*Options[$vhno-mem-bs]: scaled bytes \n";
		print CFG "routers.cgi*Graph[$vhno-mem-bs]: $PFX-memsplit$vhno \n";

		print CFG "routers.cgi*InMenu[$PFX-memsplit$vhno]: no\n";
		print CFG "routers.cgi*Summary[$PFX-memsplit$vhno]: $PFX-memsplit active\n";
		print CFG "routers.cgi*GraphStyle[$PFX-memsplit$vhno]: stack\n";
		print CFG "routers.cgi*Title[$PFX-memsplit$vhno]: Memory split for $vhname\n";
		print CFG "routers.cgi*Icon[$PFX-memsplit$vhno]: chip-sm.gif\n";
		print CFG "routers.cgi*Colours[$PFX-memsplit$vhno]: #0000ff #00ff00 #cccc00 #ff0000\n";
		} else {
			print CFG "# Cannot give memory as no max available\n";
		}

		print CFG "# Network usage\n";
		foreach $id ( keys %{$vhosts{$vhname}{net}} ) {
			$target = "$vhno-x-".clean($id);
		print CFG "Target[$target]: $VMOID.3.4.1.7.$ifseq&$VMOID.3.4.1.9.$ifseq:$community\@$hostname\n";
		print CFG "Title[$target]: Network usage on $vhname/$id $down\n";
		print CFG "routers.cgi*ShortName[$target]: $vhname:$id\n";
		print CFG "MaxBytes[$target]: 10240000000\n";
		print CFG "Options[$target]: growright bits\n";
		print CFG "routers.cgi*InMenu[$target]: no\n";
		print CFG "routers.cgi*InOut[$target]: no\n";
		print CFG "routers.cgi*InSummary[$target]: no\n";
		print CFG "routers.cgi*InCompact[$target]: no\n";
		print CFG "routers.cgi*Icon[$target]: interface-sm.gif\n";
		print CFG "routers.cgi*Options[$target]: scaled \n";

		print CFG "routers.cgi*Graph[$target]: $PFX-$id-in total noo active\n";
	print CFG "routers.cgi*Icon[$PFX-$id-in]: interface-sm.gif\n";
	print CFG "routers.cgi*ShortName[$PFX-$id-in]: $id [IN] (All VMs)\n";
	print CFG "routers.cgi*Title[$PFX-$id-in]: $id inbound on $hostname\n";
	print CFG "routers.cgi*InSummary[$PFX-$id-in]: no\n";
	print CFG "routers.cgi*InMenu[$PFX-$id-in]: no\n";
	print CFG "routers.cgi*Summary[$PFX-$id-in]: Network nodetails active\n";

		print CFG "routers.cgi*Graph[$target]: $PFX-$id-out total noi active\n";
	print CFG "routers.cgi*Icon[$PFX-$id-out]: interface-sm.gif\n";
	print CFG "routers.cgi*ShortName[$PFX-$id-out]: $id [OUT] (All VMs)\n";
	print CFG "routers.cgi*Title[$PFX-$id-out]: $id outbound on $hostname\n";
	print CFG "routers.cgi*InSummary[$PFX-$id-out]: no\n";
	print CFG "routers.cgi*InMenu[$PFX-$id-out]: no\n";
	print CFG "routers.cgi*Summary[$PFX-$id-out]: Network nodetails active\n";

		print CFG "routers.cgi*Graph[$target]: $PFX-$id total active\n";
	print CFG "routers.cgi*Icon[$PFX-$id]: interface2-sm.gif\n";
	print CFG "routers.cgi*ShortName[$PFX-$id]: $id\n";
	print CFG "routers.cgi*GraphStyle[$PFX-$id]: mirror\n";
	print CFG "routers.cgi*Title[$PFX-$id]: $id on $hostname\n";
	print CFG "routers.cgi*InSummary[$PFX-$id]: yes\n";
	
#			if($vhid < 8888 ) {
#			print CFG "routers.cgi*Graph[$target]: $PFX-running-$id-in total noo\n";
#			print CFG "routers.cgi*Graph[$target]: $PFX-running-$id-out total noi\n";
#	print CFG "routers.cgi*Icon[running-$id-in]: interface-sm.gif\n";
#	print CFG "routers.cgi*ShortName[running-$id-in]: $id [IN] (Running VMs)\n";
#	print CFG "routers.cgi*Title[running-$id-in]: $id inbound on $hostname (Running VMs)\n";
#	print CFG "routers.cgi*InSummary[running-$id-in]: yes\n";
#	print CFG "routers.cgi*Icon[running-$id-out]: interface-sm.gif\n";
#print CFG "routers.cgi*ShortName[running-$id-out]: $id [OUT] (Running VMs)\n";
#	print CFG "routers.cgi*Title[running-$id-out]: $id outbound on $hostname (Running VMs)\n";
#	print CFG "routers.cgi*InSummary[running-$id-out]: yes\n";
#			}
		} # end network ID loop
		print CFG "# HBA usage\n";
		foreach $id ( keys %{$vhosts{$vhname}{hba}} ) {
			$target = "$vhno-x-".clean($id);
		print CFG "Target[$target]: $VMOID.3.3.1.6.$ifseq&$VMOID.3.3.1.8.$ifseq:$community\@$hostname\n";
		print CFG "Title[$target]: HBA usage on $vhname/$id $down\n";
		print CFG "routers.cgi*ShortName[$target]: $vhname:$id\n";
		print CFG "MaxBytes[$target]: 10240000000\n";
		print CFG "Options[$target]: growright bits\n";
		print CFG "LegendI[$target]: Read:&nbsp;\n";
		print CFG "LegendO[$target]: Write:\n";
		print CFG "Legend1[$target]: Data read\n";
		print CFG "Legend2[$target]: Data written\n";
		print CFG "Legend3[$target]: Peak data read\n";
		print CFG "Legend4[$target]: Peak data written\n";
		print CFG "YLegend[$target]: bits per second\n";
		print CFG "ShortLegend[$target]: bps\n";
		print CFG "routers.cgi*InMenu[$target]: no\n";
		print CFG "routers.cgi*InOut[$target]: no\n";
		print CFG "routers.cgi*InSummary[$target]: no\n";
		print CFG "routers.cgi*InCompact[$target]: no\n";
		print CFG "routers.cgi*Options[$target]: scaled nomax nopercent\n";
		print CFG "routers.cgi*Icon[$target]: disk-sm.gif\n";

		print CFG "routers.cgi*Graph[$target]: $PFX-$id-in total noo active\n";
	print CFG "routers.cgi*Icon[$PFX-$id-in]: disk-sm.gif\n";
	print CFG "routers.cgi*ShortName[$PFX-$id-in]: $id [IN] (All VMs)\n";
	print CFG "routers.cgi*Title[$PFX-$id-in]: $id inbound on $hostname\n";
	print CFG "routers.cgi*InSummary[$PFX-$id-in]: no\n";
	print CFG "routers.cgi*InMenu[$PFX-$id-in]: no\n";
	print CFG "routers.cgi*Summary[$PFX-$id-in]: HBAs nodetails active\n";

		print CFG "routers.cgi*Graph[$target]: $PFX-$id-out total noi active\n";
	print CFG "routers.cgi*Icon[$PFX-$id-out]: disk-sm.gif\n";
	print CFG "routers.cgi*ShortName[$PFX-$id-out]: $id [OUT] (All VMs)\n";
	print CFG "routers.cgi*Title[$PFX-$id-out]: $id outbound on $hostname\n";
	print CFG "routers.cgi*InSummary[$PFX-$id-out]: no\n";
	print CFG "routers.cgi*InMenu[$PFX-$id-out]: no\n";
	print CFG "routers.cgi*Summary[$PFX-$id-out]: HBAs nodetails active\n";

		$hbaid=$id; $hbaid=~s/:.*$//;
		print CFG "routers.cgi*Graph[$target]: $PFX-$hbaid total active\n";
	print CFG "routers.cgi*Icon[$PFX-$hbaid]: disk-sm.gif\n";
	print CFG "routers.cgi*ShortName[$PFX-$hbaid]: $hbaid\n";
	print CFG "routers.cgi*Title[$PFX-$hbaid]: $hbaid on $hostname\n";
	print CFG "routers.cgi*InSummary[$PFX-$hbaid]: yes\n";
	print CFG "routers.cgi*InMenu[$PFX-$hbaid]: yes\n";
	print CFG "routers.cgi*GraphStyle[$PFX-$hbaid]: mirror\n";

#			if($vhid < 8888 ) {
#			print CFG "routers.cgi*Graph[$target]: $PFX-running-$id-in total noo\n";
#			print CFG "routers.cgi*Graph[$target]: $PFX-running-$id-out total noi\n";
#	print CFG "routers.cgi*Icon[running-$id-in]: disk-sm.gif\n";
#	print CFG "routers.cgi*ShortName[running-$id-in]: $id [IN] (Running VMs)\n";
#	print CFG "routers.cgi*Title[running-$id-in]: $id inbound on $hostname (Running VMs)\n";
#	print CFG "routers.cgi*InSummary[running-$id-in]: yes\n";
#	print CFG "routers.cgi*Icon[running-$id-out]: disk-sm.gif\n";
#print CFG "routers.cgi*ShortName[running-$id-out]: $id [OUT] (Running VMs)\n";
#	print CFG "routers.cgi*Title[running-$id-out]: $id outbound on $hostname (Running VMs)\n";
#	print CFG "routers.cgi*InSummary[running-$id-out]: yes\n";
#			}
		} # end HBA loop

		# now look for a mrtg cfg file for this vhostname
		$f = lc $vhname;  if( $f =~ /^\s*(\S+)/ ) { $f = $1; }
		foreach $ff ( glob( "$CFGFILES/*/$f*.cfg" ), glob( "$CFGFILES/$f*.cfg" ) ) {
			if( -f $ff ) {
				$ff =~ s/^$CFGFILES\///;
				print CFG "routers.cgi*Link[$PFX-$vhno-cpu]: \"$vhname\" $ff _summary\n";
				print CFG "routers.cgi*Link[$PFX-$vhno-mem]: \"$vhname\" $ff _summary\n";
				print CFG "routers.cgi*Link[$PFX-runningCPU]: \"$vhname\" $ff _summary\n"
				."routers.cgi*Link[$PFX-runningCPUrdy]: \"$vhname\" $ff _summary\n"
				."routers.cgi*Link[$PFX-runningMEM]: \"$vhname\" $ff _summary\n"
					if($vhid < 8888);
#				print CFG "routers.cgi*Link[definedCPU]: \"$vhname\" $ff _summary\n"
#				."routers.cgi*Link[definedCPUrdy]: \"$vhname\" $ff _summary\n"
#				."routers.cgi*Link[definedMEM]: \"$vhname\" $ff _summary\n"
#					if($vhid < 9999);
				last;
			}
		}

	} # end vhost loop
	print CFG "routers.cgi*InMenu[$PFX-memsplit]: yes\n";
	print CFG "routers.cgi*ShortName[$PFX-memsplit]: Memory Detail\n";
	print CFG "routers.cgi*Icon[$PFX-memsplit]: chip-sm.gif\n";
	print CFG "routers.cgi*GraphStyle[$PFX-memsplit]: stack\n";

	# Now the options to the sumary graphs in routers2
	my($typ);
	foreach ( qw/CPU CPUrdy runningCPU runningCPUrdy definedCPU definedCPUrdy/){
		$sufx = "All"; $sufx = "Defined" if(/^defined/); $sufx = "Running" if(/^running/);
		$typ = "CPU"; $typ = "Ready time" if(/rdy$/);
		print CFG "routers.cgi*Icon[$PFX-$_]: chip-sm.gif\n";
		print CFG "routers.cgi*ShortName[$PFX-$_]: $typ ($sufx VMs)\n";
		print CFG "routers.cgi*Title[$PFX-$_]: Guest OS $typ on $hostname\n";
		print CFG "routers.cgi*InSummary[$PFX-$_]: no \n";
		print CFG "routers.cgi*Options[$PFX-$_]: nopercent nototal \n";
		print CFG "routers.cgi*MaxBytes[$PFX-$_]: ".(abs $maxcpu)." \n";
#		print CFG "routers.cgi*HRule[$PFX-$_]: $maxcpu \"Total Available CPUs\" \n"
#			if($maxcpu>0);
		
	}

	foreach ( qw/MEM runningMEM definedMEM MEMactive runningMEMactive/){
		$sufx = "All"; $sufx = "Defined" if(/^defined/); $sufx = "Running" if(/^running/);
		$typ = ""; $typ = "Active " if(/active$/);
		print CFG "routers.cgi*Icon[$PFX-$_]: chip-sm.gif\n";
		print CFG "routers.cgi*ShortName[$PFX-$_]: Memory $typ($sufx VMs)\n";
		print CFG "routers.cgi*Title[$PFX-$_]: Guest OS Memory$typ on $hostname\n";
		print CFG "routers.cgi*InSummary[$PFX-$_]: no \n";
		print CFG "routers.cgi*Options[$PFX-$_]: nototal \n";
		print CFG "routers.cgi*MaxBytes[$PFX-$_]: ".(abs $maxmem)." \n";
		print CFG "routers.cgi*HRule[$PFX-$_]: $maxmem \"Total available memory\"\n"
			if($maxmem>0);
	}

	$f = $hostname;  if( $f =~ /^\s*([^\.]+)\./ ) { $f = $1; }
	foreach $ff ( glob( "$CFGFILES/*/$f*.cfg" ), glob( "$CFGFILES/$f*.cfg" ) ) {
		if( (-f $ff) and ($ff ne $CFGFILE) ) {
			$ff =~ s/^$CFGFILES\///;
			print CFG "routers.cgi*Link: \"ESX Server\" $ff _summary\n";
			last;
		}
	}

	close CFG;
}

sub getvmdata {
	my($k,$oid,$l,@line);
	print "(Fetching vmware-stats output)\n" if($DEBUG);
	$resp = $snmp->get_table( -baseoid=>"$UCDOID.101"); # all stat data
	if(!$resp) {
		$MSG = "Error: Unable to retrieve vmware-stats data via SNMP";
		dooutput;
		exit(0);
	}
	foreach $oid ( keys %$resp ) {
		if( $resp->{$oid} =~ /^(\S+)=(.*)/) {			
			$vmware{$1}=$2;
		}
	}
	$maxcpu = $vmware{"sys-cpu-max"};
	$maxmem = $vmware{"mem-total"};
	if(!$readvmids) {
		if( $vmware{'has-names'} ) {
			print "(Using vmware-stats output for vhost IDs)\n";
			$readvmids = 1;
			foreach ( keys %vmware ) {
				if( /vhost-(\d+)-name/ ) {
					$lookup{"999$1"} = $vmware{$_};
					$lookup{$vmware{$_}} = $1;
					$lookup{$1} = "999$1";
#					print "Added: ".$vmware{$_}." = $1\n";
				}
			}
		}
	}
	if(!$readvmids) {
		$MSG = "Unable to get a list of guests";
		dooutput;
		exit (1);
	}
}

sub getvmid {
	print "(snmp lookup of vmids)\n" if($DEBUG);


	($snmp,$snmperr) = Net::SNMP->session( -hostname=>$hostname,
		-community=>$community, -timeout=>$TIMEOUT );
	if($snmperr) {
		print "($snmperr)\n" if($DEBUG);
		$MSG = "Error: $snmperr";
		dooutput; # exit 
		exit(0);
	}
	$resp = $snmp->get_table( -baseoid=>"$VMOID.2.1.1");
	if(!$resp) {
		print "VMids lookup failed\n" if($DEBUG);
		$MSG = "WARNING: Unable to retrieve SNMP VHost data";
		return;
	}
	$readvmids = 1;
	foreach my $oid ( keys %$resp ) {
		$oid =~ /(\d+)\.(\d+)$/;
		if( $1 == 2 ) {
			$lookup{$2} = $resp->{$oid};
			$lookup{$resp->{$oid}} = $resp->{"$VMOID.2.1.1.7.$2"};
			$lookup{$resp->{"$VMOID.2.1.1.7.$2"}} = $2
				if($resp->{"$VMOID.2.1.1.7.$2"} > 0);
			print "$2: ".$lookup{$2}.": ".$lookup{$lookup{$2}}."\n" 
				if($DEBUG>1);
		}
	}
	print "Table retrieved\n" if($DEBUG);
}

sub readnet {
	my($found);
	my($vmname,$vmid,$ifid,$ifname);

	$resp = $snmp->get_table( -baseoid=>"$VMOID.3.4.1");
	if(!$resp) {
		$MSG = "Error: Unable to retrieve SNMP Network data";
		return;
	}
	foreach my $oid ( keys %$resp ) {
		$oid =~ /(\d+)\.(\d+)$/; # Type, index.
		if( $1 == 3 ) { # Running VMID.  There may be more than one!
			$ifid = $2;
			$vmid = $resp->{$oid};
			next if(!defined $lookup{$vmid});
			$vmname = $lookup{$lookup{$vmid}};
			next if(!$vmname or !defined $vhosts{$vmname});
			$ifname = $resp->{"$VMOID.3.4.1.2.$ifid"};
			next if(!$ifname);
			$vhosts{$vmname}{net} = {} if(!defined $vhosts{$vmname}{net});
			if(!defined $vhosts{$vmname}{net}{$ifname}) {
				createrrdx($vhosts{$vmname}{rrd},$ifname);
			}
			$vhosts{$vmname}{net}{$ifname} = {
				ifname=>$ifname,
				in=>($resp->{"$VMOID.3.4.1.7.$ifid"}*1024),
				out=>($resp->{"$VMOID.3.4.1.9.$ifid"}*1024)
			};
			print "NET: $vmname($ifname): "
				.$vhosts{$vmname}{net}{$ifname}{in}."/"
				.$vhosts{$vmname}{net}{$ifname}{out}."\n" if($DEBUG);
		}
	}
}

sub readhba {
	my($found);
	my($vmname,$vmid,$ifid,$ifname);

	$resp = $snmp->get_table( -baseoid=>"$VMOID.3.3.1");
	if(!$resp) {
		$MSG = "Error: Unable to retrieve SNMP HBA data";
		return;
	}
	foreach my $oid ( keys %$resp ) {
		$oid =~ /(\d+)\.(\d+)$/; # Type, index.
		if( $1 == 3 ) { # Running VMID.  There may be more than one!
			$ifid = $2;
			$vmid = $resp->{$oid};
			next if(!defined $lookup{$vmid});
			$vmname = $lookup{$lookup{$vmid}};
			next if(!$vmname or !defined $vhosts{$vmname});
			$ifname = $resp->{"$VMOID.3.3.1.2.$ifid"};
			next if(!$ifname);
			$vhosts{$vmname}{hba} = {} if(!defined $vhosts{$vmname}{hba});
			if(!defined $vhosts{$vmname}{hba}{$ifname}) {
				createrrdx($vhosts{$vmname}{rrd},$ifname);
			}
			$vhosts{$vmname}{hba}{$ifname} = {
				ifname=>$ifname,
				in=>($resp->{"$VMOID.3.3.1.6.$ifid"}*1024),
				out=>($resp->{"$VMOID.3.3.1.8.$ifid"}*1024)
			};
			print "HBA: $vmname:$ifname = "
				.$vhosts{$vmname}{hba}{$ifname}{in}."/"
				.$vhosts{$vmname}{hba}{$ifname}{out}."\n" if($DEBUG);
		}
	}
}
sub readcpu {
	my($k,@k);

	$resp = $snmp->get_request( -varbindlist=>[ "$VMOID.3.1.1.0" ] );
	if($resp) {
		$maxcpu = $resp->{"$VMOID.3.1.1.0"};
		$maxcpu = -32 if(!$maxcpu);
	} else {
		$maxcpu = -32;
	}
	print "Server has $maxcpu CPUs.\n";
	@k = ();
	foreach ( keys %lookup ) {
		push @k, "$VMOID.3.1.2.1.3.".$_ 
			if( /^\d+$/ and $_>99);
		#print "ID: $_\n" if($DEBUG);
	}
	$resp = $snmp->get_request( -varbindlist=>\@k );
	if( $resp ) {
		foreach( keys %$resp ) {
			if( /\.(\d+)$/ ) {
				$vhosts{$lookup{$lookup{$1}}}{cpu} = $resp->{$_};
				if($DEBUG) {
				print "CPU: $1 -> ".$lookup{$lookup{$1}}." = ".$resp->{$_}."\n";
				}
			}
		}
	} else {
		$MSG = "Unable to retrieve CPU statistics for ESX server: ".$snmp->error;
	}
}
sub readmem {
	my($k,@k);

	$resp = $snmp->get_request( -varbindlist=>[ "$VMOID.3.2.1.0" ] );
	if($resp) {
		$maxmem = $resp->{"$VMOID.3.2.1.0"};
		$maxmem = -102400000 if(!$maxmem);
	} else {
		$maxmem = -102400000;
	}
	print "Server has $maxmem K available.\n";
	@k = ();
	foreach ( keys %lookup ) {
		push @k, "$VMOID.3.2.4.1.3.$_", "$VMOID.3.2.4.1.4.$_"
			if( /^\d+$/ and $_>99);
	}
	$resp = $snmp->get_request( -varbindlist=>\@k );
	if( $resp ) {
		foreach( keys %$resp ) {
			if( /\.3\.(\d+)$/ ) {
				$vhosts{$lookup{$lookup{$1}}}{maxmem} = $resp->{$_} * 1024;
				print "MEM: $1 -> ".$lookup{$lookup{$1}}." = ".$resp->{$_}." Kb\n" if($DEBUG);
			} elsif( /\.4\.(\d+)$/ ) {
				$vhosts{$lookup{$lookup{$1}}}{mem} = $resp->{$_};
			}
		}
	} else {
		$MSG = "Unable to retrieve memory statistics for ESX server: ".$snmp->error;
	}
}

###########################################################################
getopts('t:hdH:c:C:m:D:');
$hostname = $opt_H if($opt_H); 
$TIMEOUT = $opt_t if($opt_t);
$community = $opt_C if($opt_C); $community = 'public' if(!$community);
$DEBUG = 1 if($opt_d);
$RRDDIR = $opt_D if($opt_D); $RRDDIR = '/tmp' if(!$RRDDIR);
$STATEFILE = $opt_c if($opt_c); $STATEFILE = "$RRDDIR/cache" if(!$STATEFILE);
$CFGFILE = $opt_m if($opt_m); $CFGFILE = "$RRDDIR/$hostname.cfg" if(!$CFGFILE);
dohelp if($opt_h);

if(!$hostname) {
	$MSG = "No ESX server hostname specified with -H";
	dooutput;
	exit 0;
}
$PFX=$hostname; $PFX =~ s/\..*$//;

readstate; # get the previous state
getvmid;   # get list of VMs, also opens SNMP object
getvmdata; # read the /proc/mem and /proc/cpu files

$maxrrd = 0;
foreach ( keys %states ) {
	next if( /^maxmem-/ );
	next if( /^cpus-/ );
	if( /^vhost-(.*)/ ) {
#		print "vhost = $1\n" if($DEBUG);
		$vhosts{$1} = {} if(!defined $vhosts{$1} );
		$vhosts{$1}{name} = $1;
		$vhosts{$1}{rrd}  = $states{$_};
		$maxrrd = $states{$_} if($states{$_}>$maxrrd);
		next;
	}
	if( /^ifname-(.*)/ ) {
		$vh = $1;
#		print "IF list = ".$states{$_}."\n" if($DEBUG);
		@list = split / /,$states{$_};
		$vhosts{$vh} = {} if(!defined $vhosts{$vh} );
		$vhosts{$vh}{net} = {};
		foreach ( @list ) { 
#			print "Already know of interface $_\n" if($DEBUG);
			$vhosts{$vh}{net}{$_} = { ifname=>$_ }; }
		next;
	}
	if( /^hbaname-(.*)/ ) {
		$vh = $1;
#		print "HBA list = ".$states{$_}."\n" if($DEBUG);
		@list = split / /,$states{$_};
		$vhosts{$vh} = {} if(!defined $vhosts{$vh} );
		$vhosts{$vh}{hba} = {};
		foreach ( @list ) { 
#			print "Already know of HBA $_\n" if($DEBUG);
			$vhosts{$vh}{hba}{$_} = { ifname=>$_ }; }
		next;
	}
	print "Bad key: $_\n";
}
print "Highest index is $maxrrd\n" if($DEBUG);

foreach (  keys %lookup ) {
	next if( /^-?\d+$/ );
	if(!defined $vhosts{$_} ) {
		$maxrrd++;
		$vhosts{$_} = { name=>$_, rrd=>$maxrrd };
		createrrd $vhosts{$_}{rrd};
	}
#	if( $lookup{$_} == -1 ) {
#		# vhost is down
#		$vhosts{$_}{mem} = 'U';
#		$vhosts{$_}{maxmem} = 'U';
#		$vhosts{$_}{cpu} = 'U';
#	}
}
print "Highest index is $maxrrd\n" if($DEBUG);
readnet; readhba; # get all the details
$snmp->close; # Done with querying SNMP
updaterrd;  # update the RRDs with the details in the vhosts hash, if held
writestate; # output all the config details
writecfg;    # create the cfg file for routers2 to display this
dooutput;   # Print any message
print "Normal exit.\n" if($DEBUG);
exit 0;
