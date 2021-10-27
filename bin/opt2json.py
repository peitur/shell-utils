#!/usr/bin/env python3

import re
import sys
import json
from pprint import pprint


def deep_dict( d, lst, v ):
    if len( lst ) == 0:
        return v

    if len( lst ) == 1:
        d[ lst.pop(0) ] = v
        return d

    k = lst.pop(0)
    if k not in d:
        d[k] = dict()

    d[k] = deep_dict( dict(), lst , v )

    return d


def deep_merge(s, d):

    for k in s:
        v = s[ k ]
        if type(v).__name__ in ( "dict" ):
            deep_merge(v, d.setdefault(k, {}) )
        else:
            d[ k ] = v

    return d


if __name__ == "__main__":
    res = dict()
    tst = dict()

    for arg in sys.argv[1:]:
        parts = re.split( r"=", arg )
        if len( parts ) == 1:
            tst[ parts[0] ] = None
        elif len( parts ) == 2:
            tst[ parts[0] ] = parts[1]

    for data in tst:
        v = tst[ data ]
        parts = re.split(r"\.", data )
        res = deep_merge( deep_dict( dict(), parts, v ), res )

    print( json.dumps( res, indent=4, sort_keys=True ) )
