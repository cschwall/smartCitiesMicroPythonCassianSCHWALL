# Labo 4 — LED RGB synchronisée avec la musique

[Retour au thème LED NeoPixel](../README.md) · [Accueil du dépôt](../../README.md)

## Objectif

Développer en MicroPython un programme qui lit le signal d'un microphone branché sur un Raspberry Pi Pico, repère les pics d'intensité sonore et change aléatoirement la couleur d'une LED RGB à chaque pic détecté. Les deux bonus demandent d'estimer le rythme en battements par minute (BPM) puis de sauvegarder la moyenne des BPM estimés toutes les 60 secondes dans un fichier texte sur le Pico.

Ce laboratoire utilise la LED adressable Grove RGB (WS2813 Mini), pilotée avec le module `neopixel` de MicroPython. La détection repose sur des pics d'amplitude ; elle ne constitue pas une analyse musicale complète du tempo.

## Fichiers

| Fichier | Rôle |
| --- | --- |
| [test_rgb.py](test_rgb.py) | Test autonome : rouge, vert et bleu pendant une seconde chacun, puis extinction. |
| [test_micro.py](test_micro.py) | Lecture analogique du microphone ; affichage du minimum, du maximum et de l'amplitude de 100 échantillons. |
| [test_detection.py](test_detection.py) | Essai autonome du seuil adaptatif, du délai minimal entre deux pics et du réarmement. |
| [ex04_rgb_musique.py](ex04_rgb_musique.py) | Programme principal : détection des pics, couleurs aléatoires, estimation des BPM et écriture périodique dans `bpm.txt`. |

Les programmes de test sont conservés pour documenter le développement progressif. Les paramètres des tests intermédiaires ne sont pas nécessairement identiques à ceux du programme principal.

## Matériel et branchements

- Raspberry Pi Pico équipé d'un Grove Shield, programmé en MicroPython dans Thonny.
- **Grove Sound Sensor** : port **A1**, entrée analogique **GP27**.
- **Grove RGB LED (WS2813 Mini)** : port **D18**, signal de commande **GP18**.
- Câbles Grove et câble USB pour relier le Pico à l'ordinateur.

Le microphone fournit une tension analogique lue par l'ADC du Pico. La LED RGB, adressable, reçoit les couleurs au format `(rouge, vert, bleu)` via `NeoPixel(Pin(18), 1)`. Les connexions ont été validées lors des tests fonctionnels. Lors des modifications du montage, débrancher l'alimentation USB et veiller à ne pas appliquer de tension supérieure à 3,3 V sur une entrée analogique du Pico.

## Méthode et fonctionnement

### 1. Test de la LED

`test_rgb.py` utilise le module `neopixel` pour afficher successivement les trois couleurs primaires. `led[0]` désigne la LED du module, et `led.write()` transmet la nouvelle couleur. Les composantes lumineuses sont limitées ici à 40 sur une échelle de 0 à 255.

**Observation :** les couleurs rouge, verte et bleue se sont affichées dans l'ordre attendu ; la LED s'est éteinte après l'essai.

### 2. Lecture du microphone

`test_micro.py` réalise 100 lectures successives avec `ADC.read_u16()` et calcule :

```python
amplitude = valeur_max - valeur_min
```

`read_u16()` renvoie une valeur numérique de 0 à 65 535. L'amplitude calculée est un indicateur des variations du signal pendant la fenêtre d'acquisition ; ce n'est ni un niveau sonore calibré en décibels, ni une mesure fréquentielle.

**Observation :** les valeurs suivaient les variations du son lors de trois essais : silence, claquements de mains et musique.

### 3. Détection des pics sonores

Le programme principal prélève une fenêtre de **40 mesures**, espacées nominalement de **1 ms**, et calcule son amplitude. Lors du démarrage, il réalise 30 fenêtres de mesures pour initialiser une moyenne de référence.

Le seuil de détection est adaptatif :

```python
seuil = max(500, moyenne * 1.3)
moyenne = 0.95 * moyenne + 0.05 * amplitude
```

Une détection est acceptée si l'amplitude dépasse le seuil, si l'algorithme est armé et si au moins **300 ms** se sont écoulées depuis le précédent pic accepté. Après une détection, il attend que l'amplitude redescende sous **80 % du seuil** avant de se réarmer. Ces précautions limitent les détections multiples, sans les éliminer dans tous les cas.

Le fichier préparatoire `test_detection.py` utilise pour sa part ses propres réglages (facteur 1,4 et délai 50 ms dans la version conservée) ; les valeurs ci-dessus correspondent au programme principal publié.

**Observation :** les pics ont été correctement reconnus lors de claquements espacés et d'une musique présentant des basses marquées.

### 4. Changement de couleur

Lorsqu'un pic valide est détecté, `changer_couleur()` choisit aléatoirement l'une des huit couleurs prédéfinies. Un nouveau tirage est effectué si la couleur choisie est identique à la précédente : chaque détection provoque ainsi un changement visible. La LED conserve sa couleur entre deux pics et est éteinte dans le bloc `finally` lorsque le programme s'arrête normalement par interruption.

**Observation :** la LED changeait de couleur lors des claquements et suivait approximativement les impulsions de la musique, sans perturber la détection.

## Bonus 1 — Estimation des BPM

`calculer_bpm(maintenant)` mesure le temps entre deux pics consécutifs reconnus à l'aide de `ticks_ms()` et `ticks_diff()` :

```text
BPM = 60000 / intervalle_en_millisecondes
```

