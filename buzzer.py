from machine import ADC, Pin, PWM
from utime import sleep

potentiometre = ADC(0)       # Potentiomètre sur A0
buzzer = PWM(Pin(16))        # Buzzer sur D16

buzzer.freq(440)             # 440 Hz = note La

while True:
    valeur = potentiometre.read_u16()

    # On transforme la valeur du potentiomètre en volume
    volume = valeur // 2

    buzzer.duty_u16(volume)

    print("Potentiometre :", valeur, " Volume :", volume)

    sleep(0.05)