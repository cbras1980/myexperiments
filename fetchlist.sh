#!/bin/bash
# Testing github and atom integration
LOGFILE=/var/log/fetchlist.log
DT=$(date +%Y%m%d-%H%M)
VHOST=zeus.claranet.pt
mkdir -p /tmp/vhannibal/
cd /tmp/vhannibal/
#wget "http://www.vhannibal.net/download_setting.php?id=8&action=download" -O vhne1.rar
#sleep 2

mkdir -p /tmp/vhannibal/
cd /tmp/vhannibal/

#sleep 3

#wget "http://www.vhannibal.net/download_setting.php?id=16&action=download" -O vhne2.rar
#wget "http://zeus.claranet.pt/vhne2.rar" -O vhne2.rar 2> /dev/null
curl -o vhne2.zip "http://www.vhannibal.net/download_setting.php?id=16&action=download"
sleep 2

## ENIGMA2
#if [ -f vhne2.rar ]; then
if [ -f vhne2.zip ]; then
unzip vhne2.zip > /dev/null 2> /dev/null
#LISTFOLDER=$(unrar v vhne2.rar | grep Vhann | sed -e "s/^ //" | cut -f1 -d"/" | grep -v rar | uniq)
LISTFOLDER=$(find . ! -path . -type d)
md5sum -c /tmp/vhne2.md5 2> /dev/null
if [ $? -ne 0 ]; then
echo "$DT - Processing list: $LISTFOLDER" >> $LOGFILE
echo "$LISTFOLDER"
mv "$LISTFOLDER" lista
#tar xfvz /var/www/$VHOST/lista_e2.tar.gz
#rsync -av --delete --update --include-from=/tmp/vhannibal/lista/LISTFILE_E2 --exclude="*" source/ lista/
#rsync -DHCPRavz source/ lista/

## Build bouquets.tv file
echo "#NAME Bouquets (TV)" > lista/bouquets.tv
for i in meo nos movistar; do
echo "Processing $i"
LIST=$(grep -i "name $i" * -R | head -n1 | cut -f1 -d: | cut -f2 -d\/)
for j in $LIST; do
echo "Adding $j"
echo "#SERVICE: 1:7:1:0:0:0:0:0:0:0:$j" >> lista/bouquets.tv
done
done
echo "#SERVICE: 1:7:1:0:0:0:0:0:0:0:userbouquet.dbe00.tv" >> lista/bouquets.tv

echo "#NAME ---------- $(stat -c %y lista/lamedb | cut -f1 -d\ ) ----------" > lista/userbouquet.dbe00.tv
echo "#Big thanks to MEPHISTO" >> lista/userbouquet.dbe00.tv

tar czvf /var/www/$VHOST/lista_e2.tar.gz lista/
#find /tmp -iname "*.rar" -delete
md5sum vhne2.zip > /tmp/vhne2.md5 2> /dev/null
#rm -rf /tmp/vhannibal
else
echo "$DT - E2 List has not been updated. Skipping." >> $LOGFILE
fi
else
echo "$DT - File vhne2.rar not found. something went wrong with the download of the file" >> $LOGFILE
fi

rm -rf /tmp/vhannibal/
