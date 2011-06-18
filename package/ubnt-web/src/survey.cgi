#!/sbin/cgi
<?
include("lib/settings.inc");
$cfg = @cfg_load($cfg_file);
include("lib/l10n.inc");
include("lib/link.inc");

$wmode = w_get_mode($wlan_iface);

if ($feature_ap_scan != 1) {
	if ($wmode == 3) {
		include("lib/err_scan.tmpl");
		exit;
	}
}

if ($feature_chanlist == 1) {
	$chanlist_active = file("/proc/sys/net/"+$wlan_iface+"/chanlist");
	$chans =  $chanlist_active[0];
}

$cmd_regex = "([[:print:]]*):([[:print:]]*)$";

Function get_cmdresult $cmd, $rgx, $ridx
(
	Exec($cmd, $arr, $result);
	if ($result == 0) {
		if (ereg($rgx, $arr[0], $res)) {
			return $res[$ridx];
		}
	}

	return "";
);

Function get_clksel
(
	global $cmd_regex;
	$cmd = "iwpriv wifi0 GetClkSel";

	$result = get_cmdresult($cmd, $cmd_regex, 2);
	switch ($result) {
		case "4";
			$clksel = 2;
			break;
		case "2";
			$clksel = 1;
			break;
		default;
			$clksel = 0;
			break;
	}

	return $clksel;
);

Function get_ieeemode
(
	global $wlan_iface, $cmd_regex;
	$cmd = "iwpriv " + $wlan_iface + " get_mode";

	return get_cmdresult($cmd, $cmd_regex, 2);
);

$clksel = get_clksel();
$ieee_mode = get_ieeemode();

include("lib/survey.tmpl");
>
