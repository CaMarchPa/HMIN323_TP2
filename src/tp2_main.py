# coding: utf8

from tp2 import GMap
 
def add_square(gmap):
    darts = [gmap.add_dart() for i in xrange(8)]
    for i in xrange(4):
        gmap.link_darts(0, darts[2*i], darts[2*i+1])
    for i in xrange(4):
        gmap.link_darts(1, darts[2*i+1], darts[(2*i+2) % 8])
    return darts

def square():
    gmap = GMap()
    add_square(gmap)
    return gmap
