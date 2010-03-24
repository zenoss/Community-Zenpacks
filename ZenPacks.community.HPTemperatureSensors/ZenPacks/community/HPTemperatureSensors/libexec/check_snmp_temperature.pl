#!/usr/bin/perl -w
#
# ============================== SUMMARY =====================================
#
# Program : check_snmp_temperature.pl
# Version : 0.21
# Date    : Dec 25 2006 
# Author  : William Leibzon - william@leibzon.org
# Summary : This is a nagios plugin that checks temperature sensors
#           using SNMP. Dell and Cisco are supported types in this version,
#           for other systems OIDs can be specified manually.
# Licence : GPL - summary below, full text at http://www.fsf.org/licenses/gpl.txt
#
# =========================== PROGRAM LICENSE =================================
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# ===================== INFORMATION ABOUT THIS PLUGIN =========================
#
# This Temperature check plugin that retreives temperature sensor values from
# SNMP and can issue alerts if selected parameters are above given number
# It also returns performance data for further nagios 2.0 post-processing
#
# This program is written and maintained by:
#   William Leibzon - william(at)leibzon.org
# It is partially based on check_snmp_* plugins by:
#   Patrick Proy (patrick at proy.org)
#
# ============================= SETUP NOTES ====================================
#
# Make sure to check and if necessary adjust the the path to utils.pm
# Make sure you have Net::SNMP perl module installed
#
# If you want to check Dell servers, HP server, Juniper routers or
# Cisco Switches/Routers (cisco 7500, 5500, 2948) then you may skip
# much of the configuration hassles and use pre-programmed settings
# by using "--type" (or -T) parameter, you do still need to specify
# though if you want output as C or F with '-o' option (see examples). 
# The plugin currently does not support finding critical & warning
# thresholds which most systems also report in SNMP, so actual thresholds
# you will need to specify as well.
#
# If you're using some other system then you need to check documentation to
# figure out correct parameters for this plugin, then specify base temperature
# sensor names OID with '-N' and values table OID with '-D. You also will need
# to specify what base sensor temperature data type it is with "-i", see below
# (once you figure above out and it works well for you, please send me an
# email with list of those parameters so I could add it as new system type).
#
# The way plugin works is to walk the snmp tree from base names OID and find all
# the sensor names. Then it compares names given with '-a' (names are separated
# by ',') to those found in the snmp tree (in '-a' you're expected to specify
# one word which would be found in the full sensor name and is unique for that
# sensor) and uses OID ending (i.e. part of OID below the base) and adds it
# to base value table OID to create OID to be retrieved (similar to how you find
# ethernet statistics OIDs based on name of the interface and in fact many of
# SNMP parameters are like that).
#
# Note: If you don't know temperature sensor attribute names on your system do:
#         check_snmp_temperature -v -a '*' ... 
#	(using '-v' option forces debugging output that should further help)
#
# The values retrieved are compared to specified warning and critical values, 
# but first the temperature has to be converted from base measurement units to
# measurement units you want. These units are either Celsius (C) or Fahrenheit (F)
# and input measurement unit is specified with '-i' while output is '-o'. For
# input you often may have situation where sensor reports 10xRealValue, i.e.
# for 33C it reports it as 330 - in that case specify input type as '-i 10C'.
#
# Warning and critical values are specified with '-w' and '-c' and each one
# must have exact same number of values (separated by ',') as number of
# sensor names specified with '-a'. Any values you dont want to compare you
# specify as 0 (yes, I know its not quite right as you might actually want
# to compare to value of 0 degrees). In some cases you also may not get data
# for specific sensor name and want to substitute default value, use '-u' option
# for that (note that default value is in fact compared against -w and -c).
#
# Additionally if you want performance output then use '-f' option to get all
# the sensors specified in '-a' or specify particular list of sensors for
# performance data with '-A' (this list can include names not found in '-a').
# A special option of -A '*' will allow to get data from all sensors found.
#
# ========================= SETUP EXAMPLES ==================================
#
# define command {
#        command_name check_cisco_temperature
#        command_line $USER1$/check_snmp_temperature.pl -f -H $HOSTADDRESS$ --type=cisco1 -o F -C $ARG1$ -a $ARG2$ -w $ARG3$ -c $ARG4$
# }
#
# define service{
#       use                             std-service
#       hostgroup_name                  cs2948
#       service_description             Temperature
#       check_command                   check_cisco_temperature!foo!Chassis!160!190
# }
#
# define command{
# 	command_name check_dell_temperature
#  	command_line $USER1$/check_snmp_temperature.pl -H $HOSTADDRESS$ -C public \
#    		-N .1.3.6.1.4.1.674.10892.1.700.20.1.8 \
#    		-D .1.3.6.1.4.1.674.10892.1.700.20.1.6 -i 10C -o F -u 0 \
#    		-a ARG1$ -w $ARG2$ -c $ARG3$ -f
# }
#
# define service {
#  	use                     std-service
#  	hostgroup_name          dell_1750
#  	service_description     Temperature
#	check_command		check_dell_temperature!CPU,Ambient,Bottom!110,90,0!135,110,0
# }
#
# Also for some dell systems with all sensors enabled you can replace the above with:
#       check_command           check_temperature!'CPU,PROC_1,PROC_2,Ambient,Bottom,BMC Planar,BMC Riser'!110,120,120,90,90,105,105!135,140,140,110,110,125,125
#
# =================================== TODO ===================================
#
# 1. [DONE - Aug 2006] To support multiple types of equipment add config
#    array/hash and --type parameter
# 2. More plugin types for various other equipment need to be added ... 
#    [DONE - Dec 2006] - added Juniper & HP
# 3. Need to update warn & crit parameters parsing code so it would support
#    both low and high values with '<' and '>' prefixed and using '~' for
#    don't check rather then 0
#    [DONE - Dec 2006] - added quick hack to interpret empty values
#    (i.e. -w ",90,") as dont check instead of specifying '0' directly
#      Note: Low temperature value checks are rarely needed for network
#            equipment so this is not high priority right now and will
#            be done together with #4 most likely as part of some general
#            library that would be shared with check_snmp_table and quite
#            likely other plugins where multiple "attributes" are specified
# 4. Support specifying table OIDs for temperature threashold values.
#    I'll do it only after adding optional file caching so these values
#    can be retrieved about once every day rather then for each check.
#
# Note: if you want #3 or #4 done faster for specific application,
#       contact me privately to discuss
#
# ========================== START OF PROGRAM CODE ============================

