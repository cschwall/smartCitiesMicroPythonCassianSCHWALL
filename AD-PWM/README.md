# Entrées analogiques et PWM

[Retour à l'accueil](../README.md)

Ce dossier regroupe les exercices utilisant la conversion analogique-numérique (ADC) et la modulation de largeur d'impulsion (PWM). Le deuxième laboratoire associe un potentiomètre à un buzzer pour régler le volume d'une mélodie.

## Labo 2 - Volume d'une mélodie

**Programme : [ex02-buzzer.py](ex02-buzzer.py)**

### Objectif et consignes

- Jouer une mélodie en boucle sur un buzzer.
- Faire varier son volume en agissant sur un potentiomètre pendant la lecture.
- Bonus réalisé : ajouter un bouton permettant de sélectionner une autre mélodie.

Le bonus proposant une LED qui clignote au rythme de la mélodie n'est pas implémenté dans cette version.

### Matériel et affectation des signaux

Le montage utilise un Raspberry Pi Pico, un module potentiomètre, un buzzer, un module bouton-poussoir pour le bonus, des câbles de connexion et une liaison USB avec l'ordinateur.

| Élément | Signal configuré dans le programme | Configuration |
| --- | --- | --- |
| Potentiomètre | ADC0, associé à GP26 sur le Pico | Entrée analogique : `ADC(0)` ; repère `A0` dans le code |
| Buzzer | GP16 | Sortie PWM : `PWM(Pin(16))` ; repère `D16` dans le code |
| Bouton-poussoir | GP18 | Entrée numérique : `Pin(18, Pin.IN)` ; repère `D18` dans le code |

Les numéros GPIO ne sont pas les numéros des broches physiques. Le programme ne configure pas de résistance de rappel interne pour le bouton : son état au repos dépend du module ou du câblage utilisé. Une photo du montage pourra compléter ces indications.

### Fonctionnement du programme

#### Mélodies et notes

Les notes sont définies par leur fréquence en hertz. Chaque mélodie est une liste de couples `(fréquence, durée_en_ms)`. Deux mélodies sont regroupées dans la liste `melodies`, et `numero_musique` indique le choix utilisé au début de chaque lecture complète.

La fonction `jouer_note(frequence, duree)` règle la fréquence du buzzer, maintient la note pendant la durée prévue, puis coupe la sortie PWM et ajoute une pause de 30 ms entre les notes.

#### Réglage du volume

Pendant une note, le programme relit le potentiomètre toutes les 20 ms :

1. `potentiometre.read_u16()` fournit une valeur comprise entre 0 et 65 535.
2. `volume = valeur // 2` ramène la commande à une plage de 0 à 32 767.
3. `buzzer.duty_u16(volume)` applique cette valeur au rapport cyclique du signal PWM, soit environ 0 à 50 %.

La fréquence détermine la note jouée ; la modification du rapport cyclique permet de faire varier le niveau sonore sur le montage. Le réglage est actualisé pendant les notes, sans attendre la fin de la mélodie. Cette commande ne constitue pas une échelle de volume sonore linéaire ou une mesure en décibels.

#### Sélection de la mélodie

Un appui est détecté lorsque l'état du bouton passe de 0 à 1. Le programme avance alors dans la liste des mélodies avec un calcul modulo, ce qui permet de revenir au premier choix après le second.

La mélodie en cours se termine avant que le nouveau choix soit joué : la liste de notes parcourue par la boucle `for` est choisie au début de chaque cycle. Le bouton sélectionne donc la mélodie du cycle suivant ; il n'interrompt pas immédiatement celle en cours.

### Utilisation

1. Préparer le montage avec les signaux indiqués ci-dessus et connecter le Pico à l'ordinateur.
2. Ouvrir `ex02-buzzer.py` dans Thonny, sélectionner l'interpréteur MicroPython du Pico et lancer le programme.
3. Écouter la mélodie, qui se répète automatiquement.
4. Tourner le potentiomètre pendant les notes pour faire varier le volume.
5. Appuyer puis relâcher le bouton pour sélectionner l'autre mélodie, qui commencera à la fin du cycle en cours.
6. Arrêter le programme depuis Thonny pour terminer l'exécution.

### Essais et résultats

Les essais matériels ont été réalisés par Cassian. La lecture en boucle et le réglage du volume ont donné le fonctionnement attendu dès le premier essai. Le changement de mélodie par bouton a également été déclaré fonctionnel, sans difficulté matérielle particulière signalée.

| Vérification demandée | Résultat rapporté |
| --- | --- |
| Lecture répétée d'une mélodie | Conforme au comportement attendu |
| Variation du volume avec le potentiomètre pendant la lecture | Conforme au comportement attendu |
| Sélection de l'autre mélodie par bouton, en tenant compte du changement au cycle suivant | Fonctionnement confirmé pour le bonus bouton |

### Mise au point et périmètre

Une relecture du fichier du dépôt a permis de corriger une incohérence de nom dans la sélection de la mélodie : la boucle utilisait `numero_melodie` alors que la variable du programme est `numero_musique`. Cette correction est conservée dans le [commit correspondant](https://github.com/cschwall/smartCitiesMicroPythonCassianSCHWALL/commit/d84259e).

Les exigences principales et le bonus bouton sont implémentés. Le changement de mélodie au cycle suivant est le comportement de cette version. Les exercices sur la variation de luminosité d'une LED ou le servomoteur pourront compléter ce dossier ultérieurement.

## Ressources

- Énoncé du cours : **Exercice 2 - Volume d'une mélodie**.
- *Beginner's Guide for Raspberry Pi Pico*, TinkerGen / Seeed Studio : leçon 6, potentiomètre et signaux analogiques, pages imprimées 48 à 52 ; leçon 7, PWM, pages 56 à 63 ; leçon 8, buzzer et fonctions, pages 64 à 69.
- [Référence MicroPython : ADC](https://docs.micropython.org/en/latest/rp2/quickref.html#adc-analog-to-digital-conversion).
- [Référence MicroPython : PWM](https://docs.micropython.org/en/latest/rp2/quickref.html#pwm-pulse-width-modulation).
- [Organisation du thème AD-PWM dans le dépôt du professeur](https://github.com/hepl-scheen/smartcities/tree/main/AD-PWM).
