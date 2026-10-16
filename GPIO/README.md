# Entrées et sorties numériques — GPIO

[Retour à l'accueil](../README.md)

Ce thème regroupe les exercices sur les entrées et les sorties numériques du Raspberry Pi Pico : LED, boutons-poussoirs et, au fil des travaux, interruptions.

## Laboratoires

| Laboratoire | Contenu | État |
| --- | --- | --- |
| [Labo 1 — LED et bouton-poussoir](labo01_led_bouton/) | Comptage des appuis, clignotement et temporisation sans blocage | Programme et essais documentés ; exigences principales réalisées |

Chaque laboratoire possède un sous-dossier contenant son README, ses programmes et les ressources directement liées au montage. Le README présente les branchements, le fonctionnement et les essais réalisés.

## Notions abordées

- Configurer une broche en entrée ou en sortie avec `machine.Pin`.
- Lire un bouton et détecter un changement d'état.
- Commander une LED et gérer les temporisations.
- Documenter les résultats et les éventuelles difficultés du montage.

Les futurs laboratoires du thème auront leurs propres sous-dossiers. Un petit exemple autonome pourra aussi être conservé ici et référencé depuis les laboratoires qui l'utilisent.

## Ressources

- [Consignes du professeur : GPIO](https://github.com/hepl-scheen/smartcities/tree/main/GPIO).
- [Référence MicroPython : GPIO et `machine.Pin`](https://docs.micropython.org/en/latest/rp2/quickref.html#pins-and-gpio).
- Les ressources spécifiques au premier laboratoire sont regroupées dans [son README](labo01_led_bouton/README.md).
