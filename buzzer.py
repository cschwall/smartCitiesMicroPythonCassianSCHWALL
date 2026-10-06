from machine import ADC
from utime import sleep

potentiometre = ADC(0)   # A0 du Grove Shield

while True:
    valeur = potentiometre.read_u16()
    print(valeur)
    sleep(0.1)