Le premier pic sert de référence. Les intervalles de **300 à 1 500 ms** sont considérés comme valides, soit une plage nominale de **40 à 200 BPM**. Les autres intervalles sont ignorés pour l'affichage du BPM. L'estimation est ponctuelle : des percussions supplémentaires ou des pics manqués peuvent faire fluctuer la valeur.

**Observation :** les valeurs BPM ont été jugées cohérentes lors des essais avec claquements et musique.

## Bonus 2 — Moyenne des BPM et fichier texte

Le programme contient une fonction `enregistrer_moyenne(minute, somme, nombre)`, appelée au bout de chaque période de **60 000 ms**. Elle prévoit :
- une moyenne arrondie à une décimale quand au moins un BPM valide a été mesuré ;
- la mention « aucune mesure valide » sinon ;
- l'ajout d'une ligne à `bpm.txt` avec `with open("bpm.txt", "a")`, ce qui referme le fichier à la fin de l'écriture ;
- un séparateur `--- Nouvelle session ---` au premier enregistrement de chaque exécution.

Le fichier `bpm.txt` est créé **sur le système de fichiers du Pico** lorsqu'on exécute le programme sur la carte ; il n'est pas automatiquement synchronisé avec ce dépôt GitHub. Seules les périodes complètes sont écrites : une minute interrompue avant son échéance n'est pas enregistrée.

**Fonctionnement validé sur le Pico :** à chaque BPM valide, `calculer_bpm()` ajoute la valeur à `somme_bpm` et incrémente `nombre_bpm`. La fonction déclare désormais ces accumulateurs avec `global somme_bpm, nombre_bpm`. À chaque minute complète, le programme calcule leur moyenne, l'enregistre dans `bpm.txt`, puis remet les accumulateurs à zéro pour la période suivante.

**Observation :** après ces corrections, le fichier texte a été consulté sur le Pico. L'enregistrement de moyennes numériques, présentes et jugées cohérentes avec les essais, a été confirmé. Aucune valeur BPM précise n'a été reportée dans ce compte rendu.

## État des essais

| Étape | Résultat |
| --- | --- |
| Commande individuelle des trois couleurs RGB | **Validée sur le Pico** |
| Lecture du microphone en silence, avec claquements et avec musique | **Validée sur le Pico** |
| Seuil adaptatif, délai et réarmement | **Validés fonctionnellement** |
| Changement aléatoire de couleur sur un pic détecté | **Validé fonctionnellement** |
| Bonus 1 : affichage du BPM estimé | **Validé fonctionnellement** |
| Bonus 2 : écriture d'une moyenne réelle toutes les minutes | **Validée sur le Pico : fichier texte contenant des moyennes numériques cohérentes** |

Ces validations reposent sur les observations faites au cours des essais, y compris la lecture du fichier `bpm.txt` sur le Pico après correction. Aucun relevé chiffré des amplitudes ou des moyennes BPM n'est conservé dans ce dépôt. Aucune précision métrologique ni synchronisation parfaite avec le tempo musical n'a été établie.

## Mise au point

Lors d'un premier essai de l'enregistrement périodique, l'absence d'import de `ticks_add` a provoqué une erreur `NameError` à l'échéance de la minute. Après l'ajout de cet import, l'inspection de `bpm.txt` a montré l'absence de moyennes numériques : les accumulateurs n'étaient pas incrémentés. L'ajout de `somme_bpm += bpm` et `nombre_bpm += 1` a nécessité également la déclaration `global somme_bpm, nombre_bpm` dans `calculer_bpm()`. Le programme corrigé a ensuite été exécuté, et la présence de données cohérentes dans `bpm.txt` a été confirmée sur le Pico. Ces corrections montrent l'intérêt de vérifier le contenu effectivement sauvegardé, et pas seulement l'exécution de la minuterie.

Le traitement sonore reste volontairement simple et dépend notamment du volume, de la distance au microphone, de la musique et des seuils choisis. L'absence de filtrage par bande fréquentielle peut conduire à détecter d'autres sons que les battements recherchés.

## Reproduire l'expérience

1. Connecter le microphone sur **A1 / GP27** et la LED RGB sur **D18 / GP18**, puis alimenter le Pico.
2. Ouvrir [ex04_rgb_musique.py](ex04_rgb_musique.py) dans Thonny avec l'interpréteur **MicroPython (Raspberry Pi Pico)**.
3. Exécuter le script et vérifier les couleurs ainsi que les messages de détection et de BPM dans la console.
4. Pour le bonus 2, laisser fonctionner au moins une minute complète, puis consulter `bpm.txt` dans les fichiers du Pico via Thonny. Contrôler la présence d'une moyenne non nulle lorsqu'il existe des BPM valides.

## Ressources

- Énoncé fourni en cours : *Exercice 4 — Contrôle d'une LED RGB en fonction du rythme de la musique*.
- *Beginner's Guide for Raspberry Pi Pico*, leçon 12 : **Intelligent Light** (capteur de son et LED RGB).
- [Documentation MicroPython — module NeoPixel](https://docs.micropython.org/en/latest/library/neopixel.html).
- [Documentation MicroPython — fonctions de temps](https://docs.micropython.org/en/latest/library/time.html).
- [Documentation du kit Grove pour Raspberry Pi Pico](https://wiki.seeedstudio.com/Grove-Starter-Kit-for-Raspberry-Pi-Pico/).
- [Organisation du dépôt de référence du professeur](https://github.com/hepl-scheen/smartcities).
