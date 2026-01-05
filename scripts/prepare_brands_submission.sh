#!/bin/bash

# Script pour préparer les fichiers pour la soumission au repository Home Assistant Brands
# Usage: ./scripts/prepare_brands_submission.sh [chemin_vers_brands_repo]

set -e

DOMAIN="pioneer_avr_lx83"
SOURCE_DIR="custom_components/pioneer_avr_lx83"
BRANDS_REPO="${1:-}"

echo "🚀 Préparation des fichiers pour Home Assistant Brands"
echo "=================================================="
echo ""

# Vérifier que les fichiers source existent
if [ ! -f "${SOURCE_DIR}/icon.png" ]; then
    echo "❌ Erreur: ${SOURCE_DIR}/icon.png introuvable"
    exit 1
fi

if [ ! -f "${SOURCE_DIR}/logo.png" ]; then
    echo "❌ Erreur: ${SOURCE_DIR}/logo.png introuvable"
    exit 1
fi

# Créer icon@2x.png si nécessaire
if [ ! -f "${SOURCE_DIR}/icon@2x.png" ]; then
    echo "📦 Création de icon@2x.png à partir de logo.png..."
    cp "${SOURCE_DIR}/logo.png" "${SOURCE_DIR}/icon@2x.png"
    echo "✅ icon@2x.png créé"
else
    echo "✅ icon@2x.png existe déjà"
fi

# Vérifier les dimensions
echo ""
echo "📏 Vérification des dimensions:"
if command -v sips &> /dev/null; then
    ICON_SIZE=$(sips -g pixelWidth -g pixelHeight "${SOURCE_DIR}/icon.png" 2>/dev/null | grep -E "pixelWidth|pixelHeight" | awk '{print $2}' | tr '\n' 'x' | sed 's/x$//')
    ICON2X_SIZE=$(sips -g pixelWidth -g pixelHeight "${SOURCE_DIR}/icon@2x.png" 2>/dev/null | grep -E "pixelWidth|pixelHeight" | awk '{print $2}' | tr '\n' 'x' | sed 's/x$//')
elif command -v identify &> /dev/null; then
    ICON_SIZE=$(identify -format "%wx%h" "${SOURCE_DIR}/icon.png" 2>/dev/null)
    ICON2X_SIZE=$(identify -format "%wx%h" "${SOURCE_DIR}/icon@2x.png" 2>/dev/null)
else
    ICON_SIZE="(non vérifié)"
    ICON2X_SIZE="(non vérifié)"
fi

echo "  - icon.png: ${ICON_SIZE} (attendu: 256x256)"
echo "  - icon@2x.png: ${ICON2X_SIZE} (attendu: 512x512)"

# Si un chemin vers le repo brands est fourni, copier les fichiers
if [ -n "${BRANDS_REPO}" ] && [ -d "${BRANDS_REPO}" ]; then
    TARGET_DIR="${BRANDS_REPO}/custom_integrations/${DOMAIN}"
    
    echo ""
    echo "📁 Copie des fichiers vers ${TARGET_DIR}..."
    mkdir -p "${TARGET_DIR}"
    cp "${SOURCE_DIR}/icon.png" "${TARGET_DIR}/"
    cp "${SOURCE_DIR}/icon@2x.png" "${TARGET_DIR}/"
    
    # Copier logo.png si différent de icon.png (optionnel)
    if [ -f "${SOURCE_DIR}/logo.png" ]; then
        cp "${SOURCE_DIR}/logo.png" "${TARGET_DIR}/"
    fi
    
    echo "✅ Fichiers copiés dans ${TARGET_DIR}"
    echo ""
    echo "📝 Prochaines étapes:"
    echo "  1. cd ${BRANDS_REPO}"
    echo "  2. git add custom_integrations/${DOMAIN}/"
    echo "  3. git commit -m 'Add icons for ${DOMAIN} integration'"
    echo "  4. git push origin main"
    echo "  5. Créer une Pull Request sur https://github.com/home-assistant/brands"
else
    echo ""
    echo "📝 Pour copier automatiquement vers votre fork du repository brands:"
    echo "  ./scripts/prepare_brands_submission.sh /chemin/vers/votre/fork/brands"
    echo ""
    echo "📋 Fichiers prêts pour la soumission:"
    echo "  - ${SOURCE_DIR}/icon.png"
    echo "  - ${SOURCE_DIR}/icon@2x.png"
    echo "  - ${SOURCE_DIR}/logo.png (optionnel)"
fi

echo ""
echo "✅ Préparation terminée!"
echo ""
echo "📖 Consultez BRANDS_SUBMISSION.md pour les instructions complètes"