use strict;

use Net::SNMP;
use Getopt::Long;
use lib "/usr/local/zenoss/common/libexec";
use utils qw(%ERRORS $TIMEOUT);
# uncomment two lines below and comment out two above lines if you do not have nagios' utils.pm
# my $TIMEOUT = 20;
# my %ERRORS=('OK'=>0,'WARNING'=>1,'CRITICAL'=>2,'UNKNOWN'=>3,'DEPENDENT'=>4);

# Below is hash array for several types of equipment, format here is that
# key is name you can specify in "--type" and data for that key is 3-value
# array with 1st value sensor names table OID (-N option), 2nd is sensor
# data table OID (-D option) and 3rd is type of temperature reading (-i)
# Additionally instead of specifying sensor names table OID and sensor data
# root table OID, the first two arguments to array can be "" and then 4th and
# 5th argument should be arrays first with list of sensor names and 2nd with
# list of OIDs for data to be retrieved (see below for how its done for Alteon)
my %system_types = ( "dell" => [ "1.3.6.1.4.1.674.10892.1.700.20.1.8", "1.3.6.1.4.1.674.10892.1.700.20.1.6", "10C" ],
		     "cisco1" => [ "1.3.6.1.4.1.9.9.13.1.3.1.2", "1.3.6.1.4.1.9.9.13.1.3.1.3", "C" ],
		     "cisco" =>  [ "1.3.6.1.4.1.9.9.13.1.3.1.2", "1.3.6.1.4.1.9.9.13.1.3.1.3", "C" ], # same as cisco 1 for now, this may change
		     "juniper" => [ "1.3.6.1.4.1.2636.3.1.13.1.5", "1.3.6.1.4.1.2636.3.1.13.1.7", "C" ], # somebody verify it, dont have juniper right now
		     "hp" => [ "1.3.6.1.4.1.232.6.2.6.8.1.3", "1.3.6.1.4.1.232.6.2.6.8.1.4", "C" ], # somebody verify this as well, only one box to test
		     "alteon" => [ "", "", "C", ['RearLeftSensor', 'RearMiddleSensor', 'FrontMiddleSensor', 'FrontRightSensor'], ['1.3.6.1.4.1.1872.2.1.1.6.0','1.3.6.1.4.1.1872.2.1.1.7.0','1.3.6.1.4.1.1872.2.1.1.8.0','1.3.6.1.4.1.1872.2.1.1.9.0'] ], # why do they need to make these alteons devices so proprietory and hard to deal with?
		   );
