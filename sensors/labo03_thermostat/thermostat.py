from machine import ADC, I2C, Pin, PWM
from time import ticks_ms, ticks_diff, sleep_ms
from dht20 import DHT20
from lcd1602 import LCD1602


potentiometre = ADC(Pin(26))
led = PWM(Pin(16))
led.freq(1000)
led.duty_u16(0)

buzzer = PWM(Pin(18))
buzzer.freq(2000)
buzzer.duty_u16(0)

i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=100_000)
capteur = DHT20(0x38, i2c)

i2c_lcd = I2C(1, sda=Pin(6), scl=Pin(7), freq=400_000)
lcd = LCD1602(i2c_lcd, 2, 16)
lcd.clear()

etat = "NORMAL"
etat_precedent = None
periode_led = 0
derniere_mesure = None
phase_led = 0
dernier_calcul_led = ticks_ms()

try:
    while True:
        maintenant = ticks_ms()
        
        if derniere_mesure is None or ticks_diff(maintenant, derniere_mesure) >= 1000:
            derniere_mesure = maintenant
        
            valeur = potentiometre.read_u16()
            consigne = 15 + (valeur / 65535) * 20
            ligne_consigne = "Set: {:.1f} C".format(consigne)
            mesures = capteur.measurements

            if mesures["crc_ok"]:
                temperature = mesures["t"]
                ligne_temperature = "Ambient: {:.1f} C".format(temperature)
                
                if temperature > consigne + 3:
                    etat = "ALARM"
                    periode_led = 400
                    ligne_consigne = "Set: {:.1f} ALARM".format(consigne)
                elif temperature > consigne:
                    etat = "DEPASSEMENT"
                    periode_led = 2000
                else:
                    etat = "NORMAL"
                    periode_led = 0

                print("Etat :", etat,
                      "| Consigne :", round(consigne, 1), "°C",
                      "| Temperature ambiante :", round(temperature, 1), "°C")
            
            else:
                
                etat = "ERREUR"
                periode_led = 0
                ligne_temperature = "Erreur capteur"
                print("Mesure invalide, nouvel essai au prochain tour.")
            
            lcd.setCursor(0, 0)
            lcd.print((ligne_consigne + " " * 16)[:16])
            lcd.setCursor(0, 1)
            lcd.print((ligne_temperature + " " * 16)[:16])
            
        maintenant = ticks_ms()

        if etat != etat_precedent:
            led.duty_u16(0)
            buzzer.duty_u16(32768 if etat == "ALARM" else 0)
            phase_led = 0
            dernier_calcul_led = maintenant
            etat_precedent = etat

        if periode_led > 0:
            # Avancer dans le cycle sans attendre la fin du battement.
            ecoule = ticks_diff(maintenant, dernier_calcul_led)
            phase_led = (phase_led + ecoule) % periode_led
            demi_periode = periode_led // 2

            # Monter puis descendre progressivement la commande lumineuse.
            if phase_led <= demi_periode:
                luminosite = phase_led * 65535 // demi_periode
            else:
                luminosite = (periode_led - phase_led) * 65535 // demi_periode

            led.duty_u16(luminosite)

        dernier_calcul_led = maintenant

        sleep_ms(10)
finally:
    buzzer.duty_u16(0)
    led.duty_u16(0)
    led.deinit()
