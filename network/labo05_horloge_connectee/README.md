# Labo 5 — Horloge connectée et profilage énergétique

[Retour au thème réseau](../README.md) · [Accueil du dépôt](../../README.md)

## Objectif

Construire avec un **Raspberry Pi Pico W** une horloge qui se synchronise sur Internet (NTP), convertit l'heure en angle sur un cadran de 12 heures et oriente un servomoteur Grove. Mesurer ensuite l'influence de la connexion réseau et des modes de veille sur le courant consommé, à l'aide d'un **Power Profiler Kit II (PPK2)**.

## Fichiers du laboratoire

| Fichier | Utilité |
| --- | --- |
| [test_angles.py](test_angles.py) | Vérification autonome de la formule de conversion heure → angle. |
| [test_servo.py](test_servo.py) | Test matériel du servomoteur : positions 45° et 90° sur GP20. |
| [exercice5_horloge.py](exercice5_horloge.py) | Programme principal : connexion Wi-Fi, NTP puis actualisation de la position du servo chaque minute environ. |
| [test_profilage.py](test_profilage.py) | Programme distinct utilisé pour solliciter successivement quatre états énergétiques. Une copie nommée `main.py` a été placée sur le Pico pour l'exécuter sans USB. |
| [wifi_config.example.py](wifi_config.example.py) | Exemple de configuration sans identifiants réels. |

Le vrai fichier `wifi_config.py` contient `SSID` et `PASSWORD`. Il a été conservé **sur le Pico**, n'est pas inclus dans le dépôt et est ignoré par Git.

## Matériel et branchements

- Raspberry Pi **Pico W**, MicroPython et Thonny.
- Grove Shield et servomoteur Grove pour la démonstration de l'horloge.
- Servo raccordé au port **D20 (GPIO 20)** du Shield ; sélection de l'alimentation du Shield sur **5 V** pour les essais moteur ; Pico alimenté par USB.
- Pour le profilage, le Pico W a finalement pu être **séparé du Shield** : servomoteur et modules débranchés. PPK2 en **Source Meter**, sortie positive **VOUT → VSYS (broche physique 39)** et **GND → GND (broche 38)**, alimentation réglée à **5 000 mV**, sans câble USB relié au Pico.

Les mesures du PPK2 portent donc sur le Pico W seul, avec son régulateur, et non sur la consommation du moteur. La tension VSYS de 5 V est comprise dans la plage acceptée de 1,8 à 5,5 V.

## 1. Connexion Wi-Fi et heure NTP

La bibliothèque `network` crée une station Wi-Fi (`network.STA_IF`) et `ntptime.settime()` synchronise l'horloge interne. Les identifiants sont importés depuis le fichier privé `wifi_config.py`.

**Essais validés sur le matériel :** scan de 9 réseaux, connexion Wi-Fi réussie et adresse IPv4 attribuée, synchronisation NTP et extraction des heures/minutes/secondes via `time.localtime()`. Le programme complet a ensuite fonctionné depuis Thonny.

Les serveurs NTP fournissent l'heure UTC. L'exemple utilise **UTC+1**, adapté à l'heure belge d'hiver lors de nos essais du 6 novembre 2026. Le passage automatique à l'heure d'été (UTC+2) n'est **pas implémenté**.

## 2. Calcul de l'angle

Le cadran demandé impose **12 h → 0°** et **6 h → 90°**. Un tour de 12 heures correspond donc à 180°, soit **15° par heure**.

```python
angle = ((heure % 12) + minute / 60) * 15
```

Valeurs obtenues lors de `test_angles.py` :

| Heure | Angle |
| --- | ---: |
| 12 h 00 | 0° |
| 3 h 00 | 45° |
| 6 h 00 | 90° |
| 9 h 00 | 135° |
| 3 h 30 | 52,5° |

Les cinq résultats ont été validés dans la console Thonny.

## 3. Commande du servomoteur

Pour le Grove Servo utilisé, le guide Seeed Studio / TinkerGen (leçon 13, pp. 115–118 imprimées) propose une fréquence PWM de **100 Hz**, avec `duty_u16` = 4 000 à 0°, 10 500 à 90° et 17 000 à 180°.

L'interpolation employée est :

```python
valeur_pwm = int(4000 + (angle_servo / 180) * 13000)
```

`test_servo.py` a permis de confirmer physiquement les positions **45° puis 90°**. L'horloge principale a ensuite orienté le servo selon une heure réelle récupérée par NTP. Exemple validé : **15 h 23 → 50,75° → PWM 7 665**.

Après ajout d'une boucle `while True`, une actualisation automatique a été observée durant quatre cycles consécutifs :

| Heure locale | Angle | PWM |
| --- | ---: | ---: |
| 15:30:52 | 52,50° | 7 791 |
| 15:31:52 | 52,75° | 7 809 |
| 15:32:52 | 53,00° | 7 827 |
| 15:33:52 | 53,25° | 7 845 |

