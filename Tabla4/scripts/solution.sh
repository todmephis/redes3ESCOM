#!/bin/bash
#Tabla 4
#Is inventory information collected from the network including all chassis, modules, and their serial numbers?
#Are device configurations collected on a regular basis?
#Are changes in device configuration detected, reported, and investigated?
#Is there a well documented base configuration template?
#Can running configurations be audited against config templates?
./routing
./inv_coll.sh #P1
./auditor.sh #P2
python3 changes.py #P3
./auditor.sh A #P4