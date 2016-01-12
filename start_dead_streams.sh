#!/bin/bash
LIST=$(/usr/bin/mysql -uroot -ppassword fos -sN -e "select id,pid from streams where status='0';" | tr -s '\t' ':')
for i in $LIST
do
  ID=$(echo $i | cut -f1 -d:) 
  PID=$(echo $i | cut -f2 -d:) 
  if [ ! -e /proc/$PID ]; then
    curl --user admin:password "http://localhost:8000/streams.php?start=$ID"
    /usr/bin/mysql -uroot -ppassword fos -sN -e "update streams set restarttimes = restarttimes + 1,restarted_at = now() where id=$ID;"
    sleep 2
  fi
done
