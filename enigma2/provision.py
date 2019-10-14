#!/usr/bin/python
import os
import sys
import datetime
from subprocess import Popen, PIPE
import fcntl, socket, struct
import xml.etree.ElementTree as ET
from urllib2 import urlopen, URLError, HTTPError

webserverurl="http://mephisto.malignia.net/enigma"
sshserver="mephisto.malignia.net"
sshuser="boxes"
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

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

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
    #mac=boxdata['e2mac'].upper().replace(':','')
    mac=getHwAddr('eth0').upper().replace(':','')

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

    #IPTV Lists Update
    dlfile("{}/update-iptv-list".format(webserverurl))
    iptv_user=argv[2]
    iptv_pass=argv[3]
    f = open("/etc/iptvlist.conf", "w")
    f.write("SERVER=\"{}\"\nUSER=\"{}\"\nPASS=\"{}\"\n".format(iptv_server,iptv_user,iptv_pass))
    f.close()
    os.system('cp update-iptv-list /etc/init.d/update-iptv-list')
    os.system('chmod +x /etc/init.d/update-iptv-list')
    os.system('/usr/sbin/update-rc.d -v update-iptv-list start 99 3 . stop 99 6 .')

    #SAT List update
    dlfile("{}/update-sat-list".format(webserverurl))
    dlfile("{}/update-sat-list.conf".format(webserverurl))
    os.system('cp update-sat-list /etc/init.d/update-sat-list')
    os.system('chmod +x /etc/init.d/update-sat-list')
    os.system('cp update-sat-list.conf /etc/init.d/update-sat-list.conf')
    os.system('/usr/sbin/update-rc.d -v update-sat-list start 99 3 . stop 99 6 .')

    #NTPD
    dlfile("{}/ntp.conf".format(webserverurl))
    os.system('cp ntp.conf /etc/ntp.conf')
    dlfile("{}/ntpd".format(webserverurl))
    os.system('cp ntpd /etc/init.d/ntpd')
    os.system('chmod +x /etc/init.d/ntpd')
    os.system('/usr/sbin/update-rc.d -v ntpd start 70 3 . stop 70 6 .')
    os.system('/etc/init.d/ntpd start')
    dlfile("{}/check-clock-sync".format(webserverurl))
    os.system('cp check-clock-sync /etc/init.d/check-clock-sync')
    os.system('chmod +x /etc/init.d/check-clock-sync')
    os.system('/usr/sbin/update-rc.d -v check-clock-sync start 71 3 . stop 71 6 .')

    #RemoteSSH
    #sshpass=argv[1]
    #dlfile("{}/remote-ssh".format(webserverurl))
    #dlfile("{}/sshpass".format(webserverurl))
    #f = open("/etc/remotessh.conf", "w")
    #f.write("HOST=\"{}\"\nUSER=\"{}\"\nPASS=\"{}\"\nLOW=15000\nHIGH=15500\n".format(sshserver,sshuser,sshpass))
    #f.close()
    #os.system('cp sshpass /usr/bin/sshpass')
    #os.system('chmod +x /usr/bin/sshpass')
    #os.system('cp remote-ssh /etc/init.d/remote-ssh')
    #os.system('chmod +x /etc/init.d/remote-ssh')
    #os.system('/usr/sbin/update-rc.d -v remote-ssh start 90 3 . stop 90 6 .')

    #OpenVPN
    openvpnpass=argv[1]
    os.system('opkg install openvpn')
    #os.system('rm -rf /etc/openvpn/*.conf')
    dlfile("{}/cs.conf".format(webserverurl))
    dlfile("{}/ca.crt".format(webserverurl))
    os.system('cp cs.conf /etc/openvpn/cs.conf')
    os.system('cp ca.crt /etc/openvpn/ca.crt')
    f = open("/etc/openvpn/auth.txt", "w")
    f.write("{}\n{}".format(macs[mac],openvpnpass))
    f.close()
    os.system('/usr/sbin/update-rc.d -v openvpn start 90 3 . stop 90 6 .')

    #MOTD
    dlfile("{}/make-motd".format(webserverurl))
    dlfile("{}/update-motd".format(webserverurl))
    dlfile("{}/enigmaInfo.py".format(webserverurl))
    os.system('cp make-motd /usr/sbin/make-motd')
    os.system('cp update-motd /etc/init.d/update-motd')
    os.system('chmod +x /usr/sbin/make-motd')
    os.system('chmod +x /etc/init.d/update-motd')
    os.system('/usr/sbin/update-rc.d -v update-motd start 99 3 . stop 99 6 .')
    os.system('cp enigmaInfo.py /usr/sbin/enigmaInfo.py')
    os.system('chmod +x /usr/sbin/enigmaInfo.py')
    os.system('/usr/sbin/make-motd > /etc/motd')
    os.system('echo \'Box Provisioned: {}\' > /etc/provisioned'.format(datetime.datetime.now()))

    print("Finished")

if __name__ == '__main__':
    sys.exit(main(sys.argv))
