#!/usr/bin/python
from subprocess import Popen, PIPE
import xml.etree.ElementTree as ET

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
    
print('Enigma version {}'.format(boxdata['e2enigmaversion']))
print('Enigma Image version {}'.format(boxdata['e2imageversion']))
print('Enigma Web version {}'.format(boxdata['e2webifversion']))
print('Network Interface name {}'.format(boxdata['e2name']))
print(' - IP Address {}/{}'.format(boxdata['e2ip'],boxdata['e2netmask']))
print(' - MAC Address {}'.format(boxdata['e2mac']))
print(' - Gateway {}'.format(boxdata['e2gateway']))
