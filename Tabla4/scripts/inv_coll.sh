#!/bin/bash
HOST="192.168.1."
INV_PATH="../inventory"
SLEEP="/bin/sleep"
FILENAME='../inputs/routers.txt'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
R='R'
USER="cisco"
PASS="cisco"

if test -e "$INV_PATH"; then
	echo -e "Directorios ... [${GREEN}OK${NC}]"
else 
	echo -e "Directorios ... [${RED}MISSING${NC}]"
	/bin/mkdir $INV_PATH
fi

i=1

while read line; do
router=$R$i
#echo $router
	
echo "Obteniendo información de inventario de R$i vía $line..."
#echo "get startup-config $CONF_PATH$R$i" | /usr/bin/tftp $line
#echo $line
($SLEEP 2;  echo "cisco"; $SLEEP 2; echo "cisco"; $SLEEP 2; echo "enable"; $SLEEP 2; echo "cisco"; echo "show inventory raw"; $SLEEP 2 ) | /usr/bin/telnet $line > $INV_PATH/R$i 
echo "quit" #| /usr/bin/tftp $HOST$i
/usr/bin/python3 inv_proc.py $router
#status=$?
#echo $status
#if [ $status == 1 ]; then
#	echo "j"
#	continue

#else
i=$((i+1))
done < $FILENAME