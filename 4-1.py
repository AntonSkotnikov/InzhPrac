import RPi.GPIO as gpio
dac = [8, 11, 7, 1, 0, 5, 12, 6]
gpio.setmode(gpio.BCM)
gpio.setup(dac, gpio.OUT)
def dec2bin(value):
    return [int(i) for i in bin(value)[2:].zfill(8)]

try:
    while True:
        input_val = input("enter number from 0 to 255: ")
        try:
            input_val = int(input_val)
            if input_val < 0:
                print("You entered number < 0")
            if input_val >= 0 and input_val <= 255:
                gpio.output(dac, dec2bin(input_val))
                print("voltage will be ", input_val/256.0 * 3.3)
            elif input_val > 255:
                print("you entered too big number")


        except ValueError:
            if input_val == 'q':
                break
            try:
                input_val = float(input_val)
                print("enter not a float number")

            except ValueError:
                print("You didn't enter number, try again")



finally:
    gpio.output(dac, 0)
    gpio.cleanup()