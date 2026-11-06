
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


# Calcul de l'angle du servomoteur

def calculer_angle(heure, minute):
    heure_12 = heure % 12
    angle = (heure_12 + minute / 60) * 15
    return angle


# Conversion de l'heure UTC en heure belge
# En novembre, la Belgique est en UTC+1
heure_belgique = (maintenant[3] + 1) % 24
minute = maintenant[4]

# Calcul de l'angle correspondant
angle_servo = calculer_angle(heure_belgique, minute)

print("Heure belge :", heure_belgique, "h", minute)
print("Angle du servo :", angle_servo, "degres")


# Commande du servomoteur

from machine import Pin, PWM

servo = PWM(Pin(20))
servo.freq(100)

# Conversion de l'angle en valeur PWM
valeur_pwm = int(4000 + (angle_servo / 180) * 13000)

print("Valeur PWM :", valeur_pwm)

# Positionner le servo selon l'heure
try:
    servo.duty_u16(valeur_pwm)
    time.sleep(2)
finally:
    servo.deinit()

print("Servomoteur positionne !")


