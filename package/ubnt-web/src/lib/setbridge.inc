<?
switch ($wlanipmode)
{
        case 0;
        $dhcpc = "disabled";
        break;
        case 1;
	$brip = ""; $brmask = ""; $brgw = "";
        $dhcpc = "enabled";
        break;
}
set_dhcpc($cfg, $br_iface, $dhcpc);
set_ipv4($cfg, $wan_iface, "", "");
set_ipv4($cfg, $eth_iface, "", "");
set_ipv4($cfg, $wlan_iface, "", "");
set_ipv4($cfg, $br_iface, $brip, $brmask);
set_ipv4gw($cfg, $br_iface, $brgw);
set_pppoe($cfg, $wlan_iface, $wanppoeuser, $wanppoepass, $wanpppoemppe, "disabled");
set_dhcpd($cfg, $eth_iface, $dhcpd_start, $dhcpd_stop, $dhcpd_netmask, $dhcpd_lease, "disabled", $dhcpd_dnsproxy_status);
cfg_set($cfg, "iptables.status", "disabled");
set_dns($cfg, $dns1, $dns2);
set_fallback($cfg, $br_iface, $dhcpc, $fallback_ip, $fallback_netmask);
set_firewall($cfg, $firewall_status, "bridge");
cfg_set($cfg, "netmode", $netmode);
cfg_set($cfg, "bridge.status", "enabled");
cfg_set($cfg, "iptables.status", "disabled");
cfg_set($cfg, "igmpproxy.status", "disabled");
cfg_set($cfg, "dnsmasq.status", "disabled");

$st = "disabled";
if ($wlanmode == "sta") {
	$st = "enabled";
	if ($macclone == "enabled" || $macclone == "on") {
		$st = "disabled";
	}
}
cfg_set($cfg, "ebtables.1.status", $st);
cfg_set($cfg, "ebtables.1.cmd", "-t nat -A PREROUTING --in-interface " + $wlan_iface + " -j arpnat --arpnat-target ACCEPT");
cfg_set($cfg, "ebtables.2.status", $st);
cfg_set($cfg, "ebtables.2.cmd", "-t nat -A POSTROUTING --out-interface " + $wlan_iface + " -j arpnat --arpnat-target ACCEPT");
cfg_set($cfg, "ebtables.3.cmd", "-t broute -A BROUTING --protocol 0x888e --in-interface " + $wlan_iface + " -j DROP");
cfg_set($cfg, "ebtables.status", "enabled");
cfg_set($cfg, "netconf.3.status", "enabled");
cfg_set($cfg, "bridge.1.devname", "br0");
if (strlen($stp) == 0) {
	$stp = "disabled";
}
cfg_set($cfg, "bridge.1.stp.status", $stp);
cfg_set($cfg, "bridge.1.fd", "1");
cfg_set($cfg, "bridge.1.port.1.devname", "eth0");
cfg_set($cfg, "bridge.1.port.1.prio", "10");
cfg_set($cfg, "bridge.1.port.2.devname", "ath0");
cfg_set($cfg, "bridge.1.port.2.prio", "30");
cfg_set($cfg, "bridge.1.port.3.devname", "eth1");
cfg_set($cfg, "bridge.1.port.3.prio", "20");
$autoip_br_status = set_autoip($cfg, $br_iface, $autoip_br_status);
disable_ipaliases($cfg, $eth_iface, $ipaliases_max);
disable_ipaliases($cfg, $wlan_iface, $ipaliases_max);
disable_ipaliases($cfg, $wan_iface, $ipaliases_max);
cfg_disable_hwaddrs($cfg, 0);
cfg_set($cfg, "tshaper.in.1.devname", $eth_iface);
cfg_set($cfg, "tshaper.out.1.devname", $wlan_iface);
include("lib/setdef.inc");
>
