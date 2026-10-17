from machine import ADC, I2C, Pin
from machine import I2C, Pin
from time import sleep
from dht20 import DHT20

potentiometre = ADC(Pin(26))

i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=100_000)
capteur = DHT20(0x38, i2c)

while True:
    valeur = potentiometre.read_u16()
    consigne = 15 + (valeur / 65535) * 20
    
    mesures = capteur.measurements

    if mesures["crc_ok"]:
        temperature = mesures["t"]
        print("Consigne :", round(consigne, 1), "°C",
              "| Temperature ambiante :", round(temperature, 1), "°C")
    else:
        print("Mesure invalide, nouvel essai au prochain tour.")

    sleep(1)