# APC OID for the temperature is .1.3.6.1.4.1.318.1.1.2.1.1.0
# APC OID for the humidity is .1.3.6.1.4.1.318.1.1.2.1.2.0

my $Version='0.22';

my $o_host=     undef;          # hostname
my $o_community= undef;         # community
my $o_port=     161;            # SNMP port
my $o_help=     undef;          # help option
my $o_verb=     undef;          # verbose mode
my $o_version=  undef;          # version info option
my $o_warn=     undef;          # warning level option
my @o_warnL=    ();             # array for above list
my $o_crit=     undef;          # Critical level option
my @o_critL=    ();             # array for above list
my $o_perf=     undef;          # Performance data option
my $o_timeout=  5;              # Default 5s Timeout
my $o_version2= undef;          # use snmp v2c
# SNMPv3 specific
my $o_login=    undef;          # Login for snmpv3
my $o_passwd=   undef;          # Pass for snmpv3

my $o_attr=	undef;  	# What attribute(s) to check (specify more then one separated by '.')
my @o_attrL=    ();             # array for above list
my $o_perfattr= undef;		# List of attributes to only provide values in performance data but no checking
my @o_perfattrL=();		# array for above list
my $o_ounit= 	'C';		# Output Temperature Measurement Units - can be 'C', 'F' or 'K'
my $o_iunit=	'C';		# Incoming Temperature Measurement Units - can prefix with number if its n*temp 
my $oid_names=	undef;		# OID for base of sensor attribute names
my $oid_data=	undef;		# OID for base of actual data for those attributes found when walking name base
my $o_unkdef=	undef;		# Default value to report for unknown attributes
my $o_type=	undef;		# Type of system to check (predefined values for $oid_names, $oid_data, $oid_iunit)
my $ar_sensornames= undef;	# Pointer to list of sensor names if specified in the sensor_types array
my $ar_sensoroids=undef;	# Pointer to list of sensor data oids if specified in sensor_types array

sub print_version { print "$0: $Version\n" };

sub print_usage {
	print "Usage: $0 [-v] -H <host> -C <snmp_community> [-2] | (-l login -x passwd)  [-P <port>] -T cisco1|dell | [-N <oid_attribnames> -D <oid_attribdata>] [-a <attributes to check> -w <warn levels> -c <crit levels> [-f]] [-A <attributes for perfdata>] [-t <timeout>] [-V] [-o <out_temp_unit: C|F|K>] [-i <in_temp_unit>] [-u <unknown_default>]\n";
}

# Return true if arg is a number
sub isnum {
	my $num = shift;
	if ( $num =~ /^(\d+\.?\d*)|(^\.\d+)$/ ) { return 1 ;}
	return 0;
}

