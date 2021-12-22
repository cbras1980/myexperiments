#!/bin/bash
NAS_IP=''
NAS_SHARE=''
MOUNT_FOLDER='/mnt/nfs'

HOSTNAME=$(hostnamectl status | grep hostname | awk '{print $3}')

if [ ! -d ${MOUNT_FOLDER} ]
then
mkdir -p ${MOUNT_FOLDER}
fi

if mountpoint -q ${MOUNT_FOLDER}
then
   echo "NAS NFS already mounted"
else
  echo "Mounting NFS share on ${MOUNT_FOLDER}"
  sudo mount -t nfs ${NAS_IP}:${NAS_SHARE} ${MOUNT_FOLDER}
fi


for i in $(lsblk | grep disk | awk '{print $1}')
do
  sudo sh -c "dd if=/dev/${i} bs=1M status=progress | gzip -9 > ${MOUNT_FOLDER}/${HOSTNAME}.img.gz"
done
echo "Finished"
