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

  $aimaxprimax = 3;
  $wmm_status = cfg_get_def($cfg, "wireless.1.wmm", "disabled");
  $level = cfg_get_def($cfg, "wireless.1.wmmlevel", "2");
  $wmode_type = get_wmode_type(cfg_get_wmode($cfg, $wlan_iface));
  $ieee_mode = cfg_get_ieee_mode($cfg, $wlan_iface, $ieee_mode);
  $ieee_mode = strtolower($ieee_mode);
  $netmode_cfg = cfg_get_def($cfg, "netmode", "bridge");
  if (strlen($netmode)==0) {
	$netmode = $netmode_cfg;
  }

  if ($REQUEST_METHOD == "POST") {
	$wmm_status = wmm_get_status($wmm_level);
	cfg_set($cfg, "wireless.1.wmm", $wmm_status);
	cfg_set($cfg, "wireless.1.wmmlevel", $wmm_level);
        $level = $wmm_level;
	set_rts_treshold($cfg, $wlan_iface, $rts, $rtsoff);
	set_frag_treshold($cfg, $wlan_iface, $frag, $fragoff);
	set_ack_distance($cfg, $wlan_iface, $ackdistance, $ieee_mode);
	set_autoack($cfg, $wlan_iface, $autoack);
  	if ($feature_super == 0)
	{
		$fast_frame = 0;
		$burst = 0;
		$compression = 0;
	}
	set_fast_frame($cfg, $wlan_iface, $fast_frame);
	set_bursting($cfg, $wlan_iface, $burst);
	set_compression($cfg, $wlan_iface, $compression);
	if ($feature_ratemodule == 1) {
		cfg_set($cfg, "radio.ratemodule", $rate_module);
	}
	cfg_set_signal_leds($cfg, $led1, $led2, $led3, $led4);

	if (strlen($shaper_status)){
		$shaper_status = "enabled";
                if ($netmode == "soho") {
                	$out_iface = $wan_iface;
                        $in_iface = $lan_iface;
                } else {
                	$in_iface = $eth_iface;
                        $out_iface = $wlan_iface;
                }
		cfg_set($cfg, "tshaper.in.1.devname", $in_iface);
		cfg_set($cfg, "tshaper.out.1.devname", $out_iface);
		cfg_set($cfg, "tshaper.in.rate", $in_rate);
		cfg_set($cfg, "tshaper.out.rate", $out_rate);
		if (strlen($in_burst) == 0 || $in_burst == "0") {
			$in_burst = 0;
			cfg_set($cfg, "tshaper.in.burst", $in_burst);
			cfg_set($cfg, "tshaper.in.cburst", $in_burst);
		} else {
			cfg_set($cfg, "tshaper.in.burst", $in_burst);
			cfg_set($cfg, "tshaper.in.cburst", "2");
		}
		if (strlen($out_burst) == 0 || $out_burst == "0") {
			$out_burst = 0;
			cfg_set($cfg, "tshaper.out.burst", $out_burst);
			cfg_set($cfg, "tshaper.out.cburst", $out_burst);
		} else {
			cfg_set($cfg, "tshaper.out.burst", $out_burst);
			cfg_set($cfg, "tshaper.out.cburst", "2");
		}
	} else {
		$shaper_status = "disabled";
	}
	cfg_set($cfg, "tshaper.status", $shaper_status);

	if ($feature_legacy != 1) {
		if (strlen($aggr_status)){
			$aggr_status = "enabled";
			cfg_set($cfg, "radio.1.ampdu.frames", $aggr_frames);
			cfg_set($cfg, "radio.1.ampdu.bytes", $aggr_bytes);
		} else {
			$aggr_status = "disabled";
		}
		cfg_set($cfg, "radio.1.ampdu.status", $aggr_status);
	}

	if (strlen($mcast_status)){
        	$mcast_status = "enabled";
        } else {
        	$mcast_status = "disabled";
        }
	if (strlen($client_isolation_status))
	{
		$client_isolation_status = "enabled";
	}
	else
	{
		$client_isolation_status = "disabled";
	}

	if (!$feature_locked_countrycode) {
		if (strlen($polling)) {
			$polling = "enabled";
		} else {
			$polling = "disabled";
		}

		cfg_set($cfg, "radio.1.polling", $polling);
	}
	cfg_set($cfg, "radio.1.pollingnoack", $polling_noack_value);

	if (strlen($mtikie)) {
		$mtikie = "enabled";
	} else {
		$mtikie = "disabled";
	}

	cfg_set($cfg, "wireless.1.addmtikie", $mtikie);

	if ($feature_ieee_mode_a) {
		cfg_set($cfg, "radio.1.dfs.status", get_status($dfs));
	}

	if ($feature_advanced_ethernet == 1) {
	if ($feature_poe_passthrough == 1) {
		cfg_set($cfg, "gpio.status", "enabled");
		cfg_set($cfg, "gpio.1.status", "enabled");
		cfg_set($cfg, "gpio.1.line", $poe_passthrough_gpio);
		cfg_set($cfg, "gpio.1.direction", 1);
			if (strlen($poe_pass)) {
				$poe_pass = "enabled";
			} else {
				$poe_pass = "disabled";
			}
		cfg_set($cfg, "gpio.1.value", $poe_pass);
		}
		if ($feature_advanced_ethernet_phy == 1) {
			if (strlen($eth_autoneg)){
				$eth_autoneg = "enabled";
			} else {
				$eth_autoneg = "disabled";
			}
			if (strlen($eth_duplex)){
				$eth_duplex = "enabled";
			} else {
				$eth_duplex = "disabled";
			}
			if (!strlen($eth_speed)) {
				$eth_speed=$eth_speed_old;
				$eth_duplex=$eth_duplex_old;
			}
			cfg_set($cfg, "netconf.1.speed", $eth_speed);
			cfg_set($cfg, "netconf.1.duplex", $eth_duplex);
			cfg_set($cfg, "netconf.1.autoneg", $eth_autoneg);
		}
	}

	cfg_set($cfg, "netconf.2.allmulti", $mcast_status);
	cfg_set($cfg, "radio.1.mcastrate", $mcast_rate);
	cfg_set($cfg, "wireless.1.l2_isolation", $client_isolation_status);

	cfg_set($cfg, "radio.1.thresh62a", $noise_immunity);
	cfg_set($cfg, "radio.1.thresh62b", $noise_immunity);
	cfg_set($cfg, "radio.1.thresh62g", $noise_immunity);

	cfg_set($cfg, "radio.1.pollingpri", $airmaxpri);

	cfg_save($cfg, $cfg_file);
	cfg_set_modified($cfg_file);
	$message = dict_translate("Configuration saved");
  }

  if (!strlen($rts)) {
	$rts = "off";
  }
  $rts = cfg_get_def($cfg, "radio.1.rts", $rts);
  if (!strlen($frag)) {
	$frag = "off";
  }
  $frag = cfg_get_def($cfg, "radio.1.frag", $frag);
  $autoack = cfg_get_autoack($cfg, $wlan_iface, $autoack);
  $fast_frame = cfg_get_fast_frame($cfg, $wlan_iface, $fast_frame);
  $burst = cfg_get_bursting($cfg, $wlan_iface, $burst);
  $compression = cfg_get_compression($cfg, $wlan_iface, $compression);
  $rate_module = cfg_get_def($cfg, "radio.ratemodule", $def_rate_module);
  $wmm_options = wmm_generate_options($wmm_status, $level);
  if ($feature_ieee_mode_a) {
	$dfs = cfg_get_dfs($cfg, $wlan_iface);
  }
  $poe_pass=cfg_get_def($cfg, "gpio.1.value", $poe_pass);

  if ($feature_advanced_ethernet_phy == 1) {
	  if (strlen($eth_autoneg) == 0) {
		  $eth_autoneg = "enabled";
	  }
	  $eth_autoneg=cfg_get_def($cfg, "netconf.1.autoneg", $eth_autoneg);
	  $eth_speed = cfg_get_def($cfg, "netconf.1.speed", "100");
	  $eth_duplex = cfg_get_def($cfg, "netconf.1.duplex", "enabled");
  }

  $leds = cfg_get_leds($cfg);

  $led1 = $leds[0];
  $led2 = $leds[1];
  $led3 = $leds[2];
  $led4 = $leds[3];

  $shaper_status = cfg_get_def($cfg, "tshaper.status", "disabled");
  if ($feature_legacy != 1) {
	  $aggr_status = cfg_get_def($cfg, "radio.1.ampdu.status", "enabled");
	  $aggr_frames = cfg_get_def($cfg, "radio.1.ampdu.frames", "32");
	  $aggr_bytes = cfg_get_def($cfg, "radio.1.ampdu.bytes", "50000");
  }
  if ($aggr_status == "enabled") { $frag = "off"; }

  $in_rate = cfg_get_def($cfg, "tshaper.in.rate", "512");
  $in_burst = cfg_get_def($cfg, "tshaper.in.burst", "0");
  $out_rate = cfg_get_def($cfg, "tshaper.out.rate", "512");
  $out_burst = cfg_get_def($cfg, "tshaper.out.burst", "0");

  if (strlen($noise_immunity) == 0) {
  	$noise_immunity = 28;
  }
  $noise_immunity = cfg_get_def($cfg, "radio.1.thresh62a", $noise_immunity);
  $clksel = cfg_get_clksel($cfg, $wlan_iface, $clksel);
  $mcast_status = cfg_get_def($cfg, "netconf.2.allmulti", "enabled");
  $client_isolation_status = cfg_get_def($cfg, "wireless.1.l2_isolation", "disabled");
  $polling = cfg_get_def($cfg, "radio.1.polling", $polling);
  $polling_noack = cfg_get_def($cfg, "radio.1.pollingnoack", "0");
  $mtikie = cfg_get_def($cfg, "wireless.1.addmtikie", $mtikie);
  if (strlen($mtikie) == 0) {
  	$mtikie = "enabled";
  }
  $mcast_rate = cfg_get_def($cfg, "radio.1.mcastrate", $mcast_rate);
  
  $timings = get_timings($ieee_mode, $clksel);
  
  $sltconst = $timings[0];
  $maxacktimeout = $timings[1];
  $ackdistance = cfg_get_ackdistance($cfg, $wlan_iface, $sltconst);
  
  $minacktimeout = $sltconst * 2 + 3;
  $acktimeout = $minacktimeout + ($ackdistance / 150);
  /* If maximum distance limit is placed on this board, we calculate new max ack timeout based
   * on speed of light. */
  if (strlen($radio1_distance_limit_km) && $radio1_distance_limit_km != "0") {
	$speed_of_light_meters_per_microsecond = 300.0;
	$uS = ((( 2 * $radio1_distance_limit_km * 1000.0 ) / $speed_of_light_meters_per_microsecond) ) + 0.5;
	$maxacktimeout = $minacktimeout + $uS;
  }

  $airmaxpri = cfg_get_def($cfg, "radio.1.pollingpri", $aimaxprimax);

  include("lib/advanced.tmpl");
>
