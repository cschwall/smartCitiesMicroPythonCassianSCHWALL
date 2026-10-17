# Labo 3 — Thermostat

[Retour au thème Capteurs](../README.md) · [Accueil du dépôt](../../README.md)

## Objectif

Réaliser un thermostat avec le Raspberry Pi Pico en MicroPython : régler une température de consigne entre 15 et 35 °C avec un potentiomètre, mesurer la température ambiante et afficher les deux valeurs sur un écran LCD. Une LED et un buzzer signalent les dépassements définis dans l'énoncé.

Ce dossier regroupe le programme principal du thermostat, les bibliothèques nécessaires et la documentation de son montage. Les exigences principales de la partie 3 ont été validées fonctionnellement sur le matériel : lectures, affichage, signalement du dépassement et alarme avec buzzer, LED accélérée et message **ALARM**. Le bonus de luminosité progressive a ensuite été intégré et validé sur le montage complet. Les deux bonus d'affichage restent facultatifs ; les mesures au PicoScope des parties 1 et 2 seront réalisées à l'école.

## Fichiers

- [thermostat.py](thermostat.py) : programme principal, réunissant les lectures, l'affichage, la comparaison des températures et les trois états du thermostat.
- [dht20.py](dht20.py) : bibliothèque du capteur, également enregistrée à la racine du Pico pour permettre son import.
- [lcd1602.py](lcd1602.py) : bibliothèque de l'écran LCD, également enregistrée à la racine du Pico ; utilisée par le thermostat et le test autonome.
- [lecture_consigne.py](../../AD-PWM/lecture_consigne.py) : exemple préparatoire conservé dans le thème AD-PWM.
- [test_lcd.py](../../LCD/test_lcd.py) : test autonome d'affichage, conservé dans le thème LCD et validé sur le matériel.
- [test_led_progressive.py](../../AD-PWM/test_led_progressive.py) : test autonome de luminosité progressive, conservé dans le thème AD-PWM et validé sur le matériel.

## État d'avancement

| Étape | État |
|---|---|
| Lecture du potentiomètre et calcul de la consigne | Validés sur le matériel ; affichage dans la console de Thonny |
| Communication I2C et lecture du capteur de température | Validées sur le matériel ; affichage dans la console de Thonny |
| Consigne et température dans le même programme | Validées sur le matériel ; affichage simultané dans la console de Thonny |
| Test du LCD seul | Validé sur le matériel ; deux lignes de texte affichées |
| Consigne et température sur le LCD | Validées sur le matériel ; affichage sur deux lignes et dans la console |
| Comparaison des températures et clignotement lent de la LED | Validés fonctionnellement sur le matériel ; fréquence nominale prévue de 0,5 Hz, non mesurée au PicoScope |
| Alarme au-delà de la consigne + 3 °C : buzzer, LED accélérée et message | Validés fonctionnellement sur le matériel, ainsi que les retours entre les trois états ; fréquence nominale de la LED prévue de 2,5 Hz |
| Test autonome de luminosité progressive de la LED | Validé sur le matériel ; montée et descente de luminosité observées |
| Bonus : luminosité progressive intégrée au thermostat | Validé sur le montage complet ; fonctionnement conservé avec variation progressive de la LED |
| Bonus : ALARM clignotant et ALARM défilant | Non implémentés |
| Mesures au PicoScope des parties 1 et 2 | À réaliser à l'école lorsque l'oscilloscope sera disponible |

## Matériel identifié

- Raspberry Pi Pico et support Grove.
- Potentiomètre connecté au port A0, correspondant à l'entrée analogique GP26.
- Écran **Grove — 16x2 LCD (White on Blue)**, connecté au port I2C1 : SDA sur GP6 et SCL sur GP7.
- Capteur portant l'inscription **Temperature and Humidity Sensor V2.1**, connecté au port I2C0 : SDA sur GP8 et SCL sur GP9. Sa compatibilité avec le pilote DHT20 est validée par l'essai de lecture.
- Module LED connecté au port D16, correspondant à GP16 ; branchement validé sur le matériel. La version actuelle utilise un PWM à 1 000 Hz pour faire varier sa luminosité.
- Buzzer connecté au port D18, correspondant à GP18 ; pilotage en PWM à 2 000 Hz et rapport cyclique d'environ 50 % pendant l'alarme, puis rapport cyclique nul pour le silence.

