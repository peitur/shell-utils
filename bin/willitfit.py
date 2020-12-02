#!/usr/bin/env python3

import sys, os, re
import pathlib
from pprint import pprint

def file_size( filename ):
    return pathlib.Path( filename ).stat().st_size

def mpoint_free( path ):
    fso = os.statvfs( path )
    fs_free = fso.f_frsize * fso.f_bfree      # Actual number of free bytes
    return fs_free

def mpoint_size( path ):
    fso = os.statvfs( path )
    fs_size = fso.f_frsize * fso.f_blocks     # Size of filesystem in bytes
    return fs_size

def tree_size( obj ):
    size_sum = 0
    


    return size_sum

def print_usage( tool ):
    print("%s <target> <sources> ..." % ( pathlib.Path( tool ).name ))
    print("Tool will check if source directories will fit into target.")


if __name__ == "__main__":
    opt = dict()
    opt['sources'] = []
    opt['targets'] = "."

    if len( sys.argv ) < 2:
        print("ERROR: Need a target and at least one source" )
        print_usage( sys.argv[0] )
        sys.exit(1)

    opt['targets'] = sys.argv[1]
    for s in sys.argv[2:]: 
        opt['sources'].append( s )

    try:
        pprint( mpoint_free( opt['targets']  ))
    except IOError as e:
        print( "ERROR: %s" % (e) )
    except Exception as e:
        raise e
