# Infrasonido
Placa utilizada Raspberry Pi 4 model B rev1.1.
Conversor Analogico Digital (ADC) ADS1115.
Solo un canal de adquisición, en modo continuo, para lograr el sample rate necesario (10 mS entre samples).

RTC DS3231

DHT22 sensor Humedad y Temperatura. 

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
[Ripepepalala.py](https://github.com/niconmn/Infrasonido/blob/main/Infrasonido/ripepepalala_0p1.py)

- Ejecutando el programa comienza a adquirir cada 10 mS.
- Los datos los guardará en un .csv que crea en la carpeta donde esta el programa.
- Como nombre utilizará la fecha y hora del inicio de la adquisicion. 
- Crea un nuevo archivo cada una hora.

## Funcionamiento de los programas y rutinas
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
## Temperatura

Para obtener la medcion de temperatura y humedad del ambiente se utilizó un sensor digital DHT22 que funciona con el protocolo i2c.

## Conexiones DHT22
  - 1 ---> GND
  - 2 ---> PIN 4 Rpi
  - 3 ---> 3V3

La mecanica de trabajo es similar que con el de Infrasonido:

1- Se configuró `contab -e` con la rutina `*/5 * * * *  /home/pi/Temperatura/programs/init_temp.sh` que dispara cada 5 minutos el script `init_temp.sh`.

2- [init_temp.sh](https://github.com/niconmn/Infrasonido/blob/main/Temperatura/init_temp.sh) Crea una carpeta con el "Año-Mes" dentro de ellas crea un archivo `Temperatura_YYYY_MM_dd.log` donde se almacenan los datos generados. Por ultimo llama a el programa `tyhdht_op1_.py`.

3- [tyhdht_op1_.py](https://github.com/niconmn/Infrasonido/blob/main/Temperatura/tyhdht_op1_.py) devuelve la fecha, hora y temperatura (°C) registrada por el sensor con el formato `YYYMMdd_HHmmss Temp °C = XX.XXX`, como los "imprime" en consola terminan escribiedose en el archivo `.log` generado en `init_temp.sh`.

## Directorios
``` Arbol de directorios
/home/pi/Temperatura
├── programs/
	temp_0p1.py
	init_temp.sh
	tyhdht_op1_.py

├── data/
	├── YYYY-MM/
		Temperatura_YYYY-MM-DD.log
```

## RTC DS3231
[Guia para instalar el RTC](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi?view=all)

## Conexiones DS 3231
Es necesario quitar el diodo o la resestencia de 200ohm para evitar la carga de la pila que la dañara en caso de no ser recargable.

  - RTC ---> Rpi

  - VCC ---> +3V
  - GND ---> GND
  - SDA ---> SDA
  - SCL ---> SCL

1° como el I2C ya está habilitado salteamos este paso (en caso de no tener habilitado el I2C habilitarlo desde config.)

2° Chequear los dispositivos conectador por I2C utilizando el comando `sudo i2cdetect -y 1`, generalmente se encuentra el modulo RTC en la direccion 68.

3° agregar la linea `dtoverlay=i2c-rtc,ds3231` al final del archivo `config.txt` (`sudo nano /boot/config.txt`) y reiniciar.

4° Chequear y corroorar nuevamente que el sensor ahora aparezca como UU con el comando `sudo i2cdetect -y 1`.

5° ejecutar los siguientes comandos: `sudo apt-get -y remove fake-hwclock`,`sudo update-rc.d -f fake-hwclock remove` y `sudo systemctl disable fake-hwclock`.

6° Abrir y modificar el archivo con `sudo nano /lib/udev/hwclock-set` y comentar (con`#`) las lineas:

	#if [ -e /run/systemd/system ] ; then
	# exit 0
	#fi
	/sbin/hwclock --rtc=$dev --systz --badyear
	/sbin/hwclock --rtc=$dev --systz
	
7° Setear la fecha al RTC: 

	- Se puede consultar la fecha directo del RTC con el comando `sudo hwclock -r`
	
	- Con la RPi conectada a internet se puede verificar la hora en la RPi con `date`
	
	- Grabar la hora de "date" al RTC con `sudo hwclock -w` y corroborar que este bien con `sudo hwclock -r`
	
	

