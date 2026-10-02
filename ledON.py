import machine
import utime

led = machine.Pin(16, machine.Pin.OUT)
button = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)

nbPressions = 0

ancienBouton = 0

etatLed = 0
dernierChangementLed = utime.ticks_ms()

dernierClic = 0


while True:

    maintenant = utime.ticks_ms()

    bouton = button.value()

    if bouton == 1 and ancienBouton == 0:


        if utime.ticks_diff(maintenant, dernierClic) > 200:

            nbPressions += 1
            dernierClic = maintenant

            print("Pression :", nbPressions)

    ancienBouton = bouton



    if nbPressions == 0:
        led.value(0)


    elif nbPressions == 1:

        if utime.ticks_diff(maintenant, dernierChangementLed) >= 1000:

            etatLed = not etatLed
            led.value(etatLed)

            dernierChangementLed = maintenant


    elif nbPressions == 2:

        if utime.ticks_diff(maintenant, dernierChangementLed) >= 200:

            etatLed = not etatLed
            led.value(etatLed)

            dernierChangementLed = maintenant


    elif nbPressions >= 3:

        led.value(0)


    utime.sleep_ms(9)