#!/usr/bin/python3
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import os
app = Flask(__name__)
api = Api(app)

def readTablePos():
  try:
    f = open('table_pos','r')
    pos = (int)(f.read().strip())
    f.close()
    return pos
  except IOError:
    return None

class Table(Resource):
  def get(self):
    parser = reqparse.RequestParser()  # initialize
    parser.add_argument('pos', required=False)  # add args
    args = parser.parse_args()  # parse arguments to dictionary

    if args.pos:
      print("/home/pi/control_table.py -p {}".format(args.pos))
      os.system("/home/pi/control_table.py -p {}".format(args.pos))

    data = readTablePos()
    return {'table_pos': data}, 200

api.add_resource(Table, '/table')  # '/users' is our entry point for Users

if __name__ == '__main__':
  app.run(host='0.0.0.0')  # run our Flask app
 
