#!/sbin/cgi
<?
	include("lib/settings.inc");
	$cfg = @cfg_load($cfg_file);
	include("lib/l10n.inc");
	include("lib/link.inc");

>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title><? echo get_title($cfg, dict_translate("Channel Scan List")); ></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Pragma" content="no-cache">
<link rel="shortcut icon" href="FULL_VERSION_LINK/favicon.ico" >
<link href="FULL_VERSION_LINK/style.css" rel="stylesheet" type="text/css">
<script type="text/javascript" language="javascript1.2" src="FULL_VERSION_LINK/slink.js"></script>
<script type="text/javascript" language="javascript" src="FULL_VERSION_LINK/js/jquery.js"></script>
<script type="text/javascript" language="javascript">
//<!--
<? if ($feature_chanshift == 1) { ?>
var feature_chanshift = 1;
<? } else { >
var feature_chanshift = 0;
<? }

if ($feature_ieee_mode_a == 1 && $feature_ieee_mode_bg == 0) {
        if ($ieee_mode != "at" && $ieee_mode != "ast" && $ieee_mode != "a") {
                $ieee_mode = "a";
        }
} elseif ($feature_ieee_mode_bg == 1 && $feature_ieee_mode_a == 0) {
        if ($ieee_mode != "b" && $ieee_mode != "g" && $ieee_mode != "pureg") {
                $ieee_mode = "g";
        }
}

generate_js_regdomain($country, "full_regdomain", $feature_ieee_mode_a,
	$feature_ieee_mode_bg, $feature_chanshift);
>

function chooseScanChannels()
{
	var x;
	var i;	
	var selected_channels = new Array();
	for (i = 0; i < channels.length; ++i)
	{
	 	x = document.getElementById("channel_"+i);
		if (x && x.checked)
		{
			selected_channels.push(x.value);
		}
	}
	window.opener.setScanChannels(selected_channels.join(","));
	window.close();
	return false;
}

function addRow(table, columns)
{
	var i;
	var tbody = table.getElementsByTagName("TBODY")[0];
	var row = document.createElement("TR");
	var td;

	for (i = 0; i < columns.length; ++i) {
		td = document.createElement("TD");
		td.innerHTML = columns[i];
		row.appendChild(td);    	
	}
	tbody.appendChild(row);
}

function fill_table(channels, table_id, selected_channels)
{
	var i;
	var columns = new Array();
	var c = 0;
	var table = document.getElementById(table_id);
	
	if (!table)
	{
		return false;
	}
	
	for (i in channels)
	{
		columns.push("<input type=\"checkbox\" id=\"channel_" + c
			+ "\" name=\"channel_" + c + "\" value=\"" + channels[i] + "\""
			+ ($.inArray(channels[i], selected_channels) > -1 ? " checked" : "") + ">"
			+ channels[i] + " MHz");
		c++;
		if ((c % 5) == 0)
		{
			addRow(table, columns);
			columns = new Array();
		}
	}
	if (columns.length == 0)
	{
		return true;
	}
	for (i = columns.length; i < 5; i++)
	{
		columns.push("&nbsp;");
	}
	addRow(table, columns);
	return true;
}

var ieee_mode = "<?echo $ieee_mode>".toLowerCase();
var clksel = "<?echo $clksel>";
var chanshift="<?echo $chanshift>";
var obey = '<? echo $obey; >' == 'true';
var regdomain = parse_full_regdomain(full_regdomain, chanshift);
var channels = get_scan_channels(regdomain, ieee_mode, clksel, chanshift, obey);

function init()
{
	var selected_channels = "<? echo ereg_replace("[\" ]","", $scan_channels);>".split(",");	
	fill_table(channels, "channels", selected_channels);
}
jQuery(document).ready(init);
//-->
</script>
</head>

<body class="popup">
<br>
<form enctype="multipart/form-data" action="#" method="POST" onSubmit="return chooseScanChannels();">
<table cellspacing="0" cellpadding="0" align="center" id="channels">
<tbody></tbody>
</table>
<br />
<table cellspacing="0" cellpadding="0" align="center" id="channels">
<tr>
<td><input class="fixwidth" type="submit" value="<? echo dict_translate("Ok");>"></td>
<td><input class="fixwidth" type="button" value="<? echo dict_translate("Close"); >" onClick="window.close()"></td>
</tr>
</table>
</form>
</body>
</html>


