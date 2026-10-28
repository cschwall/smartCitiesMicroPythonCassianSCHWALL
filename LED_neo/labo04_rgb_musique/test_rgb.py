from machine import Pin
from neopixel import NeoPixel
from utime import sleep

# LED RGB branchee sur D18 (GP18)
led = NeoPixel(Pin(18, Pin.OUT), 1)

# Couleurs au format (Rouge, Vert, Bleu)
couleurs = [
    (40, 0, 0),  # Rouge
    (0, 40, 0),  # Vert
    (0, 0, 40),  # Bleu
]

try:
    for couleur in couleurs:
        led[0] = couleur
        led.write()
        print("Couleur :", couleur)
        sleep(1)

finally:
    # Eteindre la LED a la fin du test
    led[0] = (0, 0, 0)
    led.write()
