from machine import ADC, Pin
from neopixel import NeoPixel
from utime import sleep_ms, ticks_ms, ticks_diff, ticks_add
from random import randint

# --- Initialisation du materiel ---

micro = ADC(Pin(27))           # Microphone sur A1
led = NeoPixel(Pin(18), 1)     # LED RGB sur D18

# --- Parametres de detection ---

FACTEUR_SENSIBILITE = 1.3
SEUIL_MINIMUM = 500
DELAI_MINIMUM = 300

# --- BONUS 1 : Parametres BPM ---

INTERVALLE_MIN = 300     # 200 BPM maximum
INTERVALLE_MAX = 1500    # 40 BPM minimum

dernier_battement = None

# --- BONUS 2 : Moyenne et enregistrement ---

DUREE_MINUTE = 60000

somme_bpm = 0
nombre_bpm = 0
numero_minute = 0


# --- Couleurs disponibles ---

couleurs = [
    (40, 0, 0),    # Rouge
    (0, 40, 0),    # Vert
    (0, 0, 40),    # Bleu
    (40, 40, 0),   # Jaune
    (40, 0, 40),   # Violet
    (0, 40, 40),   # Cyan
    (40, 20, 0),   # Orange
    (40, 40, 40)   # Blanc
]

dernier_indice = -1


# --- Mesure de l'amplitude sonore ---

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


# --- Changement aleatoire de couleur ---

def changer_couleur():
    global dernier_indice

    indice = randint(0, len(couleurs) - 1)

    # Eviter deux couleurs identiques de suite
    while indice == dernier_indice:
        indice = randint(0, len(couleurs) - 1)

    dernier_indice = indice

    led[0] = couleurs[indice]
    led.write()

    print("Nouvelle couleur :", couleurs[indice])

# --- BONUS 1 : Calcul des BPM ---

def calculer_bpm(maintenant):
    global dernier_battement

    if dernier_battement is not None:

        intervalle = ticks_diff(
            maintenant, dernier_battement
        )

        if INTERVALLE_MIN <= intervalle <= INTERVALLE_MAX:

            bpm = round(60000 / intervalle)

            print("Rythme estime :", bpm, "BPM")

        else:
            print("Intervalle ignore :", intervalle, "ms")

    else:
        print("Premier battement : attente du suivant")

    dernier_battement = maintenant

# --- BONUS 2 : Enregistrement des BPM ---

def enregistrer_moyenne(minute, somme, nombre):

    if nombre > 0:
        bpm_moyen = round(somme / nombre, 1)

        ligne = "Minute {} : {} BPM ({} mesures)\n".format(
            minute, bpm_moyen, nombre
        )

    else:
        ligne = "Minute {} : aucune mesure valide\n".format(
            minute
        )

    # Mode ajout : conserve les anciennes donnees
    with open("bpm.txt", "a") as fichier:

        # Separateur entre deux executions
        if minute == 1:
            fichier.write("\n--- Nouvelle session ---\n")

        fichier.write(ligne)

    print("Enregistrement :", ligne.strip())


# --- Calibrage initial ---

print("Calibrage du microphone...")
print("Garde le silence quelques instants.")

led[0] = (0, 0, 0)
led.write()

moyenne = 0

for i in range(30):
    moyenne += mesurer_amplitude()

moyenne /= 30

print("Calibrage termine !")
print("Amplitude moyenne initiale :", moyenne)

dernier_pic = ticks_ms() - DELAI_MINIMUM
dernier_affichage = ticks_ms()
debut_minute = ticks_ms()

pret = True


# --- Boucle principale ---

try:
    while True:
        amplitude = mesurer_amplitude()
        maintenant = ticks_ms()
        
        # BONUS 2 : Verification des 60 secondes
        if ticks_diff(maintenant, debut_minute) >= DUREE_MINUTE:

            numero_minute += 1

            enregistrer_moyenne(
                numero_minute,
                somme_bpm,
                nombre_bpm
            )

            # Remise a zero pour la minute suivante
            somme_bpm = 0
            nombre_bpm = 0

            debut_minute = ticks_add(
                debut_minute, DUREE_MINUTE
            )

        seuil = max(
            SEUIL_MINIMUM,
            moyenne * FACTEUR_SENSIBILITE
        )

        if (pret
                and amplitude > seuil
                and ticks_diff(maintenant, dernier_pic)
                    >= DELAI_MINIMUM):

            print(">>> BATTEMENT DETECTE !")

            # Changement de couleur a chaque pic
            changer_couleur()
            
            # BONUS 1 : Calcul du rythme
            calculer_bpm(maintenant)
            
            dernier_pic = maintenant
            pret = False

        # Rearmement apres une baisse sonore
        if not pret and amplitude < seuil * 0.8:
            pret = True

        # Actualisation de la moyenne
        moyenne = 0.95 * moyenne + 0.05 * amplitude

        # Affichage periodique
        if ticks_diff(maintenant, dernier_affichage) >= 300:
#             print("Amplitude :", amplitude,
#                   "| Seuil :", int(seuil))
            dernier_affichage = maintenant

finally:
    # Eteindre la LED a l'arret du programme
    led[0] = (0, 0, 0)
    led.write()
    print("Programme arrete")
