#!/bin/bash

case $1 in
   config)
        cat <<'EOM'
graph_title MultiCS Stats
graph_vlabel count
graph_category multics
ecm_total.label ecm_total
ecm_to.label ecm_to
ecm_from.label ecm_from
cw_total.label cw_total
cw_to.label cw_to
cw_from.label cw_from
EOM
        exit 0;;
esac

HOUR=$(date +%H)
MINUTE=$(date +%H:%M)
MINUS1=$(date -d '-1 minutes' +%H:%M)
MINUS2=$(date -d '-2 minutes' +%H:%M)
MINUS3=$(date -d '-3 minutes' +%H:%M)
MINUS4=$(date -d '-4 minutes' +%H:%M)
MINUS5=$(date -d '-5 minutes' +%H:%M)
TMPFILE=/tmp/parselog.tmp

grep "^\[$MINUS5:.*\]" /var/log/multics.log > $TMPFILE
grep "^\[$MINUS4:.*\]" /var/log/multics.log >> $TMPFILE
grep "^\[$MINUS3:.*\]" /var/log/multics.log >> $TMPFILE
grep "^\[$MINUS2:.*\]" /var/log/multics.log >> $TMPFILE
grep "^\[$MINUS1:.*\]" /var/log/multics.log >> $TMPFILE
grep "^\[$MINUTE:.*\]" /var/log/multics.log >> $TMPFILE

ECMTOTAL=$(grep 'ecm' $TMPFILE | wc -l)
ECMTO=$(grep 'ecm to' $TMPFILE | wc -l)
ECMFROM=$(grep 'ecm from' $TMPFILE | wc -l)
CWTOTAL=$(grep 'cw' $TMPFILE | wc -l)
CWFROM=$(grep 'cw from' $TMPFILE | wc -l)
CWTO=$(grep 'cw to' $TMPFILE | wc -l)
# ECMS stats
echo "ecm_total.value $ECMTOTAL"
echo "ecm_to.value $ECMTO"
echo "ecm_from.value $ECMFROM"
echo "cw_total.value $CWTOTAL"
echo "cw_to.value $CWTO"
echo "cw_from.value $CWFROM"

rm $TMPFILE
