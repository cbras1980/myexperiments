#!/usr/bin/python3
import json
import requests
import sys

#set the variables
api='api.name.com'
user='user'
token='token'
domain='example.com'
host='record'

recordid=''
#check if the record exists for the specified domain in name.com
resp = requests.get('https://{}/v4/domains/{}/records/'.format(api,domain), auth=(user, token))
records = (resp.json())['records']
for record in records:
  if record['type'] is 'A':
    if record['host'] == host:
      recordid=record['id']
      print("Found record ID: {} - Host: {}.{}".format(record['id'],record['host'],record['domainName']))
      break

#If record was not found, exit with error code 1
if recordid is '':
  print("Record {}.{} not found. Please create it first.".format(host,domain))
  sys.exit(1)

#get current IP defined for the host in name.com
resp = requests.get('https://{}/v4/domains/{}/records/{}'.format(api,domain,recordid), auth=(user, token))
#print(json.dumps(resp.json(), indent=4, sort_keys=True))
actip = json.loads(json.dumps(resp.json()))['answer']

#get external ip address using ipfy.org API
resp = requests.get('https://api.ipify.org?format=json')
curip = json.loads(json.dumps(resp.json()))['ip']

if actip == curip:
  print("No update needed")
else:
  data = '{"host":"'+host+'","type":"A","answer":"'+curip+'","ttl":300}'
  resp = requests.put('https://{}/v4/domains/{}/records/{}'.format(api,domain,recordid), auth=(user, token), data=data)
  print("Updating {}.{} from {} to {}".format(host,domain,actip,curip))
