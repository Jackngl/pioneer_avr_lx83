identique # Modes Audio Pioneer AVR LX83 - Documentation mise à jour

## Structure des commandes et réponses

### Format des commandes
- **Commande**: `SRxxxx` (où xxxx est un code à 4 chiffres)
- **Terminateur**: `\r` (CR, caractère 0x0D)

### Format des réponses
- **Réponse**: `LMxxxx` (où xxxx est un code hexadécimal à 4 chiffres)
- **Terminateur**: `\r\n`

## Groupes de modes audio

### Modes standards
| Mode | Commande | Réponse | Description |
|------|----------|---------|-------------|
| Stereo | `0001SR` | `LM0001` | Mode stéréo standard |
| Auto Surround / Stream Direct | `0006SR` | `LM0006` | Mode surround automatique / Stream Direct |
| Direct | `0007SR` | `LM0007` | Mode direct |
| Pure Direct | `0008SR` | `LM0008` | Mode direct pur |
| Standard (Dolby/DTS) | `0010SR` | Varie | Standard (Dolby/DTS) - Voir section Dolby |
| Extended Stereo | `0112SR` | `LM020d` | Stéréo étendue |
| Advanced Game | `0118SR` | `LM0208` | Mode jeu avancé |
| Optimum Surround | `0152SR` | Varie | Surround optimal |
| Eco Mode | `0200SR` | Varie | Mode éco |

### Modes THX
| Mode | Commande | Réponse | Description |
|------|----------|---------|-------------|
| THX Cinema | `0101SR` | `LM0101` | Mode THX Cinema |
| THX Music | `0102SR` | `LM0102` | Mode THX Music |
| THX Games | `0103SR` | `LM0103` | Mode THX Games |
| THX Select2 Cinema / Ultra2 Cinema | `0105SR` | `LM0105` | THX Select2 Cinema / Ultra2 Cinema |
| THX Select2 Music / Ultra2 Music | `0106SR` | `LM0106` | THX Select2 Music / Ultra2 Music |
| THX Select2 Games / Ultra2 Games | `0107SR` | `LM0107` | THX Select2 Games / Ultra2 Games |
| THX Surround EX | `0115SR` | `LM0115` | THX Surround EX |

### Modes Dolby Pro Logic
| Mode | Commande | Réponse | Description |
|------|----------|---------|-------------|
| DOLBY PLII MOVIE | `0010SR` (cycle) | `LM0102` | Dolby Pro Logic II Movie |
| DOLBY PLII MUSIC | `0010SR` (cycle) | `LM0104` | Dolby Pro Logic II Music |
| DOLBY PLII GAME | `0010SR` (cycle) | `LM0106` | Dolby Pro Logic II Game |
| DOLBY PRO LOGIC | `0010SR` (cycle) | `LM0107` | Dolby Pro Logic original |
| Neo:6 CINEMA | `0010SR` (cycle) | `LM0108` | DTS Neo:6 Cinema |
| Neo:6 MUSIC | `0010SR` (cycle) | `LM0109` | DTS Neo:6 Music |
| NEURAL SURROUND | `0010SR` (cycle) | `LM010b` | Neural Surround |
| Dolby Surround | `0151SR` | Varie | Dolby Surround (pour les modèles récents Atmos/LX) |

### Modes THX combinés
| Mode | Commande | Réponse | Description |
|------|----------|---------|-------------|
| DOLBY PLII GAME + THX | `0050SR` (cycle) | `LM030c` | Dolby Pro Logic II Game avec THX |
| DOLBY PLII MOVIE + THX | `0050SR` (cycle) | `LM0302` | Dolby Pro Logic II Movie avec THX |
| DOLBY PL + THX CINEMA | `0050SR` (cycle) | `LM0303` | Dolby Pro Logic avec THX Cinema |
| Neo:6 CINEMA + THX | `0050SR` (cycle) | `LM0304` | DTS Neo:6 Cinema avec THX |
| DOLBY PLII MUSIC + THX | `0050SR` (cycle) | `LM0307` | Dolby Pro Logic II Music avec THX |
| Neo:6 MUSIC + THX | `0050SR` (cycle) | `LM0309` | DTS Neo:6 Music avec THX |

### Modes DSP (Digital Sound Processing)
| Mode | Commande | Réponse | Description |
|------|----------|---------|-------------|
| CLASSICAL | `0100SR` (cycle) | `LM020a` | Mode optimisé pour musique classique |
| ROCK/POP | `0100SR` (cycle) | `LM020b` | Mode optimisé pour rock et pop |
| UNPLUGGED | `0100SR` (cycle) | `LM020c` | Mode optimisé pour acoustique/unplugged |
| EXT.STEREO (Extended Stereo) | `0100SR` (cycle) | `LM020d` | Stéréo étendue |
| ACTION | `0100SR` (cycle) | `LM0201` | Mode optimisé pour films d'action |
| DRAMA | `0100SR` (cycle) | `LM0202` | Mode optimisé pour films dramatiques |
| SCI-FI | `0100SR` (cycle) | `LM0203` | Mode optimisé pour science-fiction |
| MONO | `0100SR` (cycle) | `LM0204` | Mode mono |
| ENT.SHOW (Entertainment Show) | `0100SR` (cycle) | `LM0205` | Mode divertissement |
| EXPANDED | `0100SR` (cycle) | `LM0206` | Mode étendu |
| TV SURROUND | `0100SR` (cycle) | `LM0207` | Mode optimisé pour télévision |
| ADVANCED GAME | `0100SR` (cycle) | `LM0208` | Mode jeu avancé |
| SPORTS | `0100SR` (cycle) | `LM0209` | Mode optimisé pour événements sportifs |

