#!/sbin/cgi
<?
include("lib/settings.inc");
Function getReturnCode $cmd_code
(
	$res = (($cmd_code & 65280) / 256);
	if ($res > 127) {
		$res -= 256;
	}
	return $res;
);

if ($action != "pingtest")
{
	echo "-255|Invalid or no action: " + $action;
	exit;
}

$dst_ip_addr = "";
if (strlen($dst_addr_select) > 0 && $dst_addr_select != 0)
{
	$dst_ip_addr = EscapeShellCmd($dst_addr_select);
}
elseif (strlen($dst_addr_input) > 0)
{
	$dst_ip_addr = EscapeShellCmd($dst_addr_input);
}
if ($ping_size < 28 || $ping_size > 65507)
{
	$ping_size = 56;
}
$command = $cmd_webping+" -s "+EscapeShellCmd($ping_size)+" "+$dst_ip_addr;

exec($command, $lines, $res);
$res = getReturnCode($res);
$i = 0;
echo $res;
while ($i < count($lines))
{
	echo "|"+$lines[$i];    	
	$i++;
}
>
