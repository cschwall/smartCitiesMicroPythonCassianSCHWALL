from machine import ADC, Pin
from utime import sleep_ms, ticks_ms, ticks_diff

# Microphone sur A1 (GP27)
micro = ADC(Pin(27))

# Parametres de detection
FACTEUR_SENSIBILITE = 1.4
SEUIL_MINIMUM = 500
DELAI_MINIMUM = 50  # En millisecondes


def mesurer_amplitude():
    valeur_min = 65535
    valeur_max = 0

    for i in range(40):
        valeur = micro.read_u16()

        if valeur < valeur_min:
            valeur_min = valeur

        if valeur > valeur_max:
            valeur_max = valeur

        sleep_ms(1)

    return valeur_max - valeur_min


# Initialisation du niveau sonore moyen
print("Calibrage du microphone...")
print("Gardez le silence quelques instants.")

moyenne = 0

for i in range(30):
    moyenne += mesurer_amplitude()

moyenne /= 30

print("Calibrage termine !")
print("Amplitude moyenne initiale :", moyenne)

dernier_pic = ticks_ms() - DELAI_MINIMUM
dernier_affichage = ticks_ms()
pret = True

try:
    while True:
        amplitude = mesurer_amplitude()
        maintenant = ticks_ms()

        # Seuil adapte au niveau sonore moyen
        seuil = max(
            SEUIL_MINIMUM,
            moyenne * FACTEUR_SENSIBILITE
        )

        # Detection d'une augmentation sonore
        if (pret
                and amplitude > seuil
                and ticks_diff(maintenant, dernier_pic)
                    >= DELAI_MINIMUM):

            print(">>> PIC SONORE DETECTE !")

            dernier_pic = maintenant
            pret = False

        # Rearmer la detection apres une baisse
        if not pret and amplitude < seuil * 0.8:
            pret = True

        # Actualisation progressive de la moyenne
        moyenne = 0.95 * moyenne + 0.05 * amplitude

        # Affichage environ toutes les 300 ms
        if ticks_diff(maintenant, dernier_affichage) >= 300:
            print("Amplitude :", amplitude,
                  "| Seuil :", int(seuil))
            dernier_affichage = maintenant

except KeyboardInterrupt:
    print("Fin de la detection")
