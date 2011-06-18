#!/sbin/cgi
<?
include("lib/settings.inc");
$cfg = @cfg_load($cfg_file);
include("lib/l10n.inc");

switch ($olsrview)
{
	case "link";
    $regexp="([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)$";
    $page_title=dict_translate("OLSR Links");
    $table_head="<th>" + dict_translate("Local IP") + "</th><th>" + dict_translate("Remote IP") + "</th><th>" + dict_translate("Hyst.") + "</th><th>" + dict_translate("LQ") + "</th><th>" + dict_translate("NLQ") + "</th><th>" + dict_translate("Cost") + "</th>";
    $cols = 6;
    break;
	case "topo";
    $regexp="([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)$";
    $page_title=dict_translate("OLSR Topology");
    $table_head="<th>" + dict_translate("Destination") + "</th><th>" + dict_translate("Last hop") + "</th><th>" + dict_translate("LQ") + "</th><th>" + dict_translate("NLQ") + "</th><th>" + dict_translate("Cost") + "</th>";
    $cols = 5;
    break;
	case "mid";
    $regexp="([^[:space:]]+)[[:space:]]+([^[:space:]]+)$";
    $page_title=dict_translate("OLSR MID");
    $table_head="<th>" + dict_translate("IP Address") + "</th><th>" + dict_translate("Aliases") + "</th>";
    $cols = 2;
    break;
	case "hna";
    $regexp="([^[:space:]]+)[[:space:]]+([^[:space:]]+)$";
    $page_title=dict_translate("OLSR HNA");
    $table_head="<th>" + dict_translate("Destination") + "</th><th>" + dict_translate("Gateway") + "</th>";
    $cols = 2;
    break;
	case "route";
    $regexp="([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)$";
    $page_title=dict_translate("OLSR Routes");
    $table_head="<th>" + dict_translate("Destination") + "</th><th>" + dict_translate("Gateway") + "</th><th>" + dict_translate("Metric") + "</th><th>" + dict_translate("ETX") + "</th><th>" + dict_translate("Interface") + "</th>";
    $cols = 5;
    break;
	case "neigh";	
  default;
    $regexp="([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)[[:space:]]+([^[:space:]]+)$";
    $page_title=dict_translate("OLSR Neighbors");
    $table_head="<th>" + dict_translate("IP Address") + "</th><th>" + dict_translate("SYM") + "</th><th>" + dict_translate("MPR") + "</th><th>" + dict_translate("MPRS") + "</th><th>" + dict_translate("Will.") + "</th><th>" + dict_translate("2 Hop Neighbors") + "</th>";
    $cols = 6;
    $olsrview = "neigh";
		break;
}
;

include("lib/ptable_head.tmpl");

echo "<tr>" + $table_head + "</tr>";

flush();

Exec("echo /" + $olsrview + " | nc localhost 2006", $lines, $result);

if ($result == 0) {
	$i = 5;
	$size = count($lines);
	while ($i < $size) {
		if (ereg($regexp,$lines[$i],$res)) {
      $j = 1;
			echo "<tr>";
      while ($j <= $cols) {
        echo "<td class=\"str\">" + $res[$j] + "</td>";
        $j++;
      }
			echo "</tr>\n";
		}
		$i++;
	}
}
>
</table>
</td></tr>
<tr><td class="change">
<input type="button" id="_refresh" onClick="return refreshContent('solsr.cgi?olsrview=<? echo $olsrview >');" value=" <? echo dict_translate("Refresh"); > "></td>
</tr></table>
</form>
</body>
</html>

