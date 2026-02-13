# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.9] - 2026-02-13

- Correction du mapping des modes audio (ajout du mode 'Multi Ch In' code 0003)\n- Ajout de nombreux modes d'écoute Pioneer manquants pour éviter l'affichage 'Mode XXXX'\n- Amélioration de la détection des modes audio dans le dashboard

## [1.2.8] - 2026-02-13

- Amélioration de la robustesse du mapping des sources (insensible à la casse)\n- Correction de la détection de l'état des boutons sur le dashboard\n- Priorité aux noms définis dans 'DEFAULT_SOURCES'

## [1.2.7] - 2026-02-13

- Optimisation pour le dashboard Mushroom du projet\n- Ajout de l'attribut 'last_response' pour le débug en direct\n- Alignement des noms de sources sur le dashboard: 'TV' -> 'TV/Sat', 'iPod' -> 'iPod/USB', 'Blu-ray' -> 'BD'\n- Correction du domaine pour les appels de service: utiliser 'pioneer_avr_lx83.send_raw_command'

## [1.2.6] - 2026-02-13

- Rétablissement de la gestion dynamique des noms (has_entity_name)\n- Maintien du mode 'receiver' pour le contrôle complet des entrées\n- Nom par défaut 'Pioneer'

## [1.2.5] - 2026-02-13

- Retour à la configuration de nommage stable pour Alexa\n- Renommage de 'Télévision' en 'TV'\n- Rétablissement du nom par défaut 'Pioneer AVR'\n- Maintien du mode 'receiver' pour le contrôle des entrées

## [1.2.4] - 2026-02-13

- Rétablissement de la device_class 'receiver' pour corriger la détection Alexa\n- Restauration de la propriété 'name' pour une meilleure compatibilité

## [1.2.2] - 2026-02-13

- Suppression du nom redondant 'Pioneer AVR Pioneer AVR' sur Alexa\n- Optimisation de la gestion du nom de l'entité via has_entity_name

## [1.2.1] - 2026-02-13

- Correction du conflit de nom avec la TV physique\n- Passage de la device_class en 'speaker' pour éviter la confusion d'Alexa\n- Renommage de l'entrée 'TV' en 'Télévision' dans la liste principale

## [1.2.0] - 2026-02-12

- Amélioration de la compatibilité Alexa (InputController)\n- Support natif des sources reconnues par Alexa (TV, HDMI 1, etc.)\n- Ajout de la classe d'appareil 'receiver' pour une meilleure identification\n- Enrichissement des alias de sources en français\n- Amélioration du mapping des modes d'écoute (Mode 0201 -> Action)\n- Suppression du code personnalisé redondant au profit des standards Home Assistant

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
