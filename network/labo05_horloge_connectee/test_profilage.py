# Exercice 5 - Programme de profilage energetique PPK2
# Copie de l'experimentation realisee avec ce programme en main.py sur le Pico.
# Pour relancer automatiquement depuis une alimentation VSYS, enregistrer
# une copie sous le nom main.py sur le Pico W.
# wifi_config.py contient les identifiants et NE DOIT PAS etre versionne.
#
# Les durees sont des consignes nominales : elles ne garantissent pas
# que chaque mode de veille dure effectivement 15 secondes sur RP2040.

import machine
import network
import ntptime
import time

from wifi_config import SSID, PASSWORD

DUREE = 15000  # 15 secondes en millisecondes


def actif_pendant(duree):
    debut = time.ticks_ms()
    compteur = 0
    while time.ticks_diff(time.ticks_ms(), debut) < duree:
        compteur += 1


time.sleep(3)

# Etat 1 - microcontroleur actif avec Wi-Fi (connexion et NTP)
print("ETAT 1 - Wi-Fi actif")
wifi = network.WLAN(network.STA_IF)
debut = time.ticks_ms()
wifi.active(True)

try:
    wifi.connect(SSID, PASSWORD)
    attente = time.ticks_ms()
    while not wifi.isconnected():
        if time.ticks_diff(time.ticks_ms(), attente) > 7000:
            break
        time.sleep_ms(100)

    if wifi.isconnected():
        ntptime.settime()
except Exception as erreur:
    print("Erreur reseau :", erreur)

temps_passe = time.ticks_diff(time.ticks_ms(), debut)
if temps_passe < DUREE:
    actif_pendant(DUREE - temps_passe)

# Etat 2 - microcontroleur actif sans Wi-Fi
print("ETAT 2 - Wi-Fi desactive")
wifi.active(False)
actif_pendant(DUREE)

# Etat 3 - light sleep
print("ETAT 3 - Light sleep")
machine.lightsleep(DUREE)

# Etat 4 - deep sleep (comportement dependant du firmware RP2)
print("ETAT 4 - Deep sleep")
machine.deepsleep(DUREE)