La commande PWM reste active pendant environ une seconde puis est coupée via `deinit()` ; le servo n'assure donc pas un maintien actif de sa position entre les mises à jour. La boucle utilise ensuite `time.sleep(59)` : l'intervalle est **approximativement**, pas rigoureusement, de 60 secondes.

## 4. Circuit d'alimentation et PPK2

Le Pico W reçoit normalement le 5 V USB sur **VBUS (broche 40)**, relié au circuit d'entrée **VSYS** via une diode de protection. **VSYS (broche 39)** constitue l'entrée du régulateur à découpage (SMPS), qui crée le rail **3V3** nécessaire au microcontrôleur et aux composants radio ; **GND (broche 38)** sert de retour.

Alimenter via VSYS permet de conserver l'architecture d'alimentation normale de la carte, contrairement à une injection directement sur la sortie 3V3. Le PPK2, configuré en **Source Meter à 5,0 V**, a fourni l'énergie et enregistré le courant. La présence du Shield et du servo aurait faussé la comparaison : ils ont été retirés du montage de mesure.

Le fichier `test_profilage.py` enchaîne, avec des durées nominales de **15 s par état** :

1. Microcontrôleur actif et Wi-Fi activé, avec tentative de synchronisation NTP.
2. Microcontrôleur actif avec `wifi.active(False)`.
3. `machine.lightsleep(15000)`.
4. `machine.deepsleep(15000)`.

L'implémentation des modes de sommeil et le moment du réveil dépendent du firmware et de la plateforme ; les quatre étapes ne sont pas marquées directement dans les fichiers PPK2.

## 5. Résultats du profilage énergétique

Deux acquisitions PPK2 ont été réalisées le **6 novembre 2026**. La seconde, **`ppk2-20261106T161012.ppk2`**, est retenue pour l'analyse principale : **65,8073 s**, **658 073 échantillons**, **10 000 échantillons/s**, alimentation configurée à **5 V**. Les fichiers bruts sont conservés séparément ; les captures commentées seront intégrées ultérieurement au document de rapport.

Les courants ci-dessous ont été calculés sur des portions du signal considérées comme stables, en évitant les transitions. Les intervalles sont relatifs au **début de l'enregistrement**, qui ne coïncide pas nécessairement avec le début de `main.py`.

| Configuration / interprétation | Fenêtre sélectionnée | Courant moyen |
| --- | ---: | ---: |
| Actif avec Wi-Fi (phase identifiable) | 16–29 s | **63,57 mA** |
| Actif sans Wi-Fi (phase identifiable) | 33–43 s | **38,96 mA** |
| Light sleep (phase probable) | 46–57 s | **21,82 mA** |
| Zone tardive où le deep sleep était attendu, **non distinguable avec certitude** | 61–65 s | **21,81 mA** |

Le courant diminue d'environ **39 %** entre la phase Wi-Fi actif et la phase actif sans Wi-Fi, puis d'environ **44 %** entre actif sans Wi-Fi et light sleep. Les comparaisons sont effectuées à tension d'alimentation identique.

**Limite importante :** la dernière zone du deuxième enregistrement ne présente pas de chute supplémentaire identifiable par rapport au light sleep. Un bref passage vers **6,01 mA** entre **11,5 et 13,7 s** est également visible, mais il ne peut pas être attribué formellement au deep sleep à partir du seul signal. Il serait donc inexact d'affirmer qu'un deep sleep distinct de 15 secondes a été mesuré et validé. Le rapport discute cette incertitude plutôt que de fournir une mesure non vérifiée.

Ces relevés concernent **le courant d'entrée sur VSYS**, incluant le rendement du régulateur ; ils ne sont pas une mesure du courant du cœur RP2040 seul.

## 6. Avancement, limites et pistes d'amélioration

**Validé sur matériel :** Wi-Fi, NTP, calcul d'angles, commande physique du servo, plusieurs actualisations autonomes, alimentation du Pico W via VSYS et acquisitions PPK2.

**À ne pas présenter comme validé :** distinction fiable d'un deep sleep de 15 secondes, maintien mécanique de la position sans PWM, correction automatique des changements été/hiver, fonctionnement avec le PPK2 et le servo alimentés simultanément.

**Bonus facultatifs non réalisés :** bouton de sélection du fuseau horaire et double clic pour le format 24 heures.

Une amélioration ultérieure consisterait à utiliser un moyen de marquage temporel des phases énergétiques et à vérifier le comportement exact de `deepsleep()` sur la version de firmware du Pico W.

## Références

- Énoncé de cours : *Exercice 5 — Construction d'une horloge connectée et profilage énergétique*.
- *Beginner's Guide for Raspberry Pi Pico*, TinkerGen / Seeed Studio, leçon 13 (servomoteur).
- [Documentation Raspberry Pi Pico W — schémas et alimentation](https://datasheets.raspberrypi.com/picow/pico-w-datasheet.pdf).
- [Référence MicroPython : modes lightsleep/deepsleep](https://docs.micropython.org/en/latest/library/machine.html#power-related-functions).
- [Nordic Power Profiler — format des fichiers PPK2](https://github.com/nordicsemi/pc-nrfconnect-ppk#file-format).
