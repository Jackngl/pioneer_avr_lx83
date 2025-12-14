# Commandes de contrôle pour récepteurs Pioneer

Ce document organise les commandes de contrôle pour les récepteurs audio/vidéo Pioneer. Ces commandes peuvent être utilisées via une connexion série ou IP pour contrôler à distance votre appareil.

## Commandes de la zone principale

### Alimentation
- `PO` - Allumer l'appareil
- `PF` - Éteindre l'appareil
- `?P` - Interroger l'état d'alimentation
- Réponses possibles:
  - `PWR2` - Appareil allumé
  - `PWR0` - Appareil éteint

### Volume
- `VU` - Augmenter le volume
- `VD` - Diminuer le volume
- `?V` - Interroger le niveau de volume actuel
- `VL` - Définir le volume à un niveau spécifique (suivi d'une valeur)

### Sourdine (Mute)
- `MO` - Activer la sourdine
- `MF` - Désactiver la sourdine
- `?M` - Interroger l'état de sourdine

### Source / Canal d'entrée
- `?F` - Interroger la source actuelle
- `FU` - Source suivante
- `FD` - Source précédente
- `%02dFN` - Définir la source (où %02d est un nombre à 2 chiffres)

Sources prédéfinies:
- `00FN` - PHONO
- `01FN` - CD
- `02FN` - TUNER
- `03FN` - CDR/TAPE
- `04FN` - DVD
- `05FN` - TV/SAT
- `10FN` - VIDEO 1
- `12FN` - MULTI CH IN
- `14FN` - VIDEO 2
- `15FN` - DVR/BDR
- `17FN` - iPod/USB
- `18FN` - XM RADIO
- `19FN` - HDMI 1
- `20FN` - HDMI 2
- `21FN` - HDMI 3
- `22FN` - HDMI 4
- `23FN` - HDMI 5
- `25FN` - BD
- `26FN` - HMG (Home Media Gateway)
- `31FN` - HDMI CYCL
- `33FN` - ADAPTER PORT

### Raccourcis rapides pour les tests

| Action | Commande |
|--------|----------|
| CD | `01FN` |
| DVD | `04FN` |
| TV/SAT | `05FN` |
| Blu-ray | `25FN` |
| NET / HMG | `26FN` |
| HDMI 1 | `19FN` |
| Bluetooth / Adapter | `33FN` |

### Modes d'écoute courants

| Mode | Commande |
|------|----------|
| Auto Surround | `0006SR` |
| Direct | `0007SR` |
| Pure Direct | `0008SR` |
| Stereo | `0001SR` |
| Extended Stereo | `0112SR` |
| Advanced Game | `0118SR` |
| THX Cinema | `0056SR` |
| THX Music | `0069SR` |
| Optimum Surround | `0152SR` |
| Eco Mode | `0200SR` |

### Mode d'écoute
- `%04dSR` - Définir le mode d'écoute (où %04d est un nombre à 4 chiffres)
- `?L` - Interroger le mode d'écoute actuel

### Contrôle de tonalité
- `TO1` - Activer le contrôle de tonalité
- `TO0` - Contourner le contrôle de tonalité
- `?TO` - Interroger l'état du contrôle de tonalité

#### Contrôle des basses
- `BI` - Augmenter les basses
- `BD` - Diminuer les basses
- `?BA` - Interroger le niveau des basses

#### Contrôle des aigus
- `TI` - Augmenter les aigus
- `TD` - Diminuer les aigus
- `?TR` - Interroger le niveau des aigus

### Configuration des haut-parleurs
- `%01dSPK` - Configurer les haut-parleurs (où %01d est un chiffre)
- `0SPK` - Tous les haut-parleurs désactivés
- `1SPK` - Haut-parleurs A activés
- `2SPK` - Haut-parleurs B activés
- `3SPK` - Haut-parleurs A et B activés

### Configuration des sorties HDMI
- `%01dHO` - Configurer les sorties HDMI (où %01d est un chiffre)
- `0HO` - Toutes les sorties HDMI
- `1HO` - Sortie HDMI 1
- `2HO` - Sortie HDMI 2

### Configuration audio HDMI
- `0HA` - Audio HDMI via amplificateur
- `1HA` - Audio HDMI en passthrough

### Réglage PQLS (Precision Quartz Lock System)
- `0PQ` - PQLS désactivé
- `1PQ` - PQLS automatique

## Commandes de la Zone 2

### Alimentation Zone 2
- `APO` - Allumer la Zone 2
- `APF` - Éteindre la Zone 2
- `?AP` - Interroger l'état d'alimentation de la Zone 2

### Entrée Zone 2
- `%02dZS` - Définir l'entrée de la Zone 2 (où %02d est un nombre à 2 chiffres)
- `?ZS` - Interroger l'entrée actuelle de la Zone 2

Entrées prédéfinies pour la Zone 2:
- `01ZS` - CD
- `02ZS` - TUNER
- `03ZS` - CDR/TAPE
- `04ZS` - DVD
- `05ZS` - TV/SAT
- `10ZS` - VIDEO 1
- `14ZS` - VIDEO 2
- `15ZS` - DVR/BDR
- `17ZS` - iPod
- `18ZS` - XM RADIO
- `26ZS` - HMG
- `27ZS` - SIRIUS
- `33ZS` - ADAPTER

### Volume Zone 2
- `ZU` - Augmenter le volume de la Zone 2
- `ZD` - Diminuer le volume de la Zone 2
- `%02ZV` ou `ZV` - Définir le volume de la Zone 2
- `?ZV` - Interroger le niveau de volume de la Zone 2

### Sourdine Zone 2
- `Z2MO` - Activer la sourdine de la Zone 2
- `Z2MF` - Désactiver la sourdine de la Zone 2
- `?Z2M` - Interroger l'état de sourdine de la Zone 2

## Commandes de la Zone 3

### Alimentation Zone 3
- `BPO` - Allumer la Zone 3
- `BPF` - Éteindre la Zone 3
- `?BP` - Interroger l'état d'alimentation de la Zone 3

### Entrée Zone 3
- `%02dZT` - Définir l'entrée de la Zone 3 (où %02d est un nombre à 2 chiffres)
- `?ZT` - Interroger l'entrée actuelle de la Zone 3

Entrées prédéfinies pour la Zone 3:
- `01ZT` - CD
- `02ZT` - TUNER
- `03ZT` - CDR/TAPE
- `04ZT` - DVD
- `05ZT` - TV/SAT
- `10ZT` - VIDEO 1
- `14ZT` - VIDEO 2
- `15ZT` - DVR/BDR
- `17ZT` - iPod
- `18ZT` - XM RADIO
- `26ZT` - HMG
- `27ZT` - SIRIUS
- `33ZT` - ADAPTER

### Volume Zone 3
- `YU` - Augmenter le volume de la Zone 3
- `YD` - Diminuer le volume de la Zone 3
- `%02YV` - Définir le volume de la Zone 3
- `?YV` - Interroger le niveau de volume de la Zone 3

### Sourdine Zone 3
- `Z3MO` - Activer la sourdine de la Zone 3
- `Z3MF` - Désactiver la sourdine de la Zone 3
- `?Z3M` - Interroger l'état de sourdine de la Zone 3

## Commandes du tuner radio

- `TFI` - Augmenter la fréquence
- `TFD` - Diminuer la fréquence
- `?FR` - Interroger la fréquence actuelle (AM ou FM)
- `TB` - Changer de bande
- `%01dTP` - Sélectionner une présélection
- `TC` - Changer de classe
- `TPI` - Présélection suivante
- `TPD` - Présélection précédente
- `?TP` - Interroger la présélection actuelle

## Commandes de contrôle iPod

- `00IP` - Lecture
- `01IP` - Pause
- `02IP` - Arrêt
- `03IP` - Précédent
- `04IP` - Suivant
- `05IP` - Retour rapide
- `06IP` - Avance rapide
- `07IP` - Répétition
- `08IP` - Lecture aléatoire
- `09IP` - Affichage
- `10IP` - Contrôle
- `13IP` - Curseur haut
- `14IP` - Curseur bas
- `15IP` - Curseur gauche
- `16IP` - Curseur droit
- `17IP` - Entrée
- `18IP` - Retour
- `19IP` - Menu principal
- `KOF` - Désactiver les touches

## Commandes de l'adaptateur

- `20BT` - Lecture/Pause
- `10BT` - Lecture
- `11BT` - Pause
- `12BT` - Arrêt
- `13BT` - Précédent
- `14BT` - Suivant
- `15BT` - Retour rapide
- `16BT` - Avance rapide

## Commandes Home Media Gateway (HMG)

### Touches numériques
- `%02dNW` - Touche numérique (où %02d est un nombre à 2 chiffres)
- `00NW` à `09NW` - Touches 0 à 9

### Contrôle de la navigation
- `10NW` - Lecture
- `11NW` - Pause
- `12NW` - Précédent
- `13NW` - Suivant
- `18NW` - Affichage
- `20NW` - Arrêt
- `26NW` - Haut
- `27NW` - Bas
- `28NW` - Droite
- `29NW` - Gauche
- `30NW` - Entrée
- `31NW` - Retour
- `32NW` - Programme
- `33NW` - Effacer
- `34NW` - Répétition
- `35NW` - Aléatoire
- `36NW` - Menu
- `37NW` - Édition
- `38NW` - Classe

## Affichage

- `?FL` - Interroger le texte d'information affiché

## Comment utiliser ces commandes

Ces commandes peuvent être envoyées au récepteur Pioneer via une connexion série RS-232 ou via une connexion réseau TCP/IP (pour les modèles compatibles). Généralement, vous devez ajouter un caractère de retour à la ligne (`\r`) à la fin de chaque commande.

Exemple d'utilisation avec un script Python pour envoyer une commande via TCP/IP:

```python
import socket

def send_pioneer_command(command, ip_address="192.168.1.26", port=8102):
    """Envoie une commande au récepteur Pioneer via TCP/IP."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip_address, port))
        s.sendall((command + "\r").encode())
        # Optionnel: attendre une réponse
        response = s.recv(1024)
        return response.decode().strip()

# Exemple: allumer le récepteur
send_pioneer_command("PO")

# Exemple: régler le volume à 50
send_pioneer_command("50VL")

# Exemple: changer la source à HDMI 1
send_pioneer_command("19FN")
```

Note: Les modèles exacts et les commandes supportées peuvent varier selon le modèle de votre récepteur Pioneer. Consultez le manuel de votre appareil pour plus de détails.
