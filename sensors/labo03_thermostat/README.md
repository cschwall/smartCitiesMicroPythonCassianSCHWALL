# Labo 3 — Thermostat

[Retour au thème Capteurs](../README.md) · [Accueil du dépôt](../../README.md)

## Objectif

Réaliser un thermostat avec le Raspberry Pi Pico en MicroPython : régler une température de consigne entre 15 et 35 °C avec un potentiomètre, mesurer la température ambiante et afficher les deux valeurs sur un écran LCD. Une LED et un buzzer signaleront les dépassements définis dans l'énoncé.

Ce dossier regroupe le programme principal du thermostat, les bibliothèques nécessaires et la documentation de son montage. Le programme sera enrichi au fil des étapes ; sa version actuelle lit la température ambiante dans la console de Thonny.

## Fichiers

- [thermostat.py](thermostat.py) : programme principal, actuellement consacré à la lecture du capteur de température.
- [dht20.py](dht20.py) : bibliothèque du capteur, également enregistrée à la racine du Pico pour permettre son import.
- [lecture_consigne.py](../../AD-PWM/lecture_consigne.py) : exemple préparatoire conservé dans le thème AD-PWM.

## État d'avancement

| Étape | État |
|---|---|
| Lecture du potentiomètre et calcul de la consigne | Validés sur le matériel ; affichage dans la console de Thonny |
| Communication I2C et lecture du capteur de température | Validées sur le matériel ; affichage dans la console de Thonny |
| Consigne et température dans le même programme | À intégrer et à tester |
| Affichage sur le LCD | Bibliothèques installées ; essai d'affichage à effectuer |
| Comparaison, LED et buzzer | À développer et à tester |
| Mesures au PicoScope des parties 1 et 2 | À réaliser à l'école lorsque l'oscilloscope sera disponible |

## Matériel identifié

- Raspberry Pi Pico et support Grove.
- Potentiomètre connecté au port A0, correspondant à l'entrée analogique GP26.
- Écran **Grove — 16x2 LCD (White on Blue)**.
- Capteur portant l'inscription **Temperature and Humidity Sensor V2.1**, connecté au port I2C0 : SDA sur GP8 et SCL sur GP9. Sa compatibilité avec le pilote DHT20 est validée par l'essai de lecture.
- LED et buzzer pour les alertes ; leurs branchements seront précisés lors de leur intégration.

Le scan I2C a détecté l'adresse `0x38`. Cette adresse confirme la présence d'un appareil sur le bus ; elle ne suffit pas, à elle seule, à identifier précisément son modèle. Les autres branchements seront précisés au fil des essais.

## Lecture de la consigne : essai préparatoire validé

L'exemple autonome [lecture_consigne.py](../../AD-PWM/lecture_consigne.py) est conservé dans le thème AD-PWM, car il illustre la lecture analogique et la conversion d'une plage de valeurs. Il ne constitue pas encore le programme complet du thermostat.

La lecture `read_u16()` fournit une valeur comprise entre 0 et 65 535. La formule utilisée est :

```python
consigne = 15 + (valeur / 65535) * 20
```

Les essais matériels ont confirmé une variation cohérente de la consigne entre 15 et 35 °C lorsque le potentiomètre tourne. Cette étape a été validée séparément dans la console de Thonny ; cet exemple ne mesure pas la température ambiante.

La prochaine version de `thermostat.py` intégrera elle-même cette lecture et cette conversion. L'exemple restera une ressource de compréhension, sans devoir être exécuté séparément.

## Lecture de la température : étape validée

Dans `thermostat.py`, le bus I2C0 est configuré à 100 kHz et le pilote est initialisé avec `DHT20(0x38, i2c)`. À chaque tour de boucle, `capteur.measurements` déclenche une mesure et renvoie un dictionnaire. Le programme vérifie `crc_ok`, puis affiche la température `t` en degrés Celsius, arrondie à une décimale. Une pause d'une seconde espace les lectures ; une mesure dont le contrôle d'intégrité échoue produit un message dans la console.

Pour reproduire l'essai, enregistrer `dht20.py` sur le Pico, ouvrir `thermostat.py` dans Thonny et l'exécuter avec l'interpréteur MicroPython du Pico.

| Essai réalisé | Résultat observé |
|---|---|
| Scan du bus I2C0 | Adresse `0x38` détectée |
| Lecture répétée de la température | Valeurs cohérentes dans la console de Thonny |
| Approche de la main près du capteur | Évolution cohérente de la température affichée |

Ces essais ont été validés sur le matériel. Aucune valeur chiffrée ni mesure d'étalonnage n'a été relevée dans ce compte rendu. La consigne et la température n'ont pas encore été réunies dans le même programme.

## Prochaines étapes

1. Intégrer la lecture du potentiomètre dans `thermostat.py`, puis vérifier ensemble la consigne et la température dans la console.
2. Tester le LCD seul, puis afficher la consigne et la température ambiante.
3. Comparer les deux températures et ajouter le clignotement de la LED, le buzzer et le message d'alarme selon l'énoncé.
4. Tester les transitions entre les états et le retour à la normale.
5. Compléter les branchements, les bibliothèques, les résultats et les éventuelles difficultés dans ce README.

Les parties de mesure au PicoScope permettront de vérifier les signaux PWM et les échanges I2C. Aucun résultat de ces mesures n'est encore disponible ; les observations et captures seront ajoutées après leur réalisation.

## Ressources

- Énoncé du cours SmartCities : *Exercice 3*, parties mesures PWM/I2C et thermostat.
- *Beginner's Guide for Raspberry Pi Pico*, pages imprimées 56–60 (PWM), 76–83 (LCD et I2C) et 86–93 (température et alarme).
- [Consignes générales du professeur](https://github.com/hepl-scheen/smartcities).
- [Documentation du kit Grove pour Raspberry Pi Pico](https://wiki.seeedstudio.com/Grove-Starter-Kit-for-Raspberry-Pi-Pico/).
- [Bibliothèque DHT20 fournie dans les ressources Seeed](https://files.seeedstudio.com/wiki/Grove-Temperature-Humidity-Sensor/dht/DHT20.py).
