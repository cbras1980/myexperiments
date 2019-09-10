#!/usr/bin/python3
import os
import json
import requests
import sys
import socket
import subprocess

webserver='server.example.com'

#print(data.text)
def add_record(hostname,line):
        myCmd = 'upnpc -e openupnp-{} -a TO FIX!!! {} > /dev/null'.format(hostname,line)
        #print("Adding record line")
        #print(myCmd)
        os.system(myCmd)

def del_all_records():
    records = get_existing_records()
    for line in records:
        del_record(hostname,line)

def del_record(hostname,line):
    myCmd = "upnpc -L | grep openupnp-{} | awk '{{print $2\" \"$3}}' | cut -f1 -d\- | awk '{{print $2\" \"$1}}' | grep '{}'".format(hostname,line)
    #print(myCmd)
    p = subprocess.Popen(myCmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    #records = get_existing_records()
    #print(records)
    for line in output.splitlines():
        #print("Deleting record line")
        myCmd = "upnpc -d {} > /dev/null".format(line.decode('utf8'))
        #print(myCmd)
        os.system(myCmd)

def exists_record(hostname,port_protocol):
    for line in data.text.splitlines():
        tokens=port_protocol.split()
        myCmd = 'upnpc -L | grep {} | grep \'{}  {}\''.format(hostname,tokens[2],tokens[1])
        #print(myCmd)
        p = subprocess.Popen(myCmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        #print(output)
        if output.decode('utf8'):
            return True
        return False

def get_existing_records():
    myCmd = "upnpc -L | grep openupnp-{} | awk '{{print $2\" \"$3}}' | cut -f1 -d\- | awk '{{print $2\" \"$1}}'".format(hostname)
    #myCmd = "upnpc -L | grep openupnp-{}".format(hostname)
    #print(myCmd)
    p = subprocess.Popen(myCmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    records = []
    for line in output.splitlines():
        records.append(line.decode('utf8'))
    return records

try:
    hostname=os.uname()[1]
    hostip = socket.gethostbyname(hostname)

    url='http://{}/{}'.format(webserver,hostname)
    data = requests.get(url)
    data.raise_for_status()
    #delete_all_records()
    records=get_existing_records()
    #print(records)
    for line in data.text.splitlines():
        #if exists_record(hostname,line):
        #print("Line value: {}".format(line))
        tokens = line.split(" ")
        tmp = "{} {}".format(tokens[1],tokens[2])
        if tmp in records:
            #print("Record already exists")
            records.remove(tmp)
            continue
        else:
            add_record(hostname,line)
    for line in records:
        del_record(hostname,line)
except requests.exceptions.HTTPError as e:
    print("{} not found on server - deleting records".format(url))
    del_all_records()
    sys.exit(1)
except requests.exceptions.RequestException as e:  # This is the correct syntax
    print("Couldn't connect to {}".format(webserver))
    del_all_records()
    sys.exit(1)

