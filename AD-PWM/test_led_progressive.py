from machine import Pin, PWM
from time import sleep_ms

led = PWM(Pin(16))
led.freq(1000)
led.duty_u16(0)

try:
    while True:
        for niveau in range(101):
            led.duty_u16(niveau * 65535 // 100)
            sleep_ms(10)

        for niveau in range(99, 0, -1):
            led.duty_u16(niveau * 65535 // 100)
            sleep_ms(10)
finally:
    led.duty_u16(0)
    led.deinit()