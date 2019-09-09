#!/bin/bash
#################################################
# Create config file with:
# USER="username"
# PASS="password"
# HOST="hostname"
# Software needed: sshpass, python
#################################################
CONF_FILE="/etc/remotessh.conf"

if [ -f $CONF_FILE ]; then
  . $CONF_FILE
  PORT=$(python -c "import random;print(random.randrange(15000,15500))")
  sshpass -p $PASS ssh $USER@$HOST "echo $PORT > $(hostname).txt"
  sshpass -p $PASS ssh -N -R $PORT:127.0.0.1:22 $USER@$HOST "echo $PORT > $(hostname)"
else
  echo "Config file $CONF_FILE not found"
fi
