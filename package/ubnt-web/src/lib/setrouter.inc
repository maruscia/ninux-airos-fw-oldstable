<?
switch ($wlanipmode)
{
	case 0;
	$dhcpc = "disabled";
	$pppoe = "disabled";
	break;
	case 1;
	if ($wlanmode != "ap" && $wlanmode != "apwds") {
		$wlanip = ""; $wlanmask = ""; $wangw = "";
        }
	$dhcpc = "enabled";
	$pppoe = "disabled";
	break;
	case 2;
	$dhcpc = "disabled";
	$pppoe = "enabled";
	$wangw = "";
	$natifc = "ppp+";
	break;
}
if ($wlanmode == "ap" || $wlanmode == "apwds") {
	$wan_iface = $eth_iface;
	$lan_iface = $wlan_iface;
	$wan_idx = 1;
} else {
	$lan_iface = $eth_iface;
	$wan_iface = $wlan_iface;
	$wan_idx = 2;
}
set_ipv4($cfg, $wan_iface, "", "");
set_ipv4($cfg, $wlan_iface, $wlanip, $wlanmask);
set_ipv4($cfg, $eth_iface, $lanip, $lanmask);
set_ipv4gw($cfg, $wan_iface, $wangw);
cfg_set_hwaddr($cfg, $wan_iface, $hwaddr_status, $hwaddr);
set_dhcpc($cfg, $wan_iface, $dhcpc);
set_pppoe($cfg, $wan_iface, $wanppoeuser, $wanppoepass, $wanpppoemppe, $pppoe, $pppoemtu, $pppoemru);
set_dhcpd($cfg, $lan_iface, $dhcpd_start, $dhcpd_end, $dhcpd_netmask, $dhcpd_lease, $dhcpd_status, $dhcpd_dnsproxy_status);
set_dns($cfg, $dns1, $dns2);
if (strlen($natifc) == 0) {
	$natifc = $wan_iface;
}
set_nat($cfg, $natifc, $nat_status);

include("lib/setnatmodules.inc");

set_DMZ($cfg, $natifc, $dmz_status, $dmz_ip, $dmz_mgmt);
set_fallback($cfg, $wan_iface, $dhcpc, $fallback_ip, $fallback_netmask);
set_port_forward($cfg, $natifc, $port_forward_status);
set_firewall($cfg, $firewall_status, "router");
if ($nat_status=="on" || $nat_status=="enabled" ||
	$dmz_status=="on" || $dmz_status=="enabled" ||
	$port_forward_status=="enabled" || $pppoe=="enabled" ||
        $firewall_status=="enabled")
{
	cfg_set($cfg, "iptables.status", "enabled");
}
else {
	cfg_set($cfg, "iptables.status", "disabled");
}
if ($igmp_status=="on" || $igmp_status=="enabled")
{
	cfg_set($cfg, "igmpproxy.status", "enabled");
        if ($igmp_upstream == "lan") {
	        $lan_stream = "upstream";
        	$wan_stream = "1.downstream";
        } else {
	        $wan_stream = "upstream";
        	$lan_stream = "1.downstream";
        }
	if ($pppoe != "enabled") {
		cfg_set($cfg, "igmpproxy."+$wan_stream+".devname", $wan_iface);
	} else {
		cfg_set($cfg, "igmpproxy."+$wan_stream+".devname", "ppp0");
	}
	cfg_set($cfg, "igmpproxy."+$lan_stream+".devname", $lan_iface);
}
else {
	cfg_set($cfg, "igmpproxy.status", "disabled");
}
cfg_set($cfg, "netmode", $netmode);
cfg_set($cfg, "bridge.status", "disabled");
cfg_set($cfg, "ebtables.status", "disabled");
cfg_set($cfg, "netconf.3.status", "disabled");
cfg_set($cfg, "wireless.1.macclone", "disabled");
$autoip_lan_status = set_autoip($cfg, $lan_iface, $autoip_lan_status);
$autoip_wan_status = set_autoip($cfg, $wan_iface, $autoip_wan_status);
disable_ipaliases($cfg, $br_iface, $ipaliases_max);
cfg_disable_hwaddrs($cfg, $wan_idx);
cfg_set($cfg, "tshaper.in.1.devname", $eth_iface);
cfg_set($cfg, "tshaper.out.1.devname", $wlan_iface);
include("lib/setdef.inc");
>
