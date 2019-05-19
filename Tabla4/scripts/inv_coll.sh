#!/bin/bash
HOST="192.168.1."
INV_PATH="/tftpboot/snmp_manager/inventory/"
SLEEP="/bin/sleep"
FILENAME='/tftpboot/snmp_manager/inputs/testrouters.txt'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
R='R'

if test -e "$INV_PATH"; then
	echo -e "Directorios ... [${GREEN}OK${NC}]"
else 
	echo -e "Directorios ... [${RED}MISSING${NC}]"
	/bin/mkdir $INV_PATH
fi

i=1

while read line; do
router=$R$i
echo $router
echo "Obteniendo información de inventario de R$i vía $line..."
#echo "get startup-config $CONF_PATH$R$i" | /usr/bin/tftp $line
($SLEEP 2; echo "cisco"; $SLEEP 5; echo "1234"; echo "show inventory raw"; $SLEEP 2 ) | /usr/bin/telnet $line > $INV_PATH/R$i
status=$?
echo $status
if [ $status == 1 ]; then
	echo "j"
	continue

else
	echo "quit" #| /usr/bin/tftp $HOST$i
	/usr/bin/python3 inv_proc.py $router
	i=$((i+1))
fi

done < $FILENAME

