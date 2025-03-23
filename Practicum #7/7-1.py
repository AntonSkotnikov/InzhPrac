import RPi.GPIO as gpio
import matplotlib.pyplot as plt
import time

#константы
comp = 14
dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds =  [2, 3, 4, 17, 27, 22, 10, 9]
troyka = 13
max_voltage = 3.3

#настройка GPIO
gpio.setmode(gpio.BCM)
gpio.setup(dac, gpio.OUT)
gpio.setup(leds, gpio.OUT)
gpio.setup(troyka, gpio.OUT, initial=0)
gpio.setup(comp, gpio.IN)

voltage_data = []
time_data = []

def dec2bin(value): #конвертируем число в массив из 8 битов
    return [int(i) for i in bin(value)[2:].zfill(8)]

#def adc(): #измерение напряжения на выходе тройка-модуля
    # k = 0
    # for i in range(7, -1, -1):
    #     k += 2 ** i
    #     dac_val = dec2bin(k)
    #     gpio.output(dac, dac_val)
    #     time.sleep(0.01)
    #     if gpio.input(comp) == 1:
    #         k -= 2 ** i

    # return k

def adc(): #более быстрая, но менее красивая реализация
    counter = 128
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.003)
    if gpio.input(comp) == 1:
        counter -= 128
    counter += 64
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.003)
    if gpio.input(comp) == 1:
        counter -= 64
    counter += 32
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.003)
    if gpio.input(comp) == 1:
        counter -= 32
    counter += 16
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.003)
    if gpio.input(comp) == 1:
        counter -= 16
    counter += 8
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.003)
    if gpio.input(comp) == 1:
        counter -= 8
    counter += 4
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.003)
    if gpio.input(comp) == 1:
        counter -= 4
    counter += 2
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.003)
    if gpio.input(comp) == 1:
        counter -= 2
    counter += 1
    gpio.output(dac, dec2bin(counter))
    time.sleep(0.003)
    if gpio.input(comp) == 1:
        counter -= 1

    return counter

def dec2bin_into_leds(value): #вывод значения на leds
    bin_val = dec2bin(value)
    gpio.output(dac, bin_val)
    return bin_val

try:
    val = 0
    gpio.output(troyka, 1)
    initial_time = time.time()

    while(val < 207): #207 - это максимум, до которого заряжается конденсатор
        val = adc()
        voltage = val / 256 * max_voltage
        print(f"зарядка: {val}, текущее напряжение = {voltage}")
        dec2bin_into_leds(val)
        time_data.append(time.time() - initial_time)
        voltage_data.append(voltage)

    discharge_start = len(voltage_data)
    gpio.output(troyka, 0)

    #Теперь начнется разрядка конденсатора
    while(val > 168): #168 - это минимум, до которого разрядится конденсатор
        val = adc()
        voltage = val / 256 * max_voltage
        print(f"разрядка: {val}, текущее напряжение = {voltage}")
        dec2bin_into_leds(val)
        time_data.append(time.time() - initial_time)
        voltage_data.append(voltage)


    #остановка измерений
    end_time = time.time()

    with open("./settings.txt", "w") as file:
        file.write(str((end_time - initial_time) / len(voltage_data)))
        file.write(("\n"))
        file.write(str(max_voltage / 256))

    #вывод общей продолжительности, периода одного измерения, средней частоты дискретезации проведенных измерений и шага квантования
    print(f"Общая продолжительность = {end_time - initial_time} сек\n средняя частота дискретизации = {len(voltage_data) / (end_time - initial_time)} \n период измерений T = {1 / (len(voltage_data) / (end_time - initial_time))} \n шаг квантования = {max_voltage / 256}")


finally:
    gpio.output(dac, 0)
    gpio.output(troyka, 0)
    gpio.cleanup()

with open("data.txt", "w") as file:
    for i in range(discharge_start):
        print(f"Зарядка: {voltage_data[i]}", file=file)
    for i in range(discharge_start, len(voltage_data)):
        print(f"Разрядка: {voltage_data[i]}", file=file)

# график U(t)
plt.plot(time_data, voltage_data)
plt.show()