Le scan I2C a détecté l'adresse `0x38`. Cette adresse confirme la présence d'un appareil sur le bus ; elle ne suffit pas, à elle seule, à identifier précisément son modèle.

## Lecture de la consigne : essai préparatoire validé

L'exemple autonome [lecture_consigne.py](../../AD-PWM/lecture_consigne.py) est conservé dans le thème AD-PWM, car il illustre la lecture analogique et la conversion d'une plage de valeurs. Il ne constitue pas encore le programme complet du thermostat.

La lecture `read_u16()` fournit une valeur comprise entre 0 et 65 535. La formule utilisée est :

```python
consigne = 15 + (valeur / 65535) * 20
```

Les essais matériels ont confirmé une variation cohérente de la consigne entre 15 et 35 °C lorsque le potentiomètre tourne. Cette étape a été validée séparément dans la console de Thonny ; cet exemple ne mesure pas la température ambiante.

La lecture et la conversion sont désormais intégrées à `thermostat.py`. L'exemple reste une ressource de compréhension, sans devoir être exécuté séparément.

## Consigne et température : fonctionnement et essais validés

Dans `thermostat.py`, le bus I2C0 est configuré à 100 kHz et le pilote est initialisé avec `DHT20(0x38, i2c)`. Le programme lit le potentiomètre, calcule la consigne, puis `capteur.measurements` déclenche une mesure et renvoie un dictionnaire. Le programme vérifie `crc_ok`, puis affiche dans la console l'état, la consigne et la température `t`, en degrés Celsius et arrondies à une décimale. Les lectures et l'affichage sont regroupés dans un bloc déclenché environ chaque seconde ; cette cadence n'a pas été mesurée à l'oscilloscope.

Pour reproduire l'essai avec l'affichage actuel, enregistrer `dht20.py` et `lcd1602.py` à la racine du Pico, garder les branchements indiqués ci-dessus, puis ouvrir `thermostat.py` dans Thonny et l'exécuter avec l'interpréteur MicroPython du Pico.

| Essai réalisé | Résultat observé |
|---|---|
| Scan du bus I2C0 | Adresse `0x38` détectée |
| Lecture répétée de la température | Valeurs cohérentes dans la console de Thonny |
| Approche de la main près du capteur | Évolution cohérente de la température affichée |
| Lecture simultanée du potentiomètre et du capteur | Consigne entre 15 et 35 °C et température ambiante affichées ensemble ; comportement cohérent des deux lectures |

Ces essais ont été validés sur le matériel. Aucune valeur chiffrée ni mesure d'étalonnage n'a été relevée dans ce compte rendu. Le traitement d'une erreur de contrôle d'intégrité est prévu dans le code, mais n'a pas fait l'objet d'un essai provoqué.

## Affichage LCD : test autonome et intégration validés

Le test autonome [test_lcd.py](../../LCD/test_lcd.py) initialise l'écran sur le bus I2C1 à 400 kHz avec la bibliothèque `lcd1602.py`, efface son contenu, puis écrit **SmartCities** sur la première ligne et **LCD pret** sur la seconde. Ces deux lignes se sont affichées correctement lors de l'essai matériel.

La bibliothèque [lcd1602.py](lcd1602.py) est installée sur le Pico et conservée dans ce dossier. Le [README du thème LCD](../../LCD/README.md) décrit le branchement et les fonctions utilisées dans le test autonome.

