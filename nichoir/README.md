# Nichoir connecté — Développement final

Ce dossier regroupe la réalisation finale du projet **SmartCities 2026–2027**, distincte des laboratoires introductifs conservés à la racine du dépôt.

## Architecture envisagée
- **[ESP32 / TimerCam](esp32/)** : capteur PIR, photographie, éclairage IR, mesure de batterie, gestion d'énergie et communication MQTT.
- **[Raspberry Pi](raspberry/)** : réception des messages MQTT, stockage des données dans MariaDB et interface Web Flask.
- **[Hardware](hardware/)** : câblage, composants, schémas et intégration physique.
- **[Tests](tests/)** : validations fonctionnelles, essais énergétiques et fiabilité.
- **[Documentation](docs/)** : architecture, choix techniques et éléments utiles au rapport.

## État d'avancement
Structure initiale uniquement. Les programmes existants seront intégrés et vérifiés avant de déclarer les fonctions opérationnelles.

## Méthode de collaboration
Créer une branche par fonctionnalité, réaliser des commits explicites, puis proposer une Pull Request vers `main`. Ne pas versionner les identifiants Wi-Fi/MQTT/MariaDB, les fichiers `.env`, ni les images capturées ou données personnelles.
