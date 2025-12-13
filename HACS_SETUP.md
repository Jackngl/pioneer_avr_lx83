# Configuration HACS

## Topics GitHub requis

Pour que la validation HACS passe, vous devez ajouter les topics suivants à votre repository GitHub :

1. Allez sur votre repository : https://github.com/Jackngl/pioneer_avr_lx83
2. Cliquez sur l'icône d'engrenage ⚙️ à côté de "About"
3. Dans la section "Topics", ajoutez :
   - `home-assistant`
   - `homeassistant`
   - `hacs`
   - `custom-component`
   - `integration`
   - `pioneer`
   - `avr`
   - `amplifier`

## Validation HACS

Les validations suivantes sont effectuées :

- ✅ **hacs.json** : Format correct (seulement `name` et `render_readme`)
- ⚠️ **Topics** : Doit être configuré manuellement sur GitHub (voir ci-dessus)
- ⚠️ **Brands** : Optionnel pour les intégrations custom (nécessite une PR sur le repo brands de Home Assistant)

## Notes

- Le fichier `hacs.json` ne doit contenir que `name` et `render_readme`
- Les informations `domains`, `iot_class`, et `homeassistant` sont déjà dans `manifest.json`
- Les topics GitHub sont requis pour la validation HACS complète

