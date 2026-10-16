# Labo 1 - Clignotement de LED avec bouton-poussoir

[Retour au thème GPIO](../README.md) · [Accueil du dépôt](../../README.md)

**Programme : [ledON.py](ledON.py)**

## Objectif et consignes

Commander le clignotement d'une LED en fonction du nombre d'appuis sur un bouton :

- Au premier appui, la LED clignote à une fréquence de 0,5 Hz.
- Au deuxième appui, le clignotement devient plus rapide.
- Au troisième appui, la LED s'éteint.

## Matériel et affectation des signaux

Le montage utilise un Raspberry Pi Pico, un module LED, un module bouton-poussoir, des câbles de connexion et une liaison USB avec l'ordinateur.

| Élément | GPIO configuré dans le programme | Configuration |
| --- | --- | --- |
| LED | GP16 | Sortie numérique : `machine.Pin(16, machine.Pin.OUT)` |
| Bouton-poussoir | GP18 | Entrée avec rappel au niveau bas : `machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)` |

Les numéros GPIO identifient les signaux de la carte ; ils ne correspondent pas aux numéros des broches physiques. Une photo du montage pourra compléter ces indications.

## Fonctionnement du programme

Le bouton est lu dans la boucle principale. Un appui est détecté lorsque son état passe de 0 à 1 ; le maintien du bouton enfoncé n'ajoute donc pas de nouvelle pression. Le compteur `nbPressions` détermine le comportement de la LED.

| Nombre d'appuis comptabilisés | Comportement | Temporisation définie dans le code |
| --- | --- | --- |
| 0 | LED éteinte | Aucun clignotement |
| 1 | Clignotement lent à 0,5 Hz | Changement d'état toutes les 1 000 ms |
| 2 | Clignotement rapide à 2,5 Hz | Changement d'état toutes les 200 ms |
| 3 ou plus | LED éteinte | Extinction maintenue |

Une période complète comprend un état allumé et un état éteint. Deux changements d'état espacés de 1 seconde donnent donc une période de 2 secondes, soit 0,5 Hz. Les fréquences du tableau sont calculées à partir du code ; elles ne constituent pas une mesure instrumentée.

Les fonctions `utime.ticks_ms()` et `utime.ticks_diff()` servent à suivre le temps écoulé sans bloquer la boucle pendant toute la durée du clignotement. Le bouton reste ainsi surveillé entre les changements d'état. Une courte pause de 9 ms termine chaque tour de boucle.

Un filtre temporel impose plus de 200 ms entre deux appuis comptabilisés afin de limiter les doubles comptages dus aux rebonds. Cette version utilise une lecture périodique du bouton, sans interruption matérielle.

## Utilisation

1. Préparer le montage avec les signaux indiqués ci-dessus et connecter le Pico à l'ordinateur.
2. Ouvrir `ledON.py` dans Thonny, sélectionner l'interpréteur MicroPython du Pico et lancer le programme.
3. Effectuer trois appuis successifs, en relâchant le bouton entre les appuis et en les espaçant de plus de 200 ms.
4. Observer le passage du clignotement lent au clignotement rapide, puis l'extinction. Le nombre de pressions s'affiche également dans la console.

Après le troisième appui, la LED reste éteinte, y compris lors des appuis suivants. Il faut arrêter puis relancer le programme pour recommencer la séquence.

## Essais et résultats

Les essais matériels ont été réalisés par Cassian. Les étapes demandées ont donné le fonctionnement attendu dès le premier essai, sans difficulté particulière de montage ou d'utilisation signalée.

| Vérification demandée | Résultat rapporté |
| --- | --- |
| Premier appui : clignotement lent | Conforme au comportement attendu |
| Deuxième appui : accélération du clignotement | Conforme au comportement attendu |
| Troisième appui : extinction de la LED | Conforme au comportement attendu |

## Périmètre de cette version

Les exigences principales de l'exercice sont implémentées. Les bonus proposant un effet supplémentaire ou une autre répartition des appuis ne sont pas développés dans cette version. Les futurs exercices utilisant des interruptions seront classés dans un autre sous-dossier du thème [GPIO](../README.md).

## Ressources

- Énoncé du cours : **Exercice 1 - Clignotement de LED avec bouton-poussoir**.
- *Beginner's Guide for Raspberry Pi Pico*, TinkerGen / Seeed Studio : leçon 3, utilisation de la LED et des GPIO ; leçon 5, bouton et signaux numériques, notamment pages imprimées 40 à 45.
- [Référence MicroPython : GPIO et `machine.Pin`](https://docs.micropython.org/en/latest/rp2/quickref.html#pins-and-gpio).
- [Référence MicroPython : fonctions de temps](https://docs.micropython.org/en/latest/library/time.html).
- [Organisation du thème GPIO dans le dépôt du professeur](https://github.com/hepl-scheen/smartcities/tree/main/GPIO).
