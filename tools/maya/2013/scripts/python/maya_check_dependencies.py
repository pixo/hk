#/usr/bin/python
import os
import pipeline.core as core

def getRefsFromFile ( fname ):
    """open file"""
    fil = open( fname, "r" )
    lin = ""
    refs = list ()
    
    while lin.find ( "requires maya" ) < 0 :
        lin = fil.readline ()
        
        if lin.find ("//Name:") < 0 :
            for w in lin.split ( " " ): 
                
                if w.find (".mb") > 0 or w.find (".ma") > 0 :
                    for ch in ( '\n', '"', ';' ) : w = w.replace ( ch , "" )
                    
                    if not ( w in refs ) :
                        refs.append ( w )        
    fil.close()
    return refs
