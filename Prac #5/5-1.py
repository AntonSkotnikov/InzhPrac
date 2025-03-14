
import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
dac = [8, 11, 7, 1, 0, 5, 12, 6]
comp = 14
troyka = 13
gpio.setup(dac, gpio.OUT)
gpio.setup(troyka, gpio.OUT, initial=1)
gpio.setup(comp, gpio.IN)

def dec2bin(value):
    return [int(i) for i in bin(value)[2:].zfill(8)]


def adc():
    for i in range(0, 256):
        value = dec2bin(i)
        gpio.output(dac, value)
        time.sleep(0.01)
        if gpio.input(comp) != 0:
            return i
    return 0


try:
    while True:
        input = adc()
        u = input * 3.3 / 256
        if u != 0:
            print(f"цифровое значение сигнала = {input}, напряжение = {u} вольт")


finally:
    gpio.output(dac, 0)
    gpio.cleanup()

