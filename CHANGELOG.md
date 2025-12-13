# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
