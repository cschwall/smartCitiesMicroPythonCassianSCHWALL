from machine import ADC, Pin, PWM
from utime import sleep_ms

potentiometre = ADC(0)   # A0
buzzer = PWM(Pin(16))    # D16
bouton = Pin(18, Pin.IN) #D18

numero_musique = 0
etat_precedent = 0
etat_bouton = 0

# Notes en Hz
DO = 262
RE = 294
MI = 330
FA = 349
SOL = 392
LA = 440
SI = 494

# Petite mélodie
melodie1 = [
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


melodie2 = [
    (DO, 400),
    (DO, 400),
    (DO, 400),
    (RE, 400),
    (MI, 800),

    (RE, 800),
    (DO, 400),
    (MI, 400),
    (RE, 400),
    (RE, 400),
    (DO, 800)
]

melodies = [melodie1, melodie2]

def jouer_note(frequence, duree):
    global numero_musique, etat_precedent

    buzzer.freq(frequence)

    temps = 0

    while temps < duree:

        valeur = potentiometre.read_u16()
        volume = valeur // 2

        buzzer.duty_u16(volume)

        etat_bouton = bouton.value()

        if etat_bouton == 1 and etat_precedent == 0:
            numero_musique = (numero_musique + 1) % len(melodies)

        etat_precedent = etat_bouton

        sleep_ms(20)
        temps = temps + 20

    buzzer.duty_u16(0)
    sleep_ms(30)


while True:

    for note in melodies[numero_melodie]:
        jouer_note(note[0], note[1])


