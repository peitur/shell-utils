#!/usr/bin/env python3

import sys, os, re
import json, jinja2
import pathlib
from pprint import pprint

def read_json( filename, **opt ):
    return json.load( open( filename, "r" ))

def read_textfile( filename, **opt ):
    ret = list()
    with open( filename, "r") as f:
        for line in f.readlines():
            ret.append( line )
    return "".join( ret )


def print_usage( tool ):
    print("%s <varfile>.json <templatefile>" % ( tool ))

if __name__ == "__main__":

    opt = dict()

    if len( sys.argv ) < 3:
        print_usage( sys.argv[0] )
        raise AttributeError( "Need input files to work woth, variables file and a template file!" )

    opt['varfile'] = sys.argv[1]
    opt['templatefile'] = sys.argv[2]

    try:
        varpath = pathlib.Path( opt['varfile'] )
        templpath = pathlib.Path( opt['varfile'] )

        if not varpath.exists():
            raise IOError( "No such variables file %s" % ( varpath ) )

        if not templpath.exists():
            raise IOError( "No such template file %s" % ( templpath ) )

        variables = read_json( str( varpath ) )

        template = jinja2.Template( read_textfile( templpath, **opt ) )
        print( template.render( variables ))


    except IOError as e:
        print( "ERROR: %s" % (e) )
    except json.decoder.JSONDecodeError as e:
        print( "ERROR: Failed to parse JSON file, malformed or not JSON : %s" % (e) )
    except Exception as e:
        raise e
