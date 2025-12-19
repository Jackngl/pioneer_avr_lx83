# Documentation Technique - Pioneer AVR LX83 Integration

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture](#architecture)
3. [Structure du projet](#structure-du-projet)
4. [Composants principaux](#composants-principaux)
5. [Protocole de communication](#protocole-de-communication)
6. [Flux de données](#flux-de-données)
7. [Gestion des erreurs](#gestion-des-erreurs)
8. [Services](#services)
9. [Configuration](#configuration)
10. [Extensibilité](#extensibilité)

---

## Vue d'ensemble

### Description

L'intégration **Pioneer AVR LX83** est une intégration personnalisée pour Home Assistant qui permet de contrôler les amplificateurs Pioneer AVR LX83 via le protocole Telnet. Elle expose l'amplificateur comme une entité `media_player` standard de Home Assistant.

### Caractéristiques principales

- **Communication Telnet** : Utilise le protocole Telnet (port 23 par défaut) pour communiquer avec l'amplificateur
- **Polling** : Mise à jour périodique de l'état (intervalle de 10 secondes)
- **Découverte automatique** : Découverte automatique des sources configurées sur l'amplificateur via `?RGBxx`
- **Gestion des erreurs** : Système de retry avec verrouillage pour éviter les conflits de connexion
- **Services personnalisés** : Service `send_raw_command` pour envoyer des commandes Telnet arbitraires

### Compatibilité

- **Home Assistant** : 2023.1.0 ou supérieur
- **Modèles Pioneer** : AVR LX83 et modèles compatibles
- **Protocole** : Telnet/IP (port 23 par défaut)

---

## Architecture

### Architecture générale

```
┌─────────────────────────────────────────────────────────────┐
│                    Home Assistant                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Pioneer AVR LX83 Integration                 │  │
│  │                                                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │  │
│  │  │ Config Flow  │  │ Media Player │  │ Services  │ │  │
│  │  │              │  │   Entity     │  │           │ │  │
│  │  └──────────────┘  └──────────────┘  └───────────┘ │  │
│  │         │                  │                │        │  │
│  │         └──────────────────┼────────────────┘        │  │
│  │                            │                         │  │
│  │                   ┌────────▼────────┐               │  │
│  │                   │  Telnet Client  │               │  │
│  │                   │  (Socket-based)  │               │  │
│  │                   └────────┬────────┘               │  │
│  └────────────────────────────┼─────────────────────────┘  │
│                               │                            │
└───────────────────────────────┼────────────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │   Pioneer AVR LX83    │
                    │   (192.168.x.x:23)   │
                    └──────────────────────┘
```

### Flux de communication

1. **Initialisation** : L'intégration se connecte via Telnet lors de la première commande
2. **Polling** : Mise à jour périodique de l'état (power, volume, source, mute, listening mode)
3. **Commandes** : Envoi de commandes Telnet pour contrôler l'amplificateur
4. **Réponses** : Lecture des réponses Telnet pour mettre à jour l'état

---

## Structure du projet

```
pioneer_avr_lx83/
├── custom_components/
│   └── pioneer_avr_lx83/
│       ├── __init__.py          # Point d'entrée de l'intégration
│       ├── config_flow.py       # Configuration UI (Config Flow)
│       ├── const.py              # Constantes et définitions
│       ├── media_player.py       # Entité Media Player principale
│       ├── manifest.json         # Métadonnées de l'intégration
│       ├── services.yaml         # Définition des services
│       ├── strings.json          # Chaînes de traduction
│       └── translations/
│           ├── en.json           # Traductions anglaises
│           └── fr.json           # Traductions françaises
├── tests/
│   └── test_media_player.py     # Tests unitaires
├── scripts/
│   └── bump_version.py          # Script de versioning
├── README.md                    # Documentation utilisateur
├── CHANGELOG.md                 # Historique des versions
└── TECHNICAL.md                 # Cette documentation
```

---

## Composants principaux

### 1. `__init__.py` - Point d'entrée

**Rôle** : Initialise l'intégration et configure les plateformes.

**Fonctions principales** :
- `async_setup_entry()` : Configure l'intégration à partir d'une entrée de configuration
- `async_unload_entry()` : Décharge l'intégration
- `async_reload_entry()` : Recharge l'intégration après modification

**Flux** :
```python
async_setup_entry()
  └─> hass.config_entries.async_forward_entry_setups()
      └─> async_setup_entry() dans media_player.py
```

### 2. `config_flow.py` - Configuration UI

**Rôle** : Gère la configuration via l'interface utilisateur de Home Assistant.

**Classes principales** :
- `ConfigFlow` : Gère le flux de configuration initial
- `OptionsFlowHandler` : Gère les options de configuration
- `CannotConnect` : Exception pour les erreurs de connexion

**Étapes de configuration** :
1. **User Input** : Demande l'IP, le port (optionnel, défaut 23) et le nom
2. **Validation** : Teste la connexion Telnet avec la commande `?P`
3. **Création** : Crée l'entrée de configuration avec les sources par défaut

**Schéma de validation** :
```python
STEP_USER_DATA_SCHEMA = {
    "host": str (requis),
    "port": int (optionnel, défaut 23),
    "name": str (optionnel, défaut "Pioneer AVR")
}
```

### 3. `const.py` - Constantes et définitions

**Rôle** : Définit toutes les constantes, commandes et mappings.

**Sections principales** :

#### Configuration
- `DOMAIN` : `"pioneer_avr_lx83"`
- `DEFAULT_PORT` : `23`
- `DEFAULT_TIMEOUT` : `10` secondes
- `SCAN_INTERVAL` : `timedelta(seconds=10)`
- `MAX_RETRIES` : `3`
- `RETRY_DELAY` : `1` seconde
- `COMMAND_PAUSE` : `0.3` secondes entre commandes

#### Volume
- `VOLUME_MAX` : `185` (pas maximum Pioneer)
- `VOLUME_DB_OFFSET` : `85` (offset pour conversion dB)

#### Sources
- `DEFAULT_SOURCES` : Mapping nom → code (ex: `"CD": "01"`)
- `SOURCE_ALIASES` : Alias insensibles à la casse pour les sources
- `MAX_SOURCE_SLOTS` : `60` (nombre maximum de slots à interroger)

#### Listening Modes
- `DEFAULT_LISTENING_MODES` : Mapping nom → code (ex: `"Stereo": "0001"`)
- `LISTENING_MODE_ALIASES` : Alias insensibles à la casse

#### Commandes Telnet
- **Power** : `PO` (on), `PF` (off), `?P` (query)
- **Volume** : `VLxxx` (set), `VU` (up), `VD` (down), `?V` (query)
- **Mute** : `MO` (on), `MF` (off), `?M` (query)
- **Source** : `FNxx` (set), `?F` (query), `?RGBxx` (query name)
- **Listening Mode** : `SRxxxx` (set), `?L` (query)
- **Media** : `10NW` (play), `11NW` (pause)
- **Zones** : Commandes Zone 2 et Zone 3
- **Tuner** : `TFI` (freq up), `TFD` (freq down), `TPI` (preset up), `TPD` (preset down)

### 4. `media_player.py` - Entité principale

**Rôle** : Implémente l'entité `MediaPlayerEntity` pour contrôler l'amplificateur.

**Classe principale** : `PioneerAVR`

#### Propriétés

```python
# État
_power_state: str              # STATE_ON ou STATE_OFF
_playback_state: str | None    # STATE_PLAYING, STATE_PAUSED, ou None
_volume: float                 # 0.0 à 1.0
_volume_step: int              # 0 à 185 (pas Pioneer)
_is_muted: bool                # État du mute
_source: str | None            # Source actuelle
_sound_mode: str | None        # Mode d'écoute actuel
_sound_mode_code: str | None   # Code du mode d'écoute

# Sources
_sources: dict[str, str]       # Mapping nom → code
_source_code_to_name: dict     # Mapping code → nom
_source_aliases: dict          # Alias insensibles à la casse

# Connexion
_socket: socket.socket | None   # Socket Telnet réutilisable
_command_lock: asyncio.Lock()  # Verrou pour éviter les conflits
_available: bool               # Disponibilité de l'appareil
_retry_count: int              # Compteur de tentatives
```

#### Méthodes principales

##### Contrôle de base
- `async_turn_on()` : Allume l'amplificateur (`PO`)
- `async_turn_off()` : Éteint l'amplificateur (`PF`)
- `async_volume_up()` : Augmente le volume (`VU`)
- `async_volume_down()` : Diminue le volume (`VD`)
- `async_set_volume_level(volume: float)` : Définit le volume (`VLxxx`)
- `async_mute_volume(mute: bool)` : Active/désactive le mute (`MO`/`MF`)

##### Sélection
- `async_select_source(source: str)` : Sélectionne une source (`FNxx`)
- `async_select_sound_mode(mode: str)` : Sélectionne un mode d'écoute (`SRxxxx`)

##### Media
- `async_media_play()` : Lecture (`10NW`)
- `async_media_pause()` : Pause (`11NW`)

##### Services
- `async_send_raw_command(command: str)` : Envoie une commande Telnet arbitraire

##### Mise à jour
- `async_update()` : Met à jour l'état depuis l'amplificateur
  - Interroge : power, volume, mute, source, listening mode
  - Découvre les sources dynamiques si nécessaire

#### Gestion de la connexion

##### Socket réutilisable
L'intégration maintient une connexion socket réutilisable pour éviter de créer/fermer des connexions à chaque commande :

```python
def _ensure_socket() -> socket.socket:
    """Retourne un socket actif, l'ouvre si nécessaire."""
    if self._socket is not None:
        return self._socket
    # Crée une nouvelle connexion
    sock = socket.create_connection((self._host, self._port), timeout=DEFAULT_TIMEOUT)
    self._socket = sock
    return sock
```

##### Verrou de commande
Un verrou asyncio (`_command_lock`) garantit qu'une seule commande est envoyée à la fois :

```python
async def _send_command(self, command: str) -> None:
    async with self._command_lock:
        # Envoi de la commande...
```

**⚠️ Important - Délai entre commandes** :
- Un délai de **100ms** (`COMMAND_PAUSE = 0.1`) est respecté entre chaque commande Telnet
- Ce délai est **crucial** pour éviter de saturer le processeur réseau de l'amplificateur
- Ne pas réduire ce délai sous peine de provoquer des erreurs de communication

##### Gestion des erreurs
- **Retry** : Jusqu'à 3 tentatives avec délai de 1 seconde
- **Fermeture automatique** : Le socket est fermé en cas d'erreur
- **Disponibilité** : L'entité devient `unavailable` après 3 échecs consécutifs

#### Découverte automatique des sources

L'intégration interroge les slots de source (00-59) pour découvrir les sources configurées :

```python
async def _ensure_dynamic_sources(self) -> None:
    """Découvre les labels de source rapportés par l'AVR."""
    for idx in range(MAX_SOURCE_SLOTS):
        code = f"{idx:02d}"
        response = await self._send_command_with_response(f"?RGB{code}")
        # Parse la réponse et enregistre la source si trouvée
```

**Format de réponse** : `RGBxx<label>` où `xx` est le code et `<label>` est le nom configuré.

#### Résolution des sources

Le système supporte plusieurs formats pour sélectionner une source :

1. **Nom exact** : `"CD"` → `"01"`
2. **Alias** : `"cd"`, `"CD"` → `"01"` (insensible à la casse)
3. **Code direct** : `"01"` → `"01"`

```python
def _resolve_source_code(self, label: str) -> tuple[str, str] | None:
    """Retourne (code, nom_canonique) pour un label de source."""
    # 1. Vérifie le nom exact
    if label in self._sources:
        return self._sources[label], label
    # 2. Vérifie les alias
    lowered = label.lower()
    alias_code = self._source_aliases.get(lowered)
    if alias_code:
        canonical = self._source_code_to_name.get(alias_code, label)
        return alias_code, canonical
    return None
```

---

## Protocole de communication

### Format des commandes

#### Structure
- **Commande** : Chaîne ASCII (ex: `"PO"`, `"VL050"`, `"FN02"`)
- **Terminateur** : `\r` (CR, caractère 0x0D)
- **Encodage** : UTF-8

#### Exemples de commandes

```python
# Power
"PO" + "\r"    # Power On
"PF" + "\r"    # Power Off
"?P" + "\r"    # Query Power

# Volume
"VL050" + "\r" # Set volume to 50
"VU" + "\r"    # Volume Up
"VD" + "\r"    # Volume Down
"?V" + "\r"    # Query Volume

# Source
"FN02" + "\r"  # Select source 02 (Tuner)
"?F" + "\r"    # Query current source
"?RGB01" + "\r" # Query source name for code 01

# Listening Mode - Standard Modes
"0001SR" + "\r" # Set Stereo mode
"0006SR" + "\r" # Set Auto Surround / Stream Direct
"0007SR" + "\r" # Set Direct
"0008SR" + "\r" # Set Pure Direct
"0010SR" + "\r" # Set Standard (Dolby/DTS)
"0112SR" + "\r" # Set Extended Stereo
"0118SR" + "\r" # Set Advanced Game
"0152SR" + "\r" # Set Optimum Surround
"0200SR" + "\r" # Set Eco Mode

# Listening Mode - THX Modes
"0101SR" + "\r" # Set THX Cinema
"0102SR" + "\r" # Set THX Music
"0103SR" + "\r" # Set THX Games
"0105SR" + "\r" # Set THX Select2 Cinema / Ultra2 Cinema
"0106SR" + "\r" # Set THX Select2 Music / Ultra2 Music
"0107SR" + "\r" # Set THX Select2 Games / Ultra2 Games
"0115SR" + "\r" # Set THX Surround EX

# Listening Mode - Dolby Modes
"0013SR" + "\r" # Set PRO LOGIC II Movie
"0014SR" + "\r" # Set PRO LOGIC II Music
"0151SR" + "\r" # Set Dolby Surround (Atmos/LX models)

# Query
"?L" + "\r"     # Query listening mode
```

### Format des réponses

#### Structure
- **Format** : Chaîne ASCII terminée par `\r\n` ou `\n`
- **Encodage** : UTF-8
- **Timeout** : 10 secondes par défaut

#### Exemples de réponses

```
# Power
"PWR0\r\n"  # Power On
"PWR1\r\n"  # Power Off
"PWR2\r\n"  # Power On (standby)

# Volume
"VOL050\r\n"  # Volume at step 50

# Mute
"MUT0\r\n"    # Mute On
"MUT1\r\n"    # Mute Off

# Source
"FN02\r\n"    # Current source is 02 (Tuner)
"RGB01CD\r\n" # Source 01 is named "CD"

# Listening Mode
"LM0001\r\n"  # Listening mode is 0001 (Stereo)
```

### Séquence de communication

#### Envoi de commande simple
```
1. Ouvrir socket (si nécessaire)
2. Envoyer commande + "\r"
3. Attendre COMMAND_PAUSE (100ms) - IMPORTANT pour ne pas saturer l'ampli
4. Fermer socket (si erreur)
```

#### Envoi avec réponse
```
1. Ouvrir socket (si nécessaire)
2. Envoyer commande + "\r"
3. Attendre COMMAND_PAUSE (100ms) - IMPORTANT pour ne pas saturer l'ampli
4. Lire réponse jusqu'à "\r\n" ou timeout
5. Parser la réponse
6. Fermer socket (si erreur)
```

**⚠️ Rappel technique important** :
- **Délai entre commandes** : Un délai de **100ms** (0.1 seconde) est respecté entre chaque commande Telnet
- **Raison** : Éviter de saturer le processeur réseau de l'amplificateur Pioneer
- **Conséquence** : Si ce délai est réduit ou supprimé, l'amplificateur peut refuser les commandes ou générer des erreurs

### Gestion des timeouts

- **Connexion** : 10 secondes
- **Lecture** : 10 secondes
- **Retry** : 3 tentatives avec délai de 1 seconde

---

## Flux de données

### Initialisation

```
1. Home Assistant charge l'intégration
2. async_setup_entry() est appelé
3. PioneerAVR est instancié
4. L'entité est ajoutée à Home Assistant
5. async_update() est appelé automatiquement
```

### Mise à jour périodique

```
Toutes les 10 secondes (SCAN_INTERVAL):
1. async_update() est appelé
2. Vérification de l'état power (?P)
3. Si power = ON:
   a. Découverte des sources dynamiques (si première fois)
   b. Interrogation du volume (?V)
   c. Interrogation du mute (?M)
   d. Interrogation de la source (?F)
   e. Interrogation du listening mode (?L)
4. Mise à jour de l'état de l'entité
5. async_write_ha_state()
```

### Envoi de commande

```
1. Utilisateur appelle une méthode (ex: async_turn_on())
2. async_turn_on() appelle _send_command("PO")
3. _send_command() acquiert le verrou _command_lock
4. _send_command_sync() est exécuté dans un thread
5. _ensure_socket() ouvre/retourne le socket
6. Commande envoyée via socket.sendall()
7. Attente COMMAND_PAUSE (0.3s)
8. Verrou libéré
9. État mis à jour localement
10. async_write_ha_state() notifie Home Assistant
```

### Découverte des sources

```
Au premier async_update() si power = ON:
1. _ensure_dynamic_sources() est appelé
2. Pour chaque slot 00-59:
   a. Envoi de "?RGBxx" (xx = code du slot)
   b. Lecture de la réponse
   c. Si réponse valide (format RGBxx<label>):
      - Parse le label
      - Enregistre la source avec _register_source()
3. _dynamic_sources_loaded = True
```

---

## Gestion des erreurs

### Stratégie de retry

```python
for attempt in range(1, MAX_RETRIES + 1):
    try:
        # Tentative d'envoi
        sock.sendall(payload)
        return
    except (socket.timeout, socket.error, ...) as err:
        # Fermeture du socket
        self._close_socket()
        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)  # Attendre 1 seconde
        else:
            raise  # Échec après 3 tentatives
```

### Gestion de la disponibilité

```python
# Compteur de retry
self._retry_count = 0

# Après chaque erreur
self._retry_count += 1
if self._retry_count > MAX_RETRIES:
    self._available = False

# Après succès
self._retry_count = 0
self._available = True
```

### Types d'erreurs gérées

1. **Erreurs réseau** :
   - `socket.timeout` : Timeout de connexion/lecture
   - `socket.error` : Erreur réseau générique
   - `ConnectionRefusedError` : Connexion refusée
   - `OSError` : Erreur système

2. **Erreurs de parsing** :
   - `ValueError` : Erreur de conversion (ex: volume)
   - `UnicodeDecodeError` : Erreur de décodage UTF-8
   - `AttributeError` : Attribut manquant

3. **Erreurs de logique** :
   - Source inconnue
   - Mode d'écoute inconnu
   - Commande invalide

---

## Services

### Service standard : `send_raw_command`

**Définition** : `services.yaml`

```yaml
send_raw_command:
  name: Send raw Pioneer command
  description: Send an arbitrary Telnet command
  target:
    entity:
      integration: pioneer_avr_lx83
      domain: media_player
  fields:
    command:
      name: Command
      description: Raw Pioneer command without CR
      required: true
      example: "01FN"
```

**Enregistrement** : Dans `media_player.py`

```python
platform.async_register_entity_service(
    "send_raw_command",
    cv.make_entity_service_schema({vol.Required("command"): cv.string}),
    "async_send_raw_command",
)
```

**Utilisation** :

```yaml
service: pioneer_avr_lx83.send_raw_command
data:
  entity_id: media_player.pioneer_avr
  command: "01FN"  # Sélectionne la source CD
```

**Exemples de commandes** :

```yaml
# Preset Tuner 1
command: "01TP"

# Preset Tuner 2
command: "02TP"

# Previous Preset
command: "TPD"

# Next Preset
command: "TPI"

# Frequency Up
command: "TFI"

# Frequency Down
command: "TFD"

# Query Frequency
command: "?FR"
```

---

## Configuration

### Configuration via Config Flow

**Étapes** :
1. **Host** : Adresse IP de l'amplificateur (requis)
2. **Port** : Port Telnet (optionnel, défaut 23)
3. **Name** : Nom de l'entité (optionnel, défaut "Pioneer AVR")

**Validation** :
- Test de connexion avec `?P`
- Vérification de l'unicité (host + port)

### Configuration stockée

**Format** : `ConfigEntry.data`

```python
{
    "host": "192.168.1.100",
    "port": 23,
    "name": "Pioneer AVR",
    "sources": {
        "CD": "01",
        "Tuner": "02",
        # ... sources par défaut
    }
}
```

### Options (futur)

L'`OptionsFlowHandler` est prêt pour l'ajout de :
- Personnalisation des sources
- Configuration des zones
- Paramètres avancés

---

## Extensibilité

### Ajout de nouvelles commandes

1. **Définir la commande dans `const.py`** :
```python
CMD_NEW_FEATURE = "XX"
```

2. **Ajouter la méthode dans `media_player.py`** :
```python
async def async_new_feature(self) -> None:
    """Nouvelle fonctionnalité."""
    await self._send_command(CMD_NEW_FEATURE)
    self.async_write_ha_state()
```

3. **Exposer via service si nécessaire** :
```python
platform.async_register_entity_service(
    "new_feature",
    cv.make_entity_service_schema({}),
    "async_new_feature",
)
```

### Ajout de nouvelles sources

Les sources sont automatiquement découvertes via `?RGBxx`. Pour ajouter des sources par défaut :

1. **Modifier `DEFAULT_SOURCES` dans `const.py`** :
```python
DEFAULT_SOURCES = {
    # ... sources existantes
    "New Source": "XX",
}
```

2. **Ajouter des alias si nécessaire** :
```python
SOURCE_ALIASES = {
    # ... alias existants
    "newsource": "XX",
    "new": "XX",
}
```

### Ajout de nouveaux modes d'écoute

1. **Modifier `DEFAULT_LISTENING_MODES` dans `const.py`** :
```python
DEFAULT_LISTENING_MODES = {
    # ... modes existants
    "New Mode": "XXXX",
}
```

2. **Ajouter des alias** :
```python
LISTENING_MODE_ALIASES = {
    # ... alias existants
    "newmode": "XXXX",
}
```

### Modes d'écoute disponibles

L'intégration supporte les modes d'écoute suivants :

#### Modes standards
- **Stereo** (`0001SR`) : Mode stéréo standard
- **Auto Surround / Stream Direct** (`0006SR`) : Mode surround automatique / Stream Direct
- **Direct** (`0007SR`) : Mode direct
- **Pure Direct** (`0008SR`) : Mode direct pur
- **Standard** (`0010SR`) : Standard (Dolby/DTS)
- **Extended Stereo** (`0112SR`) : Stéréo étendue
- **Advanced Game** (`0118SR`) : Mode jeu avancé
- **Optimum Surround** (`0152SR`) : Surround optimal
- **Eco Mode** (`0200SR`) : Mode éco

#### Modes THX
- **THX Cinema** (`0101SR`) : Mode THX Cinema
- **THX Music** (`0102SR`) : Mode THX Music
- **THX Games** (`0103SR`) : Mode THX Games
- **THX Select2 Cinema / Ultra2 Cinema** (`0105SR`) : THX Select2 Cinema / Ultra2 Cinema
- **THX Select2 Music / Ultra2 Music** (`0106SR`) : THX Select2 Music / Ultra2 Music
- **THX Select2 Games / Ultra2 Games** (`0107SR`) : THX Select2 Games / Ultra2 Games
- **THX Surround EX** (`0115SR`) : THX Surround EX

#### Modes Dolby
- **PRO LOGIC II Movie** (`0013SR`) : Dolby Pro Logic II Movie
- **PRO LOGIC II Music** (`0014SR`) : Dolby Pro Logic II Music
- **Dolby Surround** (`0151SR`) : Dolby Surround (pour les modèles récents Atmos/LX)

### Support des zones

Les commandes Zone 2 et Zone 3 sont déjà définies dans `const.py` mais pas encore implémentées. Pour les ajouter :

1. **Créer des entités séparées** pour Zone 2 et Zone 3
2. **Utiliser les commandes définies** :
   - Zone 2 : `APO`, `APF`, `ZS`, `ZU`, `ZD`, etc.
   - Zone 3 : `BPO`, `BPF`, `ZT`, `YU`, `YD`, etc.

### Utilisation d'un DataUpdateCoordinator (futur)

Pour améliorer les performances et la conformité avec les meilleures pratiques HA 2025.12+ :

1. **Créer un coordinator** :
```python
class PioneerAVRCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, host, port):
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)
        self.host = host
        self.port = port
    
    async def _async_update_data(self):
        # Logique de mise à jour
        pass
```

2. **Utiliser CoordinatorEntity** :
```python
class PioneerAVR(CoordinatorEntity, MediaPlayerEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        # ...
```

---

## Détails d'implémentation

### Conversion du volume

#### Pioneer → Home Assistant
```python
def _step_to_level(self, step: int) -> float:
    """Convert Pioneer step (0-185) to HA 0..1 scale."""
    return step / VOLUME_MAX
```

#### Home Assistant → Pioneer
```python
async def async_set_volume_level(self, volume: float) -> None:
    """Set volume level, range 0..1."""
    volume_int = int(volume * VOLUME_MAX)  # 0-185
    await self._send_command(f"{volume_int:03d}{CMD_VOLUME}")  # "VL050"
```

#### Conversion dB (approximative)
```python
def _step_to_db(self, step: int) -> float:
    """Convert Pioneer step to approximate dB."""
    return step - VOLUME_DB_OFFSET  # step - 85
```

### Parsing des réponses

#### Volume
```python
vol_str = volume_response.decode().strip()  # "VOL050"
if "VOL" in vol_str:
    vol_value = int(vol_str.replace("VOL", ""))  # 50
```

#### Source
```python
src_str = source_response.decode().strip()  # "FN02"
if "FN" in src_str:
    src_code = src_str.split("FN", 1)[1].strip()  # "02"
```

#### Listening Mode
```python
raw = response.decode().strip()  # "LM0001"
digits = "".join(ch for ch in raw if ch.isdigit())  # "0001"
code = digits[-4:].zfill(4)  # "0001"
```

### Gestion du socket

#### Réutilisation
Le socket est réutilisé pour éviter les overheads de connexion/déconnexion :

```python
def _ensure_socket(self) -> socket.socket:
    if self._socket is not None:
        return self._socket  # Réutilise
    # Crée nouvelle connexion
    self._socket = socket.create_connection(...)
    return self._socket
```

#### Fermeture
Le socket est fermé en cas d'erreur ou lors de la suppression de l'entité :

```python
def _close_socket(self) -> None:
    if self._socket is None:
        return
    try:
        self._socket.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    try:
        self._socket.close()
    except OSError:
        pass
    self._socket = None
```

---

## Tests

### Structure des tests

Le fichier `tests/test_media_player.py` contient les tests unitaires. Pour exécuter :

```bash
pytest tests/
```

### Points de test recommandés

1. **Connexion** : Test de connexion réussie/échouée
2. **Commandes** : Test d'envoi de commandes
3. **Parsing** : Test du parsing des réponses
4. **Sources** : Test de résolution des sources
5. **Volume** : Test de conversion volume
6. **Erreurs** : Test de gestion des erreurs

---

## Performance

### Optimisations actuelles

1. **Socket réutilisable** : Évite les overheads de connexion
2. **Verrou asyncio** : Évite les conflits de commandes
3. **Découverte différée** : Les sources sont découvertes seulement si nécessaire
4. **Mise à jour conditionnelle** : Seulement si power = ON

### Améliorations possibles

1. **DataUpdateCoordinator** : Centraliser les mises à jour
2. **Cache des réponses** : Réduire les requêtes redondantes
3. **Batching** : Envoyer plusieurs commandes en une seule connexion
4. **WebSocket** : Si l'amplificateur le supporte (non disponible sur LX83)

---

## Sécurité

### Considérations

1. **Réseau local uniquement** : L'intégration communique uniquement sur le réseau local
2. **Pas d'authentification** : Le protocole Telnet Pioneer ne nécessite pas d'authentification
3. **Validation des entrées** : Les commandes sont validées avant envoi
4. **Gestion des erreurs** : Les erreurs sont loggées mais ne causent pas de crash

### Recommandations

- Utiliser un réseau local sécurisé
- Ne pas exposer le port Telnet de l'amplificateur à Internet
- Surveiller les logs pour détecter les erreurs

---

## Limitations connues

1. **Une seule connexion Telnet** : L'amplificateur n'accepte qu'une seule connexion à la fois
2. **Pas de support Zone 2/3** : Les commandes sont définies mais non implémentées
3. **Polling uniquement** : Pas de notifications push de l'amplificateur
4. **Pas de support multi-zone** : Une seule entité par amplificateur
5. **Timeout fixes** : Les timeouts ne sont pas configurables

---

## Références

### Documentation Pioneer

- Manuel utilisateur Pioneer AVR LX83
- Protocole Telnet/IP Pioneer (documentation interne)

### Ressources Home Assistant

- [Développement d'intégrations](https://developers.home-assistant.io/docs/creating_integration/)
- [Media Player Entity](https://developers.home-assistant.io/docs/core/entity/media-player/)
- [Config Flow](https://developers.home-assistant.io/docs/config_entries_config_flow_handler/)

### Projets similaires

- `aiopioneer` : Bibliothèque Python asyncio pour Pioneer AVR
- Autres intégrations Pioneer pour Home Assistant

---

## Maintenance

### Logs

Les logs sont disponibles dans Home Assistant :
- **Niveau DEBUG** : Détails des commandes et réponses
- **Niveau ERROR** : Erreurs de connexion et parsing

### Débogage

Pour activer les logs détaillés, ajouter dans `configuration.yaml` :

```yaml
logger:
  default: info
  logs:
    custom_components.pioneer_avr_lx83: debug
```

### Contribution

Voir `CONTRIBUTING.md` pour les guidelines de contribution.

---

## Version

**Version actuelle** : 1.1.0 (selon `manifest.json`)

**Historique** : Voir `CHANGELOG.md`

---

*Documentation générée le 2024-12-19*

