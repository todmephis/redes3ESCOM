#!/bin/bash

PATH='/tftpboot/snmp_manager/scripts'

echo 'Inciando scripts ...'
/bin/bash $PATH/auditor
/bin/bash $PATH/inv_coll.sh

