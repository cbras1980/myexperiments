#!/bin/bash
LIST=$(/usr/bin/mysql -uroot -ppassword fos -sN -e "select id,pid from streams where status > '0';" | tr -s '\t' ':')
for i in $LIST
do
  ID=$(echo $i | cut -f1 -d:) 
  PID=$(echo $i | cut -f2 -d:) 
  if [ ! -e /proc/$PID ]; then
    echo "UPDATE streams SET running='0',status='0',updated_at=NOW(),audio_codec_name='',video_codec_name='' where id='$ID';"
    /usr/bin/mysql -u root -pZxcvbnm00 fos -e "UPDATE streams SET running='0',status='0',updated_at=NOW(),audio_codec_name='',video_codec_name='' where id='$ID';"
  fi
done
curl -o /usr/local/nginx/html/tv.m3u --user admin:password "http://localhost:8000/getfile.php?m3u=true&id=1"
