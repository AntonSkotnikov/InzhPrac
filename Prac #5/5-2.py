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
    counter = 128
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.01)
    if gpio.input(comp) == 1:
        counter -= 128
    counter += 64
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.01)
    if gpio.input(comp) == 1:
        counter -= 64
    counter += 32
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.01)
    if gpio.input(comp) == 1:
        counter -= 32
    counter += 16
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.01)
    if gpio.input(comp) == 1:
        counter -= 16
    counter += 8
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.01)
    if gpio.input(comp) == 1:
        counter -= 8
    counter += 4
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.01)
    if gpio.input(comp) == 1:
        counter -= 4
    counter += 2
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.01)
    if gpio.input(comp) == 1:
        counter -= 2
    counter += 1
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.01)
    if gpio.input(comp) == 1:
        counter -= 1

    return counter 


try:
    while True:
        input = adc()
        u = input * 3.3 / 256
        if u != 0:
            print(f"цифровое значение сигнала = {input}, напряжение = {u} вольт")


finally:
    gpio.output(dac, 0)
    gpio.cleanup()
