# Labo 3 — Thermostat

[Retour au thème Capteurs](../README.md) · [Accueil du dépôt](../../README.md)

## Objectif

Réaliser un thermostat avec le Raspberry Pi Pico en MicroPython : régler une température de consigne entre 15 et 35 °C avec un potentiomètre, mesurer la température ambiante et afficher les deux valeurs sur un écran LCD. Une LED et un buzzer signaleront les dépassements définis dans l'énoncé.

Ce dossier regroupera le programme principal du thermostat, les bibliothèques nécessaires et la documentation de son montage. Le programme principal prévu, `thermostat.py`, n'est pas encore créé.

## État d'avancement

| Étape | État |
|---|---|
| Lecture du potentiomètre et calcul de la consigne | Validés sur le matériel ; affichage dans la console de Thonny |
| Lecture du capteur de température | À réaliser ; bibliothèque à confirmer |
| Affichage sur le LCD | Bibliothèques installées ; essai d'affichage à effectuer |
| Comparaison, LED et buzzer | À développer et à tester |
| Mesures au PicoScope des parties 1 et 2 | À réaliser à l'école lorsque l'oscilloscope sera disponible |

## Matériel identifié

- Raspberry Pi Pico et support Grove.
- Potentiomètre connecté au port A0, correspondant à l'entrée analogique GP26.
- Écran **Grove — 16x2 LCD (White on Blue)**.
- Capteur portant l'inscription **Temperature and Humidity Sensor V2.1** : compatibilité du pilote à confirmer lors de l'essai de lecture.
- LED et buzzer pour les alertes ; leurs branchements seront précisés lors de leur intégration.

Les branchements détaillés et les références des bibliothèques seront ajoutés au fur et à mesure des essais.

## Essai préparatoire validé

L'exemple autonome [lecture_consigne.py](../../AD-PWM/lecture_consigne.py) est conservé dans le thème AD-PWM, car il illustre la lecture analogique et la conversion d'une plage de valeurs. Il ne constitue pas encore le programme complet du thermostat.

La lecture `read_u16()` fournit une valeur comprise entre 0 et 65 535. La formule utilisée est :

```python
consigne = 15 + (valeur / 65535) * 20
```

Les essais matériels ont confirmé une variation cohérente de la consigne entre 15 et 35 °C lorsque le potentiomètre tourne. Cette étape a été validée dans la console de Thonny ; elle ne mesure pas encore la température ambiante.

Le futur programme du thermostat intégrera lui-même cette lecture et cette conversion. L'exemple restera une ressource de compréhension, sans devoir être exécuté séparément.

## Prochaines étapes

1. Lire la température du capteur et vérifier la valeur dans Thonny.
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
