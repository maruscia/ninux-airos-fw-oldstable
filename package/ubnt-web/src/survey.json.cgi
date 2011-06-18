#!/sbin/cgi
<?
include("lib/settings.inc");
PassThru("iwlist "+$wlan_iface+" scan | " + $cmd_scanparser);
>
