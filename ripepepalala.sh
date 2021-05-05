#!/bin/bash
# esto debería correr en CRON upon reboot/start
#   1   . chequea que existe la carpeta de directorio mensual
#   2   . ejecuta el programa Ripepepalala.py en el directorio correspondiente
#         guarda el log en un archivo diario


#### para cargar todo donde tiene que ir
#		$ mkdir -p /home/pi/Infrasonido/{data,programs}
#		$ chmod u+c /home/pi/Infrasonido/rpices_Ripepepalala_init.sh

#se utiliza el programa:
#		$ chmod u+c /home/pi/Infrasonido/programs/ripepepalala_0p1.py
 

#		$ crontab -e
#		@reboot sleep 60 && /home/pi/Infrasonido/ripepepalala.sh

#		$sudo nano /etc/crontab
#		$0 0     * * *   root    reboot

# ADS1115_Ripepepalala
# MONTHLY FOLDER
HOME_DIR_ADS_Ri="/home/pi/Infrasonido/data"
DATE_DIR_ADS_Ri=$(date +%Y-%m)
mkdir -p "${HOME_DIR_ADS_Ri}/${DATE_DIR_ADS_Ri}"
# DAYLY file
FILE_ADS_Ri=ADS_Ri
DATE2=$(date +%F.log)         
INIT_FILE_ADS_Ri=${FILE_ADS_Ri}_${DATE2}
#RUN FPS RUN
cd "${HOME_DIR_ADS_Ri}/${DATE_DIR_ADS_Ri}"
echo "Starting ripepepalala_0p1 program"
python3 -u /home/pi/Infrasonido/programs/ripepepalala_0p1.py &>>${FILE_ADS_Ri}_$DATE2&
