import RPi.GPIO as gpio
pin = 21

gpio.setmode(gpio.BCM)
gpio.setup(pin, gpio.OUT)

pw = gpio.PWM(pin, 1000)
pw.start(0)
try:
    while True:
        input_val = input("enter duty cycle: ")
        if input_val == 'q':
            break
        try: 
            input_val = int(input_val)
            pw.ChangeDutyCycle(input_val)
            print(3.3 * input_val / 100)
        except ValueError:
            print("Enter an integer")
        
finally:
    pw.stop(0)
    gpio.output(pin, 0)
    gpio.cleanup()
