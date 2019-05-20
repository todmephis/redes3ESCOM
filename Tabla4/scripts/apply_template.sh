#!/bin/bash
HOST=$1
FILE=$2
HOST16="192.168.1.1"
#R16="R16"
PATH="../templates"
R="R"
SLEEP="/bin/sleep"
SENDFILE="$PATH/$FILE"
N_S="/tftpboot/$FILE"
echo "Enviando template al router $HOST"
sudo cp $SENDFILE /tftpboot/$FILE


if [[ $# -eq 0 || $# -eq 1 ]]; 
	then
		echo "Uso: ./apply_template.sh [target router] [template file]"
		exit 1
	else
		($SLEEP 2; echo "cisco"; $SLEEP 2; echo "cisco"; echo "enable"; $SLEEP 2; echo "cisco"; $SLEEP 2; echo "copy tftp startup-config"; $SLEEP 2; echo "192.168.1.118"; $SLEEP 2; echo $N_S; $SLEEP 2; echo "startup-config"; $SLEEP 5 ; echo "reload"; $SLEEP 2; echo "exit"; ) | /usr/bin/telnet $HOST
fi


#for i in {1..117..4}; do
#if (($i % 4)); then
# echo "get startup-config $PATH$HOST$i.conf" | /usr/bin/tftp $HOST$i
# echo "quit" #| /usr/bin/tftp $HOST$i
#/bin/mv $PATH ~/Documents
echo "Listo"
