
import network
import ntptime
import time

from wifi_config import SSID, PASSWORD

# Activation du Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Connexion au reseau
if not wifi.isconnected():
    print("Connexion au Wi-Fi...")
    wifi.connect(SSID, PASSWORD)

    # Attendre la connexion pendant 15 secondes maximum
    debut = time.ticks_ms()

    while not wifi.isconnected():
        if time.ticks_diff(time.ticks_ms(), debut) > 15000:
            raise RuntimeError("Connexion Wi-Fi impossible")
        time.sleep(0.5)

print("Wi-Fi connecte !")
print("Adresse IP :", wifi.ifconfig()[0])

# Synchronisation de l'horloge
ntptime.settime()

# Recuperation de l'heure UTC
maintenant = time.localtime()

print("Heure UTC :", maintenant)
print("Heure :", maintenant[3])
print("Minutes :", maintenant[4])
print("Secondes :", maintenant[5])
