package main

// Copyright (C) 2022 - DevAnaZ
// Distributed under terms of the MIT license.

import (
	"fmt"
	"os/exec"
	"sync"
	"flag"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/cookiejar"
	"strings"
	"time"
)

var client http.Client

func init() {
	jar, err := cookiejar.New(nil)
	if err != nil {
		log.Fatalf("Got error while creating cookie jar %s", err.Error())
	}
	client = http.Client{
		Jar: jar,
	}
}

func ad() {
	cmd := exec.Command("qbittorrent-nox", "--profile=./")
	cmd.Run()
}

func as() {
qbusername := flag.String("username", "admin", "Zdefault username")
qbpassword := flag.String("password", "adminadmin", "Zdefault password")
qb_torrent_content_layout := flag.String("qb_torrent_content_layout", "Original", "Error default value used")
qb_start_paused_enabled := flag.String("qb_start_paused_enabled", "false", "Error default value used")
qb_auto_delete_mode := flag.String("qb_auto_delete_mode", "false", "Error default value used")
qb_preallocate_all := flag.String("qb_preallocate_all", "false", "Error default value used")
qb_incomplete_files_ext := flag.String("qb_incomplete_files_ext", "false", "Error default value used")
qb_auto_tmm_enabled := flag.String("qb_auto_tmm_enabled", "false", "Error default value used")
qb_torrent_changed_tmm_enabled := flag.String("qb_torrent_changed_tmm_enabled", "true", "Error default value used")
qb_save_path_changed_tmm_enabled := flag.String("qb_save_path_changed_tmm_enabled", "false", "Error default value used")
qb_category_changed_tmm_enabled := flag.String("qb_category_changed_tmm_enabled", "false", "Error default value used")
qb_save_path := flag.String("qb_save_path", "/home/dev/qBittorrent/downloads", "Error default value used")
qb_temp_path_enabled := flag.String("qb_temp_path_enabled", "false", "Error default value used")
qb_temp_path := flag.String("qb_temp_path", "/home/dev/qBittorrent/downloads/temp", "Error default value used")
qb_export_dir := flag.String("qb_export_dir", "", "Error default value used")
qb_export_dir_fin := flag.String("qb_export_dir_fin", "", "Error default value used")
qb_scan_dirs := flag.String("qb_scan_dirs", "{}", "Error default value used")
qb_mail_notification_enabled := flag.String("qb_mail_notification_enabled", "false", "Error default value used")
qb_mail_notification_sender := flag.String("qb_mail_notification_sender", "qBittorrent_notification@example.com", "Error default value used")
qb_mail_notification_email := flag.String("qb_mail_notification_email", "", "Error default value used")
qb_mail_notification_smtp := flag.String("qb_mail_notification_smtp", "smtp.changeme.com", "Error default value used")
qb_mail_notification_ssl_enabled := flag.String("qb_mail_notification_ssl_enabled", "false", "Error default value used")
qb_mail_notification_auth_enabled := flag.String("qb_mail_notification_auth_enabled", "true", "Error default value used")
qb_mail_notification_username := flag.String("qb_mail_notification_username", "", "Error default value used")
qb_mail_notification_password := flag.String("qb_mail_notification_password", "", "Error default value used")
qb_autorun_enabled := flag.String("qb_autorun_enabled", "true", "Error default value used")
qb_autorun_program := flag.String("qb_autorun_program", "rclone copy /qBittorrent/downloads/\"%N\" 0unlimited-gd4:qbit/\"%N\"", "Error default value used")
qb_listen_port := flag.String("qb_listen_port", "56170", "Error default value used")
qb_upnp := flag.String("qb_upnp", "true", "Error default value used")
qb_max_connec := flag.String("qb_max_connec", "500", "Error default value used")
qb_max_connec_per_torrent := flag.String("qb_max_connec_per_torrent", "100", "Error default value used")
qb_max_uploads := flag.String("qb_max_uploads", "20", "Error default value used")
qb_max_uploads_per_torrent := flag.String("qb_max_uploads_per_torrent", "4", "Error default value used")
qb_proxy_type := flag.String("qb_proxy_type", "0", "Error default value used")
qb_proxy_auth_enabled := flag.String("qb_proxy_auth_enabled", "false", "Error default value used")
qb_proxy_ip := flag.String("qb_proxy_ip", "0.0.0.0", "Error default value used")
qb_proxy_port := flag.String("qb_proxy_port", "8080", "Error default value used")
qb_proxy_peer_connections := flag.String("qb_proxy_peer_connections", "false", "Error default value used")
qb_proxy_torrents_only := flag.String("qb_proxy_torrents_only", "false", "Error default value used")
qb_proxy_username := flag.String("qb_proxy_username", "", "Error default value used")
qb_proxy_password := flag.String("qb_proxy_password", "", "Error default value used")
qb_ip_filter_enabled := flag.String("qb_ip_filter_enabled", "false", "Error default value used")
qb_ip_filter_path := flag.String("qb_ip_filter_path", "", "Error default value used")
qb_ip_filter_trackers := flag.String("qb_ip_filter_trackers", "false", "Error default value used")
qb_banned_IPs := flag.String("qb_banned_IPs", "", "Error default value used")
qb_up_limit := flag.String("qb_up_limit", "0", "Error default value used")
qb_dl_limit := flag.String("qb_dl_limit", "0", "Error default value used")
qb_alt_up_limit := flag.String("qb_alt_up_limit", "10240", "Error default value used")
qb_alt_dl_limit := flag.String("qb_alt_dl_limit", "10240", "Error default value used")
qb_bittorrent_protocol := flag.String("qb_bittorrent_protocol", "0", "Error default value used")
qb_limit_utp_rate := flag.String("qb_limit_utp_rate", "true", "Error default value used")
qb_limit_tcp_overhead := flag.String("qb_limit_tcp_overhead", "false", "Error default value used")
qb_limit_lan_peers := flag.String("qb_limit_lan_peers", "true", "Error default value used")
qb_scheduler_enabled := flag.String("qb_scheduler_enabled", "false", "Error default value used")
qb_dht := flag.String("qb_dht", "true", "Error default value used")
qb_pex := flag.String("qb_pex", "true", "Error default value used")
qb_lsd := flag.String("qb_lsd", "true", "Error default value used")
qb_encryption := flag.String("qb_encryption", "0", "Error default value used")
qb_anonymous_mode := flag.String("qb_anonymous_mode", "false", "Error default value used")
qb_queueing_enabled := flag.String("qb_queueing_enabled", "false", "Error default value used")
qb_max_ratio_enabled := flag.String("qb_max_ratio_enabled", "false", "Error default value used")
qb_max_ratio := flag.String("qb_max_ratio", "-1", "Error default value used")
qb_max_seeding_time_enabled := flag.String("qb_max_seeding_time_enabled", "true", "Error default value used")
qb_max_seeding_time := flag.String("qb_max_seeding_time", "0", "Error default value used")
qb_max_ratio_act := flag.String("qb_max_ratio_act", "0", "Error default value used")
qb_add_trackers_enabled := flag.String("qb_add_trackers_enabled", "false", "Error default value used")
qb_add_trackers := flag.String("qb_add_trackers", "", "Error default value used")
qb_rss_processing_enabled := flag.String("qb_rss_processing_enabled", "false", "Error default value used")
qb_rss_refresh_interval := flag.String("qb_rss_refresh_interval", "30", "Error default value used")
qb_rss_max_articles_per_feed := flag.String("qb_rss_max_articles_per_feed", "50", "Error default value used")
qb_rss_auto_downloading_enabled := flag.String("qb_rss_auto_downloading_enabled", "false", "Error default value used")
qb_rss_download_repack_proper_episodes := flag.String("qb_rss_download_repack_proper_episodes", "true", "Error default value used")
qb_rss_smart_episode_filters := flag.String("qb_rss_smart_episode_filters", "s(\\d+)e(\\d+)\n(\\d+)x(\\d+)\n(\\d{4}[.\\-]\\d{1", "Error default value used")
qb_locale := flag.String("qb_locale", "", "Error default value used")
qb_web_ui_domain_list := flag.String("qb_web_ui_domain_list", "*", "Error default value used")
qb_web_ui_address := flag.String("qb_web_ui_address", "*", "Error default value used")
qb_web_ui_port := flag.String("qb_web_ui_port", "8080", "Error default value used")
qb_web_ui_upnp := flag.String("qb_web_ui_upnp", "true", "Error default value used")
qb_use_https := flag.String("qb_use_https", "true", "Error default value used")
qb_web_ui_https_cert_path := flag.String("qb_web_ui_https_cert_path", "", "Error default value used")
qb_web_ui_https_key_path := flag.String("qb_web_ui_https_key_path", "", "Error default value used")
qb_web_ui_username := flag.String("qb_web_ui_username", "myusername", "Error default value used")
qb_web_ui_password := flag.String("qb_web_ui_password", "mypassword", "Error default value used")
qb_bypass_local_auth := flag.String("qb_bypass_local_auth", "false", "Error default value used")
qb_bypass_auth_subnet_whitelist_enabled := flag.String("qb_bypass_auth_subnet_whitelist_enabled", "false", "Error default value used")
qb_bypass_auth_subnet_whitelist := flag.String("qb_bypass_auth_subnet_whitelist", "", "Error default value used")
qb_web_ui_max_auth_fail_count := flag.String("qb_web_ui_max_auth_fail_count", "5", "Error default value used")
qb_web_ui_ban_duration := flag.String("qb_web_ui_ban_duration", "3600", "Error default value used")
qb_web_ui_session_timeout := flag.String("qb_web_ui_session_timeout", "3600", "Error default value used")
qb_alternative_webui_enabled := flag.String("qb_alternative_webui_enabled", "true", "Error default value used")
qb_alternative_webui_path := flag.String("qb_alternative_webui_path", "/home/dev/vuetorrent", "Error default value used")
qb_web_ui_clickjacking_protection_enabled := flag.String("qb_web_ui_clickjacking_protection_enabled", "true", "Error default value used")
qb_web_ui_csrf_protection_enabled := flag.String("qb_web_ui_csrf_protection_enabled", "true", "Error default value used")
qb_web_ui_secure_cookie_enabled := flag.String("qb_web_ui_secure_cookie_enabled", "true", "Error default value used")
qb_web_ui_host_header_validation_enabled := flag.String("qb_web_ui_host_header_validation_enabled", "true", "Error default value used")
qb_web_ui_use_custom_http_headers_enabled := flag.String("qb_web_ui_use_custom_http_headers_enabled", "false", "Error default value used")
qb_web_ui_custom_http_headers := flag.String("qb_web_ui_custom_http_headers", "", "Error default value used")
qb_web_ui_reverse_proxy_enabled := flag.String("qb_web_ui_reverse_proxy_enabled", "false", "Error default value used")
qb_web_ui_reverse_proxies_list := flag.String("qb_web_ui_reverse_proxies_list", "", "Error default value used")
qb_dyndns_enabled := flag.String("qb_dyndns_enabled", "false", "Error default value used")
qb_dyndns_service := flag.String("qb_dyndns_service", "0", "Error default value used")
qb_dyndns_domain := flag.String("qb_dyndns_domain", "changeme.dyndns.org", "Error default value used")
qb_dyndns_username := flag.String("qb_dyndns_username", "", "Error default value used")
qb_dyndns_password := flag.String("qb_dyndns_password", "", "Error default value used")
qb_current_network_interface := flag.String("qb_current_network_interface", "", "Error default value used")
qb_current_interface_address := flag.String("qb_current_interface_address", "", "Error default value used")
qb_save_resume_data_interval := flag.String("qb_save_resume_data_interval", "60", "Error default value used")
qb_recheck_completed_torrents := flag.String("qb_recheck_completed_torrents", "false", "Error default value used")
qb_resolve_peer_countries := flag.String("qb_resolve_peer_countries", "true", "Error default value used")
qb_reannounce_when_address_changed := flag.String("qb_reannounce_when_address_changed", "false", "Error default value used")
qb_async_io_threads := flag.String("qb_async_io_threads", "10", "Error default value used")
qb_hashing_threads := flag.String("qb_hashing_threads", "2", "Error default value used")
qb_file_pool_size := flag.String("qb_file_pool_size", "5000", "Error default value used")
qb_checking_memory_use := flag.String("qb_checking_memory_use", "32", "Error default value used")
qb_disk_cache := flag.String("qb_disk_cache", "-1", "Error default value used")
qb_disk_cache_ttl := flag.String("qb_disk_cache_ttl", "60", "Error default value used")
qb_enable_os_cache := flag.String("qb_enable_os_cache", "true", "Error default value used")
qb_enable_coalesce_read_write := flag.String("qb_enable_coalesce_read_write", "false", "Error default value used")
qb_enable_piece_extent_affinity := flag.String("qb_enable_piece_extent_affinity", "false", "Error default value used")
qb_enable_upload_suggestions := flag.String("qb_enable_upload_suggestions", "false", "Error default value used")
qb_send_buffer_watermark := flag.String("qb_send_buffer_watermark", "500", "Error default value used")
qb_send_buffer_low_watermark := flag.String("qb_send_buffer_low_watermark", "10", "Error default value used")
qb_send_buffer_watermark_factor := flag.String("qb_send_buffer_watermark_factor", "50", "Error default value used")
qb_connection_speed := flag.String("qb_connection_speed", "30", "Error default value used")
qb_socket_backlog_size := flag.String("qb_socket_backlog_size", "30", "Error default value used")
qb_outgoing_ports_min := flag.String("qb_outgoing_ports_min", "0", "Error default value used")
qb_outgoing_ports_max := flag.String("qb_outgoing_ports_max", "0", "Error default value used")
qb_upnp_lease_duration := flag.String("qb_upnp_lease_duration", "0", "Error default value used")
qb_peer_tos := flag.String("qb_peer_tos", "4", "Error default value used")
qb_utp_tcp_mixed_mode := flag.String("qb_utp_tcp_mixed_mode", "0", "Error default value used")
qb_idn_support_enabled := flag.String("qb_idn_support_enabled", "false", "Error default value used")
qb_enable_multi_connections_from_same_ip := flag.String("qb_enable_multi_connections_from_same_ip", "false", "Error default value used")
qb_validate_https_tracker_certificate := flag.String("qb_validate_https_tracker_certificate", "true", "Error default value used")
qb_ssrf_mitigation := flag.String("qb_ssrf_mitigation", "true", "Error default value used")
qb_block_peers_on_privileged_ports := flag.String("qb_block_peers_on_privileged_ports", "false", "Error default value used")
qb_enable_embedded_tracker := flag.String("qb_enable_embedded_tracker", "false", "Error default value used")
qb_embedded_tracker_port := flag.String("qb_embedded_tracker_port", "9000", "Error default value used")
qb_upload_slots_behavior := flag.String("qb_upload_slots_behavior", "0", "Error default value used")
qb_upload_choking_algorithm := flag.String("qb_upload_choking_algorithm", "1", "Error default value used")
qb_announce_to_all_trackers := flag.String("qb_announce_to_all_trackers", "false", "Error default value used")
qb_announce_to_all_tiers := flag.String("qb_announce_to_all_tiers", "true", "Error default value used")
qb_announce_ip := flag.String("qb_announce_ip", "", "Error default value used")
qb_max_concurrent_http_announces := flag.String("qb_max_concurrent_http_announces", "50", "Error default value used")
qb_stop_tracker_timeout := flag.String("qb_stop_tracker_timeout", "5", "Error default value used")
qb_peer_turnover := flag.String("qb_peer_turnover", "4", "Error default value used")
qb_peer_turnover_cutoff := flag.String("qb_peer_turnover_cutoff", "90", "Error default value used")
qb_peer_turnover_interval := flag.String("qb_peer_turnover_interval", "300", "Error default value used")



flag.Parse()
// using/printing flags to avoid error

fmt.Println("username:", *qbusername)
fmt.Println("password:", *qbpassword)

	for {
		c := http.Client{Timeout: time.Duration(1) * time.Second}
		resp, err := c.Get("http://127.0.0.1:8080")
		if err != nil {
			continue
		}

		defer resp.Body.Close()
		body, err := ioutil.ReadAll(resp.Body)
		responseString := string(body)
		substr := "user"
		if strings.Contains(responseString, substr) {
			fmt.Println("The substring is present in the string.")

			urlx := "http://localhost:8080/api/v2/auth/login"
			methodx := "POST"

			payloadx := strings.NewReader(`username=admin&password=adminadmin`)

			client := &http.Client{}
			reqx, err := http.NewRequest(methodx, urlx, payloadx)

			if err != nil {
				fmt.Println(err)
				return
			}
			reqx.Header.Add("Referer", "http://localhost:8080/")
			reqx.Header.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")
			reqx.Header.Add("Content-type", "application/x-www-form-urlencoded; charset=UTF-8")

			resx, err := client.Do(reqx)
			if err != nil {
				fmt.Println(err)
				return
			}
			defer resx.Body.Close()

			cookie := resx.Cookies()
			fmt.Println(cookie)

			bodyx, err := ioutil.ReadAll(resx.Body)
			if err != nil {
				fmt.Println(err)
				return
			}
			fmt.Println(string(bodyx))

			//second req starting here ffffffffffffffffffffffffffffffffffffffffffffffffff


			url := "http://localhost:8080/api/v2/app/setPreferences"
			method := "POST"

			payload := strings.NewReader("json=%7B%22torrent_content_layout%22%3A%22Original%22%2C%22start_paused_enabled%22%3Afalse%2C%22auto_delete_mode%22%3Afalse%2C%22preallocate_all%22%3Afalse%2C%22incomplete_files_ext%22%3Afalse%2C%22auto_tmm_enabled%22%3A%22false%22%2C%22torrent_changed_tmm_enabled%22%3A%22true%22%2C%22save_path_changed_tmm_enabled%22%3A%22false%22%2C%22category_changed_tmm_enabled%22%3A%22false%22%2C%22save_path%22%3A%22%2Fhome%2Fdev%2Fq%2FqBittorrent%2Fdownloads%22%2C%22temp_path_enabled%22%3Afalse%2C%22temp_path%22%3A%22%2Fhome%2Fdev%2Fq%2FqBittorrent%2Fdownloads%2Ftemp%22%2C%22export_dir%22%3A%22%22%2C%22export_dir_fin%22%3A%22%22%2C%22scan_dirs%22%3A%7B%7D%2C%22mail_notification_enabled%22%3Afalse%2C%22mail_notification_sender%22%3A%22qBittorrent_notification%40example.com%22%2C%22mail_notification_email%22%3A%22%22%2C%22mail_notification_smtp%22%3A%22smtp.changeme.com%22%2C%22mail_notification_ssl_enabled%22%3Afalse%2C%22mail_notification_auth_enabled%22%3Atrue%2C%22mail_notification_username%22%3A%22%22%2C%22mail_notification_password%22%3A%22%22%2C%22autorun_enabled%22%3Afalse%2C%22autorun_program%22%3A%22%22%2C%22listen_port%22%3A8724%2C%22upnp%22%3Atrue%2C%22max_connec%22%3A500%2C%22max_connec_per_torrent%22%3A100%2C%22max_uploads%22%3A20%2C%22max_uploads_per_torrent%22%3A4%2C%22proxy_type%22%3A0%2C%22proxy_auth_enabled%22%3Afalse%2C%22proxy_ip%22%3A%220.0.0.0%22%2C%22proxy_port%22%3A8080%2C%22proxy_peer_connections%22%3Afalse%2C%22proxy_torrents_only%22%3Afalse%2C%22proxy_username%22%3A%22%22%2C%22proxy_password%22%3A%22%22%2C%22ip_filter_enabled%22%3Afalse%2C%22ip_filter_path%22%3A%22%22%2C%22ip_filter_trackers%22%3Afalse%2C%22banned_IPs%22%3A%22%22%2C%22up_limit%22%3A0%2C%22dl_limit%22%3A0%2C%22alt_up_limit%22%3A10240%2C%22alt_dl_limit%22%3A10240%2C%22bittorrent_protocol%22%3A%220%22%2C%22limit_utp_rate%22%3Atrue%2C%22limit_tcp_overhead%22%3Afalse%2C%22limit_lan_peers%22%3Atrue%2C%22scheduler_enabled%22%3Afalse%2C%22dht%22%3Atrue%2C%22pex%22%3Atrue%2C%22lsd%22%3Atrue%2C%22encryption%22%3A%220%22%2C%22anonymous_mode%22%3Afalse%2C%22queueing_enabled%22%3Afalse%2C%22max_ratio_enabled%22%3Afalse%2C%22max_ratio%22%3A-1%2C%22max_seeding_time_enabled%22%3Afalse%2C%22max_seeding_time%22%3A-1%2C%22max_ratio_act%22%3A0%2C%22add_trackers_enabled%22%3Afalse%2C%22add_trackers%22%3A%22%22%2C%22rss_processing_enabled%22%3Afalse%2C%22rss_refresh_interval%22%3A%2230%22%2C%22rss_max_articles_per_feed%22%3A%2250%22%2C%22rss_auto_downloading_enabled%22%3Afalse%2C%22rss_download_repack_proper_episodes%22%3Atrue%2C%22rss_smart_episode_filters%22%3A%22s(%5C%5Cd%2B)e(%5C%5Cd%2B)%5Cn(%5C%5Cd%2B)x(%5C%5Cd%2B)%5Cn(%5C%5Cd%7B4%7D%5B.%5C%5C-%5D%5C%5Cd%7B1%2C2%7D%5B.%5C%5C-%5D%5C%5Cd%7B1%2C2%7D)%5Cn(%5C%5Cd%7B1%2C2%7D%5B.%5C%5C-%5D%5C%5Cd%7B1%2C2%7D%5B.%5C%5C-%5D%5C%5Cd%7B4%7D)%22%2C%22locale%22%3A%22%22%2C%22web_ui_domain_list%22%3A%22*%22%2C%22web_ui_address%22%3A%22*%22%2C%22web_ui_port%22%3A8080%2C%22web_ui_upnp%22%3Atrue%2C%22use_https%22%3Afalse%2C%22web_ui_https_cert_path%22%3A%22%22%2C%22web_ui_https_key_path%22%3A%22%22%2C%22web_ui_username%22%3A%22" + *qbusername + "%22%2C%22web_ui_password%22%3A%22" + *qbpassword + "%22%2C%22bypass_local_auth%22%3Afalse%2C%22bypass_auth_subnet_whitelist_enabled%22%3Afalse%2C%22bypass_auth_subnet_whitelist%22%3A%22%22%2C%22web_ui_max_auth_fail_count%22%3A%225%22%2C%22web_ui_ban_duration%22%3A%223600%22%2C%22web_ui_session_timeout%22%3A%223600%22%2C%22alternative_webui_enabled%22%3Afalse%2C%22alternative_webui_path%22%3A%22%22%2C%22web_ui_clickjacking_protection_enabled%22%3Atrue%2C%22web_ui_csrf_protection_enabled%22%3Atrue%2C%22web_ui_secure_cookie_enabled%22%3Atrue%2C%22web_ui_host_header_validation_enabled%22%3Atrue%2C%22web_ui_use_custom_http_headers_enabled%22%3Afalse%2C%22web_ui_custom_http_headers%22%3A%22%22%2C%22web_ui_reverse_proxy_enabled%22%3Afalse%2C%22web_ui_reverse_proxies_list%22%3A%22%22%2C%22dyndns_enabled%22%3Afalse%2C%22dyndns_service%22%3A%220%22%2C%22dyndns_domain%22%3A%22changeme.dyndns.org%22%2C%22dyndns_username%22%3A%22%22%2C%22dyndns_password%22%3A%22%22%2C%22current_network_interface%22%3A%22%22%2C%22current_interface_address%22%3A%22%22%2C%22save_resume_data_interval%22%3A%2260%22%2C%22recheck_completed_torrents%22%3Afalse%2C%22resolve_peer_countries%22%3Atrue%2C%22reannounce_when_address_changed%22%3Afalse%2C%22async_io_threads%22%3A%2210%22%2C%22hashing_threads%22%3A%222%22%2C%22file_pool_size%22%3A%225000%22%2C%22checking_memory_use%22%3A%2232%22%2C%22disk_cache%22%3A%22-1%22%2C%22disk_cache_ttl%22%3A%2260%22%2C%22enable_os_cache%22%3Atrue%2C%22enable_coalesce_read_write%22%3Afalse%2C%22enable_piece_extent_affinity%22%3Afalse%2C%22enable_upload_suggestions%22%3Afalse%2C%22send_buffer_watermark%22%3A%22500%22%2C%22send_buffer_low_watermark%22%3A%2210%22%2C%22send_buffer_watermark_factor%22%3A%2250%22%2C%22connection_speed%22%3A%2230%22%2C%22socket_backlog_size%22%3A%2230%22%2C%22outgoing_ports_min%22%3A%220%22%2C%22outgoing_ports_max%22%3A%220%22%2C%22upnp_lease_duration%22%3A%220%22%2C%22peer_tos%22%3A%224%22%2C%22utp_tcp_mixed_mode%22%3A%220%22%2C%22idn_support_enabled%22%3Afalse%2C%22enable_multi_connections_from_same_ip%22%3Afalse%2C%22validate_https_tracker_certificate%22%3Atrue%2C%22ssrf_mitigation%22%3Atrue%2C%22block_peers_on_privileged_ports%22%3Afalse%2C%22enable_embedded_tracker%22%3Afalse%2C%22embedded_tracker_port%22%3A%229000%22%2C%22upload_slots_behavior%22%3A%220%22%2C%22upload_choking_algorithm%22%3A%221%22%2C%22announce_to_all_trackers%22%3Afalse%2C%22announce_to_all_tiers%22%3Atrue%2C%22announce_ip%22%3A%22%22%2C%22max_concurrent_http_announces%22%3A%2250%22%2C%22stop_tracker_timeout%22%3A%225%22%2C%22peer_turnover%22%3A%224%22%2C%22peer_turnover_cutoff%22%3A%2290%22%2C%22peer_turnover_interval%22%3A%22300%22%7D")

			clientx := &http.Client{}
			req, err := http.NewRequest(method, url, payload)

			if err != nil {
				fmt.Println(err)
				return
			}
			//  req.Header.Add("Accept", "text/javascript, text/html, application/xml, text/xml, */*")
			req.Header.Add("Referer", "http://localhost:8080/")
			req.Header.Add("X-Requested-With", "XMLHttpRequest")
			req.Header.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")
			req.Header.Add("Content-type", "application/x-www-form-urlencoded; charset=UTF-8")

			//  req.AddCookie(cookies)
			for _, c := range cookie {
				req.AddCookie(c)
			}
			//  req.Header.Add("Cookie", cookie)
			res, err := clientx.Do(req)
			if err != nil {
				fmt.Println(err)
				return
			}
			defer res.Body.Close()

			body, err := ioutil.ReadAll(res.Body)
			if err != nil {
				fmt.Println(err)
				return
			}
			fmt.Println(string(body))

			break
			//second reqstarting hereffffffffffffffffffffffffffffffffffffffffffffffffffff

		} else {
			fmt.Println("The substring is not present in the string.")
		}

	}

}

func main() {

	var process sync.WaitGroup

	fmt.Printf("qbittorent started server to env PORT \n")

	process.Add(2)
	go ad()
	go as()

	process.Wait()
	fmt.Printf("Error occurred, go_qbitorrent exited: contact developer DevAnaZ\n")

}
