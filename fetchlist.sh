#!/bin/bash
LOGFILE=/var/log/fetchlist.log
DT=$(date +%Y%m%d-%H%M)
VHOST=zeus.claranet.pt
mkdir -p /tmp/vhannibal/
cd /tmp/vhannibal/
#wget "http://www.vhannibal.net/download_setting.php?id=8&action=download" -O vhne1.rar
#sleep 2

## ENIGMA1
#if [ -f vhne1.rar ]; then
#LISTFOLDER=$(unrar v vhne1.rar | grep Vhann | sed -e "s/^ //" | cut -f1 -d"/" | grep -v rar | uniq)
#md5sum -c /tmp/vhne1.md5
#if [ $? -ne 0 ]; then
#echo "$DT - Processing list: $LISTFOLDER" >> $LOGFILE
#unrar x vhne1.rar
#mv "$LISTFOLDER" source
#tar xfvz /var/www/zeus.claranet.pt/lista_e1.tar.gz
#rsync -av --delete --update --include-from=/var/www/zeus.claranet.pt/LISTFILE_E1 --exclude="*" source/ lista_e1/
#echo "#NAME ---------- $(stat -c %y lista_e1/services | cut -f1 -d\ ) ----------" > lista_e1/userbouquet.dbe00.tv
#tar czvf /var/www/zeus.claranet.pt/lista_e1.tar.gz lista_e1/
##find /tmp -iname "*.rar" -delete
#md5sum vhne1.rar > /tmp/vhne1.md5
#rm -rf /tmp/vhannibal
#else
#echo "$DT - E1 List has not been updated. Skipping." >> $LOGFILE
#fi
#else
#echo "$DT - File vhne1.rar not found. something went wrong with the download of the file" >> $LOGFILE
#fi

#cd /tmp
#rm -rf /tmp/vhannibal/*
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
#unrar x vhne2.rar
echo "$LISTFOLDER"
mv "$LISTFOLDER" source
tar xfvz /var/www/$VHOST/lista_e2.tar.gz
rsync -av --delete --update --include-from=/var/www/$VHOST/LISTFILE_E2 --exclude="*" source/ lista/
cp /var/www/zeus.claranet.pt/bouquets.tv lista/
echo "#NAME ---------- $(stat -c %y lista/lamedb | cut -f1 -d\ ) ----------" > lista/userbouquet.dbe00.tv
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
