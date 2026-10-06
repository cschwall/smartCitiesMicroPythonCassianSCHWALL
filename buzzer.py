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


