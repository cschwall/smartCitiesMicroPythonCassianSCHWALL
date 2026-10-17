# Entrées analogiques et PWM

[Retour à l'accueil](../README.md)

Ce thème regroupe la lecture analogique (ADC) et la modulation de largeur d'impulsion (PWM) : potentiomètre, commande de LED, buzzer et servomoteur selon les exercices réalisés.

## Laboratoires

| Laboratoire | Contenu | État |
| --- | --- | --- |
| [Labo 2 — Volume d'une mélodie](labo02_buzzer/) | Potentiomètre, buzzer PWM et sélection de mélodie par bouton | Programme et essais documentés ; exigences principales et bonus bouton réalisés |

Chaque laboratoire possède un sous-dossier contenant son README, ses programmes et les ressources directement liées au montage.

## Exemples préparatoires

[lecture_consigne.py](lecture_consigne.py) lit le potentiomètre sur GP26 et convertit sa valeur en une consigne comprise entre 15 et 35 °C. La variation a été validée sur le matériel, avec affichage dans la console de Thonny.

[test_led_progressive.py](test_led_progressive.py) commande la LED sur GP16 avec un PWM à 1 000 Hz. Son rapport cyclique augmente puis diminue, pour un battement lumineux d'environ deux secondes. Cette variation progressive a été validée sur le matériel.

Ces exemples autonomes préparent le [labo 3 — Thermostat](../sensors/labo03_thermostat/), dont le programme et la documentation sont regroupés dans le thème Capteurs. La consigne y est déjà validée ; la variation progressive de la LED vient d'être intégrée et reste à tester dans le montage complet. Les exemples restent ici pour illustrer séparément la conversion analogique et la commande PWM.

## Notions et ressources

- Lecture de `ADC.read_u16()` et conversion d'une plage de valeurs.
- Fréquence et rapport cyclique d'un signal PWM.
- [Référence MicroPython : ADC](https://docs.micropython.org/en/latest/rp2/quickref.html#adc-analog-to-digital-conversion).
- [Référence MicroPython : PWM](https://docs.micropython.org/en/latest/rp2/quickref.html#pwm-pulse-width-modulation).
- [Consignes du professeur : AD-PWM](https://github.com/hepl-scheen/smartcities/tree/main/AD-PWM).
- Les branchements, les essais et les ressources du labo 2 se trouvent dans [son README](labo02_buzzer/README.md).
