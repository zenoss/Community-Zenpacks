#!/usr/bin/perl
# 
# Version: 1.2
# Date: 25-April-2009
# Updater: Andrew Margerison
# Summary: Minor change to code in lines 74 - 77 where test is made for literal Error or Warning in
# output returned from typeperf.  Added colon to end of literal strings to prevent script from
# indicating an error when the name of the perf counter itself contained the text Error or Warning
#
# Version: 1.1 
# Date: 30-12-07
# Author:  Mark Gold
# Summary: Script to run typeperf remotely on servers using WINEXE.  The script then retrieves performance counters from typeperf
# 	   and returns them to Zenoss.   
# Syntax:
# perfmon.pl NUMBER_OF_COUNTERS HOSTNAME USERNAME PASSWORD COUNTER1 DATAPOINT1 COUNTER2...
# Make sure there are quotes around the variables otherwise problems could occur.
#
# Arguments:
# 
# NUMBER_OF_COUNTERS : The number of counters for the script to retrieve. If this doesn't match the number of arguments then the
#		       script won't run. 
# HOSTNAME : The ip address or server hostname.
# USERNAME : The username and password for the server.  Use Domain\Username.  
# PASSWORD : Password for the username.
# COUNTER1 : The Counter name to retrieve performance data from.  Get the syntax from the Performance Monitor program.
#	     EG:   \Memory\Available bytes 
# DATAPOINT1 : The Datapoint name under Zenoss to store the counter data.
# Additional Counters and Datapoints as required.  There should always be both a datapoint and counter. The number of counters 
# should match the NUMBER_OF_COUNTERS 

# Get Args
  $numargs = $#ARGV;
  
  $counternumber = @ARGV[0];
  $additionalargs = 4 + ((2 * $counternumber)-1);

  if  ( $numargs == $additionalargs ) {
	$hostname = @ARGV[1];
	$username = @ARGV[2];
	$password = @ARGV[3];
	$counter = @ARGV[4];
	$datapoint = @ARGV[5];

	splice(@ARGV, 0, 4);
	
	$count = @ARGV; 
	while ($count >= 1)  {
		$arg = @ARGV[0];
		push (@counters, $arg);
		shift (@ARGV);
		$arg = @ARGV[0];
		push (@datapoints, $arg);
		shift (@ARGV);
		$count = @ARGV;
	}
	}
  else  {
	print "perfmon.pl NUMBER_OF_COUNTERS HOSTNAME USERNAME PASSWORD COUNTER1 DATAPOINT1 COUNTER2...\n";
	exit 0;
  }

# Format the counter string for Winexe
  $counter = '"';
  $counter = join('" "', @counters);
# Change the Username to work with winexe
  $username =~ s!//!\/!g;    

# Run Winexe and get the results
  $output = `\$ZENHOME/bin/winexe -U '$username'%'$password' //$hostname 'typeperf -sc 1 "$counter"'`;

# Check the output, and do basic error checking
  if ($output)	{
	$w = index ($output, "ERROR:");
	$x = index ($output, "Warning:");
	$y = index ($output, "Error:");
	$z = index ($output, "WARNING:");
	$checkerror = $w + $x + $y + $z;
	if ($checkerror != -4)  {
		print "Errors Found:$output\n";
		exit 0;
	}
  } 
  else  {
		print "Errors Found:$output\n";
		exit 0;
  }

# Get the performance counter fields
  @result_lines = split (/\n/, $output);
  @results_fields = split (/,/,@result_lines[2]);

# Put perfcounter results into an array
  shift (@results_fields);  
  $count = @results_fields; 
  while ($count >= 1)  {
	$results = @results_fields[0];
	$results =~ s!"!!g;
	$results = sprintf("%.2f", $results);
	push (@perfcounters, $results);
	shift (@results_fields);
	$count = @results_fields;
  }

# Create the final output from the perfcounter and datapoint arrays  

  $count = @datapoints;
  $perf_output = "";
  while ($count >= 1)  {
	$results = @datapoints[0];
	$results = $results . '=';
	shift (@datapoints);
	
	$results = $results . @perfcounters[0];
	$results = $results . ' ';
	shift (@perfcounters);
	$perf_output = $perf_output . $results; 
	$count = @datapoints;
  }
# Output the final performance counters back
  print "OK|$perf_output\n";
