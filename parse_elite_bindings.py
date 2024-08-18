#!/usr/bin/python3 -v

# Parses an elite bindings file and inserts all entries in a local SQLite Database
# ToDo: Write the contents of the DB back into the binds file in XML format
import xml.etree.ElementTree as ET
import sqlite3

def create_tables(conn):
  cursor = conn.cursor()
  cursor.execute('''CREATE TABLE IF NOT EXISTS controls (controlid integer primary key autoincrement, name text, value integer)''')
  cursor.execute('''CREATE TABLE IF NOT EXISTS triggers (triggerid integer primary key autoincrement,type text,value integer,controlid integer,keyid integer)''')
  cursor.execute('''CREATE TABLE IF NOT EXISTS devices (deviceid integer primary key autoincrement, name text)''')
  cursor.execute('''CREATE TABLE IF NOT EXISTS keys (keyid integer primary key autoincrement, name text, deviceid integer)''')
  cursor.execute('''CREATE TABLE IF NOT EXISTS modifiers (type text, triggerid integer,keyid integer, value integer)''')
  conn.commit()

def insertControl(conn,name,value):
  sql = "INSERT INTO controls (name,value) VALUES ('{}','{}')".format(name,value)
  #print(sql)
  cursor = conn.cursor()
  cursor.execute(sql)
  conn.commit()

def insertTrigger(conn,typ,value,controlid,keyid):
  sql = "INSERT INTO triggers (type,value,controlid,keyid) VALUES ('{}','{}','{}','{}')".format(typ,value,controlid,keyid)
  #print(sql)
  cursor = conn.cursor()
  cursor.execute(sql)
  conn.commit()

def insertDevice(conn,name):
  sql = "INSERT INTO devices (name) VALUES ('{}')".format(name)
  #print(sql)
  cursor = conn.cursor()
  cursor.execute(sql)
  conn.commit()

def insertKey(conn,name,deviceid):
  sql = "INSERT INTO keys (name,deviceid) VALUES ('{}','{}')".format(name,deviceid)
  #print(sql)
  cursor = conn.cursor()
  cursor.execute(sql)
  conn.commit()

def insertModifier(conn,typ,value,triggerid,keyid):
  sql =  "INSERT INTO modifiers (type,value,triggerid,keyid) VALUES ('{}','{}','{}','{}')".format(typ,value,triggerid,keyid)
  #print(sql)
  cursor = conn.cursor()
  cursor.execute(sql)
  conn.commit()

def getControlIDByName(conn,name):
  sql = "SELECT controlid FROM controls WHERE name = '{}'".format(name)
  #print(sql)
  cursor = conn.cursor()
  rows = cursor.execute(sql).fetchall()
  if len(rows) == 0: return 0
  return rows[0][0]

def getDeviceIDByName(conn,name):
  sql = "SELECT deviceid FROM devices WHERE name = '{}'".format(name)
  #print(sql)
  cursor = conn.cursor()
  rows = cursor.execute(sql).fetchall()
  #print(rows)
  #print(len(rows))
  if len(rows) == 0: return 0
  return rows[0][0]

def getControlIDByName(conn,name):
  sql = "SELECT controlid FROM controls WHERE name = '{}'".format(name)
  #print(sql)
  cursor = conn.cursor()
  rows = cursor.execute(sql).fetchall()
  if len(rows) == 0: return 0
  return rows[0][0]

def getTriggerIDByControlIDTypeID(conn,controlid,typ):
  sql = "SELECT triggerid FROM triggers WHERE controlid = '{}' and type = '{}'".format(controlid,typ)
  #print(sql)
  cursor = conn.cursor()
  rows = cursor.execute(sql).fetchall()
  if len(rows) == 0: return 0
  return rows[0][0]

def getKeyIDByDeviceIDName(conn,deviceid,name):
  sql = "SELECT keyid FROM keys WHERE deviceid = '{}' and name = '{}'".format(deviceid,name)
  #print(sql)
  cursor = conn.cursor()
  rows = cursor.execute(sql).fetchall()
  if len(rows) == 0: return 0
  return rows[0][0]

def main():
  conn = sqlite3.connect('bindings.db')
  cursor = conn.cursor()

  tree = ET.parse('elite.binds')
  root = tree.getroot()

  create_tables(conn)

  for control in root:
    control_name = control.tag
    if len(control) > 0:
      insertControl(conn,control.tag,None)
      controlid = getControlIDByName(conn,control.tag)
      for trigger in iter(control):
        typ = trigger.tag

        if typ in ['Primary','Secondary','Binding']:
          device = trigger.attrib['Device']
          key =  trigger.attrib['Key']

          # Check if device exists and gets it's ID
          deviceid = getDeviceIDByName(conn,device)
          #print("DeviceID: {}".format(deviceid))
          # If device does not exists, adds device do DB
          if deviceid == 0:
            insertDevice(conn,device)
            deviceid = getDeviceIDByName(conn,device)

          # Check if key exists and gets the ID
          keyid = getKeyIDByDeviceIDName(conn,deviceid,key)
          #print("KeyID: {}".format(keyid))
          # If key does not exists, adds key to DB
          if keyid == 0:
            insertKey(conn,key,deviceid)
            keyid = getKeyIDByDeviceIDName(conn,deviceid,key)

          # Now adds the trigger to the DB
          insertTrigger(conn,typ,None,controlid,keyid)

          # Checks if any modifiers existye for this trigger
          if len(trigger) > 0:
            # Is yes gets the trigger ID to relate
            triggerid = getTriggerIDByControlIDTypeID(conn,controlid,typ)
            #print("TriggerID: {}".format(triggerid))
            for modifier in iter(trigger):
              #print(modifier.tag, modifier.attrib)
              if modifier.tag == 'Modifier':
                mod_device = modifier.attrib['Device']
                mod_key = modifier.attrib['Key']

                # Needs to check again if the Device existx in the DB and gets the ID
                mod_deviceid = getDeviceIDByName(conn,mod_device)
                # If device does not exists, adds device do DB
                if mod_deviceid == 0:
                  insertDevice(conn,mod_device)
                  mod_deviceid = getDeviceIDByName(conn,mod_device)

                # Same for the Modifier Key
                mod_keyid = getKeyIDByDeviceIDName(conn,mod_deviceid,mod_key)
                # Again if does not exist adds to DB
                if mod_keyid == 0:
                  insertKey(conn,mod_key,mod_deviceid)
                  mod_keyid = getKeyIDByDeviceIDName(conn,mod_deviceid,mod_key)
                # Inserts the Modifier
                insertModifier(conn,modifier.tag,None,triggerid,mod_keyid)
              else:
                mod_value =  modifier.attrib['Value']
                insertModifier(conn,modifier.tag,mod_value,triggerid,None)
        elif typ in ['Inverted','ToggleOn','Deadzone']:
          value = trigger.attrib['Value']
          insertTrigger(conn,typ,value,controlid,None)
    else:
      if len(control.attrib) > 0:
        insertControl(conn,control.tag,control.attrib['Value'])
      else:
        insertControl(conn,control.tag,None)
  conn.close()

if __name__ == "__main__":
  main()

