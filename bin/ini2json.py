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
    print("%s <inputfile>.ini" % ( pathlib.Path( tool ).name ))

def convert( data ):
    ret = dict()
    currentKey = None

    for line in data:
        line = line.lstrip().rstrip()
        if len( line ) == 0:
            continue

        m = re.match( r"^\[\s*(.+)\s*\]$", line )
        if m:
            currentKey = m.group(1)
            if currentKey not in ret:
                ret[ currentKey ] = dict()
        
        v = re.match( r"^\s*(.+)\s*=\s*(.*)$", line )
        if currentKey and v:
            if len( v.groups() ) == 2:
                ret[ currentKey ][ v.group(1).lower() ] = v.group(2).lstrip().rstrip()
            elif len( v.groups() ) == 1:
                ret[ currentKey ][ v.group(1).lower() ] = None
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
