#!/bin/sh
CONF_FILE="/etc/iptvlist.conf"

if [ -f $CONF_FILE ]; then
  . $CONF_FILE
else
  echo "Configuration file not found"
  exit 1
fi



REPLACE=$(echo ${SERVER} | cut -f1 -d\.)

rm -rf /etc/enigma2/userbouquet.dbe00.tv
rm -rf /etc/enigma2/userbouquet.iptv.tv

wget -O /etc/enigma2/userbouquet.iptv.tv "http://${USER}:${PASS}@${SERVER}:9981/playlist/e2/channels"

sed -i "s/${REPLACE}/${USER}\:${PASS}@${REPLACE}/" /etc/enigma2/userbouquet.iptv.tv


C=$(cat /etc/enigma2/bouquets.tv | grep userbouquet.iptv.tv | wc -l)
if [ $C -eq 0 ]; then
cat << EOF >> /etc/enigma2/bouquets.tv
#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.iptv.tv" ORDER BY bouquet
EOF
fi

C=$(cat /etc/enigma2/bouquets.tv | grep userbouquet.dbe00.tv | wc -l)
if [ $C -eq 0 ]; then
cat << EOF >> /etc/enigma2/bouquets.tv
#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.dbe00.tv" ORDER BY bouquet
EOF
fi

NOW=$(date "+%Y-%m-%d")
cat << EOF > /etc/enigma2/userbouquet.dbe00.tv
#NAME ---------- ${NOW} ----------
#Big thanks to MEPHISTO
EOF

wget -O- "http://localhost/web/servicelistreload?mode=2"

echo "Finished!"
