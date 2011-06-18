<?
$is_ap = 0;
if ($wlanmode == "ap" || $wlanmode == "apwds")
{
	$wan_iface = $eth_iface;
	$lan_iface = $wlan_iface;
	$is_ap = 1;
}
else
{
	$lan_iface = $eth_iface;
	$wan_iface = $wlan_iface;
}
$dhcpc = cfg_get_dhcpc($cfg, $wan_iface, $dhcpc);
$pppoe = cfg_get_pppoe($cfg, $wan_iface, $pppoe);
$wlanipmode = 0;
if ($dhcpc == "enabled")
{
	$wlanipmode = 1;
}
elseif ($pppoe == "enabled")
{
	$wlanipmode = 2;
}
$wanppoeuser = cfg_get_pppoe_user($cfg, $wan_iface, $wanppoeuser);
$wanppoepass = cfg_get_pppoe_pass($cfg, $wan_iface, $wanppoepass);
$wanpppoemppe = cfg_get_pppoe_mppe($cfg, $wan_iface, $wanpppoemppe);
$pppoemtu = cfg_get_pppoe_mtu($cfg, $wan_iface, $pppoemtu);
$pppoemru = cfg_get_pppoe_mru($cfg, $wan_iface, $pppoemru);
$wlanip = cfg_get_ipv4addr($cfg, $wlan_iface, $wlanip);
$wlanmask = cfg_get_ipv4mask($cfg, $wlan_iface, $wlanmask);
$wangw = cfg_get_ipv4gw($cfg, $wan_iface, $wangw);
$hwaddr_status = cfg_get_hwaddr_status($cfg, $wan_iface);
$hwaddr = cfg_get_hwaddr($cfg, $wan_iface);
$lanip = cfg_get_ipv4addr($cfg, $eth_iface, $lanip);
$lanmask = cfg_get_ipv4mask($cfg, $eth_iface, $lanmask);
$dhcpd_status = cfg_get_dhcpd($cfg, $lan_iface, $dhcpd_status);
$dhcpd_start = cfg_get_dhcpd_start($cfg, $lan_iface, $dhcpd_start);
$dhcpd_end = cfg_get_dhcpd_end($cfg, $lan_iface, $dhcpd_end);
$dhcpd_netmask = cfg_get_dhcpd_mask($cfg, $lan_iface, $dhcpd_netmask);
$dhcpd_lease = cfg_get_dhcpd_lease($cfg, $lan_iface, $dhcpd_lease);
$dhcpd_dnsproxy_status = cfg_get_dhcpd_dnsproxy($cfg, $lan_iface, $dhcpd_dnsproxy_status);
$dns1 = cfg_get_dns($cfg, $dns1);
$dns2 = cfg_get_dns2($cfg, $dns2);
$nat_status = cfg_get_nat($cfg, $wan_iface, $nat_status);
$dmz_status = cfg_get_DMZ_status($cfg, $wan_iface, $dmz_status);
$dmz_ip = cfg_get_DMZ_ip($cfg, $wan_iface, $dmz_ip);
$dmz_mgmt = cfg_get_DMZ_mgmt($cfg, $wan_iface, $dmz_mgmt);
$fallback_ip = cfg_get_fallback_ip($cfg, $wan_iface, $fallback_ip);
$fallback_netmask = cfg_get_fallback_netmask($cfg, $wan_iface, $fallback_netmask);
$port_forward_status = cfg_get_port_forward($cfg, $wan_iface, $port_forward_status);
$igmp_status = cfg_get_igmp_status($cfg, $wan_iface, $igmp_status);
$igmp_upstream = cfg_get_igmp_upstream($cfg, $wan_iface);
$autoip_lan_status = cfg_get_autoip($cfg, $lan_iface, $autoip_lan_status);
$autoip_wan_status= cfg_get_autoip($cfg, $wan_iface, $autoip_wan_status);
$firewall_status = cfg_get_firewall($cfg, $firewall_status, $netmode);
include("lib/getnatmodules.inc");
>
