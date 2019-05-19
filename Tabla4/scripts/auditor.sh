#!/bin/bash
echo "Obteniendo configuraciones"
HOST="192.168.1."
HOST16="192.168.1.1"
#R16="R16"
CONF_PATH="/tftpboot/snmp_manager/routerconfig"
T_PATH="/tftpboot/snmp_manager/templates"
O_PATH="/tftpboot/snmp_manager/outputs"
CH_PATH="$O_PATH/changes"
R="R"
SLEEP="/bin/sleep"
SENDFILE="R16.tmp"
FILENAME="/tftpboot/snmp_manager/outputs/$2"
echo $FILENAME
#FILENAME='/tftpboot/snmp_manager/inputs/routers.txt'
#FILENAME=$FILEPATH/$FILE 


RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

if test -e "$CONF_PATH" && test -e "$T_PATH" && test -e "$O_PATH" && test -e "$CH_PATH"; then
	echo -e "Directorios ... [${GREEN}OK${NC}]"
else 
	/bin/mkdir $CONF_PATH
	/bin/mkdir $T_PATH
	/bin/mkdir $O_PATH
	/bin/mkdir $CH_PATH

fi
a=16
i=1
while read line; do
# 
echo "Obteniendo la configuración de $line..."
echo "get startup-config $CONF_PATH/$line" | /usr/bin/tftp $line
echo "quit" #| /usr/bin/tftp $HOST$i
if [[ $1 = 'T' ]]; then 
	#echo "El archivo de configuración ha cambiado, la plantilla se restaurará." 
	#echo "Restaurando plantilla en el router $R$i ..."
	echo "Comparando configuración de $line con su template ..."
	diff --brief <(sort $CONF_PATH/$line) <(sort $T_PATH/$line) >/dev/null
	comp_value=$?
	if [ $comp_value -eq 1 ]; then 
		echo "El archivo de configuración ha cambiado, la plantilla cambiará." 
		echo "Cambiando plantilla  del router $R$i ..."
		echo "Plantilla cambiada"
		sudo cp $CONF_PATH/$line $T_PATH/$line
		#($SLEEP 2; echo "enable"; $SLEEP 2; echo "1234"; $SLEEP 2; echo "copy tftp startup-config"; $SLEEP 2; echo "192.168.1.118"; $SLEEP 2; echo $T_PATH$R$i; $SLEEP 2; echo "startup-config"; $SLEEP 5 ; echo "reload"; $SLEEP 2; echo "exit"; ) | /usr/bin/telnet $line	
	else 
		echo "No se han encontrado cambios"		
	fi
elif [[ $1 = 'A' ]]; then
	echo "Investigando cambios ..."
	diff --brief <(sort $CONF_PATH/$line) <(sort $T_PATH/$line) >/dev/null
	comp_value=$?
	echo $comp_value
	if [ $comp_value -eq 1 ]; then
		diff -y $CONF_PATH/$line $T_PATH/$line > $CH_PATH/changes_$line
		echo "Cambios detectados: Se han reportado en $CH_PATH/changes_$line"
	else 
		echo "No se han encontrado cambios"
	fi
fi
i=$((i+1))
done < $FILENAME

/bin/ls $CONF_PATH
echo "Listo"


#if [[ $1 = 'T' ]];
#then 
#	echo "Comparando con templates..."
#	diff --brief <(sort $CONF_PATH/$R$) <(sort /tftpboot/configR1) >/dev/null
#	comp_value=$?
