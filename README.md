# Infrasonido
Placa utilizada Raspberry Pi 4 model B rev1.1.
Conversor Analogico Digital (ADC) ADS1115.
Solo un canal de adquisición, en modo continuo, para lograr el sample rate necesario (10 mS entre samples).

## Conexiones ADS1115 (en puerto GPIO)
  - PIN SDA Rpi a SDA ADS1115
  - PIN SCL Rpi a SCL ADS1115
  - PIN 3V a VDD ADS1115
  - PIN GND a GND ADS1115
  - No se realizan modificaciones en en address en caso de conectar solo un ADC a la Rpi.

## Libreria ADS1115 "Adafruit Circuipython"

https://circuitpython.readthedocs.io/projects/ads1x15/en/latest/
https://circuitpython.readthedocs.io/projects/ads1x15/en/latest/api.html#analog-in
https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15/blob/master/adafruit_ads1x15/ads1x15.py
https://circuitpython.readthedocs.io/projects/ads1x15/en/latest/api.html#analog-in

## Instalaciones

1° Habilitar I2C (`sudo raspi-config`)

2° Cargar las libreria de Circuipython.

## Programa Ripepepalala.py
[Ripepepalala.py](./Infrasonido/programas)

- Ejecutando el programa comienza a adquirir cada 10 mS.
- Los datos los guardará en un .csv que crea en la carpeta donde esta el programa.
- Como nombre utilizará la fecha y hora del inicio de la adquisicion. 
- Crea un nuevo archivo cada una hora.

## Corriendo en Raspberry
1- La raspberry se configura para reiniciar todos los dias a las 00:00 hs.  Esto se debe configurar en `sudo nano /etc/crontab` y dentro de ese archivo `$0 0     * * *   root    reboot`.

2- Para que el programa comience despues de cada reinicio se debe configurar una tarea en `crontab -e`: `@reboot sleep 60 && /home/pi/Infrasonido/ripepepalala.sh`. De esta manera, despues de cada reinicio aguarda 60 segundos y "llama" a el archivo `ripepepalala.sh`

3- Las rutinas en `ripepepalala.sh` se encargan de crear las carpetas "Año Mes" donde se guardan los datos (un archivo por hora) y el log de eventos (creacion de archivos, etc) y inician el programa `ripepepalala_0p1.py`.

4- Directorios:
``` Arbol de directorios
/home/pi/Infrasonido
├── programs/
	ripepepalala_0p1.py
	ripepepalala.sh

├── data/
	├── YYYY-MM/
		ADS_Ri_YYYY-MM-DD.log
		"YYYY-MM-dd HH:mm:ss.6f.csv"
```


