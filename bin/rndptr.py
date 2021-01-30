#!/usr/bin/env python3

import os, sys, re
import random
import string

from pprint import pprint

def random_length( dataset, length ):
    return ''.join( random.SystemRandom().choice( dataset ) for _ in range( length ))

def random_string( length ):
    dataset = string.ascii_lowercase + string.ascii_uppercase + string.digits
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

if __name__ == "__main__":
    length = random.randint(0,64)
    pprint( random_string( length ) )
    pprint( random_alfabetic( length ) )
    pprint( random_number( length ) )
    pprint( random_lower( length ) )
    pprint( random_upper( length ) )
    pprint( random_printable( length ) )
    pprint( random_special( length ) )
    pprint( random_hex( length ) )
    pprint( random_octal( length ) )
    pprint( random_all( length ) )
