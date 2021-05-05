# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 11:24:50 2021

@author: NCLS

Basicamente una copia del programa de Diego Perez rpices_fpss250b.py

"""
import time
import datetime
import sys
import board
import busio
import os
import os.path
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode

#%%
sys.stdout.write("=================================""\n")
sys.stdout.write("           CNEA - ICES           ""\n")
sys.stdout.write("    Infrasonido - Ripepepalala   ""\n")
sys.stdout.write("=================================""\n")

#%% Archivo de almacenamiento de datos

nombrearchivo = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) # agrego strftime para que se lean bien en otros SO
#nombre_fichero = os.path.join(os.sep, "home", "pi", "nico_ADS1115", "datos", nombrearchivo)
file = open(nombrearchivo + ".csv" ,'w+')
sys.stdout.write("Archivo de trabajo abierto correctamente: ")
sys.stdout.write(str(nombrearchivo)+ ".csv" + "\n")


#/home/pi/nico_ADS1115/datos

#%% Config ADS1115 I2C

i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000) # Create the I2C bus para alta velocidad
ads = ADS.ADS1115(i2c) # Create the ADC object using the I2C bus
chan = AnalogIn(ads, ADS.P0) # Create single-ended input on channel 0
ads.mode = Mode.CONTINUOUS #modo funcionamiento ADC
ads.data_rate = 128 #seteo del sample rate del ADS1115
_ = chan.value
muestras = 0

#%% Temporizadores: Archivos y muestreo
sample_interval = 1.0 / 100 # Intervalo entre muestras 0.01 Seg

#Control de grabacion de archivos cada una hora

start = datetime.datetime.now()
time_diff = datetime.timedelta(days=0, seconds=3600, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

#Control de temporiazacion del sensor de Infrasonido
sleepInfra=datetime.timedelta(days=0, seconds=sample_interval , microseconds=0, milliseconds=0, minutes=0, hours=0,weeks=0)
startInfra=start

#%% Loop General

try:
    while True:
        if (not ((datetime.datetime.now() - start) > time_diff)):

            if((datetime.datetime.now() - startInfra) >= sleepInfra):
                startInfra=datetime.datetime.now()		  		    
                file.write(f'{muestras} , {str(datetime.datetime.now())} , {str(chan.voltage)} , {str(chan.value)} \n')					
                muestras = muestras + 1

        else:
            muestras = 0
            start = datetime.datetime.now()
            #nombre_fichero = os.path.join(os.sep, "home", "pi", "nico_ADS1115", "datos", start.strftime("%Y%m%d_%H%M%S"))
            file = open(str(start.strftime("%Y%m%d_%H%M%S")) + ".csv",'w+')
            sys.stdout.write("Archivo de trabajo abierto correctamente: ")
            sys.stdout.write(str(start.strftime("%Y%m%d_%H%M%S"))+ ".csv" + "\n")
            sys.stdout.flush()
            
except KeyboardInterrupt: 
    sys.stdout.write("Interrupcion de teclado, cerrando archivo\n")
    sys.stdout.flush()
    file.close()