sub help {
	print "\nSNMP Temperature Monitor for Nagios version ",$Version,"\n";
	print " by William Leibzon - william(at)leibzon.org\n\n";
	print_usage();
	print <<EOD;
-v, --verbose
	print extra debugging information
-h, --help
	print this help message
-H, --hostname=HOST
	name or IP address of host to check
-C, --community=COMMUNITY NAME
	community name for the host's SNMP agent (implies v 1 protocol)
-2, --v2c 
        use SNMP v2 (instead of SNMP v1)
-P, --port=PORT
	SNMPd port (Default 161)
-w, --warn=INT[,INT[,INT[..]]]
	warning temperature level(s) (if more then one attribute is checked, must have multiple values)
-c, --crit=INT[,INT[,INT[..]]]
	critical temperature level(s) (if more then one attribute is checked, must have multiple values)
-f, --perfdata
	Perfparse compatible output
-t, --timeout=INTEGER
	timeout for SNMP in seconds (Default: 5)
-V, --version
	prints version number
-N, --oid_attribnames=OID_STRING
	Base OID to walk through to find names of those attributes supported and from that corresponding data OIDs
-D, --oid_attribdata=OID_STRING
	BASE OID for sensor attribute data, one number is added to that to make up full attribute OID
-a, --attributes=STRING[,STRING[..]]
	Which attribute(s) to check. This is used as regex to check if attribute is found in attribnames.
	For Dell the attribute names to use are: PROC_1, PROC_2, Ambient, Planar, Riser
-A, --perf_attributes=STRING[,STRING[..]]
	Which attribute(s) to add to as part of performance data output. These names can be different then the
	ones listed in '-a' to only output attributes in perf data but not check. Special value of '*' gets them all.
-f, --perfparse
        Used only with '-a'. Causes to output data not only in main status line but also as perfparse output
-o  --out_temp_unit=C|F|K
	What temperature measurement units are used for output and warning/critical - 'C', 'F' or 'K' - default is 'C'
-i  --in_temp_unit=[num]C|F|K
	What temperature measurement reported by data OID - format is <num>C|F|K (default is 'C')
 	where num is used if data is num*realdata, i.e. if reported data of 330 means 33C, then its: -i 10C
-u, --unknown_default=INT
        If attribute is not found then report the output as this number (i.e. -u 0)
-T, --type=dell|hp|cisco1|juniper|alteon
	This allows to use pre-defined system type to set Base, Data OIDs and incoming temperature measurement type
	Currently support systems types are: dell, hp, cisco1 (7500, 5500, 2948, etc), juniper, alteon
EOD
}

# For verbose output - don't use it right now
sub verb { my $t=shift; print $t,"\n" if defined($o_verb) ; }

# Get the alarm signal (just in case snmp timout screws up)
$SIG{'ALRM'} = sub {
     print ("ERROR: Alarm signal (Nagios time-out)\n");
     exit $ERRORS{"UNKNOWN"};
};

# converts temperature from input format unit into output format units
sub convert_temp {
    my ($temp, $in_unit, $out_unit) = @_;

    # that is not super great algorithm if both input and output are F
    my $in_mult = 1;
    my $ctemp = undef;
    $in_mult = $1 if $in_unit =~ /(\d+)\w/;
    $in_unit =~ s/\d+//;
    $ctemp = $temp / $in_mult if $in_unit eq 'C';
    $ctemp = ($temp / $in_mult - 32) / 1.8 if $in_unit eq 'F';
    $ctemp = $temp / $in_mult - 273.15 if $in_unit eq 'F';
    $ctemp = $temp / $in_mult if !defined($ctemp);
    return $ctemp if $out_unit eq "C";
    return $ctemp * 1.8 + 32 if $out_unit eq "F";
    return $ctemp + 273.15 if $out_unit eq "K"; 
    return $ctemp; # should not get here
}