## Comportement cyclique des modes

Certains codes de commande fonctionnent de manière cyclique, passant à travers différents sous-modes à chaque envoi répété de la même commande:

### Cycle `SR0010` (Modes Dolby/DTS standards)
1. `DOLBY PLII MOVIE` (LM0102)
2. `DOLBY PLII MUSIC` (LM0104)
3. `DOLBY PLII GAME` (LM0106)
4. `DOLBY PRO LOGIC` (LM0107)
5. `Neo:6 CINEMA` (LM0108)
6. `Neo:6 MUSIC` (LM0109)
7. `NEURAL SURROUND` (LM010b)
8. Retour à 1

### Cycle `SR0050` (Modes Dolby/DTS + THX)
1. `DOLBY PLII GAME + THX` (LM030c)
2. `DOLBY PLII MOVIE + THX` (LM0302)
3. `DOLBY PL + THX CINEMA` (LM0303)
4. `Neo:6 CINEMA + THX` (LM0304)
5. `DOLBY PLII MUSIC + THX` (LM0307)
6. `Neo:6 MUSIC + THX` (LM0309)
7. Retour à 1

### Cycle `SR0100` (Modes DSP)
1. `CLASSICAL` (LM020a)
2. `ROCK/POP` (LM020b)
3. `UNPLUGGED` (LM020c)
4. `EXT.STEREO` (LM020d)
5. `ACTION` (LM0201)
6. `DRAMA` (LM0202)
7. `SCI-FI` (LM0203)
8. `MONO` (LM0204)
9. `ENT.SHOW` (LM0205)
10. `EXPANDED` (LM0206)
11. `TV SURROUND` (LM0207)
12. `ADVANCED GAME` (LM0208)
13. `SPORTS` (LM0209)
14. Retour à 1

## Implications pour l'intégration Home Assistant

Pour l'intégration Home Assistant, il est recommandé de:

1. **Mapper les codes de réponse**: Créer un dictionnaire qui associe les codes `LMxxxx` à des noms de modes d'écoute conviviaux
2. **Gérer les modes cycliques**: Pour les modes qui fonctionnent en cycle, il peut être préférable d'implémenter des services distincts pour chaque sous-mode plutôt que d'utiliser le comportement cyclique
3. **Vérifier l'état actuel**: Interroger l'état actuel (`?L`) avant d'envoyer une commande pour déterminer si plusieurs commandes sont nécessaires pour atteindre le mode souhaité

## Exemple de mise à jour pour le dictionnaire de modes d'écoute

```python
DEFAULT_LISTENING_MODES = {
    # Modes standards
    "Stereo": "0001",
    "Auto Surround": "0006",
    "Direct": "0007",
    "Pure Direct": "0008",
    "Extended Stereo": "0112",
    "Advanced Game": "0118",
    
    # Modes Dolby/DTS
    "Dolby PL II Movie": "0013",  # Commande directe pour PLII Movie
    "Dolby PL II Music": "0014",  # Commande directe pour PLII Music
    "Dolby Surround": "0151",
    
    # Modes THX
    "THX Cinema": "0101",
    "THX Music": "0102",
    "THX Games": "0103",
    "THX Select2 Cinema": "0105",
    "THX Select2 Music": "0106",
    "THX Select2 Games": "0107",
    "THX Surround EX": "0115",
    
    # Modes DSP spécifiques
    "Classical": "0100",  # Utilise le cycle, s'arrête à Classical
    "Rock/Pop": "0100",   # Utilise le cycle, nécessite vérification d'état
    "Action": "0100",     # Utilise le cycle, nécessite vérification d'état
    "Sports": "0100",     # Utilise le cycle, nécessite vérification d'état
}

# Dictionnaire inverse pour les réponses LM
LISTENING_MODE_RESPONSES = {
    "0001": "Stereo",
    "0006": "Auto Surround",
    "0007": "Direct",
    "0008": "Pure Direct",
    "0102": "Dolby PL II Movie",
    "0104": "Dolby PL II Music",
    "0106": "Dolby PL II Game",
    "0107": "Dolby Pro Logic",
    "0108": "Neo:6 Cinema",
    "0109": "Neo:6 Music",
    "010b": "Neural Surround",
    "0101": "THX Cinema",
    "0102": "THX Music",
    "0103": "THX Games",
    "0105": "THX Select2 Cinema",
    "0106": "THX Select2 Music",
    "0107": "THX Select2 Games",
    "0115": "THX Surround EX",
    "020a": "Classical",
    "020b": "Rock/Pop",
    "020c": "Unplugged",
    "020d": "Extended Stereo",
    "0201": "Action",
    "0202": "Drama",
    "0203": "Sci-Fi",
    "0204": "Mono",
    "0205": "Entertainment Show",
    "0206": "Expanded",
    "0207": "TV Surround",
    "0208": "Advanced Game",
    "0209": "Sports",
    "0302": "Dolby PL II Movie + THX",
    "0303": "Dolby PL + THX Cinema",
    "0304": "Neo:6 Cinema + THX",
    "0307": "Dolby PL II Music + THX",
    "0309": "Neo:6 Music + THX",
    "030c": "Dolby PL II Game + THX",
}
```

Cette mise à jour permettra une meilleure gestion des modes d'écoute dans l'intégration Pioneer AVR LX83 pour Home Assistant.