from machine import ADC, I2C, Pin, PWM
from time import ticks_ms, ticks_diff, sleep_ms
from dht20 import DHT20
from lcd1602 import LCD1602


potentiometre = ADC(Pin(26))
led = Pin(16, Pin.OUT, value=0)

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
intervalle_led = 0
derniere_mesure = None
dernier_changement_led = ticks_ms()

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
                    intervalle_led = 200
                    ligne_consigne = "Set: {:.1f} ALARM".format(consigne)
                elif temperature > consigne:
                    etat = "DEPASSEMENT"
                    intervalle_led = 1000
                else:
                    etat = "NORMAL"
                    intervalle_led = 0

                print("Etat :", etat,
                      "| Consigne :", round(consigne, 1), "°C",
                      "| Temperature ambiante :", round(temperature, 1), "°C")
            
            else:
                
                etat = "ERREUR"
                intervalle_led = 0
                ligne_temperature = "Erreur capteur"
                print("Mesure invalide, nouvel essai au prochain tour.")
            
            lcd.setCursor(0, 0)
            lcd.print((ligne_consigne + " " * 16)[:16])
            lcd.setCursor(0, 1)
            lcd.print((ligne_temperature + " " * 16)[:16])
            
        maintenant = ticks_ms()

        if etat != etat_precedent:
            led.off()
            buzzer.duty_u16(32768 if etat == "ALARM" else 0)
            dernier_changement_led = maintenant
            etat_precedent = etat

        if intervalle_led > 0:
            if ticks_diff(maintenant, dernier_changement_led) >= intervalle_led:
                led.toggle()
                dernier_changement_led = maintenant

        sleep_ms(10)
finally:
    buzzer.duty_u16(0)
    led.off()