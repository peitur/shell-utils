#!/usr/bin/env python3

import sys, os, re
import pathlib, shutil
import hashlib
import json
from pprint import pprint


DEFAULT_CHECKSUM="sha256"
WANTED_ALGORITHMS=("sha1", "sha256", "sha512", "md5")

DEF_MOVE=False
DEF_NAIVE=False
DEF_DEST_REF=False

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

def asbool( s ):
    if s in ( True, "True", "true","yes","y","1",1): return True
    elif s in (False, "False","false","no","n","0",0): return False
    else: 
        raise AttributeError("Not supported bool string %s" % (s) )

if __name__ == "__main__":
    options = dict()
    options['debug'] = False
    options['config-file'] = None
    options['source-dir'] = None
    options['dest-dir'] = None
    options['move'] = False
    options['naive'] = False
    options['prefix'] = ""
    options['postfix'] = ""
    options['use-dest-ref'] = True

    if len( sys.argv ) <= 1:
        raise AttributeError("Missing configuration file")

    options['config-file'] = sys.argv[1]
    try:
        config = json.load( open( options['config-file'] ) )
    except Exception as e:
        print("ERROR: Could not read configuration : %s" % ( e ) )

    if not pathlib.Path( config['src'] ).exists(): raise FileNotFoundError("Missing source directory")
    if not pathlib.Path( config['dest'] ).exists(): raise FileNotFoundError("Missing destination directory")

    options['source-dir'] = config['src']
    options['dest-dir'] = config['dest']

    options['debug'] = asbool( config.get('debug', False ) )
    options['naive'] = asbool( config.get('naive', DEF_NAIVE ) )
    options['move'] = asbool( config.get('move', DEF_MOVE ) )
    options['prefix'] = config.get('prefix', '' )
    options['postfix'] = config.get('postfix', '' )

    sourcelist = { FileHash( f ).hash(): "%s/%s" % ( options['source-dir'], f.name ) for f in dirlist( options['source-dir' ])  }
#     destlist = { FileHash( f ).hash(): "%s/%s%s%s" % ( options['dest-dir'], options['prefix'], f.name, options['postfix'] )  for f in dirlist( options['source-dir' ])  }

    for s in sourcelist:
        f = pathlib.Path( sourcelist[ s ] )
        d = pathlib.Path( "%s/%s%s%s" % ( options['dest-dir'], options['prefix'], f.name, options['postfix'] ) )

        if not d.exists():
            if options['move']:
                print("[+] Nove %s -> %s" % ( f.resolve(), d.resolve() ) )
                shutil.move( str( f ), str( d ) )
            else:
                print("[+] Copy %s -> %s" % ( f.resolve(), d.resolve() ) )
                shutil.copyfile( str( f ), str( d )   )
