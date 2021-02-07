#!/usr/bin/env python3

import os, sys, re
import random
import string
import getopt

from pprint import pprint

def random_length( dataset, length ):
    return ''.join( random.SystemRandom().choice( dataset ) for _ in range( length ))

def random_string( length ):
    dataset = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return random_length( dataset, length )

def random_base64( length ):
    dataset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "+/"
    return random_length( dataset, length )


def random_alfabetic( length ):
    dataset = string.ascii_lowercase + string.ascii_uppercase
    return random_length( dataset, length )

def random_number( length ):
    dataset =  string.digits
    return random_length( dataset, length )

def random_lower( length ):
    dataset = string.ascii_lowercase
    return random_length( dataset, length )

def random_upper( length ):
    dataset = string.ascii_uppercase
    return random_length( dataset, length )

def random_printable( length ):
    dataset = string.printable
    return random_length( dataset, length )

def random_special( length ):
    dataset = string.punctuation
    return random_length( dataset, length )

def random_hex( length ):
    dataset = string.hexdigits
    return random_length( dataset, length )

def random_octal( length ):
    dataset = string.octdigits
    return random_length( dataset, length )

def random_all( length ):
    dataset = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.printable + string.punctuation + string.hexdigits + string.octdigits
    return random_length( dataset, length )


def random_by_type( strtype, length ):

    if strtype in ("n","N", "num"):
        return random_number( length )
    elif strtype in ("A","ALFA"):
        return random_lower( length).upper()
    elif strtype in ("a","alfa"):
        return random_lower( length )
    elif strtype in ("s","S","str"):
        return random_string( length )
    elif strtype in ("b","B","b64"):
        return random_base64( length )
    elif strtype in ("X","HEX"):
        return random_hex( length ).upper()
    elif strtype in ("x","hex"):
        return random_hex( length )
    elif strtype in ("O","OCT"):
        return random_octal( length ).upper()
    elif strtype in ("o","oct" ):
        return random_octal( length )
    else:
        return strtype

def load_pattern( pattern ):
    
    matches = list()
    rx = re.findall( r'\[\s*(([A-Za-z]{,4}):([0-9]+))\s*\]', pattern, re.DOTALL )
    for x in rx:
        full = x[0]
        dtype = x[1]
        dnum = int( x[2] )
        rndstr = random_by_type( dtype, dnum )

        matches.append( (full, rndstr ) )
        pattern = re.sub( r"\[\s*%s\s*\]" %( full ), rndstr, pattern, 1 )

    return pattern

def print_help():
    print("%s <pattern>" % ( sys.argv[0]) )
    print("Pattern:")
    print("The patterns are of format [X:Y], where X is the type and B is the length. Each specification must be inside []")
    print( "\t%-20s : %-30s" % ("[a|A|alfa]", "Alfabetical, lower-case" ))
    print( "\t%-20s : %-30s" % ("[n|N|num]", "Numerical, number" ))
    print( "\t%-20s : %-30s" % ("[a|A|alfa]", "Alfabetical, lower-case" ))
    print( "\t%-20s : %-30s" % ("[s|S|str]", "Alfabetical and numerical, lower-case, upper-case and numbers" ))
    print( "\t%-20s : %-30s" % ("[b|B|b64]", "Radom base64 characters" ))
    print("Examples:")
    print("\trndptr.py \"yyy[a:10]zzzz[n:10]wwww[s:10]\"")
    print("\tyyyenbxbhhjtlzzzz8151491174wwwwvfUPCshIZd")
if __name__ == "__main__":

#    print( getopt.getopt( sys.argv[1:], 'ab:c:') )
    if len( sys.argv ) == 1:
        print_help()
        print("Missing args")
        sys.exit(1)
    
    print( load_pattern( sys.argv[1] ) )

