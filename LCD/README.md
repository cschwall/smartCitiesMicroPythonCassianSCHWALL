# Affichage LCD

[Retour à l'accueil](../README.md)

## Objectif

Regrouper les exercices d'affichage de texte et de valeurs sur un écran LCD piloté par le Raspberry Pi Pico avec MicroPython.

## État actuel

Le test autonome [test_lcd.py](test_lcd.py) est validé sur le matériel : l'écran affiche **SmartCities** sur la première ligne et **LCD pret** sur la seconde.

L'affichage de la consigne et de la température est également intégré et validé dans le programme du [labo 3 — Thermostat](../sensors/labo03_thermostat/), conservé avec le reste du labo dans le thème `sensors`. Les deux valeurs apparaissent sur les lignes **Set:** et **Ambient:**, avec une décimale, et restent affichées dans la console. En état d'alarme, le mot **ALARM** apparaît sur la première ligne sans masquer les deux températures ; ce comportement a aussi été validé sur le matériel.

## Test de l'écran

L'écran **Grove — 16x2 LCD (White on Blue)** est branché au port I2C1 du support : SDA sur GP6 et SCL sur GP7. Le programme configure ce bus à 400 kHz et utilise la classe `LCD1602` de la bibliothèque `lcd1602.py`.

La bibliothèque [lcd1602.py](../sensors/labo03_thermostat/lcd1602.py) est conservée avec le labo 3 et installée à la racine du Pico pour permettre son import. Cette même bibliothèque sert au test autonome et au thermostat.

Pour reproduire le test, ouvrir `test_lcd.py` dans Thonny, sélectionner l'interpréteur MicroPython du Pico et lancer le programme.

- `lcd.clear()` efface le contenu de l'écran.
- `lcd.setCursor(colonne, ligne)` place le curseur ; les coordonnées commencent à zéro.
- `lcd.print(texte)` écrit à la position choisie.

Le programme écrit les deux lignes une seule fois, puis se termine. Le texte reste affiché ; ce comportement a été confirmé lors de l'essai.

Dans le thermostat, les valeurs sont actualisées dans la boucle de lecture. `clear()` est appelé uniquement à l'initialisation ; chaque nouvelle ligne est complétée par des espaces jusqu'à 16 caractères pour effacer le texte précédent sans effacer tout l'écran à chaque tour. La variation du potentiomètre et l'approche de la main près du capteur ont confirmé la mise à jour cohérente du LCD et de la console.

Le message **ALARM** est actuellement fixe. Ses variantes clignotante et défilante, proposées en bonus dans l'énoncé du labo 3, restent à développer et à tester.

## Organisation du thème

- Chaque labo principalement consacré à l'affichage aura son propre sous-dossier, avec un README, ses programmes et les ressources directement liées.
- L'exemple autonome `test_lcd.py` reste au niveau de ce thème et est relié depuis le README du labo 3.
- Un labo faisant intervenir plusieurs thèmes conserve un seul dossier principal, accessible par des liens depuis les autres thèmes.

Les résultats des prochains essais seront ajoutés au fil de l'avancement.

## Ressources

- [Consignes et exercices du professeur : LCD](https://github.com/hepl-scheen/smartcities/tree/main/LCD)
- [Documentation du kit Grove pour Raspberry Pi Pico](https://wiki.seeedstudio.com/Grove-Starter-Kit-for-Raspberry-Pi-Pico/).
