#!/usr/bin/env python3

import sys, re, os
import pathlib
import string
import getopt
from pprint import pprint

DEFAULT_SIZE="10m"
DEFAULT_SEPPARATOR='_'
ALLOWED_SEPPARSTORS="._-" + string.ascii_lowercase + string.ascii_uppercase

def filename( srcf, itr, sep=DEFAULT_SEPPARATOR ):
  itr = int( itr )
  fparts = re.split( "\.", srcf.name )
  if len( fparts ) > 1:
      last = fparts[-1]
      del fparts[-1]
      return "%s%s%s%s" % ( ".".join( fparts ), sep, itr, last )
  else:
    return "%s%s%s" % ( srcf, sep, itr )

def size_as_bytes( s ):
  if type( s ).__name__ == "int": return s
  if type( s ).__name__ == "float": return int( s )

  x = re.match( r"([0-9]+)([bBkmM]{0,1})", s )
  if x:
    p = x.groups()
    if p[1] in ('', 'b', 'B'): 
      return int(x[0])
    elif p[1] in ( "k" ):
      return int( p[0] ) * 1024
    elif p[1] in ("m", "M"):
      return int( p[0] ) * 1024 * 1024
    else:
      raise AttributeError("Malformed size")
  else:
    raise AttributeError("Malformed size reference")

def valid_sepparator( sep ):
  for s in sep:
    if s not in ALLOWED_SEPPARSTORS:
      return False
  return True

def process_file( srcfname, tpath, psize, **opt ):
  
  numbytes = 0
  partbytes = 0
  iteration = 0
  start_iteration = 0

  fname = None
  fout = None
  with open( srcfname, "r" ) as fin:
    for line in fin.readlines():
      
      nbytes = len( line )

      if not fout:
            
        while not fname or fname.exists():
          fname = pathlib.Path( "%s/%s" % ( tpath, filename( srcfname, iteration, opt['sepparator'] ) ) )
          iteration += 1
      
        fout = open( fname.name , "w" )
        partbytes = 0

      fout.write( line )
      numbytes += nbytes
      partbytes += nbytes

      if opt['stop'] in ("under"):
        if partbytes + nbytes > psize:
          if opt['debug']: print("Wrote %s bytes to %s" %( partbytes, fname ))
          fout.close()
          fout = None
          
      if opt['stop'] in ("over"):
        if partbytes > psize:
          if opt['debug']: print("Wrote %s bytes to %s" %( partbytes, fname ))
          fout.close()
          fout = None




  if opt['debug']: print("Wrote %s bytes to %s" %( partbytes, fname ))

  return (iteration, numbytes )

def print_help():
  print("Help for: %s" % ( pathlib.Path( sys.argv[0]).name ) )

if __name__ == "__main__":
  opt = dict()
  opt['debug'] = False
  opt['file'] = None
  opt['suffix'] = None
  opt['prefix'] = None
  opt['target'] = "."
  opt['stop-point'] = "under"
  opt['sep'] = DEFAULT_SEPPARATOR
  opt['size'] = size_as_bytes( DEFAULT_SIZE )

  (options, rest ) = getopt.getopt( sys.argv[1:], "hi:o:p:s:x:c:", ["debug","help", "in", "out", "suffix=", "prefix=", "sepparator=", "stop=", "size="] )

  for o, a in options:
    if o in ("-h", "--help" ):
      print_help()
      sys.exit(0)
    if o in ("--debug"):
      opt['debug'] = True   
    elif o in ("-i", "--in" ):
      opt['file'] = pathlib.Path( a )
    elif o in ("-o", "--out"):
      opt['target'] = pathlib.Path( a )
    elif o in ("-x", "--sepparator"):
      opt['sep'] = a
    elif o in ("-s", "--suffix" ):
      opt['suffix'] = a
    elif o in ("-p","--prefix"):
      opt['prefix'] = a
    if o in ("-c", "--size"):
      opt['size'] = size_as_bytes( a )
    elif o in ("--stop"):
      if a.lower() in ("under", "over" ):
        opt['stop-point'] = a.lower()


  if len( rest ) > 0:
    if not opt['file']:
      opt['file'] = pathlib.Path( rest.pop(0) )

  if opt['file'] and opt['file'].exists():
    
    if not valid_sepparator( opt['sep'] ):
      raise AttributeError("Unvalid sepparator")

    if not pathlib.Path( opt['file'] ).exists():
      raise FileNotFoundError( opt['file'] )

    (numparts, totbytes ) = process_file( opt['file'], opt['target'], opt['size'],  debug=opt['debug'], sepparator=opt['sep'], stop=opt['stop-point'] )
    if opt['debug']: print("Created %s parts, total %s bytes" % ( numparts, totbytes))
  else:
    print_help()     

  

