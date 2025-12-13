# Configuration HACS

## État actuel de la validation

Votre intégration passe **6/8 validations HACS** :

- ✅ **Information** : Passé
- ✅ **Description** : Passé
- ✅ **Issues** : Passé
- ✅ **Archived** : Passé
- ✅ **Integration Manifest** : Passé
- ✅ **HACS JSON** : Passé
- ⚠️ **Topics** : Échec (action manuelle requise, voir ci-dessous)
- ⚠️ **Brands** : Échec (optionnel pour les intégrations custom)

## Topics GitHub (optionnel mais recommandé)

Pour améliorer la découvrabilité et passer la validation topics, ajoutez les topics suivants à votre repository GitHub :

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

**Note** : Cette validation est optionnelle. Votre intégration fonctionne parfaitement même si cette validation échoue.

## Brands (optionnel)

L'erreur "brands" est **normale et attendue** pour les intégrations custom. Pour la corriger, il faudrait faire une Pull Request sur le repository [home-assistant/brands](https://github.com/home-assistant/brands), ce qui n'est **pas nécessaire** pour une intégration custom.

Cette validation peut être ignorée en toute sécurité.

## Notes importantes

- ✅ Le fichier `hacs.json` est correct (seulement `name` et `render_readme`)
- ✅ Les informations `domains`, `iot_class`, et `homeassistant` sont dans `manifest.json`
- ✅ Les validations critiques passent toutes
- ⚠️ Les erreurs topics et brands sont **non-bloquantes** pour les intégrations custom

## Conclusion

Votre intégration est **prête pour HACS** ! Les 2 validations qui échouent sont optionnelles et n'empêchent pas l'utilisation de l'intégration via HACS.

