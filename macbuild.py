#!/usr/bin/python
from math import *

def cursiveP(res):
  #hex = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
  hex = ['A','B','c']
  if ( len(res) == 2 ):
    return res 
  for i in range(0, len(hex)):
    #print str(i)+"-"+str(depth)
    print str(cursiveP(res+hex[i]))



#hex = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']


li=cursiveP("")
