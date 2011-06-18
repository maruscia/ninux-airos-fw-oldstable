<?
$ipaddress = 0;
$lanipaddress = 0;
$http_proto = "";
$http_port = "";
if ($cfg_bak != -1) {
	$cfg_bak = @cfg_load($cfg_file_bak);
	$wlanmode = cfg_get_wmode($cfg, $wlan_iface);
	$cfgnetmode = cfg_get_def($cfg, "netmode", "bridge");
	if ($cfgnetmode == "bridge") {
		$ipaddress = cfg_get_ipv4addr($cfg, $br_iface, $defip);
                if ($cfg_bak == -1) {
                	$running_ip = if_get_ipaddr($br_iface);
                } else {
                	$running_ip = cfg_get_ipv4addr($cfg_bak, $br_iface, $defip);
                }
                if ($ipaddress == $running_ip) {
       	        	$ipaddress = 0;
                }
                $lanipaddress = $ipaddress;
	} else {
              	if ($cfgnetmode == "router") {
	        	if ($wlanmode == "ap" || $wlanmode == "apwds") {
				$wan_iface = $eth_iface;
				$lan_iface = $wlan_iface;
		        } else {
                		$wan_iface = $wlan_iface;
				$lan_iface = $eth_iface;
                        }
	        }

		$ipaddress = cfg_get_ipv4addr($cfg, $wan_iface, $defip);
                $lanipaddress = cfg_get_ipv4addr($cfg, $lan_iface, $defip);
                if ($cfg_bak == -1) {
	                $running_ip = if_get_ipaddr($wan_iface);
        	        $running_lanip = if_get_ipaddr($lan_iface);
                } else {
			$running_ip = cfg_get_ipv4addr($cfg_bak, $wan_iface, $defip);
			$running_lanip = cfg_get_ipv4addr($cfg_bak, $lan_iface, $defip);
                
                }
              	if ($ipaddress == $running_ip) {
               		$ipaddress = 0;
                }
       	        if ($lanipaddress == $running_lanip) {
       			$lanipaddress = 0;
                }
        }
       	$https_state = cfg_get_def($cfg, "httpd.https.status", "disabled");
        if ($https_state == "enabled") {
        	$http_proto = "https";
	        $http_port = cfg_get_def($cfg, "httpd.https.port", "443");
        } else {
        	$http_proto = "http";
	        $http_port = cfg_get_def($cfg, "httpd.port", "80");
        }
        if ($cfg_bak != -1) {
       		$running_https_state = cfg_get_def($cfg_bak, "httpd.https.status", "disabled");
	        if ($running_https_state == "enabled") {
        		$running_http_proto = "https";
	        	$running_http_port = cfg_get_def($cfg_bak, "httpd.https.port", "443");
	        } else {
        		$running_http_proto = "http";
	        	$running_http_port = cfg_get_def($cfg_bak, "httpd.port", "80");
	        }
        }
        if ($https_state == $running_https_state &&
            $http_proto == $running_http_proto &&
            $http_port == $running_http_port) {
            $http_proto = "";
            $http_port = "";
        }
}
>
