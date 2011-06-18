#!/sbin/cgi
<?
include("lib/settings.inc");
$cfg = @cfg_load($cfg_file);
include("lib/l10n.inc");
include("lib/misc.inc");

$global_ack = 0;
$autoack = cfg_get_def($cfg, "radio.1.ack.auto", "disabled");
if ($autoack == "enabled") {
	$global_ack = get_current_ack();
}
>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title><? echo dict_translate("Associated Stations"); ></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Pragma" content="no-cache">
<link rel="shortcut icon" href="FULL_VERSION_LINK/favicon.ico" >
<link href="FULL_VERSION_LINK/style.css" rel="stylesheet" type="text/css">
</head>

<body class="popup">
<script type="text/javascript" src="FULL_VERSION_LINK/js/jquery.js"></script>
<script type="text/javascript" src="FULL_VERSION_LINK/js/jquery.l10n.js"></script>
<script type="text/javascript" src="FULL_VERSION_LINK/js/jquery.utils.js"></script>
<script type="text/javascript" src="FULL_VERSION_LINK/util.js"></script>
<script type="text/javascript" language="javascript">

var l10n_stalist = {
	'day' : '<? echo dict_translate("day"); >',
	'days' : '<? echo dict_translate("days"); >',
	'unknown' : '<? echo dict_translate("unknown"); >',
	'AP-WDS' : '<? echo dict_translate("AP-WDS"); >',
	'No Associated Stations' : '<? echo dict_translate("No Associated Stations"); >',
	'_' : '_'
};

var sl_global = {
	'wlan_iface' : '<? echo $wlan_iface; >',
	'autoack' : ('<? echo $autoack; >' == 'enabled'),
	'ack' : '<? echo $global_ack; >',
	'_': '_'
};

</script>
<script type="text/javascript" src="FULL_VERSION_LINK/stalist.js"></script>

<br>
<form action="<?echo $PHP_SELF;>" method="GET">
<table cellspacing="0" cellpadding="0" align="center">
	<tr>
		<td>
			<table cellspacing="0" cellpadding="0" class="listhead sortable" id="sta_list">
				<thead>
					<tr>
						<th><? echo dict_translate("Station MAC"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("Device Name"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("Signal") + " / "+ dict_translate("Noise"); >, dBm&nbsp;&nbsp;&nbsp;</th>
						<? if ($autoack == "enabled") { >
							<th><? echo dict_translate("ACK"); >&nbsp;&nbsp;&nbsp;</th>
						<? } >
						<th><? echo dict_translate("TX/RX"); >, Mbps&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("CCQ"); >, %&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("Connection Time"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("Last IP"); >&nbsp;&nbsp;&nbsp;</th>
						<th><? echo dict_translate("Action"); >&nbsp;</th>
					</tr>
				</thead>
				<tbody>
				</tbody>
			</table>
		</td>
	</tr>
	<tr>
		<td class="change">
			<input type="button" id="_refresh" value="<? echo dict_translate("Refresh"); >">
		</td>
	</tr>
</table>
</form>
</body>
</html>
