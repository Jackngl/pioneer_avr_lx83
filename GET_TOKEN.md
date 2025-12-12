# 🔑 Obtenir un Token GitHub (30 secondes)

## Méthode rapide :

1. **Allez sur** : https://github.com/settings/tokens/new
2. **Note** : Donnez un nom (ex: "HA Integration")
3. **Expiration** : Choisissez (90 jours recommandé)
4. **Permissions** : Cochez **`repo`** (toutes les permissions repo)
5. **Cliquez** : "Generate token"
6. **Copiez** le token (vous ne le reverrez plus!)

## Ensuite, exécutez :

```bash
export GITHUB_TOKEN='collez_votre_token_ici'
python3 create_repo.py
```

**OU** pour le sauvegarder :

```bash
echo 'votre_token' > ~/.github_token
python3 create_repo.py
```

---

## Alternative : Création manuelle (2 minutes)

Si vous préférez créer le dépôt manuellement :

1. Allez sur : https://github.com/new
2. Nom : `pioneer_avr_lx83`
3. Ne cochez **RIEN**
4. Créez le dépôt
5. Exécutez : `git push -u origin main`

