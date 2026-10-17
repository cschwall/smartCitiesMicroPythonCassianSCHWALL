from machine import I2C, Pin
from lcd1602 import LCD1602

i2c_lcd = I2C(1, sda=Pin(6), scl=Pin(7), freq=400_000)
lcd = LCD1602(i2c_lcd, 2, 16)

lcd.clear()

lcd.setCursor(0, 0)
lcd.print("SmartCities")

lcd.setCursor(0, 1)
lcd.print("LCD pret")