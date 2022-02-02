#!/usr/bin/python3
import glob
import os.path
import time
import os
import json
import telegram_send
import time

def getnewestfile():
  folder_path = 'C:/Users/cbras/Saved Games/Frontier Developments/Elite Dangerous/'
  file_type = '*log'
  files = glob.glob(folder_path + file_type)
  max_file = max(files, key=os.path.getctime)
  return max_file
  
def shutdown():
  #cmdCommand = "shutdown /s /t 1"
  cmdCommand = "taskkill /f /im EliteDangerous64.exe"
  os.system(cmdCommand)

def follow():
  file = getnewestfile()
  thefile = open(file,"r")
  print(file)
  '''generator function that yields new lines in a file'''
  # seek the end of the file
  thefile.seek(0, os.SEEK_END)

  # start infinite loop
  while True:
    nfile = getnewestfile()
    if nfile != file:
      print("New file opened",nfile)    
      thefile.close()
      thefile = open(nfile,"r")
      file = nfile
      thefile.seek(0, os.SEEK_END)
    # read last line of file
    line = thefile.readline()
    # sleep if file hasn't been updated
    if not line:
      time.sleep(0.1)
      continue
    yield line

def send_msg(msg):
  message = [msg]
  telegram_send.send(conf='C:/Users/cbras/OneDrive/Ambiente de Trabalho/telegram-send.conf',parse_mode='html',messages=message)

loglines = follow()

bounties = []

lastkill = 0

for line in loglines:
  m = None
  data = json.loads(line)
  try:
    if lastkill != 0: elapsed = time.time() - lastkill
    if elapsed >= 3600:
      m = "Is has been more then one hour since last ship was killed. I am sutting down."      
      send_msg(m)
      shutdown()
      exit()
    if data['event'] == "LoadGame":
      m = "Game loaded for CMDR {} with ship {} at {}".format(data['Commander'],data['Ship_Localised'],data['timestamp'])
    elif data['event'] == "Died":
          m = "Your ship was killed by {} , rank {} with a {} at {}".format(data['KillerName'],data['KillerShip'],data['KillerRank'],data['timestamp'])
    elif data['event'] == "FighterDestroyed":
          m = "Your ship fighter has been detroyed"
    elif data['event'] == "Bounty":
      print(data)
      for reward in data['Rewards']:
        print(reward)
        bounties.append(reward)
      total = 0
      for reward in bounties:
        total += reward['Reward']
      if len(bounties) % 5 == 0:
        m = "You have already killed {} ships with a total of {} CR.".format(len(bounties),total)
      lastkill = time.time()
    elif data['event'] == "MissionRedirected":
      m = "Mission Completed at {}".format(data['timestamp'])
    elif data['event'] == "HullDamage":
      if data['PlayerPilot']:
        health = data['Health']
        if health < 0.2:
          m = "&#9888; &#9888; &#9888; &#9888; &#9888; &#9888; Your ship is getting CRITICALLY damaged, Hull currently at {} &#9888; &#9888; &#9888; &#9888; &#9888; &#9888; - I AM SHUTTING DOWN".format(data['Health'])      
          send_msg(m)
          shutdown()
          exit()
        elif health < 0.4:
          m = "&#9888; &#9888; &#9888; &#9888; &#9888; &#9888; Your ship is getting CRITICALLY damaged, Hull currently at {} &#9888; &#9888; &#9888; &#9888; &#9888; &#9888;".format(data['Health'])
        else:
          m = "Your ship is getting damaged, Hull currently at {}".format(data['Health'])
    if m is not None: 
      print(line)
      send_msg(m)
  except KeyError:
    pass