sub check_options {
    Getopt::Long::Configure ("bundling");
    GetOptions(
        'v'     => \$o_verb,            'verbose'       => \$o_verb,
        'h'     => \$o_help,            'help'          => \$o_help,
        'H:s'   => \$o_host,            'hostname:s'    => \$o_host,
        'P:i'   => \$o_port,            'port:i'        => \$o_port,
        'C:s'   => \$o_community,       'community:s'   => \$o_community,
        'l:s'   => \$o_login,           'login:s'       => \$o_login,
        'x:s'   => \$o_passwd,          'passwd:s'      => \$o_passwd,
        't:i'   => \$o_timeout,         'timeout:i'     => \$o_timeout,
        'V'     => \$o_version,         'version'       => \$o_version,
        '2'     => \$o_version2,        'v2c'           => \$o_version2,
        'c:s'   => \$o_crit,            'critical:s'    => \$o_crit,
        'w:s'   => \$o_warn,            'warn:s'        => \$o_warn,
        'f'     => \$o_perf,            'perfparse'      => \$o_perf,
        'a:s'   => \$o_attr,         	'attributes:s' 	=> \$o_attr,
	'A:s'	=> \$o_perfattr,	'perf_attributes:s' => \$o_perfattr,
	'o:s'	=> \$o_ounit,		'out_temp_unit:s' => \$o_ounit,
	'i:s'	=> \$o_iunit,		'in_temp_unit:s' => \$o_iunit,
	'u:i'	=> \$o_unkdef,		'unknown_default:i' => \$o_unkdef,
	'N:s'	=> \$oid_names,		'oid_attribnames:s' => \$oid_names,
	'D:s'	=> \$oid_data,		'oid_attribdata:s'  => \$oid_data,
	'T:s'   => \$o_type,		'type:s'	=> \$o_type
    );
    if (defined($o_help) ) { help(); exit $ERRORS{"UNKNOWN"}; }
    if (defined($o_version)) { p_version(); exit $ERRORS{"UNKNOWN"}; }
    if (! defined($o_host) ) # check host and filter
        { print "No host defined!\n";print_usage(); exit $ERRORS{"UNKNOWN"}; }
    # check snmp information
    if (!defined($o_community) && (!defined($o_login) || !defined($o_passwd)) )
        { print "Put snmp login info!\n"; print_usage(); exit $ERRORS{"UNKNOWN"}; }
    $o_ounit =~ tr/[a-z]/[A-Z]/;
    if ($o_ounit ne 'C' && $o_ounit ne 'F' && $o_ounit ne 'K') 
	{ print "Invalid output measurement unit specified!\n"; print_usage(); exit $ERRORS{"UNKNOWN"}; }
    $o_iunit =~ tr/[a-z]/[A-Z]/;
    if ($o_iunit !~ /\d*[C|K|F]/)
	{ print "Invalid input measurement unit specified!\n"; print_usage(); exit $ERRORS{"UNKNOWN"}; }
    if (defined ($o_type)) {
	if (defined($oid_names) || defined($oid_data))
	   { print "Please either specify specify system type (-T) OR base SNMP OIDs for name (-N) and data (-D) !\n"; print_usage(); exit $ERRORS{"UNKNOWN"}; }
	if (defined($system_types{$o_type})) {
	   $oid_names = $system_types{$o_type}[0];
	   $oid_data = $system_types{$o_type}[1];
	   $o_iunit = $system_types{$o_type}[2];
	   $ar_sensornames= $system_types{$o_type}[3] if defined($system_types{$o_type}[3]) && !$oid_names;
	   $ar_sensoroids= $system_types{$o_type}[4] if defined($system_types{$o_type}[4]) && !$oid_data;
	}
	else { print "Unknown system type $o_type !\n"; print_usage(); exit $ERRORS{"UNKNOWN"}; }
    }
    if (!(defined($ar_sensornames) && defined($ar_sensoroids)) && !(defined($oid_names) && defined($oid_data)))
	{ print "Specify system type (-T) OR base SNMP OIDs for name (-N) and data (-D) !\n"; print_usage(); exit $ERRORS{"UNKNOWN"}; }

    if (defined($o_perfattr)) {
        @o_perfattrL=split(/,/ ,$o_perfattr) if defined($o_perfattr);
    }
    if (defined($o_warn) || defined($o_crit) || defined($o_attr)) {
        if (defined($o_attr)) {
          @o_attrL=split(/,/, $o_attr);
          @o_warnL=split(/,/ ,$o_warn) if defined($o_warn);
          @o_critL=split(/,/ ,$o_crit) if defined($o_crit);
        }
        else {
          print "Specifying warning and critical levels requires '-a' parameter with attribute names\n";
          print_usage();
          exit $ERRORS{"UNKNOWN"};
        }
        if (scalar(@o_warnL)!=scalar(@o_attrL) || scalar(@o_critL)!=scalar(@o_attrL)) {
          printf "Number of spefied warning levels (%d) and critical levels (%d) must be equal to the number of attributes specified at '-a' (%d). If you need to ignore some attribute specify it as '0'\n", scalar(@o_warnL), scalar(@o_critL), scalar(@o_attrL);
          print_usage();
          exit $ERRORS{"UNKNOWN"};
	}
        for (my $i=0; $i<scalar(@o_attrL); $i++) {
	  $o_warnL[$i]=0 if $o_warnL[$i] eq "";
	  $o_critL[$i]=0 if $o_critL[$i] eq "";
          if (!isnum($o_warnL[$i]) || !isnum($o_critL[$i])) {
              print "Numeric value required for warning and critical !\n";
              print_usage();
              exit $ERRORS{"UNKNOWN"};
          }
          if ($o_warnL[$i] > $o_critL[$i] && $o_critL[$i]!=0) {
             print "warning must be <= critical !\n";
             print_usage();
             exit $ERRORS{"UNKNOWN"};
          }
        }
    }
    if (scalar(@o_attrL)==0 && scalar(@o_perfattrL)==0) {
        print "You must specify list of attributes with either '-a' or '-A'\n";
        print_usage();
        exit $ERRORS{"UNKNOWN"};
    }
}

