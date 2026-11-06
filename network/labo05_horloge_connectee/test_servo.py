
from machine import Pin, PWM
from time import sleep

# Servo branche sur D20 (GP20)
servo = PWM(Pin(20))

# Frequence specifiee dans notre documentation
servo.freq(100)

try:
    # Position 45 degres
    print("Position : 45 degres")
    servo.duty_u16(7250)
    sleep(2)

    # Position 90 degres
    print("Position : 90 degres")
    servo.duty_u16(10500)
    sleep(2)

finally:
    # Arret du signal PWM
    servo.deinit()
    print("Test termine !")
