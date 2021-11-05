#!/usr/bin/python3

import sys, os, re
import pathlib, shutil
import hashlib
import json
import tempfile
from pprint import pprint


DEFAULT_CHECKSUM="sha1"
WANTED_ALGORITHMS=("sha1", "sha256", "sha512", "md5")


class FileHash( object ):

    def __init__( self, filename, algorithm=DEFAULT_CHECKSUM, **opt ):
        self._debug = False
        self._blocksize = 65536
        self._algorithm = algorithm
        self._filename = filename

        if 'debug' in opt and opt['debug'] in (True, False):
            self._debug = opt['debug']

        if 'blocksize' in opt and int( opt['blocksize'] ) > 0:
            self._blocksize = int( opt['blocksize'] )

        if self._algorithm not in hashlib.algorithms_available:
            raise AttributeError("Unsupported hash algorithm: %s" % ( self._algorithm ) )

    def hash( self ):
        hasher = None
        BLOCKSIZE = self._blocksize

        if self._algorithm in WANTED_ALGORITHMS:
            hasher = hashlib.new( self._algorithm )
        else:
            raise AttributeError("Unwanted hash algorithm: %s" % ( self._algorithm ) )

        with open( self._filename, 'rb') as f:
            buf = f.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(BLOCKSIZE)

        self._hash = hasher.hexdigest()
        return hasher.hexdigest()


def dirlist( path, pattern=r".*" ):
    p = pathlib.Path( path )
    if not p.is_dir():
        raise AttributeError("Not directory")
    return [ f.resolve() for f in p.iterdir() if re.match( r"^%s$" % ( pattern ), f.name ) and f not in (".", "..") and not f.is_dir() ]

def dict_list_merge( ad, bd ):
  for b in bd:
    if b not in ad:
      ad[ b ] = bd[ b ]
    else:
      ad[ b ] += bd[ b ]
  return ad.copy()

def dirtree( path, pattern=r".*" ):
  p = pathlib.Path( path )

  flist = dict()
  for fle in p.iterdir():

    if not re.match( pattern, str( fle) ):
      continue

    if fle.is_dir():
      flist = dict_list_merge( flist, dirtree( fle, pattern ) )
    else:
        fhash = FileHash( fle ).hash()
        if fhash not in flist:
          flist[ fhash ] = list()
        flist[ fhash ].append( fle.resolve() )
      
  return flist    


def byte_unit( s ):
    current = int( s )
    units = ["B","KB","MB","GB", "TB", "PB"]

    for i,x in enumerate( units ):
        if current < 1024:
            return (current, units[i] )

        if i >= len( units ) - 1:
            return (current, units[i] )

        current = current / 1024
    return (0,"none")


if __name__ == "__main__":
  options = dict()
  options['paths'] = list()

  if len( sys.argv ) > 1:
    options['paths'] = sys.argv[1:]
  else:
    options['paths'] = ["."]

  sums = dict()
  totssize = 0
  totxsize = 0
  totysize = 0

  for path in options['paths']:
    fullt_list = dirtree( path )
    for f in fullt_list:
          
      if len( fullt_list[ f ] ) > 1:
        sfsize = byte_unit( fullt_list[ f ][0].stat().st_size )
        xfsize = byte_unit( fullt_list[ f ][0].stat().st_size * (len( fullt_list[ f ] )  ) )
        yfsize = byte_unit( fullt_list[ f ][0].stat().st_size * (len( fullt_list[ f ] ) - 1) )

        totssize += fullt_list[ f ][0].stat().st_size
        totxsize += fullt_list[ f ][0].stat().st_size * (len( fullt_list[ f ] )  ) 
        totysize += fullt_list[ f ][0].stat().st_size * (len( fullt_list[ f ] ) - 1 )
        
        print("")        
        print("%s - %s :" % ( f, fullt_list[ f ][0].name ) )
        print("-"*32)
        print("%s" % (  "\n".join( [ str(x) for x in fullt_list[ f ] ] ) ) )
        print("-"*32)
        print( "Total %.2f %s [%.2f %s], could save %.2f %s"% ( xfsize[0],xfsize[1], sfsize[0], sfsize[1] , yfsize[0], yfsize[1] ) )

  ( sumssize, sunit ) = byte_unit( totssize ) 
  ( sumxsize, xunit ) = byte_unit( totxsize ) 
  ( sumysize, yunit ) = byte_unit( totysize )    

  print( "Total %.2f %s [%.2f %s], could save %.2f %s"% ( sumxsize, xunit, sumssize, sunit, sumysize, yunit  ) )
