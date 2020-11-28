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
    print("%s <inputfile>.json" % ( pathlib.Path( tool ).name ))
    print("Use in scripts with:")
    print(">\teval $( %s file.json )" % ( tool ))

## Basically, get all leaves while tracking the path to them (through lists and dicts)
def convert( data, key=None ):
    ret = list()
    
    if istype( data, "str") and key:
        ret.append( "%s=\"%s\"" % ( key.upper(), data ) )
    else:
        if istype( data, "list" ):
            for e, item in enumerate( data ):
                ret += convert( item, "%s%s" % ( key, e ) )

        if istype( data, "dict" ):
            for k in  data:
                item = data[k]
                nkey = k
                if key:
                    nkey = "%s_%s" % ( key, k )
                ret += convert( item, nkey )

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
        print("ERROR: Need input file as only argument" )
        print_usage( sys.argv[0] )
        sys.exit(1)

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
