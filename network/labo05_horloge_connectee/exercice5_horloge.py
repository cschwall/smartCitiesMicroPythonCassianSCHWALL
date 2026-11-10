# Exercice 5 - Horloge connectee avec Raspberry Pi Pico W
# Controle du servomoteur Grove D20 / GP20 a partir de l'heure NTP.
# Le fichier wifi_config.py (SSID, PASSWORD) reste prive sur le Pico.

import network
import ntptime
import time
from machine import Pin, PWM
from wifi_config import SSID, PASSWORD


def calculer_angle(heure, minute):
    """Convertit une heure au format 24 h en position sur un cadran 12 h."""
    heure_12 = heure % 12
    return (heure_12 + minute / 60) * 15


# Connexion au Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

if not wifi.isconnected():
    print("Connexion au Wi-Fi...")
    wifi.connect(SSID, PASSWORD)
    debut = time.ticks_ms()
    while not wifi.isconnected():
        if time.ticks_diff(time.ticks_ms(), debut) > 15000:
            raise RuntimeError("Connexion Wi-Fi impossible")
        time.sleep(0.5)

print("Wi-Fi connecte !")
print("Adresse IP :", wifi.ifconfig()[0])

# Une synchronisation NTP au demarrage, puis lecture de la RTC.
ntptime.settime()
print("Heure UTC :", time.localtime())
print("Horloge connectee demarree !")

try:
    while True:
        maintenant = time.localtime()

        # UTC+1 = heure belge d'hiver uniquement.
        # L'heure d'ete (UTC+2) n'est pas geree automatiquement ici.
        heure_belgique = (maintenant[3] + 1) % 24
        minute = maintenant[4]
        seconde = maintenant[5]

        angle_servo = calculer_angle(heure_belgique, minute)
        valeur_pwm = int(4000 + (angle_servo / 180) * 13000)

        print("Heure belge : {:02d}:{:02d}:{:02d}".format(
            heure_belgique, minute, seconde))
        print("Angle :", angle_servo, "degres")
        print("PWM :", valeur_pwm)
        print("------------------")

        # Le signal PWM est maintenu une seconde puis coupe.
        servo = PWM(Pin(20))
        try:
            servo.freq(100)
            servo.duty_u16(valeur_pwm)
            time.sleep(1)
        finally:
            servo.deinit()

        # Environ 60 secondes entre deux mesures de l'heure.
        time.sleep(59)

except KeyboardInterrupt:
    print("Horloge arretee !")
