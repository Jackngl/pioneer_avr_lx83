# Intégration Pioneer AVR LX83 pour Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/Jackngl/pioneer_avr_lx83.svg)](https://GitHub.com/Jackngl/pioneer_avr_lx83/releases/)
[![License](https://img.shields.io/github/license/Jackngl/pioneer_avr_lx83.svg)](LICENSE)

Intégration personnalisée Home Assistant pour les récepteurs Pioneer AVR LX83 utilisant le protocole Telnet.

## Fonctionnalités

- ✅ Contrôle d'alimentation (allumer/éteindre)
- ✅ Contrôle du volume (réglage, augmenter, diminuer)
- ✅ Activer/désactiver le mode muet
- ✅ Sélection de la source d'entrée
- ✅ Mises à jour d'état en temps réel
- ✅ Commandes de transport de base (lecture/pause)
- ✅ Sélection des modes audio + service `send_raw_command`
- ✅ Configuration via l'interface utilisateur
- ✅ Compatible HACS
- ✅ Utilise DataUpdateCoordinator (conforme HA 2025.12+)
- ✅ Découverte automatique des sources (`?RGBxx`)

## Installation

### HACS (Recommandé)

1. Ouvrez HACS dans Home Assistant
2. Cliquez sur "Intégrations"
3. Cliquez sur les trois points en haut à droite
4. Sélectionnez "Dépôts personnalisés"
5. Ajoutez `https://github.com/Jackngl/pioneer_avr_lx83` comme dépôt
6. Sélectionnez "Intégration" comme catégorie
7. Cliquez sur "Ajouter"
8. Recherchez "Pioneer AVR LX83" et installez

### Installation manuelle

1. Copiez le répertoire `custom_components/pioneer_avr_lx83` dans le répertoire `custom_components` de votre Home Assistant
2. Redémarrez Home Assistant

## Configuration

1. Allez dans Paramètres > Appareils et services
2. Cliquez sur "+ Ajouter une intégration"
3. Recherchez "Pioneer AVR LX83"
4. Entrez l'adresse IP de votre appareil, le port (par défaut: 23) et un nom
5. Cliquez sur "Envoyer"

Une fois configuré, l'intégration crée **une seule entité** sous le domaine `media_player`. Cette entité peut être utilisée dans vos automatisations, scripts et tableaux de bord.

### Comment trouver le nom exact de votre entité

**Important** : Vous devez connaître le nom exact de votre entité pour l'utiliser dans les automatisations. Voici comment le trouver :

1. **Méthode 1 - Via l'interface** :
   - Allez dans **Paramètres > Appareils et services**
   - Cliquez sur votre intégration **Pioneer AVR LX83**
   - Cliquez sur l'entité listée (vous verrez une entité `media_player`)
   - Le nom complet de l'entité est affiché en haut (ex: `media_player.pioneer_avr` ou `media_player.salon_ampli`)

2. **Méthode 2 - Via le développeur** :
   - Allez dans **Paramètres > Appareils et services**
   - Cliquez sur **ENTITÉS** en haut
   - Recherchez "Pioneer" ou le nom que vous avez donné
   - L'ID de l'entité est affiché (ex: `media_player.pioneer_avr`)

3. **Méthode 3 - Via les logs** :
   - Allez dans **Paramètres > Système > Logs**
   - Recherchez les messages de l'intégration lors du démarrage

**Note** : Le nom de l'entité est généré automatiquement par Home Assistant à partir du nom que vous avez donné lors de la configuration. Les espaces sont remplacés par des underscores et tout est en minuscules. Par exemple, si vous avez nommé votre appareil "Salon Ampli", l'entité sera probablement `media_player.salon_ampli`.

## Sources supportées

- Analogiques : Phono, CD, Tuner, CDR/Tape, Video 1/2, Multi CH IN
- Numériques : DVD, TV/SAT, DVR/BDR, iPod/USB, XM Radio, NET/HMG
- Entrées HDMI 1 → 5 (ainsi que HDMI Cycle)
- BD / Blu-ray
- Port adaptateur / Bluetooth

> Astuce : lorsque l'ampli est allumé, l'intégration interroge automatiquement `?RGBxx` et ajoute les libellés configurés sur l'appareil en plus de la liste ci-dessus.

## Intégration avec Alexa

L'entité Pioneer AVR est exposée à Amazon Alexa **via le support natif media_player de Home Assistant**. Utilisez soit le [skill Alexa Smart Home](https://www.home-assistant.io/integrations/alexa.smart_home/) (avec votre propre Lambda/endpoint), soit [Home Assistant Cloud](https://www.nabucasa.com/) (Nabu Casa) ; aucun « plugin Alexa Pioneer » séparé n'est nécessaire.

- **Exposer l'appareil** : Vérifiez que l'entité est bien incluse pour Alexa. Si vous utilisez un filtre dans la configuration `alexa: smart_home:`, incluez soit le domaine `media_player` (ex. `filter: include_domains: - media_player`), soit votre entité explicitement (ex. `include_entities: - media_player.pioneer_avr` — utilisez votre vrai entity ID).
- **Personnalisation (optionnel)** : Dans `configuration.yaml`, sous `alexa: smart_home: entity_config:`, vous pouvez définir un **nom** convivial et **display_categories** (ex. `SPEAKER`) pour que l'ampli s'affiche avec le bon libellé et la bonne icône dans l'app Alexa.
- Après avoir modifié la configuration Alexa ou lancé **Découvrir les appareils** dans l'app Alexa, l'amplificateur apparaît comme **haut-parleur** et peut être contrôlé à la voix (alimentation, volume, muet, source, mode d'écoute, lecture/pause) selon les interfaces supportées par Home Assistant pour les media players.

### Renommer l'ampli pour Alexa

Le nom affiché dans l'app Alexa est le « friendly name » envoyé lors de la découverte. Sans configuration, Alexa utilise le nom de l'appareil dans Home Assistant (celui donné lors de la configuration de l'intégration Pioneer). Pour afficher un autre nom (ex. « Ampli Salon »), définissez-le dans `entity_config` pour votre entité media_player :

```yaml
alexa:
  smart_home:
    entity_config:
      media_player.pioneer_avr:   # utilisez votre vrai entity_id
        name: Ampli
        display_categories: SPEAKER  # ou TV
```

Après modification, redémarrez Home Assistant (ou rechargez la config Alexa si possible), puis dans l'app Alexa supprimez l'appareil et lancez **Découvrir les appareils** pour que le nouveau nom et la catégorie soient pris en compte.

### Commandes vocales supportées

Voici les phrases types pour contrôler votre amplificateur avec Alexa (en utilisant le nom "Ampli" par exemple) :

**Alimentation :**
- "Alexa, allume l'Ampli"
- "Alexa, éteins l'Ampli"

**Volume :**
- "Alexa, mets le volume de l'Ampli à 20"
- "Alexa, augmente le volume de l'Ampli"
- "Alexa, baisse le volume de l'Ampli"
- "Alexa, coupe le son de l'Ampli" (Mute)
- "Alexa, remets le son de l'Ampli" (Unmute)

**Sources (Entrées) :**
- "Alexa, mets l'Ampli sur TV" (ou "Télé", "Télévision")
- "Alexa, mets l'Ampli sur DVD"
- "Alexa, mets l'Ampli sur Bluetooth"
- "Alexa, mets l'Ampli sur Tuner" (ou "Radio")
- "Alexa, change l'entrée de l'Ampli sur Blu-ray"

**Modes d'écoute :**
- "Alexa, règle le mode de l'Ampli sur Stéréo"
- "Alexa, règle le mode de l'Ampli sur Cinéma" (THX Cinema)

> **Note :** Pour l'entrée TV/Sat, l'intégration reconnait désormais plusieurs variations : "TV", "Télé", "Télévision", "Sat TV" ou "TV Sat".

## Automatisations

L'intégration Pioneer AVR LX83 peut être utilisée dans des automatisations Home Assistant pour automatiser le contrôle de votre amplificateur.

**⚠️ Important** : Dans tous les exemples ci-dessous, remplacez `media_player.pioneer_avr` par le nom exact de votre entité (voir section "Comment trouver le nom exact de votre entité" ci-dessus).

Voici quelques exemples pratiques :

### Exemple 1 : Allumer l'ampli lors de la lecture de musique

Cette automatisation allume l'ampli et sélectionne la source appropriée quand vous commencez à lire de la musique :

```yaml
alias: "Allumer l'ampli pour la musique"
description: "Allume l'ampli quand la musique commence"
trigger:
  - platform: state
    entity_id: media_player.spotify  # Remplacez par votre lecteur de musique
    to: 'playing'
condition: []
action:
  - service: media_player.turn_on
    target:
      entity_id: media_player.pioneer_avr  # ⚠️ REMPLACEZ par le nom exact de votre entité
  - delay:
      seconds: 2  # Attendre 2 secondes que l'ampli s'allume
  - service: media_player.select_source
    target:
      entity_id: media_player.pioneer_avr
    data:
      source: "NET"  # Ou "iPod/USB" selon votre source
  - service: media_player.set_volume_level
    target:
      entity_id: media_player.pioneer_avr
    data:
      volume_level: 0.3  # Volume à 30%
mode: single
```

### Exemple 2 : Éteindre l'ampli automatiquement

Éteindre l'ampli après une période d'inactivité ou à une heure précise :

```yaml
alias: "Éteindre l'ampli le soir"
description: "Éteint l'ampli à 23h00 s'il est allumé"
trigger:
  - platform: time
    at: "23:00:00"  # 23h00
condition:
  - condition: state
    entity_id: media_player.pioneer_avr  # ⚠️ REMPLACEZ par le nom exact de votre entité
    state: 'on'
action:
  - service: media_player.turn_off
    target:
      entity_id: media_player.pioneer_avr
mode: single
```

### Exemple 3 : Ajuster le volume selon l'heure

Réduire automatiquement le volume pendant les heures de repos :

```yaml
alias: "Volume réduit la nuit"
description: "Réduit le volume à 22h00"
trigger:
  - platform: time
    at: "22:00:00"  # 22h00
condition:
  - condition: state
    entity_id: media_player.pioneer_avr  # ⚠️ REMPLACEZ par le nom exact de votre entité
    state: 'on'
action:
  - service: media_player.set_volume_level
    target:
      entity_id: media_player.pioneer_avr
    data:
      volume_level: 0.15  # Volume réduit à 15%
mode: single
```

### Exemple 4 : Changer de source selon l'activité TV

Changer automatiquement la source de l'ampli quand la TV s'allume :

```yaml
alias: "Source TV quand la TV s'allume"
description: "Change la source vers TV/Sat quand la TV s'allume"
trigger:
  - platform: state
    entity_id: media_player.tv  # Remplacez par votre TV
    to: 'on'
condition: []
action:
  - service: media_player.turn_on
    target:
      entity_id: media_player.pioneer_avr  # ⚠️ REMPLACEZ par le nom exact de votre entité
  - delay:
      seconds: 2
  - service: media_player.select_source
    target:
      entity_id: media_player.pioneer_avr
    data:
      source: "TV/Sat"
mode: single
```

### Exemple 5 : Mode muet automatique

Activer le mode muet lors d'un appel téléphonique ou d'une notification importante :

```yaml
alias: "Muet pendant les appels"
description: "Active le mode muet lors d'un appel"
trigger:
  - platform: state
    entity_id: sensor.phone_call_status  # Exemple de capteur
    to: 'ringing'
condition:
  - condition: state
    entity_id: media_player.pioneer_avr  # ⚠️ REMPLACEZ par le nom exact de votre entité
    state: 'on'
action:
  - service: media_player.volume_mute
    target:
      entity_id: media_player.pioneer_avr
    data:
      is_volume_muted: true
mode: single
```

### Exemple 6 : Script pour un scénario "Cinéma"

Créer un script qui configure l'ampli pour une expérience cinéma optimale :

```yaml
script:
  mode_cinema:
    alias: "Mode Cinéma"
    sequence:
      - service: media_player.turn_on
        target:
          entity_id: media_player.pioneer_avr
      - delay: "00:00:02"
      - service: media_player.select_source
        target:
          entity_id: media_player.pioneer_avr
        data:
          source: "DVD"
      - service: media_player.set_volume_level
        target:
          entity_id: media_player.pioneer_avr
        data:
          volume_level: 0.4  # Volume à 40%
      - service: media_player.volume_mute
        target:
          entity_id: media_player.pioneer_avr
        data:
          is_volume_muted: false
```

### Services disponibles

L'entité créée sous le domaine `media_player` expose les services suivants :

- `media_player.turn_on` : Allumer l'amplificateur
- `media_player.turn_off` : Éteindre l'amplificateur
- `media_player.volume_up` : Augmenter le volume
- `media_player.volume_down` : Diminuer le volume
- `media_player.set_volume_level` : Régler le volume (0.0 à 1.0)
- `media_player.volume_mute` : Activer/désactiver le mode muet
- `media_player.select_source` : Sélectionner une source d'entrée

### États disponibles

Vous pouvez utiliser ces états dans vos conditions d'automatisation :

- `state` : `on` ou `off`
- `volume_level` : Niveau de volume (0.0 à 1.0)
- `is_volume_muted` : `true` ou `false`
- `source` : Source actuellement sélectionnée

## Tableau de bord Lovelace

Vous pouvez créer un tableau de bord personnalisé avec une télécommande virtuelle pour contrôler votre amplificateur Pioneer. Voici un exemple complet :

### Exemple de télécommande virtuelle

Créez un nouveau tableau de bord dans Home Assistant et ajoutez cette configuration YAML :

```yaml
type: vertical-stack
cards:
  # Carte principale avec état et contrôle on/off
  - type: media-control
    entity: media_player.pioneer_avr  # Remplacez par votre entité
    
  # Contrôle du volume avec boutons
  - type: horizontal-stack
    cards:
      - type: button
        name: Volume -
        icon: mdi:volume-minus
        tap_action:
          action: call-service
          service: media_player.volume_down
          target:
            entity_id: media_player.pioneer_avr
      - type: gauge
        entity: media_player.pioneer_avr
        attribute: volume_level
        min: 0
        max: 1
        severity:
          green: 0
          yellow: 0.5
          red: 0.8
        name: Volume
      - type: button
        name: Volume +
        icon: mdi:volume-plus
        tap_action:
          action: call-service
          service: media_player.volume_up
          target:
            entity_id: media_player.pioneer_avr

  # Bouton Mute
  - type: button
    name: Mute
    icon: mdi:volume-mute
    tap_action:
      action: toggle
      service: media_player.volume_mute
      target:
        entity_id: media_player.pioneer_avr
    state:
      - value: 'on'
        styles:
          icon:
            - color: red
      - value: 'off'
        styles:
          icon:
            - color: grey

  # Sélecteur de source
  - type: entities
    title: Source d'entrée
    entities:
      - entity: media_player.pioneer_avr
        name: Source
        secondary_info: last-changed

  # Boutons de sources rapides
  - type: grid
    columns: 3
    square: false
    cards:
      - type: button
        name: CD
        icon: mdi:disc-player
        tap_action:
          action: call-service
          service: media_player.select_source
          target:
            entity_id: media_player.pioneer_avr
          data:
            source: CD
      - type: button
        name: DVD
        icon: mdi:disc
        tap_action:
          action: call-service
          service: media_player.select_source
          target:
            entity_id: media_player.pioneer_avr
          data:
            source: DVD
      - type: button
        name: TV/Sat
        icon: mdi:television
        tap_action:
          action: call-service
          service: media_player.select_source
          target:
            entity_id: media_player.pioneer_avr
          data:
            source: TV/Sat
      - type: button
        name: NET
        icon: mdi:network
        tap_action:
          action: call-service
          service: media_player.select_source
          target:
            entity_id: media_player.pioneer_avr
          data:
            source: NET
      - type: button
        name: iPod/USB
        icon: mdi:usb
        tap_action:
          action: call-service
          service: media_player.select_source
          target:
            entity_id: media_player.pioneer_avr
          data:
            source: iPod/USB
      - type: button
        name: Tuner
        icon: mdi:radio
        tap_action:
          action: call-service
          service: media_player.select_source
          target:
            entity_id: media_player.pioneer_avr
          data:
            source: Tuner

  # Informations de l'appareil
  - type: entities
    title: État de l'amplificateur
    entities:
      - entity: media_player.pioneer_avr
        name: État
      - type: attribute
        entity: media_player.pioneer_avr
        attribute: volume_level
        name: Volume
        unit_of_measurement: '%'
      - type: attribute
        entity: media_player.pioneer_avr
        attribute: source
        name: Source actuelle
      - type: attribute
        entity: media_player.pioneer_avr
        attribute: is_volume_muted
        name: Mode muet
```

### Exemple premium avec Mushroom

> Nécessite les cartes Mushroom, button-card et (optionnel) card-mod.
> Remplacez `media_player.pioneer_avr` par l'identifiant de votre entité.

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-title-card
    title: Pioneer AVR
    subtitle: Amplificateur Audio/Vidéo

  - type: horizontal-stack
    cards:
      - type: custom:mushroom-entity-card
        entity: media_player.pioneer_avr
        name: Alimentation
        icon: mdi:power
        tap_action:
          action: toggle
        hold_action:
          action: more-info
        card_mod:
          style: |
            ha-card {
              background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
              border-radius: 20px;
              box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            }
      - type: custom:mushroom-template-card
        primary: "{{ states('media_player.pioneer_avr') | title }}"
        secondary: "{{ state_attr('media_player.pioneer_avr', 'source') | default('Aucune source') }}"
        icon: mdi:speaker
        icon_color: >
          {% if is_state('media_player.pioneer_avr', 'on') %}
            green
          {% else %}
            red
          {% endif %}
        card_mod:
          style: |
            ha-card {
              background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
              border-radius: 20px;
              box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            }

  - type: custom:mushroom-media-player-card
    entity: media_player.pioneer_avr
    use_media_info: false
    use_media_artwork: false
    show_volume_level: true
    volume_controls:
      - volume_mute
      - volume_set
      - volume_buttons
    card_mod:
      style: |
        ha-card {
          background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
          border-radius: 20px;
          box-shadow: 0 8px 16px rgba(0,0,0,0.3);
          padding: 16px;
        }

  - type: custom:mushroom-title-card
    title: 🎵 Sources audio

  - type: grid
    columns: 5
    square: false
    cards:
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: CD
        icon: mdi:disc-player
        tap_action:
          action: call-service
          service: media_player.select_source
          service_data:
            entity_id: media_player.pioneer_avr
            source: CD
        styles:
          card:
            - background: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'CD') {
                    return 'linear-gradient(135deg, #a855f7 0%, #ec4899 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'CD') {
                    return '0 8px 16px rgba(168, 85, 247, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'CD') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: Tuner
        icon: mdi:radio
        tap_action:
          action: call-service
          service: media_player.select_source
          service_data:
            entity_id: media_player.pioneer_avr
            source: Tuner
        styles:
          card:
            - background: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'Tuner') {
                    return 'linear-gradient(135deg, #eab308 0%, #f97316 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'Tuner') {
                    return '0 8px 16px rgba(234, 179, 8, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'Tuner') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: Phono
        icon: mdi:album
        tap_action:
          action: call-service
          service: media_player.select_source
          service_data:
            entity_id: media_player.pioneer_avr
            source: Phono
        styles:
          card:
            - background: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'Phono') {
                    return 'linear-gradient(135deg, #f43f5e 0%, #dc2626 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'Phono') {
                    return '0 8px 16px rgba(244, 63, 94, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'Phono') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: iPod/USB
        icon: mdi:usb
        tap_action:
          action: call-service
          service: media_player.select_source
          service_data:
            entity_id: media_player.pioneer_avr
            source: iPod/USB
        styles:
          card:
            - background: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'iPod/USB') {
                    return 'linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'iPod/USB') {
                    return '0 8px 16px rgba(139, 92, 246, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'iPod/USB') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: Bluetooth
        icon: mdi:bluetooth
        tap_action:
          action: call-service
          service: media_player.select_source
          service_data:
            entity_id: media_player.pioneer_avr
            source: Bluetooth
        styles:
          card:
            - background: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'Bluetooth') {
                    return 'linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'Bluetooth') {
                    return '0 8px 16px rgba(6, 182, 212, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'Bluetooth') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px

  - type: custom:mushroom-title-card
    title: 📺 Sources vidéo

  - type: grid
    columns: 3
    square: false
    cards:
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: DVD
        icon: mdi:disc
        tap_action:
          action: call-service
          service: media_player.select_source
          service_data:
            entity_id: media_player.pioneer_avr
            source: DVD
        styles:
          card:
            - background: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'DVD') {
                    return 'linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'DVD') {
                    return '0 8px 16px rgba(59, 130, 246, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'DVD') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: BD
        icon: mdi:disc
        tap_action:
          action: call-service
          service: media_player.select_source
          service_data:
            entity_id: media_player.pioneer_avr
            source: Blu-ray
        styles:
          card:
            - background: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'Blu-ray') {
                    return 'linear-gradient(135deg, #6366f1 0%, #3b82f6 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'Blu-ray') {
                    return '0 8px 16px rgba(99, 102, 241, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'Blu-ray') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: TV/Sat
        icon: mdi:television
        tap_action:
          action: call-service
          service: media_player.select_source
          service_data:
            entity_id: media_player.pioneer_avr
            source: TV/Sat
        styles:
          card:
            - background: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'TV/Sat') {
                    return 'linear-gradient(135deg, #f97316 0%, #dc2626 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'TV/Sat') {
                    return '0 8px 16px rgba(249, 115, 22, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (states['media_player.pioneer_avr'].attributes.source === 'TV/Sat') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px

  - type: custom:mushroom-title-card
    title: 🎚 Modes audio

  - type: grid
    columns: 4
    square: false
    cards:
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: Auto
        icon: mdi:surround-sound
        tap_action:
          action: call-service
          service: media_player.select_sound_mode
          service_data:
            entity_id: media_player.pioneer_avr
            sound_mode: "Auto Surround"
        styles:
          card:
            - background: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Auto Surround') {
                    return 'linear-gradient(135deg, #14b8a6 0%, #0ea5e9 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Auto Surround') {
                    return '0 8px 16px rgba(20, 184, 166, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Auto Surround') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: Direct
        icon: mdi:tune
        tap_action:
          action: call-service
          service: media_player.select_sound_mode
          service_data:
            entity_id: media_player.pioneer_avr
            sound_mode: Direct
        styles:
          card:
            - background: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Direct') {
                    return 'linear-gradient(135deg, #a855f7 0%, #6366f1 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Direct') {
                    return '0 8px 16px rgba(99, 102, 241, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Direct') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: Pure
        icon: mdi:waveform
        tap_action:
          action: call-service
          service: media_player.select_sound_mode
          service_data:
            entity_id: media_player.pioneer_avr
            sound_mode: "Pure Direct"
        styles:
          card:
            - background: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Pure Direct') {
                    return 'linear-gradient(135deg, #f43f5e 0%, #ef4444 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Pure Direct') {
                    return '0 8px 16px rgba(239, 68, 68, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Pure Direct') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: Stéréo
        icon: mdi:headphones
        tap_action:
          action: call-service
          service: media_player.select_sound_mode
          service_data:
            entity_id: media_player.pioneer_avr
            sound_mode: Stereo
        styles:
          card:
            - background: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Stereo') {
                    return 'linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Stereo') {
                    return '0 8px 16px rgba(14, 165, 233, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Stereo') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: Étendu
        icon: mdi:speaker-multiple
        tap_action:
          action: call-service
          service: media_player.select_sound_mode
          service_data:
            entity_id: media_player.pioneer_avr
            sound_mode: "Extended Stereo"
        styles:
          card:
            - background: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Extended Stereo') {
                    return 'linear-gradient(135deg, #d946ef 0%, #9333ea 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Extended Stereo') {
                    return '0 8px 16px rgba(217, 70, 239, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Extended Stereo') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: Jeu
        icon: mdi:gamepad-variant
        tap_action:
          action: call-service
          service: media_player.select_sound_mode
          service_data:
            entity_id: media_player.pioneer_avr
            sound_mode: "Advanced Game"
        styles:
          card:
            - background: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Advanced Game') {
                    return 'linear-gradient(135deg, #f97316 0%, #facc15 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Advanced Game') {
                    return '0 8px 16px rgba(249, 115, 22, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Advanced Game') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: THX
        icon: mdi:surround-sound-71
        tap_action:
          action: call-service
          service: media_player.select_sound_mode
          service_data:
            entity_id: media_player.pioneer_avr
            sound_mode: "THX Cinema"
        styles:
          card:
            - background: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'THX Cinema') {
                    return 'linear-gradient(135deg, #22d3ee 0%, #0ea5e9 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'THX Cinema') {
                    return '0 8px 16px rgba(34, 211, 238, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'THX Cinema') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px
      - type: custom:button-card
        entity: media_player.pioneer_avr
        name: Éco
        icon: mdi:leaf
        tap_action:
          action: call-service
          service: media_player.select_sound_mode
          service_data:
            entity_id: media_player.pioneer_avr
            sound_mode: "Eco Mode"
        styles:
          card:
            - background: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Eco Mode') {
                    return 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)';
                  }
                  return 'linear-gradient(135deg, #475569 0%, #334155 100%)';
                ]]]
            - border-radius: 20px
            - box-shadow: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Eco Mode') {
                    return '0 8px 16px rgba(34, 197, 94, 0.4)';
                  }
                  return '0 4px 8px rgba(0,0,0,0.2)';
                ]]]
            - transition: all 0.3s ease
            - transform: |
                [[[
                  if (state_attr('media_player.pioneer_avr','sound_mode') === 'Eco Mode') {
                    return 'scale(1.05)';
                  }
                  return 'scale(1)';
                ]]]
          name:
            - color: white
            - font-weight: bold
            - font-size: 14px
          icon:
            - color: white
            - width: 32px

  - type: custom:mushroom-title-card
    title: 📊 État actuel

  - type: grid
    columns: 2
    square: false
    cards:
      - type: custom:mushroom-template-card
        primary: Alimentation
        secondary: >
          {% if is_state('media_player.pioneer_avr', 'on') %}
            ● Allumé
          {% else %}
            ○ Éteint
          {% endif %}
        icon: mdi:power
        icon_color: >
          {% if is_state('media_player.pioneer_avr', 'on') %}
            green
          {% else %}
            red
          {% endif %}
        card_mod:
          style: |
            ha-card {
              background: linear-gradient(135deg, #475569 0%, #334155 100%);
              border-radius: 16px;
            }
      - type: custom:mushroom-template-card
        primary: Source active
        secondary: "{{ state_attr('media_player.pioneer_avr', 'source') | default('Aucune') }}"
        icon: mdi:import
        icon_color: purple
        card_mod:
          style: |
            ha-card {
              background: linear-gradient(135deg, #475569 0%, #334155 100%);
              border-radius: 16px;
            }
      - type: custom:mushroom-template-card
        primary: Volume
        secondary: >
          {% if state_attr('media_player.pioneer_avr', 'is_volume_muted') %}
            🔇 Muet
          {% elif state_attr('media_player.pioneer_avr', 'volume_level') != None %}
            {{ ((state_attr('media_player.pioneer_avr', 'volume_level') | float(0)) * 100) | round }}%
          {% else %}
            N/A
          {% endif %}
        icon: mdi:volume-high
        icon_color: blue
        card_mod:
          style: |
            ha-card {
              background: linear-gradient(135deg, #475569 0%, #334155 100%);
              border-radius: 16px;
            }
      - type: custom:mushroom-template-card
        primary: Mode audio
        secondary: "{{ state_attr('media_player.pioneer_avr', 'sound_mode') | default('Stéréo') }}"
        icon: mdi:surround-sound
        icon_color: cyan
        card_mod:
          style: |
            ha-card {
              background: linear-gradient(135deg, #475569 0%, #334155 100%);
              border-radius: 16px;
            }
```

### Version simplifiée avec carte compacte

### Version simplifiée avec carte compacte

Pour une télécommande plus compacte, voici une version simplifiée :

```yaml
type: vertical-stack
cards:
  # Carte de contrôle principale
  - type: media-control
    entity: media_player.pioneer_avr
    
  # Contrôles rapides
  - type: grid
    columns: 4
    square: true
    cards:
      - type: button
        name: ON
        icon: mdi:power
        tap_action:
          action: call-service
          service: media_player.turn_on
          target:
            entity_id: media_player.pioneer_avr
      - type: button
        name: OFF
        icon: mdi:power-off
        tap_action:
          action: call-service
          service: media_player.turn_off
          target:
            entity_id: media_player.pioneer_avr
      - type: button
        name: Mute
        icon: mdi:volume-mute
        tap_action:
          action: toggle
          service: media_player.volume_mute
          target:
            entity_id: media_player.pioneer_avr
      - type: button
        name: Volume
        icon: mdi:volume-high
        tap_action:
          action: more-info
          entity: media_player.pioneer_avr

  # Sélecteur de source compact
  - type: button
    entity: media_player.pioneer_avr
    name: Source
    icon: mdi:input-hdmi
    tap_action:
      action: more-info
```

### Notes importantes

- Remplacez `media_player.pioneer_avr` par le nom réel de votre entité (visible dans Paramètres > Appareils et services)
- Pour trouver le nom exact de votre entité, allez dans Paramètres > Appareils et services, cliquez sur votre intégration Pioneer AVR LX83, puis sur l'entité
- Les cartes peuvent être personnalisées selon vos préférences (couleurs, icônes, disposition)
- Vous pouvez ajouter ces cartes à un tableau de bord existant ou créer un nouveau tableau de bord dédié

## Commandes Telnet

L'intégration utilise les commandes Telnet suivantes :

| Commande | Description |
|----------|-------------|
| `PO` | Allumer |
| `PF` | Éteindre |
| `?P` | Interroger l'état d'alimentation |
| `VLxxx` | Régler le volume (000-185) |
| `?V` | Interroger le volume |
| `MO` | Activer le mode muet |
| `MF` | Désactiver le mode muet |
| `?M` | Interroger l'état du mode muet |
| `FNxx` | Sélectionner la source |
| `?F` | Interroger la source |
| `?L` | Interroger le mode audio |

### Raccourcis pour tester les sources

Envoyez ces commandes depuis un terminal (`telnet 192.168.1.26 23`) ou via le service `pioneer_avr_lx83.send_raw_command` :

| Action | Commande |
|--------|----------|
| Forcer l'entrée CD | `01FN` |
| Forcer l'entrée DVD | `04FN` |
| Forcer l'entrée TV/Sat | `05FN` |
| Forcer l'entrée Blu-ray | `25FN` |
| Basculer Bluetooth / Port adaptateur | `33FN` |
| Basculer NET / Home Media Gallery | `26FN` |
| Basculer Phono | `00FN` |
| Interroger la source en cours | `?F` (réponse `FNxx`) |

### Modes audio populaires

| Mode audio | Commande |
|------------|----------|
| Auto Surround | `0006SR` |
| Direct | `0007SR` |
| Pure Direct | `0008SR` |
| Stéréo | `0001SR` |
| Stéréo étendu | `0112SR` |
| Advanced Game | `0118SR` |
| THX Cinema | `0056SR` |
| THX Music | `0069SR` |
| Optimum Surround | `0152SR` |
| Eco Mode | `0200SR` |

> Astuce : dans Home Assistant vous pouvez appeler `media_player.select_sound_mode` avec les mêmes libellés (par ex. `"Auto Surround"`). Pour des cartes Lovelace avancées ou des tests ponctuels, utilisez le service `pioneer_avr_lx83.send_raw_command`.

## Test et vérification

### Comment tester votre intégration

Une fois l'intégration configurée, voici comment tester que tout fonctionne correctement :

#### 1. Vérifier que l'entité est créée

1. Allez dans **Paramètres > Appareils et services**
2. Cliquez sur votre intégration **Pioneer AVR LX83**
3. Vous devriez voir :
   - **1 appareil** (Pioneer AVR LX83)
   - **1 entité** (media_player)

Si vous ne voyez pas l'entité :

- Vérifiez les logs (Paramètres > Système > Logs)
- Redémarrez Home Assistant
- Vérifiez que l'intégration est bien configurée (statut "Configuré")

#### 2. Tester les services manuellement

Vous pouvez tester chaque fonctionnalité via l'interface de développement :

1. Allez dans **Paramètres > Appareils et services > Outils de développement**
2. Cliquez sur l'onglet **SERVICES**
3. Testez les services suivants :

**Test 1 - Allumer l'ampli** :

```yaml
Service: media_player.turn_on
Entity: media_player.pioneer_avr  # Remplacez par votre entité
```

**Test 2 - Éteindre l'ampli** :

```yaml
Service: media_player.turn_off
Entity: media_player.pioneer_avr
```

**Test 3 - Régler le volume** :

```yaml
Service: media_player.set_volume_level
Entity: media_player.pioneer_avr
Service Data:
  volume_level: 0.3
```

**Test 4 - Activer le mode muet** :

```yaml
Service: media_player.volume_mute
Entity: media_player.pioneer_avr
Service Data:
  is_volume_muted: true
```

**Test 5 - Changer de source** :

```yaml
Service: media_player.select_source
Entity: media_player.pioneer_avr
Service Data:
  source: CD
```

#### 3. Vérifier l'état de l'entité

1. Allez dans **Paramètres > Appareils et services > Outils de développement**
2. Cliquez sur l'onglet **ÉTATS**
3. Recherchez votre entité (ex: `media_player.pioneer_avr`)
4. Vérifiez les attributs :
   - `state` : doit être `on` ou `off`
   - `volume_level` : doit être entre 0.0 et 1.0
   - `is_volume_muted` : doit être `true` ou `false`
   - `source` : doit afficher la source actuelle
   - `available` : doit être `true` si l'appareil est connecté

#### 4. Tester avec un script simple

Créez un script de test dans **Paramètres > Automatisations et scénarios > Scripts** :

```yaml
test_pioneer:
  alias: "Test Pioneer AVR"
  sequence:
    - service: media_player.turn_on
      target:
        entity_id: media_player.pioneer_avr  # Remplacez par votre entité
    - delay: "00:00:03"
    - service: media_player.set_volume_level
      target:
        entity_id: media_player.pioneer_avr
      data:
        volume_level: 0.2
    - delay: "00:00:02"
    - service: media_player.select_source
      target:
        entity_id: media_player.pioneer_avr
      data:
        source: CD
    - delay: "00:00:02"
    - service: media_player.volume_mute
      target:
        entity_id: media_player.pioneer_avr
      data:
        is_volume_muted: true
    - delay: "00:00:02"
    - service: media_player.volume_mute
      target:
        entity_id: media_player.pioneer_avr
      data:
        is_volume_muted: false
    - delay: "00:00:02"
    - service: media_player.turn_off
      target:
        entity_id: media_player.pioneer_avr
```

Exécutez ce script et vérifiez que chaque action fonctionne sur votre amplificateur.

#### 5. Vérifier les logs

Si quelque chose ne fonctionne pas, consultez les logs :

1. Allez dans **Paramètres > Système > Logs**
2. Recherchez les messages contenant "pioneer" ou "avr"
3. Les erreurs seront affichées avec le préfixe `pioneer_avr_lx83`

### Problèmes courants

#### L'entité n'apparaît pas

- **Solution 1** : Vérifiez que l'intégration est bien configurée et activée
- **Solution 2** : Redémarrez Home Assistant
- **Solution 3** : Vérifiez les logs pour des erreurs de connexion
- **Solution 4** : Supprimez et reconfigurez l'intégration

#### L'entité est "unavailable" (indisponible)

- Vérifiez la connexion réseau entre Home Assistant et l'amplificateur
- Vérifiez que Telnet est activé sur l'amplificateur
- Vérifiez que l'adresse IP est correcte
- Testez la connexion Telnet manuellement depuis un terminal

#### Les commandes ne fonctionnent pas

- Vérifiez que l'amplificateur est allumé
- Vérifiez les logs pour des erreurs
- Testez chaque service individuellement via l'interface de développement
- Vérifiez que vous utilisez le bon nom d'entité

## Dépannage

### Impossible de se connecter à l'appareil

- Vérifiez que l'adresse IP est correcte
- Assurez-vous que Telnet est activé sur votre Pioneer AVR
- Vérifiez que le port 23 n'est pas bloqué par un pare-feu
- Vérifiez que l'appareil est sur le même réseau

### L'appareil ne répond pas

- Redémarrez le Pioneer AVR
- Redémarrez Home Assistant
- Vérifiez la connectivité réseau

## Versionnement & Releases

- L'intégration suit le [versionnement sémantique](https://semver.org/lang/fr/) et la version courante est stockée dans le fichier `VERSION` ainsi que dans `manifest.json`.
- Exécutez `./scripts/bump_version.py 1.1.0` (en adaptant la valeur) pour mettre à jour toutes les références et générer un nouveau bloc dans le changelog.
- Validez vos changements puis créez un tag `git tag -a v1.1.0 -m "Release v1.1.0"` et poussez-le (`git push --tags`).
- Un workflow GitHub Actions (`.github/workflows/release.yml`) publie automatiquement une release GitHub dès qu'un tag `v*` est poussé. Il récupère l'entrée correspondante dans `CHANGELOG.md` via `scripts/extract_changelog.py` pour alimenter la note de version, ce qui donne des détails utiles dans HACS.
- Un second workflow (`release-drafter.yml`) tient à jour un brouillon de release à chaque push sur `main`, vous n'avez plus qu'à vérifier puis publier une fois le tag créé.

## Compatibilité

- Home Assistant 2023.1.0 ou supérieur
- Compatible avec Home Assistant 2025.12 et 2026.01
- Utilise les meilleures pratiques modernes (DataUpdateCoordinator)

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à soumettre une Pull Request.

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Crédits

- Développé par Jack
- Table de modes audio adaptée du projet [aiopioneer](https://github.com/fgierlinger/aiopioneer) (Apache-2.0)

## Support

Si vous rencontrez des problèmes, veuillez [ouvrir une issue](https://github.com/Jackngl/pioneer_avr_lx83/issues) sur GitHub.
