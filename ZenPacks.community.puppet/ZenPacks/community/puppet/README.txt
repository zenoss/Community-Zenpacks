
Puppet zenpack:

- Enable forwarding of syslog messages on puppet client to foward to zenoss
    *.warn	@zenossserver
- Add something in puppet which triggers logger to run like so:
    logger -p warn -t puppetd "Zenoss addserver myservername"
    Example:
	class addtozenoss {
	    exec { "add to zenoss":
		command => "logger -p warn -t puppetd \"Zenoss addserver $hostname\"",
		path => "/usr/bin"
	    }
	}
    For busy zenoss servers, you probably want to add some conditions around this so it does not run every single time, e.g. perhaps do an on boot or on kick check

- You can change which server class this defaults to or other items in Events/App/puppetd/puppetd_zenoss_commands

