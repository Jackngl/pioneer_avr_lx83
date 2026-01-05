# Guide de soumission des icônes au repository Home Assistant Brands

Ce guide explique comment soumettre les icônes de l'intégration Pioneer AVR LX83 au repository [Home Assistant Brands](https://github.com/home-assistant/brands) pour qu'elles soient affichées dans Home Assistant.

## Prérequis

- Un compte GitHub
- Les icônes doivent respecter les spécifications (voir ci-dessous)

## Spécifications des images

### Icon (icône)
- **Format** : PNG
- **Aspect ratio** : 1:1 (carré)
- **Taille normale** : 256x256 pixels ✅ (déjà conforme)
- **Taille hDPI** : 512x512 pixels (à créer : `icon@2x.png`)

### Logo
- **Format** : PNG
- **Aspect ratio** : Landscape (paysage) préféré
- **Taille normale** : Le côté le plus court doit être entre 128-256 pixels
- **Taille hDPI** : Le côté le plus court doit être entre 256-512 pixels

**Note** : Si le logo est identique à l'icône (format carré), vous pouvez ne fournir que les icônes. Le système utilisera automatiquement l'icône comme fallback pour le logo.

## Étape 1 : Préparer les fichiers

Vos fichiers actuels :
- ✅ `icon.png` : 256x256 (conforme)
- ⚠️ `logo.png` : 512x512 (carré, peut être utilisé comme icon@2x)

### Fichiers nécessaires pour la soumission

1. **icon.png** : 256x256 (déjà disponible)
2. **icon@2x.png** : 512x512 (à créer à partir de logo.png ou icon.png)
3. **logo.png** : Format landscape si différent de l'icon (optionnel si identique à l'icon)

## Étape 2 : Forker le repository Home Assistant Brands

1. Allez sur https://github.com/home-assistant/brands
2. Cliquez sur "Fork" en haut à droite
3. Attendez que le fork soit créé

## Étape 3 : Cloner votre fork

```bash
git clone https://github.com/VOTRE_USERNAME/brands.git
cd brands
```

## Étape 4 : Créer le dossier et copier les fichiers

```bash
# Créer le dossier pour votre intégration
mkdir -p custom_integrations/pioneer_avr_lx83

# Copier les fichiers depuis votre projet
cp /Users/jack/Documents/Projets/pionner_AVR-83LX/custom_components/pioneer_avr_lx83/icon.png custom_integrations/pioneer_avr_lx83/
cp /Users/jack/Documents/Projets/pionner_AVR-83LX/custom_components/pioneer_avr_lx83/logo.png custom_integrations/pioneer_avr_lx83/icon@2x.png
```

**Note** : Si votre logo.png est carré (512x512), vous pouvez l'utiliser comme `icon@2x.png`. Si vous avez un vrai logo en format landscape, créez-le séparément.

## Étape 5 : Optimiser les images (recommandé)

Les images doivent être :
- Optimisées pour le web (compression PNG)
- Avec transparence si possible
- Interlacées (progressive) si possible
- Sans bordures blanches/noires inutiles

Vous pouvez utiliser des outils en ligne comme :
- [TinyPNG](https://tinypng.com/) pour la compression
- [RedKetchup Image Resizer](https://redketchup.io/image-resizer) pour le redimensionnement

## Étape 6 : Commit et Push

```bash
git add custom_integrations/pioneer_avr_lx83/
git commit -m "Add icons for pioneer_avr_lx83 integration"
git push origin main
```

## Étape 7 : Créer une Pull Request

1. Allez sur https://github.com/home-assistant/brands
2. GitHub devrait vous proposer de créer une PR depuis votre fork
3. Sinon, cliquez sur "Pull requests" > "New pull request"
4. Sélectionnez votre fork comme source
5. Remplissez le titre : `Add icons for pioneer_avr_lx83 integration`
6. Dans la description, mentionnez :
   ```
   This PR adds icons for the custom integration pioneer_avr_lx83.
   
   Domain: pioneer_avr_lx83
   Repository: https://github.com/Jackngl/pioneer_avr_lx83
   ```
7. Cliquez sur "Create pull request"

## Étape 8 : Attendre la review

Les mainteneurs du repository vont :
1. Vérifier que les images respectent les spécifications
2. Tester que les images s'affichent correctement
3. Merger la PR si tout est OK

Une fois mergé, vos icônes seront disponibles via :
- `https://brands.home-assistant.io/pioneer_avr_lx83/icon.png`
- `https://brands.home-assistant.io/pioneer_avr_lx83/icon@2x.png`

## Utilisation dans Home Assistant

Une fois les icônes disponibles sur brands.home-assistant.io, Home Assistant les utilisera automatiquement pour afficher votre intégration dans l'interface.

## Vérification

Après le merge, vous pouvez vérifier que vos icônes sont disponibles en visitant :
- https://brands.home-assistant.io/pioneer_avr_lx83/icon.png
- https://brands.home-assistant.io/_/pioneer_avr_lx83/icon.png (avec placeholder si manquant)

## Notes importantes

- ⚠️ Les images sont mises en cache pendant 7 jours par les navigateurs
- ⚠️ Le cache Cloudflare est de 24 heures
- ⚠️ Les changements peuvent prendre jusqu'à 1 jour pour être visibles partout
- ✅ Les images doivent être optimisées et sans bordures inutiles
- ✅ Le domaine doit correspondre exactement à celui dans votre `manifest.json`

