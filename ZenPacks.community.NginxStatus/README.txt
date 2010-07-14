Collect and graph Nginx metrics provided by the stub_status module.
    Nginx Connections and Requests per second
        Connections Per Second
        Requests Per Second
    Nginx Requests per Connection	
        Requests Per Connection
    Nginx Connections
        Total Active Connections
	Reading
	Writing
	Waiting
	
Enable stub_status in Nginx config
http://wiki.nginx.org/NginxHttpStubStatusModule

    location /nginx_status {
        stub_status on;
        access_log   off;
        allow ZENOSS_IP;
        deny all;
    }

Attach the template to the device or device class you want to monitor.
	Navigate to the device
	:menuselection:`More --> Templates`
	:menuselection:`Bind Templates -> nginx_status` 
