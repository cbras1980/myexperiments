#!/usr/bin/python3

import json
import urllib.request
import urllib.parse
import base64

tvhhost = '10.69.69.3'
tvhport = 9981
username = 'admin'
password = 'password'

providers = {'1802:000000':'NOS','1814:005211':'MEO'}

url = 'http://{}:{}/api/mpegts/service/grid'.format(tvhhost,tvhport)
data = urllib.parse.urlencode({"limit": "10000"})
data = data.encode('ascii')
request = urllib.request.Request(url)
base64string = base64.b64encode(bytes('%s:%s' % (username, password),'ascii'))
request.add_header("Authorization", "Basic %s" % base64string.decode('utf-8'))
json_data = json.load(urllib.request.urlopen(request,data))

for entry in json_data['entries']:
  s = int(entry['sid'])
  sid=hex(s).split('x')[-1].zfill(4).upper()
  try:
    p = providers[entry['caid']]
  except KeyError:
    p = 'Unknown Provider'
  try:
    #if entry['enabled']:
    print("[{}]\t{}\t{}".format(entry['svcname'].ljust(30),sid,p))
  except KeyError:
    #print("[] - {}".format(sid))
    pass
