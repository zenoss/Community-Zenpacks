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

my $host_view = Vim::find_entity_views(
	view_type => 'HostSystem'
);

my $host = @$host_view[0];

print $host->summary->config->product->vendor . ";" . $host->summary->config->product->name . " " . $host->summary->config->product->licenseProductVersion . ";" . $host->summary->hardware->vendor . ";" . $host->summary->hardware->model . "\n";


Util::disconnect();
