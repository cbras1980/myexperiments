#!/bin/bash
CONF_FILE="/etc/remotessh.conf"

if [ -f $CONF_FILE ];
then

. $CONF_FILE

PORT=$(python -c "import random;print(random.randrange(15000,15500))")

#trap cleanup SIGINT SIGTERM SIGKILL SIGSTOP

sshpass -p $PASS ssh $HOST "echo $PORT > $(hostname).txt"
sshpass -p $PASS ssh -N -R $PORT:127.0.0.1:22 $HOST "echo $PORT > $(hostname)"

else

echo "Config file $CONF_FILE not found"

fi
