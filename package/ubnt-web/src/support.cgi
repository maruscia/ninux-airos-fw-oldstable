#!/sbin/cgi
<?
include("lib/settings.inc");
$cfg = @cfg_load($cfg_file);
include("lib/system.inc");
$hwaddr = if_get_hwaddr($wlan_iface);
if (strlen($hwaddr) == 0) {
        $hwaddr = if_get_hwaddr($eth_iface);
}
$hwaddrstr = ereg_replace(":", "", $hwaddr);
$version = fw_get_version();
$p = strtok($version, ".");
$filename = $p + "-" + $hwaddrstr + ".sup";
$file = "/tmp/" + $filename;
$dirname = "support-" + $p + "-" + $hwaddrstr;
$ddir =  "/tmp/" + $dirname;

exec("rm -rf " + $ddir);
exec("rm -rf " + $file);
@mkdir($ddir, 0755);

exec("cp /tmp/boot.txt " + $ddir);
exec("cp /etc/board.info " + $ddir);
exec("cp /tmp/running.cfg " + $ddir);
exec("cp /tmp/system.cfg " + $ddir);
exec("cp /usr/lib/version " + $ddir);
exec("ifconfig -a > " + $ddir + "/ifconfig.txt");
exec("route -n > " + $ddir + "/routes.txt");
exec("iwconfig > " + $ddir + "/iwconfig.txt");
exec("athstats > " + $ddir + "/athstats.txt");
exec("80211stats -a > " + $ddir + "/80211stats.txt");
exec("wlanconfig ath0 list > " + $ddir + "/wlist.txt");
exec("iwlist ath0 scan > " + $ddir + "/wscan.txt");
exec("iwlist ath0 keys > " + $ddir + "/wkeys.txt");
exec("dmesg -s 16384 > " + $ddir + "/dmesg.txt");
exec("ps > " + $ddir + "/ps.txt");
exec("uptime > " + $ddir + "/uptime.txt");
exec("iwpriv wifi0 get_dacount > " + $ddir + "/dynack.txt");
exec("iwpriv wifi0 get_distance >> " + $ddir + "/dynack.txt");
exec("iwpriv wifi0 get_acktimeout >> " + $ddir + "/dynack.txt");

$syslog_status = "disabled";
$syslog_status = cfg_get_def($cfg, "syslog.status", $syslog_status);
if ($syslog_status == "enabled") {
	exec("cp /var/log/messages " + $ddir + "/syslog.txt");
}

exec("cp /proc/meminfo /proc/slabinfo /proc/loadavg /proc/vmstat /proc/modules /proc/kallsyms /proc/net/arp /proc/mtd /proc/uptime " + $ddir);

$mtd_regexp = "^mtd([^[:space:]]+):.*\"([[:print:]]+)\"";
$fp = @fopen("/proc/mtd", "r");
if ($fp > -1) {
$line=fgets($fp,255);
while(!feof($fp)) {
        $line=fgets($fp,255);
        if (ereg($mtd_regexp,$line,$res)) {
		if ($res[2] == "cfg") {
			exec("dd if=/dev/mtdblock"+$res[1]+" of="+$ddir+"/part.cfg > /dev/null 2>&1");
		} elseif ($res[2] == "EEPROM") {
			exec("dd if=/dev/mtdblock"+$res[1]+" of="+$ddir+"/part.eeprom > /dev/null 2>&1");
		}
        }
}
fclose($fp);
}

exec("tar -C /tmp -zcf " + $file + " " + $dirname);

if (fileinode($file) != -1) {
header("Content-Type: application/x-download");
header("Content-Disposition: attachment;filename=" + $filename);
passthru("cat " + $file);
exit;
}
>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head><title>Main</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Pragma" content="no-cache">
<link rel="shortcut icon" href="FULL_VERSION_LINK/favicon.ico" >
<style type="text/css">
body, td, th, table {
    font-family: Verdana, Arial, Helvetica, sans-serif;
    font-size: 12px;
}
th {
color: #990000;
font-size: 14px;
}
</style>
</head>
<body bgcolor="white">
<th>OOPS - FAILED generating support information file!</th>
</body>
</html>
