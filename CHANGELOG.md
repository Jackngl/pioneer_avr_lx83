# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2025-12-14

### Fixed
- Fixed "Update took longer than scheduled update interval" warning by optimizing update timeouts
- Reduced update query timeout from 10s to 2s to prevent exceeding scan interval
- Added global timeout wrapper to async_update() to ensure it completes within scan interval
- Optimized dynamic sources discovery to not block updates indefinitely

## [1.1.0] - 2025-12-14

- Added sound-mode support (media_player.select_sound_mode) with listening-mode parsing
- Registered `pioneer_avr_lx83.send_raw_command` in docs, plus telnet quick-reference tables
- Expanded Lovelace examples (audio/video grids, mode buttons) and added bilingual instructions
- Added Pioneer-styled logo/icon assets for HACS + noted third-party license for listening modes

## [1.0.1] - 2025-12-13

- Improved telnet stability and added versioning workflow
- Added media transport commands (play/pause)
- Discovered source labels dynamically via `?RGBxx` when available
- Fixed source selection by sending proper `xxFN` payloads and allowing case-insensitive source names

## [1.0.0] - 2025-01-XX

### Added
- Initial release
- Power on/off control
- Volume control (set, up, down)
- Mute/unmute functionality
- Source selection
- Real-time status updates via polling
- Config flow UI for easy setup
- Support for multiple input sources (CD, Tuner, Phono, DVD, TV/Sat, DVR/BDR, Video, iPod/USB, NET)
- English and French translations
- HACS compatibility
