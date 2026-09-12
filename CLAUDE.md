# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

This is a personal grab-bag of unrelated, standalone scripts ("experimental scripts to play with some things I like to play with", per README.md) — not a single application. There is no shared build system, package manifest, dependency file, linter, or test suite anywhere in the repo, and scripts do not import from each other. Each file (or the `enigma2/` and `munin/` directories) is its own independent tool with its own language, runtime, and purpose. Treat every file as a separate unit of work: changes to one script have no effect on any other.

Because there's no build/lint/test tooling, verify changes by reading the script and, where safe, running it directly with the appropriate interpreter (`python3 <script>.py`, `perl <script>.pl`, `bash <script>.sh`, `php <script>`). Several scripts assume they run on specific hardware/network context (a Raspberry Pi with GPIO wired up, an Enigma2 set-top box, a specific home LAN, a Windows machine with a running game) and cannot be meaningfully executed elsewhere.

## Script inventory

**Home automation / hardware**
- `control_table.py` — controls an IKEA RODULF standing desk via Raspberry Pi GPIO (`RPi.GPIO`); CLI flags for up/down/seconds/absolute position (0–15).
- `apitest.py` — Flask + flask-restful API exposing the desk's current position (`table_pos` file) as a REST resource; used alongside `control_table.py`.

**Enigma2 set-top box tooling** (`enigma2/`)
- `provision.py`, `openUPNP.py` — provisioning/UPnP helpers for Enigma2 boxes.
- `enigmaInfo.py` (also duplicated at repo root) — fetches `/web/deviceinfo` from a local Enigma2 box via `wget` and prints firmware/image version.
- `make-motd`, `update-motd`, `figlet.php`, `clock.php` — MOTD generation for the box's SSH login banner.
- `check-clock-sync`, `ntpd`, `ntp.conf`, `cs.conf` — NTP/clock sync config and checks.
- `update-iptv-list`, `update-sat-list*`, `updateIPTVlist.sh` — refresh IPTV/satellite channel lists.
- `openRemoteSSH.sh`, `remote-ssh`, `sshpass` — remote SSH access helpers (bundles the `sshpass` binary).
- `boxes`, `ca.crt` — box inventory / TLS CA cert used by the above.

**Elite Dangerous game tooling**
- `parse_elite_bindings.py` — parses an Elite Dangerous `.binds` XML file and loads controls/triggers/devices/keys/modifiers into a local SQLite DB; round-tripping back to XML is a documented TODO in the file.
- `elite_alert.py` — tails the newest Elite Dangerous log file (Windows path under `Saved Games`) and uses `telegram_send` to alert / can kill the game process.
- `HCS Gremlin.4.0.binds`, `HCS Gremlin.4.1.binds`, `JoystickBindings` — Elite Dangerous binding data files consumed by the scripts above, not code.

**Streaming / IPTV server ops**
- `check_dead_streams.sh`, `start_dead_streams.sh` — query a MySQL `fos` database for stream processes, verify the PID is alive via `/proc`, and update stream status / restart via a local HTTP API. Contain hardcoded DB credentials — treat as sensitive, don't reuse verbatim.
- `tvh-srvid-generator.py` — talks to a TVHeadend server's REST API (Basic Auth) to generate service IDs, matching against a `providers` map.
- `fetchlist.sh` — downloads/updates a vhannibal channel list bundle.
- `check_dead_streams.sh`'s companion `curl` call writes an `.m3u` playlist for nginx.

**DNS / networking**
- `updateDNS.py` — updates an A record on name.com via their v4 API for dynamic DNS.
- `generate_hosts_openvpn.sh` — derives `/etc/hosts`-style entries from OpenVPN `ccd` client config directory (IP → `<name>.vpn`).
- `pibackup.sh` — mounts an NFS share and is intended to back up a Raspberry Pi to NAS (script is templated — `NAS_IP`/`NAS_SHARE` are blank).

**Misc / security / small utilities**
- `check_availability.sh` — scrapes product pages for "out of stock" text and diffs against last run to notify when items come back in stock.
- `check_change.pl` — parses `/tmp/currencies_log_*` files and reports percentage changes outside a threshold window.
- `gen.pl` — password/word-list generator (part of the "eland" toolset).
- `macbuild.pl`, `macbuild2.pl`, `macbuild.py` — brute-force generate MAC address ranges / permutations (Python variant uses Python 2 `print` statement syntax and will not run under Python 3 as-is).
- `parsejson.pl` — reads `lista2.json` and remaps entries to a target host.
- `get_page_http` — PHP script that scrapes and normalizes a page (date/string cleanup helpers).
- `color-gradients` — static reference data mapping temperatures to hex colors; not executable code.
- `get-pip.py` — vendored, upstream `pip` bootstrap installer (not authored here; don't modify).
- `munin/plugins/multics.sh`, `multics_avg.sh` — Munin monitoring plugins.

## Working conventions

- Don't assume any two files share configuration, credentials, or state — each hardcodes its own (IPs, ports, DB credentials, API tokens). When editing one script's config, don't propagate it elsewhere.
- Several Python scripts are Python 2 (e.g. `macbuild.py`, and parts of `control_table.py`/`enigmaInfo.py` use Python 2-only syntax); check shebang and syntax before assuming Python 3.
- Hardcoded credentials/tokens present in several scripts (e.g. `check_dead_streams.sh`, `start_dead_streams.sh`, `tvh-srvid-generator.py`, `updateDNS.py`) are placeholders/personal-use values already in git history — don't add new real secrets to any script.
