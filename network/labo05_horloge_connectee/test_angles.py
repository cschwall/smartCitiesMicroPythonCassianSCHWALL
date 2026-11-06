
# Labo 5 - Test du calcul des angles

def calculer_angle(heure, minute):
    heure_12 = heure % 12
    angle = (heure_12 + minute / 60) * 15
    return angle


# Quelques heures pour verifier le calcul
print("12h00 :", calculer_angle(12, 0), "degres")
print("3h00 :", calculer_angle(3, 0), "degres")
print("6h00 :", calculer_angle(6, 0), "degres")
print("9h00 :", calculer_angle(9, 0), "degres")
print("3h30 :", calculer_angle(3, 30), "degres")
