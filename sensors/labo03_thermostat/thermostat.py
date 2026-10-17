from machine import I2C, Pin
from time import sleep
from dht20 import DHT20

i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=100_000)
capteur = DHT20(0x38, i2c)

while True:
    mesures = capteur.measurements

    if mesures["crc_ok"]:
        temperature = mesures["t"]
        print("Temperature ambiante :", round(temperature, 1), "°C")
    else:
        print("Mesure invalide, nouvel essai au prochain tour.")

    sleep(1)