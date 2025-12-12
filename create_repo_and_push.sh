#!/bin/bash

# Script pour créer automatiquement le dépôt GitHub et pousser le code
USERNAME="jack"
REPO_NAME="pioneer_avr_lx83"
REPO_DESCRIPTION="Home Assistant integration for Pioneer AVR LX83"

echo "🚀 Création automatique du dépôt GitHub..."
echo ""

# Vérifier si un token GitHub est disponible
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  Variable GITHUB_TOKEN non trouvée."
    echo ""
    echo "Pour créer le dépôt automatiquement, vous avez deux options:"
    echo ""
    echo "Option 1: Créer un Personal Access Token"
    echo "  1. Allez sur: https://github.com/settings/tokens"
    echo "  2. Cliquez sur 'Generate new token (classic)'"
    echo "  3. Donnez-lui le nom 'HA Integration'"
    echo "  4. Cochez 'repo' (toutes les permissions repo)"
    echo "  5. Cliquez sur 'Generate token'"
    echo "  6. Copiez le token"
    echo "  7. Exécutez: export GITHUB_TOKEN='votre_token'"
    echo "  8. Relancez ce script"
    echo ""
    echo "Option 2: Créer le dépôt manuellement"
    echo "  1. Allez sur: https://github.com/new"
    echo "  2. Nom: $REPO_NAME"
    echo "  3. Ne cochez rien"
    echo "  4. Créez le dépôt"
    echo "  5. Exécutez: git push -u origin main"
    echo ""
    exit 1
fi

# Créer le dépôt via l'API GitHub
echo "📦 Création du dépôt sur GitHub..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$REPO_NAME\",\"description\":\"$REPO_DESCRIPTION\",\"private\":false}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "201" ]; then
    echo "✅ Dépôt créé avec succès!"
elif [ "$HTTP_CODE" = "422" ]; then
    echo "ℹ️  Le dépôt existe déjà, c'est parfait!"
elif [ "$HTTP_CODE" = "401" ]; then
    echo "❌ Erreur d'authentification. Vérifiez votre token."
    exit 1
else
    echo "❌ Erreur lors de la création: HTTP $HTTP_CODE"
    echo "$BODY"
    exit 1
fi

# Vérifier si le remote existe
if ! git remote get-url origin >/dev/null 2>&1; then
    echo "➕ Configuration du remote..."
    git remote add origin "https://github.com/${USERNAME}/${REPO_NAME}.git"
else
    echo "✅ Remote déjà configuré"
fi

# Pousser le code
echo ""
echo "📤 Poussage du code vers GitHub..."
if git push -u origin main; then
    echo ""
    echo "✅ Succès! Votre code est maintenant sur GitHub:"
    echo "   https://github.com/${USERNAME}/${REPO_NAME}"
    echo ""
    echo "🎉 Prochaines étapes:"
    echo "   1. Allez sur votre dépôt GitHub"
    echo "   2. Créez une release v1.0.0"
    echo "   3. Partagez le lien avec la communauté Home Assistant!"
else
    echo ""
    echo "❌ Erreur lors du push."
    echo "   Vérifiez vos permissions et votre authentification Git."
fi

