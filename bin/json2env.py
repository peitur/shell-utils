#!/usr/bin/env python3


import sys, os, re
import pathlib
import json
from pprint import pprint

def read_json( filename, **opt ):
    return json.load( open( filename, "r" ))

def read_textfile( filename, **opt ):
    ret = list()
    with open( filename, "r") as f:
        for line in f.readlines():
            ret.append( line )
    return "".join( ret )

def print_source( slines, **opt ):
    for line in slines:
        print( line )

def print_usage( tool ):
    print("%s <inputfile>.json" % ( tool ))

## Basically, get all leaves while tracking the path to them (through lists and dicts)
def convert( data, key=None ):
    ret = list()
    


    return ret


def istype( obj, t ):
    if type( obj ).__name__ == t:
        return True
    return False

def gettype( obj ):
    return type( obj ).__name__

if __name__ == "__main__":
    opt = dict()

    if len( sys.argv ) < 2:
        print_usage( sys.argv[0] )
        raise AttributeError( "Need input file as only argument" )

    opt['inputfile'] = sys.argv[1]

    try:
        fpath = pathlib.Path( opt['inputfile'] )
        if not fpath.exists():
            raise IOError( "No such file %s" % ( fpath ) )

        ## This tool always asumes json in file
        print_source( convert( read_json( str( fpath ) ) ) )

    except IOError as e:
        print( "ERROR: %s" % (e) )
    except json.decoder.JSONDecodeError as e:
        print( "ERROR: Failed to parse JSON file, malformed or not JSON : %s" % (e) )
    except Exception as e:
        raise e
