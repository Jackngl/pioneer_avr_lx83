# Guide de publication sur GitHub

## Étape 1 : Créer le dépôt sur GitHub

1. Allez sur [GitHub](https://github.com)
2. Cliquez sur le bouton "+" en haut à droite
3. Sélectionnez "New repository"
4. Nommez-le : `pioneer_avr_lx83`
5. **Ne cochez PAS** "Initialize with README" (on a déjà tout)
6. Cliquez sur "Create repository"

## Étape 2 : Connecter votre dépôt local

```bash
git remote add origin https://github.com/VOTRE_USERNAME/pioneer_avr_lx83.git
```

Remplacez `VOTRE_USERNAME` par votre nom d'utilisateur GitHub.

## Étape 3 : Pousser le code

```bash
git push -u origin main
```

## Étape 4 : Mettre à jour les URLs dans les fichiers

Après avoir créé le dépôt, mettez à jour ces fichiers avec votre URL GitHub :

1. **manifest.json** : ligne 6
   ```json
   "documentation": "https://github.com/VOTRE_USERNAME/pioneer_avr_lx83",
   ```

2. **manifest.json** : ligne 9
   ```json
   "issue_tracker": "https://github.com/VOTRE_USERNAME/pioneer_avr_lx83/issues",
   ```

3. **README.md** : toutes les URLs contenant `jack/pioneer_avr_lx83`

## Étape 5 : Créer une release

1. Bumper la version localement :
   ```bash
   ./scripts/bump_version.py 1.0.1
   git add VERSION CHANGELOG.md custom_components/pioneer_avr_lx83/manifest.json
   git commit -m "chore: prepare v1.0.1"
   ```
2. Créez et poussez le tag :
   ```bash
   git tag -a v1.0.1 -m "Release v1.0.1"
   git push origin main --tags
   ```
3. Le workflow `.github/workflows/release.yml` publiera automatiquement la release GitHub (HACS détectera alors la version `1.0.1` au lieu d'un hash).

## Étape 6 : Ajouter à HACS (optionnel)

Les utilisateurs pourront installer votre intégration via HACS en ajoutant :
- Repository: `https://github.com/VOTRE_USERNAME/pioneer_avr_lx83`
- Category: Integration

## Commandes Git utiles

```bash
# Voir l'état
git status

# Ajouter des fichiers modifiés
git add .

# Créer un commit
git commit -m "Description des changements"

# Pousser vers GitHub
git push

# Créer une nouvelle branche
git checkout -b feature/nouvelle-fonctionnalite
```
