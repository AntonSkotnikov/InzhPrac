import RPi.GPIO as gpio
import time
dac = [8, 11, 7, 1, 0, 5, 12, 6]
gpio.setmode(gpio.BCM)
gpio.setup(dac, gpio.OUT)
def dec2bin(value):
    return [int(i) for i in bin(value)[2:].zfill(8)]



x = 0
counter = 1
try:
    T = input("enter period: ")
    try:
        T = int(T)
    except ValueError:
        print("enter integer period, please")
    

    while True:
        if x == 0:
            counter = 1
        elif x == 255:
            counter = -1
        

        gpio.output(dac, dec2bin(x))
        x += counter
        time.sleep(abs(T)/512)
        


finally:
    gpio.output(dac, 0)
    gpio.cleanup()
