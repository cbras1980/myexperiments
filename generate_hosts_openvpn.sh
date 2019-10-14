#!/bin/bash
for i in $(find /etc/openvpn/ccd -type f | xargs); do 
HOST=$(basename $i)
IP=$(cat $i | awk '{print $2}')
echo $IP $HOST.vpn
done
