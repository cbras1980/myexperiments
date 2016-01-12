#!/bin/bash

SERVERS=$(egrep "(^C\:|^N\:)" /var/etc/multics.cfg | awk '{print $2}')

case $1 in
   config)
        cat <<'EOM'
graph_title MultiCS Average CW per server
graph_vlabel time(ms)
graph_category multics
EOM
for i in $SERVERS
do
SERVER_S=$(echo $i | tr -s '.' '_')
echo "$SERVER_S.label $i"
done
        exit 0;;
esac

HOUR=$(date +%H)
MINUTE=$(date +%H:%M)
MINUS1=$(date -d '-1 minutes' +%H:%M)
MINUS2=$(date -d '-2 minutes' +%H:%M)
MINUS3=$(date -d '-3 minutes' +%H:%M)
MINUS4=$(date -d '-4 minutes' +%H:%M)
MINUS5=$(date -d '-5 minutes' +%H:%M)
TMPFILE=/tmp/parselog_avg.tmp

grep "^\[$MINUS5:.*\]" /var/log/multics.log > $TMPFILE
grep "^\[$MINUS4:.*\]" /var/log/multics.log >> $TMPFILE
grep "^\[$MINUS3:.*\]" /var/log/multics.log >> $TMPFILE
grep "^\[$MINUS2:.*\]" /var/log/multics.log >> $TMPFILE
grep "^\[$MINUS1:.*\]" /var/log/multics.log >> $TMPFILE
grep "^\[$MINUTE:.*\]" /var/log/multics.log >> $TMPFILE

for i in $SERVERS
do
AVG=$(grep 'cw from' $TMPFILE | grep $i | awk '{print $10}' | tr -d \( | tr -d \) | tr -d "ms" | awk '{sum+=$1; count+=1;} END {if (count > 0) { print sum/count } else { print 0}}')
SERVER_S=$(echo $i | tr -s '.' '_')
echo "${SERVER_S}.value $AVG"
done

rm $TMPFILE
