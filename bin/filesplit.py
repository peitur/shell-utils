#!/usr/bin/env python3

import sys, re, os
import pathlib
import string

from pprint import pprint


DEFAULT_SEPPARATOR='_'
ALLOWED_SEPPARSTORS="._-" + string.ascii_lowercase + string.ascii_uppercase

def filename( srcf, itr, sep=DEFAULT_SEPPARATOR ):
  itr = int( itr )
  fparts = re.split( "\.", srcf )
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


def print_help():
  pass

if __name__ == "__main__":
  opt = dict()
  opt['debug'] = False
  opt['file'] = None
  opt['sep'] = DEFAULT_SEPPARATOR
  opt['target'] = None


