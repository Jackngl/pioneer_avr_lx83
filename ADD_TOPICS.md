# Ajouter les Topics GitHub

## Méthode 1 : Script automatique (recommandé)

### Prérequis
1. Un token GitHub avec les permissions `public_repo`
2. Le script `scripts/add_github_topics.sh`

### Obtenir un token GitHub
1. Allez sur : https://github.com/settings/tokens/new
2. Donnez un nom (ex: "Add Topics")
3. Sélectionnez la portée : **`public_repo`**
4. Cliquez sur "Generate token"
5. **Copiez le token** (vous ne le reverrez plus !)

### Exécuter le script

**Option A - Variable d'environnement :**
```bash
export GITHUB_TOKEN='votre_token_ici'
./scripts/add_github_topics.sh
```

**Option B - Fichier de configuration :**
```bash
echo 'votre_token_ici' > ~/.github_token
./scripts/add_github_topics.sh
```

**Option C - Fichier local :**
```bash
echo 'votre_token_ici' > .github_token
./scripts/add_github_topics.sh
```

## Méthode 2 : Via l'interface GitHub (manuelle)

1. Allez sur : https://github.com/Jackngl/pioneer_avr_lx83
2. Cliquez sur l'icône d'engrenage ⚙️ à côté de "About"
3. Dans la section "Topics", ajoutez un par un :
   - `home-assistant`
   - `homeassistant`
   - `hacs`
   - `custom-component`
   - `integration`
   - `pioneer`
   - `avr`
   - `amplifier`
   - `home-automation`
   - `iot`
4. Cliquez sur "Save changes"

## Méthode 3 : Via l'API GitHub avec curl

Si vous avez un token GitHub :

```bash
export GITHUB_TOKEN='votre_token_ici'

curl -X PUT \
  -H "Accept: application/vnd.github.mercy-preview+json" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "names": [
      "home-assistant",
      "homeassistant",
      "hacs",
      "custom-component",
      "integration",
      "pioneer",
      "avr",
      "amplifier",
      "home-automation",
      "iot"
    ]
  }' \
  https://api.github.com/repos/Jackngl/pioneer_avr_lx83/topics
```

## Topics qui seront ajoutés

- `home-assistant` - Pour la communauté Home Assistant
- `homeassistant` - Alternative de recherche
- `hacs` - Pour HACS
- `custom-component` - Type de composant
- `integration` - Type d'intégration
- `pioneer` - Marque
- `avr` - Type d'appareil
- `amplifier` - Type d'appareil
- `home-automation` - Catégorie
- `iot` - Catégorie

## Vérification

Après avoir ajouté les topics, vérifiez sur :
https://github.com/Jackngl/pioneer_avr_lx83

Les topics devraient apparaître dans la section "About" du repository.

