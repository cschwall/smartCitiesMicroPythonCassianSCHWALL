from machine import ADC, Pin
from utime import sleep_ms

potentiometre = ADC(Pin(26))

while True:
    valeur = potentiometre.read_u16()

    consigne = 15 + (valeur / 65535) * 20

    print("ADC :", valeur,
          "| Consigne :", round(consigne, 1), "°C")

    sleep_ms(300)