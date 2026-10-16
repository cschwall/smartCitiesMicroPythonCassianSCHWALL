# SmartCities — MicroPython

**Cassian SCHWALL**

Ce dépôt rassemble les programmes, les explications et les ressources des laboratoires de MicroPython réalisés dans le cadre du projet SmartCities. Ces exercices permettent de prendre en main le Raspberry Pi Pico et les composants utiles à la réalisation d'un nichoir connecté.

## Matériel et environnement de travail

- **Raspberry Pi Pico** : carte à microcontrôleur utilisée pour lire des entrées, commander des sorties et interagir avec des composants électroniques.
- **MicroPython** : environnement permettant de programmer le microcontrôleur en Python, notamment avec les fonctions du module `machine`.
- **Thonny** : environnement de développement utilisé pour écrire les programmes et les exécuter sur la carte.
- **Git, GitHub Desktop et GitHub** : outils utilisés pour conserver l'historique des modifications et publier le travail.

Les références précises des composants, les branchements et les bibliothèques utilisées seront documentés avec les exercices concernés.

### Repère de brochage

<img width="1107" height="727" alt="Schéma de brochage" src="https://github.com/user-attachments/assets/dd33bb98-14d3-40ea-8918-4465e0039f57" />

## Organisation du dépôt

Les dossiers sont organisés par thème, conformément au [dépôt de référence du professeur](https://github.com/hepl-scheen/smartcities). Un même dossier peut regrouper plusieurs exercices.

| Dossier | Thèmes abordés | État du contenu dans le dépôt |
| --- | --- | --- |
| [GPIO](GPIO/) | LED, bouton-poussoir et interruptions | Programme du labo 1 disponible à la racine : [ledON.py](ledON.py). Classement et README du thème à compléter. |
| [AD-PWM](AD-PWM/) | Lecture analogique, potentiomètre, PWM, musique et servomoteur | Programme du labo 2 disponible à la racine : [ex02-buzzer.py](ex02-buzzer.py). README de démarrage disponible ; classement du programme à effectuer. |
| [LCD](LCD/) | Affichage LCD et documentation des fonctions de la bibliothèque | Dossier préparé ; programmes et documentation des exercices à intégrer. |
| [LED_neo](LED_neo/) | LED NeoPixel et animations lumineuses | Dossier préparé ; programmes et documentation des exercices à intégrer. |
| [sensors](sensors/) | Température, humidité, luminosité et détection de présence | Dossier préparé ; programmes et documentation des exercices à intégrer. |
| [network](network/) | Accès réseau avec le Raspberry Pi Pico | Dossier préparé ; programmes et documentation des exercices à intégrer. |

Les programmes déjà présents restent pour le moment à la racine. Leur déplacement dans les dossiers thématiques sera effectué dans une étape distincte, en conservant leur historique.

## Documentation des exercices

Chaque dossier thématique contient un `README.md`, à enrichir au fil des laboratoires avec :

1. L'objectif de l'exercice et le comportement attendu.
2. Le matériel utilisé et les branchements, accompagnés d'un schéma ou d'une photo si utile.
3. Les liens vers les programmes et les bibliothèques nécessaires.
4. Les notions et les fonctions MicroPython utilisées.
5. Les essais réalisés, les résultats observés et les difficultés rencontrées.
6. Les ressources consultées : documentation, fiches techniques et supports du cours.

Les contenus prévus sont distingués des programmes déjà intégrés. Les README de démarrage indiquent les informations restant à compléter.

## Suivi du travail

Les commits décrivent des étapes cohérentes : ajout d'un exercice, correction, documentation ou réorganisation. Ils permettent de suivre l'évolution du dépôt au fil du travail.

## Ressources

- [Consignes et organisation attendue par le professeur](https://github.com/hepl-scheen/smartcities).
- [Documentation officielle des cartes Raspberry Pi Pico](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html).
- [Référence MicroPython pour les cartes RP2](https://docs.micropython.org/en/latest/rp2/quickref.html) : sélectionner la version correspondant au firmware utilisé.
- [Thonny](https://thonny.org/).

## Licence

Ce dépôt est distribué sous [licence MIT](LICENSE).
