#!/bin/bash
#################################################
# Create config file with:
# USER="username"
# PASS="password"
# HOST="hostname"
# Software needed: sshpass, python
#################################################
CONF_FILE="/etc/remotessh.conf"

# PORT RANGE
LOW=15000
HIGH=15500

if [ -f $CONF_FILE ]; then
  . $CONF_FILE
  PORT=$(python -c "import random;print(random.randrange($LOW,$HIGH))")
  sshpass -p $PASS ssh -y -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" $USER@$HOST "echo $PORT > $(hostname).txt"
  sshpass -p $PASS ssh -y -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" -N -R $PORT:127.0.0.1:22 $USER@$HOST &
else
  echo "Config file $CONF_FILE not found"
fi
