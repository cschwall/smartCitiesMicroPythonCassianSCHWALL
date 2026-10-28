from machine import ADC, Pin
from utime import sleep_ms

# Microphone connecte sur A1 (GP27)
micro = ADC(Pin(27))

print("Lecture du microphone...")

try:
    while True:
        valeur_min = 65535
        valeur_max = 0

        # Effectuer 100 mesures successives
        for i in range(100):
            valeur = micro.read_u16()

            if valeur < valeur_min:
                valeur_min = valeur

            if valeur > valeur_max:
                valeur_max = valeur

            sleep_ms(1)

        # Amplitude du signal sur la periode
        amplitude = valeur_max - valeur_min

        print("Min:", valeur_min,
              "Max:", valeur_max,
              "Amplitude:", amplitude)

        sleep_ms(100)

except KeyboardInterrupt:
    print("Fin des mesures")
