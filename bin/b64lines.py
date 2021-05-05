#!/usr/bin/env python3

import sys, re, os
import string
import select
import signal
import base64
from pprint import pprint

running = True

def process_file( ):

  while running:
    i, o, e = select.select( [sys.stdin], [], [] )
    if i:
        line = sys.stdin.readline()
        if len( line ) > 0:
            print( base64.b64encode( line.encode(("utf-8")) ).decode("utf-8") )  

  return

def print_help():
  print("Help for: %s" % ( pathlib.Path( sys.argv[0]).name ) )

def signal_handler(sig, frame):
  running = False
  sys.exit(0)

if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)

  (numparts, totbytes ) = process_file()

  

