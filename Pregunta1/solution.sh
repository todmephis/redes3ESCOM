#!/bin/bash
PYTHON2=$(which python)
PYTHON3=$(which python3)
NMAP=$(which nmap)
XSLT=$(which xsltproc)
MYPATH=$(pwd)
OUT="outputs"
SUBNETS="subnets.list"
NMAPOUT="network_hosts.xml"
if [ ! -d $MYPATH/$OUT ]
then
    echo "[+]Creando el directorio outputs/"
    mkdir $OUT
    echo "[*]Listo"
    ls -l
else
    echo "[!]El directorio outputs/ ya existe"
fi
echo "[+]Obteniendo subredes"
$PYTHON2 scripts/obtenersubredes.py $OUT/$SUBNETS
echo "[*]Listo"
echo "[+]Nmaping $SUBNETS..."
sudo $NMAP -vvv -sP -iL $OUT/$SUBNETS -oX $OUT/$NMAPOUT
echo "[*]Listo"
echo "[+]Convirtiendo $OUT/$NMAPOUT a $OUT/network_hosts.html"
$XSLT $OUT/$NMAPOUT -o $OUT/network_hosts.html
echo "[*]Listo"
echo "[+]Generando listas de direcciones IP del archivo $OUT/$NMAPOUT"
$PYTHON2 scripts/parse.py $OUT/$NMAPOUT
echo "[*]Listo: $OUT/hostsfound.list"
echo "[+]Analizando hosts:"
read -n 1 -s -r -p "Press any key to continue"
$PYTHON3 scripts/ping.py $OUT/hostsfound.list
echo "[*]Listo..."
