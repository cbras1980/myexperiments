#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import argparse
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
GPIO.setwarnings(False)

# Create the parser
parser = argparse.ArgumentParser(prog='control_table',
                                 usage='%(prog)s [options] direction',
                                 description='Control the IKEA RODULF table',
                                 epilog='Enjoy the program! :)')

parser.add_argument('-u','--up',action='store_true',help="Pull the table UP")
parser.add_argument('-d','--down',action='store_true',help="Push the table DOWN"                                                                                                             )
parser.add_argument('-s','--seconds',action='store',type=int,help="Time in secon                                                                                                             ds")
parser.add_argument('-p','--position',action='store',type=int,help="Set table he                                                                                                             ight in position 0 to 15")

args = parser.parse_args()

if args.seconds:
  stime = args.seconds
else:
  stime = 2

#Read table position
try:
  f = open('table_pos','r')
  pos = (int)(f.read().strip())
  f.close()
except IOError:
  print("File with position does not exist, resetting...")
  print("I will put the table all UP, starting in 5 seconds, please BE aware of                                                                                                              any objects preventing the table from moving.")
  print("Press Ctrl+C to cancel...")
  count = 5
  RELAIS_1_GPIO = 2
  GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
  try:
    while count >= 0:
      print(count)
      time.sleep(1)
      count = count - 1
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW)
    time.sleep(17)
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
    print("Finished re-setting table")
    pos = 15
    f = open('table_pos','w')
    f.write(str(pos))
    f.close()
  except KeyboardInterrupt:
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)
    GPIO.cleanup()
    print("Cancelled")
    exit(3)

if args.up:
  print("Table goes UP")
  RELAIS_1_GPIO = 2
  increment = 1
elif args.down:
  RELAIS_1_GPIO = 3
  print("Table goes DOWN")
  increment = -1
elif args.position is not None:
  targetpos = args.position
  if targetpos > 15: targetpos = 15
  if targetpos < 0: targetpos = 0
  if targetpos > pos:
    print("Table goes UP")
    RELAIS_1_GPIO = 2
    increment = 1
    stime = targetpos - pos
  elif targetpos < pos:
    print("Table goes DOWN")
    RELAIS_1_GPIO = 3
    increment = -1
    stime = pos - targetpos
  else:
    print("Table is already at position {}".format(targetpos))
    exit(2)
else:
  print("You have to set a direction UP or DOWN or a target POSITION from 0 to 1                                                                                                             5")
  exit(1)

try:
  print("Table is at position: {}".format(pos))
  if pos <= 0 and args.down:
    print("Table is already completely down")
    exit(0)
  elif pos >= 15 and args.up:
    print("Table is already completely up")
    exit(0)
  GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
  GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
  while stime >= 1:
    time.sleep(1)
    pos = pos + increment
    stime = stime - 1
    print("Position: {}".format(pos))
  GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
except KeyboardInterrupt:
  GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
  f = open('table_pos','w')
  f.write(pos)
  f.close()
  print("Exiting cleanly")
except:
  print("some error")
finally:
  print("Finished")
  GPIO.cleanup() # cleanup all GPIO
  f = open('table_pos','w')
  f.write(str(pos))
  f.close()
