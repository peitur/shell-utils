#!/usr/bin/env python3

import sys, os, re
import json
import pathlib
from pprint import pprint


def print_json( data , **opt ):
    print( json.dumps( data, ensure_ascii=True, check_circular=True, allow_nan=True, indent=2, sort_keys=True ))

def read_textfile( filename, **opt ):
    ret = list()
    with open( filename, "r") as f:
        for line in f.readlines():
            ret.append( line )
    return ret


def print_usage( tool ):
    print("%s <inputfile>.sh" % ( pathlib.Path( tool ).name ))

def convert( data ):
    ret = dict()
    for line in data:
        line = line.lstrip().rstrip()
        kv = [ v.lstrip().rstrip() for v in re.split( r"=", line ) ]

        parts = re.split( r"_", kv[0] )
        value = kv[1].lstrip().rstrip()
        part = parts.pop(0)

        ret[ part ] = convert_x( parts, ret, value )

    return ret
    

def convert_x( parts, subdata, value = None ):
    ret = dict()

    if len( parts ) == 0:
        return value 

    part = parts.pop(0)

    ret[ part ] = convert_x( parts, subdata, value )    

    return ret
 
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
        print_json( convert( read_textfile( str( fpath ) ) ) )

    except IOError as e:
        print( "ERROR: %s" % (e) )
    except json.decoder.JSONDecodeError as e:
        print( "ERROR: Failed to parse JSON file, malformed or not JSON : %s" % (e) )
    except Exception as e:
        raise e
