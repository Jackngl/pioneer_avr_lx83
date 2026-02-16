# Pioneer SC-LX83 (2010) : Référence Complète des Modes Audio

Ce document est basé sur des **tests Telnet directs** effectués sur le matériel (192.168.1.26:8102).

---

## 1. Cycle STÉRÉO (Commande `0001SR`)

Chaque appui successif fait défiler :

| Appui | Réponse `LM` | Mode |
| :--- | :--- | :--- |
| 1 | `0001` | **Stéréo** |
| 2 | `0002` | **ALC** (Auto Level Control) |
| 3 | `0003` | **F.S.S.A. Advance** |
| 4 | `0004` | **F.S. Surround** (nouveau !) |
| → retour à 1 | | |

---

## 2. Cycle STANDARD / DOLBY / DTS (Commande `0010SR`)

Chaque appui successif fait défiler :

| Appui | Réponse `LM` | Mode |
| :--- | :--- | :--- |
| 1 | `0102` | **Dolby PL II Movie** |
| 2 | `0104` | **Dolby PL II Music** |
| 3 | `0106` | **Dolby PL II Game** |
| 4 | `0107` | **Dolby Pro Logic** |
| 5 | `0108` | **Neo:6 Cinema** |
| 6 | `0109` | **Neo:6 Music** |
| 7 | `010b` | **Neural Surround** |
| → retour à 1 | | |

**Commandes directes :**
| Mode | Commande | Réponse `LM` |
| :--- | :--- | :--- |
| **PL II Movie** | `0013SR` | `0102` |
| **PL II Music** | `0014SR` | `0104` |
| **PL II Game** | `0015SR` | `0106` |
| **Neo:6 Cinema** | `0011SR` | `0102` |
| **Neo:6 Music** | `0012SR` | `0107` |
| **Dolby Surround** | `0151SR` | `0501` |

---

## 3. Cycle THX COMBINÉ (Commande `0050SR`)

> [!IMPORTANT]
> Il faut **d'abord être en mode Dolby/DTS** (ex: `0013SR`) pour que le cycle THX fonctionne.

Chaque appui successif fait défiler :

| Appui | Réponse `LM` | Mode |
| :--- | :--- | :--- |
| 1 | `0302` | **Dolby PL II Movie + THX** |
| 2 | `0303` | **Dolby PL + THX Cinema** |
| 3 | `0304` | **Neo:6 Cinema + THX** |
| 4 | `0307` | **Dolby PL II Music + THX** |
| 5 | `0309` | **Neo:6 Music + THX** |
| 6 | `030c` | **Dolby PL II Game + THX** |
| → retour à 1 | | |

**Commandes THX directes (sans pré-requis Dolby) :**
| Mode | Commande | Réponse `LM` |
| :--- | :--- | :--- |
| **THX Cinema** | `0051SR` | `0303` |
| **THX Music** | `0052SR` | `0302` |
| **THX Games** | `0053SR` | `0304` |

**Commandes THX Select2 (pré-requis Dolby) :**
| Mode | Commande | Réponse `LM` |
| :--- | :--- | :--- |
| **THX Select2 Cinema** | `0054SR` | `0302` |
| **THX Select2 Music** | `0055SR` | ⚠️ Non confirmé |
| **THX Select2 Games** | `0056SR` | ⚠️ Non confirmé |
| **THX Surround EX** | `0057SR` | ⚠️ Non confirmé |

---

## 4. Cycle DSP / ADVANCED SURROUND (Commande `0100SR`)

Chaque appui successif fait défiler :

| Appui | Réponse `LM` | Mode |
| :--- | :--- | :--- |
| 1 | `0201` | **Action** |
| 2 | `0202` | **Drama** |
| 3 | `0203` | **Sci-Fi** |
| 4 | `0204` | **Mono Film** |
| 5 | `0205` | **Entertainment Show** |
| 6 | `0206` | **Expanded Theater** |
| 7 | `0207` | **TV Surround** |
| 8 | `0208` | **Advanced Game** |
| 9 | `0209` | **Sports** |
| 10 | `020a` | **Classical** |
| 11 | `020b` | **Rock/Pop** |
| 12 | `020c` | **Unplugged** |
| 13 | `020d` | **Extended Stereo** |
| → retour à 1 | | |

**Commandes directes :**
| Mode | Commande | Réponse `LM` |
| :--- | :--- | :--- |
| **Action** | `0101SR` | `0201` |
| **Sci-Fi** | `0102SR` | `0203` |
| **Drama** | `0103SR` | `0202` |
| **Entertainment Show** | `0104SR` | `0205` |
| **TV Surround** | `0105SR` | `0204` |
| **Expanded Theater** | `0106SR` | `0206` |
| **Classical** | `0107SR` | `020a` |
| **Rock/Pop** | `0108SR` | `020b` |
| **Unplugged** | `0109SR` | `020c` |
| **Extended Stereo** | `0112SR` | `020d` |
| **Advanced Game** | `0118SR` | `0208` |

---

## 5. Modes SPÉCIAUX
| Mode | Commande | Réponse `LM` | Status |
| :--- | :--- | :--- | :--- |
| **Auto Surround** | `0006SR` | `040e` | ✅ |
| **Direct** | `0007SR` | `0601` | ✅ |
| **Pure Direct** | `0008SR` | `0701` | ✅ |
| **Optimum Surround** | `0152SR` | `0881` | ✅ |
| **Eco Mode** | `0200SR` | E06 | ❌ Non supporté |

---

## 6. Entrées (Sources)
| Entrée | Commande | Note |
| :--- | :--- | :--- |
| **Phono** | `00FN` | |
| **CD** | `01FN` | |
| **TV/SAT** | `05FN` | |
| **HDMI 1** | `19FN` | |
| **HDMI 2** | `20FN` | |
| **HDMI 3** | `21FN` | |
| **Blu-ray** | `25FN` | |
| **Bluetooth** | `33FN` | Adaptateur AS-BT100 |

---

## 7. Réglages Matériels
| Action | Commande |
| :--- | :--- |
| **Speaker A** | `1SPK` |
| **Speaker B** | `2SPK` |
| **Speaker A+B** | `3SPK` |
| **HDMI OUT 1** | `1HO` |
| **HDMI OUT 2** | `2HO` |
| **HDMI ALL** | `0HO` |

> [!WARNING]
> Les commandes vidéo (VCONV, VRES, VASP) retournent **E04** (non supportées via Telnet). Elles ne sont accessibles que par le menu OSD.