########## MAIN #######

check_options();

# Check global timeout if something goes wrong
if (defined($TIMEOUT)) {
  verb("Alarm at $TIMEOUT");
  alarm($TIMEOUT);
} else {
  verb("no timeout defined : $o_timeout + 10");
  alarm ($o_timeout+10);
}

# SNMP Connection to the host
my ($session,$error);
if (defined($o_login) && defined($o_passwd)) {
  # SNMPv3 login
  verb("SNMPv3 login");
  ($session, $error) = Net::SNMP->session(
      -hostname         => $o_host,
      -version          => '3',
      -username         => $o_login,
      -authpassword     => $o_passwd,
      -authprotocol     => 'md5',
      -privpassword     => $o_passwd,
      -timeout          => $o_timeout
   );
} else {
   if (defined ($o_version2)) {
     # SNMPv2 Login
         ($session, $error) = Net::SNMP->session(
        -hostname  => $o_host,
            -version   => 2,
        -community => $o_community,
        -port      => $o_port,
        -timeout   => $o_timeout
     );
   } else {
    # SNMPV1 login
    ($session, $error) = Net::SNMP->session(
       -hostname  => $o_host,
       -community => $o_community,
       -port      => $o_port,
       -timeout   => $o_timeout
    );
  }
}

# next part of the code builds list of attributes to be retrieved
my $i;
my $oid;
my $line;
my $attr;
my @varlist = ();
my %dataresults;

for ($i=0;$i<scalar(@o_attrL);$i++) {
  $dataresults{$o_attrL[$i]} = ["check", undef, undef];
}
if (defined($o_perfattr) && $o_perfattr ne '*') {
  for ($i=0;$i<scalar(@o_perfattrL);$i++) {
    $dataresults{$o_perfattrL[$i]} = ["perf", undef, undef];
  }
}

verb("Retrieving SNMP table $oid_names to find sensor attribute names");
my $result;

if (!defined($ar_sensornames)) {
    $result = $session->get_table( -baseoid => $oid_names );
    if (!defined($result)) {
        printf("ERROR: Problem retrieving OID %s table: %s.\n", $oid_names, $session->error);
        $session->close();
        exit $ERRORS{"UNKNOWN"};
    }
    L1: foreach $oid (Net::SNMP::oid_lex_sort(keys %{$result})) {
        $line=$result->{$oid};
        verb("got $oid : $line");
	foreach $attr (keys %dataresults) {
	   if ($line =~ /$attr/) {
		$oid =~ s/$oid_names/$oid_data/;
		$dataresults{$attr}[1] = $oid;
		push(@varlist,$oid);
		verb("match found for $attr, now set to retrieve $oid");
		next L1;
	   }
	}
	if (defined($o_perfattr) && $o_perfattr eq '*') {
		$oid =~ s/$oid_names/$oid_data/;
		$dataresults{$line} = ["perf", $oid, undef];
		push(@varlist,$oid);
		verb("match found based on -A '*', now set to retrieve $oid");
	}
    }
}
else {
    my $i;
    for ($i=0;$i<scalar(@{$ar_sensornames});$i++) {
	$line=$ar_sensornames->[$i];
	$oid=$ar_sensoroids->[$i];
        L2: foreach $attr (keys %dataresults) {
           if ($line =~ /$attr/) {
                $dataresults{$attr}[1] = $oid;
                push(@varlist,$oid);
                verb("match found for $attr, now set to retrieve $oid");
                next L2;
           }
        }
        if (defined($o_perfattr) && $o_perfattr eq '*') {
                $dataresults{$line} = ["perf", $oid, undef];
                push(@varlist,$oid);
                verb("match found based on -A '*', now set to retrieve $oid");
        }
    }
}

