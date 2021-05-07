#%%
"""
Programa lectura DS18B20 en Raspberry PI.

-Funciona en RPi4.
- DS18B20 conectado en PIN 4 del GPIO.
- Protocolo 1-Wire (habilitarlo desde consola "sudo raspi-config")
- Resistencia de 10K entre Data y +VCC 3V3

Libreria Adafruit:
    https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing
    



"""
#%%

import glob
import time
import datetime

#%%

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#%%

def print_temp():
    '''
    Pido la temperatura al sensor con read_temp, que a su vez llama a read_temp_raw.
    Si el sensor falla (por ejemplo no tiene tension) atrapo el error e imprimo "Error Sensor"
    '''
    try:
        horaMedicion = datetime.datetime.now()
        print(f'{str(horaMedicion.strftime("%Y%m%d_%H%M%S"))} Temp °C = {read_temp()}')
    except:
        print(f'{str(horaMedicion.strftime("%Y%m%d_%H%M%S"))} Temp °C = Error sensor')
    return

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

print_temp() # corro la funcion que larga la medicion e imprime el valor de T en °C
