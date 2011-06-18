#!/sbin/cgi
<?
  SecureVar("cmd*");
  SecureVar("lines");
  include("lib/settings.inc");
  $cfg = @cfg_load($cfg_file);
  include("lib/l10n.inc");
  include("lib/link.inc");
  include("lib/misc.inc");

  if ($cfg == -1) {
	  include("lib/busy.tmpl");
	  exit;
  }

  if ($radio_count < 1) {
	include("lib/linknoradio.tmpl");
	exit;
  }

  if (strlen($wep_key_type) == 0) {
	$wep_key_type = 1;
  }
  $netmode = cfg_get_def($cfg, "netmode", "bridge");
  $oldwmode = cfg_get_wmode($cfg, $wlan_iface);
  if (strlen($oldwmode) == 0) {
	  $oldwmode = "sta";
  }

  if (strlen($wmode) == 0) {
	  $wmode = $oldwmode;
  }

	if ($radio1_antennas == 1 || has_builtin_antenna() == 1) {
		if (strlen($antenna) == 0) {
			$antenna = get_antenna_diversity($cfg, $wlan_iface, "enabled");
		}
		$antenna_idx = get_antenna_index($antenna);
		if ($radio1_ant_builtin[$antenna_idx] == 1) {
			$antenna_gain = $radio1_ant_gain[$antenna_idx];
			$cable_loss = 0;
		}
	}
	else {
		$antenna_idx = 0;
	}

	if ($REQUEST_METHOD == "POST")
	{
		if ($wmode == "ap" || $wmode == "apwds")
		{
                	if (!isset($mac_acl_policy)) {
                        	$mac_acl_policy = cfg_get_mac_acl_policy($cfg, $wlan_iface, $mac_acl_policy);
                        }
			if (isset($mac_acl_mac_0))
			{
				$i = 0;
				while ($i < $mac_acl_max)
				{
					$name = "mac_acl_mac_" + $i;
					if (strlen($$name))
					{
						$mac_acl_list[] = $$name;
					}
					$i++;
				}
			}
			else
			{
				$mac_acl_list = cfg_get_mac_acl_list($cfg, $wlan_iface, $mac_acl_max);
			}
		}

		if ($feature_legacy != 1)
		{
			if (strlen($ieee_mode) == 6)
			{
				if ($clksel == "E")
				{
					$ieee_mode += "40";
					if (strstr($wmode, "ap") > 0)
					{
						$ieee_mode += $extchannel;
					}
				}
				else
				{
					$ieee_mode += "20";
				}
			}
		}

		if ($cc != "changed")
		{
			$netwarning = 0;
			if ($netmode == "router" &&
				  (get_wmode_type($oldwmode) != get_wmode_type($wmode)))
			{
				$netwarning = 1;
			}

			/* common variables */
			set_wmode($cfg, $wlan_iface, $wmode, $chan_freq, $macclone);

			set_essid($cfg, $wlan_iface, $essid);
			set_country($cfg, $wlan_iface, $country, $radio1_subsystemid);

			if (strlen($obey_regulatory_status)) {
				$obey_regulatory_status = "enabled";
			} else {
				$obey_regulatory_status = "disabled";
			}
			set_obey($cfg, $wlan_iface, $obey_regulatory_status);
            		$rtxpower = intval($txpower);
			if ($rtxpower < $radio1_txpower_offset)
			{
				$rtxpower = $radio1_txpower_offset;
			}
			set_txpower($cfg, $wlan_iface, $rtxpower);

			if ($feature_legacy != 1)
			{
				if (strstr($ieee_mode, "11ng") > 0)
				{
					$forbiasauto = 1;
				}
				else
				{
					$forbiasauto = 0;
				}
				if (strstr($ieee_mode, "ht40") > 0)
				{
					if (strstr($wmode, "sta") > 0)
					{
						$cwm_mode = 1;
					}
					else
					{
						$cwm_mode = 2;
					}
				}
				else
				{
					$cwm_mode = 0;
				}
				$cwm_enable = 0;
				cfg_set($cfg, "radio.1.cwm.mode", $cwm_mode);
				cfg_set($cfg, "radio.1.forbiasauto", $forbiasauto)
				cfg_set($cfg, "radio.1.cwm.enable", $cwm_enable);
			}
			set_ieee_mode($cfg, $wlan_iface, $ieee_mode);
			set_ack_distance($cfg, $wlan_iface, $ackdistance, $ieee_mode);
			set_rate($cfg, $wlan_iface, $rate, $rate_auto);
			cfg_set($cfg, "radio.1.mcastrate", $mcast_rate);
			set_clksel($cfg, $wlan_iface, $clksel);
			set_chanshift($cfg, $wlan_iface, $chanshift);
			set_authtype($cfg, $wlan_iface, $authtype);
			if ($radio1_antennas == 1) {
				set_antenna($cfg, $wlan_iface, $antenna, $tx_antenna, $rx_antenna);
			} else {
				set_antenna($cfg, $wlan_iface, 4, 0, 0);
			}

			if ($radio1_ant_builtin[$antenna_idx] != 1) {
				set_antenna_gain($cfg, $wlan_iface, $antenna_gain, $cable_loss);
			}

			/* mode specific */
			if ($wmode == "sta" || $wmode == "stawds")
			{
				set_apmac($cfg, $wlan_iface, $apmac);
				set_hide_ssid($cfg, $wlan_iface, "");
				set_channel_scan_list($cfg, $wlan_iface, $channel_scan_list);
				if (IsSet($scan_channels))
				{
					set_scan_channels($cfg, $wlan_iface, $scan_channels);
				}
			}
			else
			{
				$apmac = "";
				set_apmac($cfg, $wlan_iface, $apmac);
				set_hide_ssid($cfg, $wlan_iface, $hidessid);
				if ($wmode == "apwds")
				{
					set_wds_info($cfg, $wlan_iface, $wds_auto, $peer1, $peer2, $peer3, $peer4, $peer5, $peer6);
				}
				set_mac_acl($cfg, $wlan_iface, $mac_acl_status);
				set_mac_acl_policy($cfg, $wlan_iface, $mac_acl_policy);
				set_mac_acl_list($cfg, $wlan_iface, $mac_acl_list, $mac_acl_max);
			}

			set_security($cfg, $wlan_iface, $security, $wep_key_length, $wmode);
			if ($security == "wep")
			{
				set_def_wep_key_id($cfg, $wlan_iface, $wep_key_id);
				set_wep_key($cfg, $wlan_iface, $wep_key_id, $wep_key, $wep_key_type);
			}
			elseif (substr($security, 0, 3) == "wpa")
			{
				if ($wmode == "ap" || $wmode == "apwds")
				{
					set_wpa_ap($cfg, $wlan_iface, $wpa_auth, $wpa_key,
					$radius_auth_ip, $radius_auth_port, $radius_auth_secret);
				}
				else
				{
					set_wpa_sta($cfg, $wlan_iface, $wpa_auth, $wpa_key, $wpa_eap,
					$wpa_inner, $wpa_ident, $wpa_user, $wpa_passwd, $apmac);
				}
			}

			$wlanmode = $wmode;
			if ($netmode == "bridge")
			{
				include("lib/getbridge.inc");
				include("lib/setbridge.inc");
			}
			elseif ($netmode == "router")
			{
				include("lib/getrouter.inc");
				include("lib/setrouter.inc");
			}
			elseif ($netmode == "soho")
			{
				include("lib/getsoho.inc");
				include("lib/setsoho.inc");
			}

			cfg_save($cfg, $cfg_file);
			cfg_set_modified($cfg_file);
			$message = dict_translate("Configuration saved");
		}
		else
		{
			$txpower = cfg_get_txpower($cfg, $wlan_iface, $txpower);
			if ($old_country != $country)
			{
				if ($country != 511) {
					$obey_regulatory_status = "enabled";
				}
				else {
					$obey_regulatory_status = "disabled";
				}
			}

			if ($radio1_ant_builtin[$antenna_idx] != 1)
			{
				$antenna_gain = get_manual_antenna_gain($cfg, $wlan_iface, $antenna_gain);
				$cable_loss = get_cable_loss($cfg, $wlan_iface, $cable_loss);
			}

			if ($wmode == "ap" || $wmode == "apwds")
			{
				if ($feature_ap == 1) {
					$include_page="ap";
					include("lib/linkap.tmpl");
					exit;
				}
			}
			if ($wmode == "sta" || $wmode == "stawds" || $feature_ap == 0)
			{
				$channel_scan_list = cfg_get_channel_scan_list($cfg, $wlan_iface, $channel_scan_list);
				if (!IsSet($scan_channels))
				{
					$scan_channels = cfg_get_scan_channels($cfg, $wlan_iface,
						$scan_channels);
				}
				$include_page="sta";
				include("lib/linksta.tmpl");
				exit;
			}

		}
	}

  /* retrieve common variables */
  $essid = cfg_get_essid($cfg, $wlan_iface, $essid);
  $hidessid = cfg_get_hide_ssid($cfg, $wlan_iface, $hidessid);
  $ieee_mode = cfg_get_ieee_mode($cfg, $wlan_iface, $ieee_mode);

	if ($radio1_ant_builtin[$antenna_idx] != 1)
 	{
		$antenna_gain = get_manual_antenna_gain($cfg, $wlan_iface, $antenna_gain);
		$cable_loss = get_cable_loss($cfg, $wlan_iface, $cable_loss);
	}
  $country = cfg_get_country($cfg, $wlan_iface, $country);
  $old_country = $country;
  $txpower = cfg_get_txpower($cfg, $wlan_iface, $txpower);
  $rtxpower = intval($txpower);
  if ($rtxpower <= $radio1_txpower_max) {
	  $txpower = $rtxpower;
  } else {
	  $txpower = $radio1_txpower_max;
  }
  $obey_default = cfg_get_obey_default($cfg, $wlan_iface);
  $obey_regulatory_status = cfg_get_obey($cfg, $wlan_iface, $obey_default);
  $rate_auto = cfg_get_def($cfg, "radio.1.rate.auto", "enabled");
  $rate = cfg_get_rate($cfg, $wlan_iface, $rate);
  $mcast_rate = cfg_get_def($cfg, "radio.1.mcastrate", $mcast_rate);
  $clksel = cfg_get_clksel($cfg, $wlan_iface, $clksel);
  $timings = get_timings($ieee_mode, $clksel);
  $sltconst = $timings[0];
  $ackdistance = cfg_get_ackdistance($cfg, $wlan_iface, $sltconst);

  $chanshift = cfg_get_chanshift($cfg, $wlan_iface, $chanshift);
  $authtype = cfg_get_authtype($cfg, $wlan_iface, $authtype);
  $wep_key_id = cfg_get_def_wep_id($cfg, $wlan_iface, $wep_key_id);
  $wep_key = cfg_get_wep_key($cfg, $wlan_iface, $wep_key_id, $wep_key);
  $wep_key_length = cfg_get_wep_key_length($cfg, $wlan_iface, $wep_key_length);
  $wep_key_type = 1;
  if (strlen($wep_key) > 2 && "s:" == substr($wep_key, 0, 2)) {
        $wep_key_type = 2;
        $wep_key = substr($wep_key, 2, strlen($wep_key) - 2);
  }

  $essid = htmlspecialchars($essid);
  $wpa_key = htmlspecialchars(cfg_get_wpa_key($cfg, $wlan_iface, $wmode, $wpa_key));

  $wpa_auth = cfg_get_wpa_auth($cfg, $wlan_iface, $wmode, $wpa_auth);
  $wpa_eap = cfg_get_wpa_eap($cfg, $wlan_iface, $wmode, $wpa_eap);
  $wpa_inner = cfg_get_wpa_inner($cfg, $wlan_iface, $wpa_inner);
  $wpa_ident = htmlspecialchars(cfg_get_wpa_ident($cfg, $wlan_iface, $wpa_ident));
  $wpa_user = htmlspecialchars(cfg_get_wpa_user($cfg, $wlan_iface, $wpa_user));
  $wpa_passwd = htmlspecialchars(cfg_get_wpa_passwd($cfg, $wlan_iface, $wpa_passwd));

  $radius_auth_ip = cfg_get_radius_auth_ip($cfg, $wlan_iface, $radius_auth_ip);
  $radius_auth_port = cfg_get_radius_auth_port($cfg, $wlan_iface, "1812");
  $radius_auth_secret = htmlspecialchars(cfg_get_radius_auth_secret($cfg,
		$wlan_iface, "secret"));

  $security = cfg_get_security($cfg, $wlan_iface, $security, $wmode);

  if ($wmode == "sta" || $wmode == "stawds" || $feature_ap == 0) {
	  $apmac = cfg_get_apmac($cfg, $wlan_iface, $apmac);
	  $macclone = cfg_get_def($cfg, "wireless.1.macclone", $macclone);
	  $channel_scan_list = cfg_get_channel_scan_list($cfg, $wlan_iface, $channel_scan_list);
	  $scan_channels = cfg_get_scan_channels($cfg, $wlan_iface, $scan_channels);
	  $include_page="sta";
	  include("lib/linksta.tmpl");
  } else {
		if ($wmode == "apwds") {
			$info = get_wds_info($cfg, $wlan_iface);
	        $wds_auto = $info[0];
	        $peer1 = $info[1];
	        $peer2 = $info[2];
	        $peer3 = $info[3];
	        $peer4 = $info[4];
	        $peer5 = $info[5];
	        $peer6 = $info[6];
		}
		$chan_freq = cfg_get_def($cfg, "radio.1.freq", $chan_freq);
		$mac_acl_status = cfg_get_mac_acl($cfg, $wlan_iface, $mac_acl_status);
		$mac_acl_policy = cfg_get_mac_acl_policy($cfg, $wlan_iface, $mac_acl_policy);
		$mac_acl_list = cfg_get_mac_acl_list($cfg, $wlan_iface, $mac_acl_max);
		$include_page="ap";
		include("lib/linkap.tmpl");
  }
>
