#!/sbin/cgi
<?
header("Content-Type: application/x-download");
header("Content-Disposition: attachment;filename=olsrd.conf");

if (fileinode("/etc/persistent/olsrd.conf") == -1)
{
  passthru("cat /usr/etc/olsrd.conf");
  exit;
}
passthru("cat /etc/persistent/olsrd.conf");
exit;
>