# now we actually retrieve the attributes
my $statuscode = "OK";
my $statusinfo = "";
my $statusdata = "";
my $perfdata = "";

verb("Getting SNMP data for oids" . join(" ",@varlist));
$result = $session->get_request(
	-Varbindlist => \@varlist
);
if (!defined($result)) {
        printf("ERROR: Can not retrieve OID(s) %s: %s.\n", join(" ",@varlist), $session->error);
        $session->close();
        exit $ERRORS{"UNKNOWN"};
}
else {
	foreach $attr (keys %dataresults) {
	    if (defined($dataresults{$attr}[1]) && defined($$result{$dataresults{$attr}[1]})) {
		$dataresults{$attr}[2]=convert_temp($$result{$dataresults{$attr}[1]},$o_iunit,$o_ounit);
		verb("got $dataresults{$attr}[1] : $attr = $dataresults{$attr}[2]");
	    }
	    else { 
		if (defined($o_unkdef)) {
		   $dataresults{$attr}[2]=$o_unkdef;
		   verb("could not find snmp data for $attr, setting to to default value $o_unkdef");
		}
		else {
		   verb("could not find snmp data for $attr");
		}
	    }
	}
} 

# loop to check if warning & critical attributes are ok
for ($i=0;$i<scalar(@o_attrL);$i++) {
  if (defined($dataresults{$o_attrL[$i]}[2])) {
    if ($dataresults{$o_attrL[$i]}[2]>$o_critL[$i] && $o_critL[$i]>0) {
	$statuscode="CRITICAL";
	$statusinfo .= " " . $o_attrL[$i] . " Temperature is " . $dataresults{$o_attrL[$i]}[2] . $o_ounit . " > ". $o_critL[$i] . $o_ounit;
    }
    elsif ($dataresults{$o_attrL[$i]}[2]>$o_warnL[$i] && $o_warnL[$i]>0) {
	$statuscode="WARNING" if $statuscode eq "OK";
	$statusinfo .= " " . $o_attrL[$i] . " Temperature is " . $dataresults{$o_attrL[$i]}[2] . $o_ounit . " > ". $o_warnL[$i] . $o_ounit;
    }
    else {
	$statusdata .= "," if ($statusdata);
	$statusdata .= " " . $o_attrL[$i] . " Temperature is " . $dataresults{$o_attrL[$i]}[2] . $o_ounit;
    }
    $perfdata .= " " . $o_attrL[$i] . "=" . $dataresults{$o_attrL[$i]}[2] if defined($o_perf) && $dataresults{$o_attrL[$i]}[0] ne "perf";
  }
  else {
	$statusdata .= "," if ($statusdata);
        $statusdata .= " $o_attrL[$i] data is missing";
  }
}

# add data for performance-only attributes
if (defined($o_perfattr) && $o_perfattr eq '*') {
  foreach $attr (keys %dataresults) {
     if ($dataresults{$attr}[0] eq "perf" && defined($dataresults{$attr}[2])) {
	$perfdata .= " " . $attr . "=" . $dataresults{$attr}[2];
     }
  }
}
else {
  for ($i=0;$i<scalar(@o_perfattrL);$i++) {
     if (defined($dataresults{$o_perfattrL[$i]}[2])) {
	$perfdata .= " " . $o_perfattrL[$i] . "=" . $dataresults{$o_perfattrL[$i]}[2];
     }
  }
}

$session->close;
print $statuscode . $statusinfo;
print " -".$statusdata if $statusdata;
print " |".$perfdata if $perfdata;
print "\n";

exit $ERRORS{$statuscode};
