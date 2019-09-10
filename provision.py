#!/usr/bin/python
import os
import sys
import datetime
from subprocess import Popen, PIPE
import fcntl, socket, struct
import xml.etree.ElementTree as ET
from urllib2 import urlopen, URLError, HTTPError

webserverurl="http://server.example.com/"
sshserver="server.example.com"
sshuser="sshuser"
iptv_server=sshserver

def getBoxData():
    try:
        process = Popen(["wget", "-q", "-O", "/tmp/deviceinfo.xml", "http://127.0.0.1/web/deviceinfo"], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
    except OSError:
        raise Exception("Error!")

    deviceinfo = ET.parse('/tmp/deviceinfo.xml')
    boxdata = {}

    for child in deviceinfo.getroot().iter():
        boxdata[child.tag]=child.text
    return boxdata

def getAllMacs():
    macs = {}
    try:
        process = Popen(["wget", "-q", "-O-", "{}/boxes".format(webserverurl)], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()
    except OSError:
        raise Exception("Error, couldn't find this box on the server.")
    for line in output.splitlines():
        macs[line.split(';')[0]]=line.split(';')[1]
    return macs

def dlfile(url):
    try:
        f = urlopen(url)
        print "Downloading " + url
        # Open our local file for writing
        with open(os.path.basename(url), "wb") as local_file:
            local_file.write(f.read())
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url

def main(argv):
    if len(argv) < 4:
        sys.stderr.write("Usage: {} <ssh_password> <iptv_user> <iptv_pass>\n".format(argv[0]))
        return 1

    boxdata=getBoxData()
    macs=getAllMacs()
    mac=boxdata['e2mac'].upper().replace(':','')

    if mac in macs:
      print "Found box {}, starting provisioning.".format(macs[mac])
    else:
      print "Sorry box not found"
      exit(1)

    #Set Hostname
    f = open("/etc/hostname", "w")
    f.write(macs[mac])
    f.close()

    #Downloading necessary software

    #IPTV List Update
    dlfile("{}/updateIPTVlist.sh".format(webserverurl))
    iptv_user=argv[2]
    iptv_pass=argv[3]
    f = open("/etc/iptvlist.conf", "w")
    f.write("SERVER=\"{}\"\nUSER=\"{}\"\nPASS=\"{}\"\n".format(iptv_server,iptv_user,iptv_pass))
    f.close()
    os.system('cp updateIPTVlist.sh /etc/init.d/updateIPTVlist.sh')
    os.system('chmod +x /etc/init.d/updateIPTVlist.sh')
    os.system('ln -sf /etc/init.d/updateIPTVlist.sh /etc/rcS.d/S99updateiptvlist')

    #RemoteSSH
    sshpass=argv[1]
    dlfile("{}/openRemoteSSH.sh".format(webserverurl))
    f = open("/etc/remotessh.conf", "w")
    f.write("HOST=\"{}\"\nUSER=\"{}\"\nPASS=\"{}\"\n".format(sshserver,sshuser,sshpass))
    f.close()
    os.system('cp openRemoteSSH.sh /etc/init.d/openRemoteSSH.sh')
    os.system('chmod +x /etc/init.d/openRemoteSSH.sh')
    os.system('ln -sf /etc/init.d/openRemoteSSH.sh /etc/rcS.d/S98remotessh')

    #MOTD
    dlfile("{}/make-motd".format(webserverurl))
    dlfile("{}/enigmaInfo.py".format(webserverurl))
    os.system('cp make-motd /usr/sbin/make-motd')
    os.system('chmod +x /usr/sbin/make-motd')
    os.system('cp enigmaInfo.py /usr/sbin/enigmaInfo.py')
    os.system('chmod +x /usr/sbin/enigmaInfo.py')
    os.system('/usr/sbin/make-motd > /etc/motd')
    os.system('echo \'Box Provisioned: {}\' > /etc/provisioned'.format(datetime.datetime.now()))

    print("Finished")

if __name__ == '__main__':
    sys.exit(main(sys.argv))
