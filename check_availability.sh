#!/bin/bash
urls="https://www.samedaysupplements.com/gl3-l-glutamine-by-ast-sports-science-750-mg-500-caps.html https://www.samedaysupplements.com/mass-tech-by-muscletech-weight-gainer.html https://www.samedaysupplements.com/bcaa-complex-2200-by-dymatize-nutrition-400-caplets-eu-version.html https://www.samedaysupplements.com/hydroxyelite-by-hi-tech-pharmaceuticals-90-caps.html"
s="";
for i in $urls; do
s=$s$(curl -s $i | grep -i "out of stock" | wc -l)
done
if [ -e /tmp/suplements_status ]; then
status=$(cat /tmp/suplements_status)
fi
echo $s > /tmp/suplements_status
message=""
if [ "x$s" != "x$status" ];then
if [ "x${s:0:1}" == "x0" ] && [ "x${status:0:1}" == "x1" ]; then
message=$message"GL3 is now available"
fi
if [ "x${s:1:1}" == "x0" ] && [ "x${status:1:1}" == "x1" ]; then
message=$message" Mass is now available"
fi
if [ "x${s:2:1}" == "x0" ] && [ "x${status:2:1}" == "x1" ]; then
message=$message" BCAA is now available"
fi
if [ "x${s:3:1}" == "x0" ] && [ "x${status:3:1}" == "x1" ]; then
message+=" Hydro is now available"
fi
if [ "x$message" != "x" ]; then
/root/send_sms.py 41764405888 "$message"
fi
fi
