# LED NeoPixel

[Retour à l'accueil](../README.md)

## Objectif

Regrouper les programmes et ressources consacrés aux LED RGB adressables (NeoPixel) avec Raspberry Pi Pico et MicroPython : choix des couleurs, animations et réactions aux mesures de capteurs.

## Laboratoires

| Laboratoire | Contenu | État |
| --- | --- | --- |
| [Labo 4 — LED RGB synchronisée avec la musique](labo04_rgb_musique/) | Microphone analogique, détection adaptative des pics, couleurs aléatoires, estimation des BPM et enregistrement périodique dans un fichier texte | Fonctionnalités principales et BPM validés ; incréments des accumulateurs ajoutés, portée `global` et vérification du fichier encore nécessaires |

Le labo 4 dispose de son propre [compte rendu](labo04_rgb_musique/README.md), qui détaille les branchements, le fonctionnement, les essais réalisés et l'état précis de la correction du second bonus.

## Programmes du labo 4

- [test_rgb.py](labo04_rgb_musique/test_rgb.py) : contrôle successif du rouge, du vert et du bleu.
- [test_micro.py](labo04_rgb_musique/test_micro.py) : acquisition analogique et amplitude du son.
- [test_detection.py](labo04_rgb_musique/test_detection.py) : détection de pics avec seuil adaptatif et réarmement.
- [ex04_rgb_musique.py](labo04_rgb_musique/ex04_rgb_musique.py) : intégration du microphone, de la LED RGB et des deux bonus.

Le matériel utilisé comprend un **Grove Sound Sensor** sur **A1 / GP27** et une **Grove RGB LED WS2813 Mini** sur **D18 / GP18**, avec le Grove Shield du Raspberry Pi Pico. Le programme utilise `neopixel` pour la LED et `ADC` pour le microphone.

## Notions mises en pratique

- Couleurs RGB représentées par un triplet et envoyées à une LED adressable avec `NeoPixel.write()`.
- Lecture d'une entrée analogique grâce à `ADC.read_u16()`.
- Estimation de l'amplitude d'un signal à partir de son minimum et de son maximum.
- Détection de pics sonores avec seuil adaptatif, temporisation et réarmement.
- Mesure des intervalles avec `ticks_ms()` et `ticks_diff()`, puis estimation du BPM.
- Écriture de données sur le Pico avec `with open(..., "a")`.

Le labo concerne aussi le traitement d'un signal de capteur, mais son programme principal est classé ici pour conserver **un seul dossier par laboratoire** et éviter les copies divergentes.

## Ressources

- [Consignes du professeur : LED_neo](https://github.com/hepl-scheen/smartcities/tree/main/LED_neo).
- *Beginner's Guide for Raspberry Pi Pico*, leçon 12 : **Intelligent Light**.
- [Référence du module NeoPixel dans MicroPython](https://docs.micropython.org/en/latest/library/neopixel.html).
- [Documentation du kit Grove](https://wiki.seeedstudio.com/Grove-Starter-Kit-for-Raspberry-Pi-Pico/).
