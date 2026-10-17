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

Les six dossiers thématiques reprennent l'organisation du [dépôt de référence du professeur](https://github.com/hepl-scheen/smartcities). À l'intérieur de ces thèmes, chaque laboratoire possède son propre sous-dossier : son README explique le travail et donne accès aux programmes et aux ressources directement liés au laboratoire.

| Dossier | Thèmes abordés | État du contenu dans le dépôt |
| --- | --- | --- |
| [GPIO](GPIO/) | LED, bouton-poussoir et interruptions | [Labo 1 — LED et bouton-poussoir](GPIO/labo01_led_bouton/) : programme, explications et essais disponibles. |
| [AD-PWM](AD-PWM/) | Lecture analogique, potentiomètre, PWM, musique et servomoteur | [Labo 2 — Volume d'une mélodie](AD-PWM/labo02_buzzer/) : programme, explications et essais disponibles ; bonus bouton inclus. Exemple autonome [lecture_consigne.py](AD-PWM/lecture_consigne.py) validé pour préparer le labo 3. |
| [LCD](LCD/) | Affichage LCD et documentation des fonctions de la bibliothèque | L'affichage prévu pour le [labo 3](sensors/labo03_thermostat/) sera documenté avec le thermostat. |
| [LED_neo](LED_neo/) | LED NeoPixel et animations lumineuses | Dossier préparé ; programmes et documentation des exercices à intégrer. |
| [sensors](sensors/) | Température, humidité, luminosité et détection de présence | [Labo 3 — Thermostat](sensors/labo03_thermostat/) en cours : consigne et température affichées ensemble dans la console et validées ; affichage LCD à réaliser. |
| [network](network/) | Accès réseau avec le Raspberry Pi Pico | Dossier préparé ; programmes et documentation des exercices à intégrer. |

La navigation suit trois niveaux : **accueil du dépôt → thème → laboratoire**. Le README d'un thème sert d'index général ; celui d'un laboratoire contient son compte rendu. Le lien du sous-dossier du laboratoire peut ainsi être transmis au professeur pour accéder au travail correspondant.

Un laboratoire qui mobilise plusieurs thèmes est regroupé dans un seul dossier principal. Les autres thèmes peuvent y renvoyer. Les petits exemples préparatoires autonomes restent dans le thème qui décrit le mieux leur rôle, avec un lien depuis le README du laboratoire concerné : c'est le cas de la lecture de consigne, classée dans AD-PWM et référencée par le labo 3.

## Documentation des exercices

Chaque sous-dossier de laboratoire contient un `README.md`, à enrichir au fil du travail avec :

1. L'objectif de l'exercice et le comportement attendu.
2. Le matériel utilisé et les branchements, accompagnés d'un schéma ou d'une photo si utile.
3. Les liens vers les programmes et les bibliothèques nécessaires.
4. Les notions et les fonctions MicroPython utilisées.
5. Les essais réalisés, les résultats observés et les difficultés rencontrées.
6. Les ressources consultées : documentation, fiches techniques et supports du cours.

Les bibliothèques et les éventuelles photos ou captures seront ajoutées au dossier du laboratoire lorsqu'elles seront nécessaires et disponibles. Les README précisent ce qui a été réalisé, ce qui a été testé et ce qui reste à compléter.

## Suivi du travail

Les commits décrivent des étapes cohérentes : ajout d'un exercice, correction, documentation ou réorganisation. Ils permettent de suivre l'évolution du dépôt au fil du travail.

## Ressources

- [Consignes et organisation attendue par le professeur](https://github.com/hepl-scheen/smartcities).
- [Documentation officielle des cartes Raspberry Pi Pico](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html).
- [Référence MicroPython pour les cartes RP2](https://docs.micropython.org/en/latest/rp2/quickref.html) : sélectionner la version correspondant au firmware utilisé.
- [Thonny](https://thonny.org/).

## Licence

Ce dépôt est distribué sous [licence MIT](LICENSE).