Dans `thermostat.py`, un deuxième objet I2C initialise l'écran sur I2C1, tandis que le capteur reste sur I2C0. Le programme affiche **Set:** suivi de la consigne sur la première ligne et **Ambient:** suivi de la température ambiante sur la seconde, avec une décimale. L'unité `C` est affichée en fonctionnement normal ; en alarme, **ALARM** remplace cette unité sur la première ligne, tout en conservant les deux valeurs visibles. Elles restent également affichées dans la console.

`lcd.clear()` est appelé au démarrage uniquement. À chaque actualisation, `(texte + " " * 16)[:16]` complète la ligne avec des espaces jusqu'à 16 caractères et limite sa longueur à celle de l'écran. Cela efface les anciens caractères sans effacer tout l'écran à chaque tour. Si le contrôle d'intégrité du capteur échoue, le code prévoit le texte **Erreur capteur** sur la seconde ligne ; ce cas n'a pas fait l'objet d'un essai provoqué.

| Essai réalisé | Résultat observé |
|---|---|
| Exécution du thermostat avec le LCD | Consigne et température ambiante affichées correctement sur deux lignes et dans la console |
| Rotation du potentiomètre | Variation cohérente de la consigne, visible sur le LCD et dans la console |
| Approche de la main près du capteur | Évolution cohérente de la température ambiante, visible sur le LCD et dans la console |

Ces essais ont été validés sur le matériel. Les résultats sont décrits sans ajouter de valeurs chiffrées non relevées.

## États du thermostat et essais

La température ambiante `T` est comparée à la consigne `C`. Le seuil d'alarme est testé en premier, car une température supérieure à `C + 3` dépasse aussi simplement `C`.

| Condition | État | LED | Buzzer et affichage |
|---|---|---|---|
| `T <= C` | NORMAL | Éteinte | Buzzer silencieux ; deux températures visibles |
| `C < T <= C + 3` | DEPASSEMENT | Battement progressif lent, période nominale de 2 000 ms (0,5 Hz) | Buzzer silencieux ; deux températures visibles |
| `T > C + 3` | ALARM | Battement progressif rapide, période nominale de 400 ms (2,5 Hz) | Buzzer actif ; **ALARM** fixe sur la première ligne, avec les deux températures toujours visibles |

Dans la version précédemment validée, `led.toggle()` inversait l'état de la LED après un intervalle de 1 000 ms ou de 200 ms : deux basculements formaient une période complète. La version actuelle remplace ce fonctionnement tout ou rien par une variation progressive du rapport cyclique ; les conditions des trois états, le buzzer et l'affichage restent identiques.

`etat_precedent` permet de mettre à jour les sorties lors d'une transition : le buzzer sonne uniquement dans l'état ALARM et le rythme de la LED redémarre à chaque changement d'état.

| Essai réalisé | Résultat observé |
|---|---|
| Passage à l'état NORMAL en réglant la consigne | LED éteinte et buzzer silencieux |
| Passage à l'état DEPASSEMENT | Clignotement lent de la LED et buzzer silencieux |
| Passage à l'état ALARM | LED accélérée, buzzer actif et message **ALARM** sur le LCD |
| Retour ALARM → DEPASSEMENT → NORMAL | Arrêt du buzzer dès la sortie d'alarme, retour au clignotement lent puis extinction ; LCD et console toujours actualisés |

L'ensemble de ces comportements a d'abord été confirmé sur le matériel dans la version à clignotement tout ou rien. Après l'intégration de la luminosité progressive, l'essai du montage complet a confirmé le maintien du fonctionnement du thermostat avec la nouvelle variation de la LED. Les seuils exacts à l'égalité n'ont pas fait l'objet de relevés chiffrés : le tableau décrit les conditions du programme.

Si le contrôle `crc_ok` échoue, le code prévoit l'état ERREUR, le texte **Erreur capteur**, l'extinction de la LED et le silence du buzzer. Le bloc `finally` prévoit également l'arrêt des deux sorties lors d'une interruption du programme. Ces deux cas n'ont pas fait l'objet d'essais provoqués.

