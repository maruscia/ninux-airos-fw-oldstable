function handleError(xhr, textStatus, errorThrown) {
	if (xhr && xhr.status != 200 && xhr.status != 0)
		window.location.reload();
}

function kickEnd(data, textStatus, xhr) {
	$(this).enable();
	refreshStaList();
}

function kickStation(a, ifname, hwaddr) {
	$(a).parent().parent('tr').hide();
	var kick_url = '/stakick.cgi?staif=' + ifname + '&staid=' + hwaddr;
	jQuery.ajax({
		url: kick_url,
		cache: false,
		dataType: "json",
		success: kickEnd,
		error: handleError
	});
	return false;
}

function refreshStaList() {
	$.ajax({
		cache: false,
		url: '/sta.cgi',
		dataType: 'json',
		success: showStaList,
		error: handleError
	});
}

function refreshAll() {
	if (typeof reloadStatus == 'function')
		reloadStatus();
	refreshStaList();
}

function showStaList(sl) {
	$('#sta_list > tbody').empty();

	var tbody = [];
	for (var i = 0; i < sl.length; ++i) {
		var sta = sl[i];
		
		var row = [];
		row.push('<tr>');

		var win_height = sta.rates.length > 8 ? 520 : 400;
		var open_page = 'openPage(\'stainfo.cgi?ifname=' + sl_global.wlan_iface + '&sta_mac=' + sta.mac + '\', 700, ' + win_height + ');';

		row.push('<td><a href="#" onClick="' + open_page + '">' + sta.mac + '</a>' +
			((sta.apwds == 0) ? '' : '&nbsp;(' + $.l10n._('AP-WDS') + ')') + '&nbsp;&nbsp;&nbsp;</td>');
		row.push('<td>' + sta.name.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') + '&nbsp;</td>');
		row.push('<td class="centered">' + sta.signal + '&nbsp;/&nbsp;' + sta.noisefloor + '</td>');
		if (sl_global.autoack)
			row.push('<td class="centered">' + (sta.ack > 0 ? sta.ack : sl_global.ack) + '</td>');
		row.push('<td class="centered">' + sta.tx + '&nbsp;/&nbsp;' + sta.rx + '</td>');
		row.push('<td class="centered">' + ((sta.ccq > 0) ? sta.ccq : '-') + '</td>');
		row.push('<td>' + secsToCountdown(sta.uptime, $.l10n._('day'), $.l10n._('days')) + '</td>');

		var lastip_str = (sta.lastip != '0.0.0.0') ?
			'<a href="http://' + sta.lastip + '" target="_blank">' + sta.lastip + '</a>' : lastip_str = $.l10n._('unknown');
		row.push('<td>' + lastip_str + '</td>');

		var kick_str = '&nbsp;';
		if (sta.apwds == 0) {
			kick_str = '<a href="#" onClick="return kickStation(this, \'' + sl_global.wlan_iface + '\', \'' + sta.mac + '\');">kick</a>';
		}
		row.push('<td class="centered">' + kick_str + '</td>');
		row.push('</tr>');
		tbody.push(row.join(''));
	}

	if (sl.length == 0 || typeof sl.length == 'undefined')
		tbody.push('<tr><td colspan="' + $('#sta_list >thead >tr >th').length + '">' + $.l10n._('No Associated Stations') + '</td></tr>');

	$('#sta_list > tbody').append(tbody.join(''));
}

$(document).ready(function() {
	$.l10n.init({ dictionary: l10n_stalist });
	$('#_refresh').click(refreshAll);
	refreshStaList();
});
