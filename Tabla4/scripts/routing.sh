#!/bin/bash
sudo tunctl -t tap0 -u valtzz
sudo route del -net 0.0.0.0 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.0/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.4/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.8/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.12/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.16/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.20/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.24/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.28/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.32/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.36/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.40/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.44/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.48/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.52/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.56/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.60/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.64/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.68/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.72/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.76/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.80/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.84/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.88/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.92/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.96/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.100/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.104/30 gw 192.168.1.117 dev tap0
sudo route add -net 192.168.1.108/30 gw 192.168.1.117 dev tap0