## Bonus PWM : test autonome et intégration validés

Le test autonome [test_led_progressive.py](../../AD-PWM/test_led_progressive.py) fait monter puis descendre le rapport cyclique de la LED sur GP16, avec des boucles `for` et de courtes pauses. Le battement progressif a été observé sur le matériel ; sa période complète est prévue à environ deux secondes, sans mesure au PicoScope.

Dans `thermostat.py`, le signal PWM est fixé à 1 000 Hz. Cette fréquence commande rapidement la LED ; la variation plus lente de son rapport cyclique produit le battement visible. Le programme utilise un cycle de 2 000 ms en DEPASSEMENT et de 400 ms en ALARM. En NORMAL ou ERREUR, le rapport cyclique reste nul.

L'intégration utilise `ticks_ms()` et `ticks_diff()` pour ajouter le temps écoulé à `phase_led`. Le modulo ramène cette phase dans la période choisie ; un calcul triangulaire fait ensuite monter puis descendre la commande lumineuse entre 0 et 65 535. Il n'y a pas de boucle `for` attendant la fin du battement : la boucle principale continue de gérer les lectures, le LCD et les changements d'état, avec une courte pause de 10 ms. Les échanges avec le capteur et l'écran peuvent toutefois espacer les mises à jour de la LED ; les périodes indiquées restent nominales.

Le buzzer reste à 2 000 Hz pendant ALARM et le message **ALARM** reste fixe sur le LCD. Les bibliothèques n'ont pas changé. Le bloc `finally` coupe les sorties et désactive le PWM de la LED à l'interruption.

L'essai du montage complet a confirmé une variation progressive de la luminosité et un fonctionnement cohérent avec la version précédente. Cette validation est fonctionnelle : aucune période ni courbe de luminosité n'a été mesurée au PicoScope.

## Mise au point

Lors de l'intégration par modifications successives, l'oubli de `ADC` dans l'import a provoqué une erreur `NameError`. L'import a été complété ; un caractère superflu et un doublon dans l'affichage ont également été corrigés. Après correction, l'exécution et l'affichage des deux valeurs ont été validés sur le matériel.

Une relecture après l'ajout de la LED a repéré un défaut d'indentation : les lectures et l'affichage restaient exécutés à chaque tour. La correction a été appliquée lors de l'ajout de l'alarme : ces opérations se trouvent désormais dans la condition des 1 000 ms. Le fonctionnement global a ensuite été validé sur le matériel, sans mesure précise des temporisations.

## Travail restant pour le labo 3

1. Réaliser à l'école les mesures au PicoScope des parties 1 et 2 sur les signaux PWM et les échanges I2C, puis ajouter les observations et captures.
2. Si souhaité, réaliser les deux bonus d'affichage : message **ALARM** clignotant, puis défilant.
3. Compléter ce compte rendu avec une photo du montage ou des relevés d'essais lorsqu'ils seront disponibles.

La partie 3 principale et le bonus de luminosité progressive sont terminés et validés fonctionnellement sur le matériel. Aucun résultat des mesures PicoScope n'est encore disponible. Les bonus LCD ne sont pas nécessaires pour commencer l'exercice 4.

## Ressources

- Énoncé du cours SmartCities : *Exercice 3*, parties mesures PWM/I2C et thermostat.
- *Beginner's Guide for Raspberry Pi Pico*, pages imprimées 56–60 (PWM), 76–83 (LCD et I2C) et 86–93 (température et alarme).
- [Consignes générales du professeur](https://github.com/hepl-scheen/smartcities).
- [Documentation du kit Grove pour Raspberry Pi Pico](https://wiki.seeedstudio.com/Grove-Starter-Kit-for-Raspberry-Pi-Pico/).
- [Bibliothèque DHT20 fournie dans les ressources Seeed](https://files.seeedstudio.com/wiki/Grove-Temperature-Humidity-Sensor/dht/DHT20.py).
