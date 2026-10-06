from machine import ADC, Pin, PWM
from utime import sleep_ms

potentiometre = ADC(0)   # A0
buzzer = PWM(Pin(16))    # D16

# Notes en Hz
DO = 262
RE = 294
MI = 330
FA = 349
SOL = 392
LA = 440
SI = 494

# Petite mélodie
melodie = [
    (DO, 400),
    (RE, 400),
    (MI, 400),
    (DO, 400),

    (DO, 400),
    (RE, 400),
    (MI, 400),
    (DO, 400),

    (MI, 400),
    (FA, 400),
    (SOL, 800)
]
def jouer_note(frequence, duree):
    buzzer.freq(frequence)

    temps = 0

    while temps < duree:

        valeur = potentiometre.read_u16()
        volume = valeur // 2

        buzzer.duty_u16(volume)

        sleep_ms(20)

        temps = temps + 20

    # Petite coupure entre deux notes
    buzzer.duty_u16(0)
    sleep_ms(30)


while True:

    for note in melodie:
        jouer_note(note[0], note[1])


