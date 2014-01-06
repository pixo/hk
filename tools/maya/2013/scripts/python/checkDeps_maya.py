#/usr/bin/python
import os
import badass.apps as apps
import maya.cmds as cmds

def getRefsFromFile ( fname ):
    """open file"""
    fil = open ( fname, "r" )
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

def setRefsToFile ( paths, fname ):
    """open file for reading"""
    fil = open ( fname, "r" )
    lines = fil.readlines() 
    maxline = len ( lines )
    
    for i in range ( 0, maxline ) :
        lin = lines [i] 
        
        if lin.find ( "requires maya" ) >= 0 :
            break
        
        if lin.find ("//Name:") < 0 :
            
            if lin.find (".mb") >= 0 or lin.find (".ma") >= 0 :
                
                for w in lin.split ( " " ):
                    
                    if w.find (".mb") > 0 or w.find (".ma") > 0 :
                        for ch in ( '\n', '"', ';' ) : w = w.replace ( ch , "" )
                
                        if w in paths :
                            lines [i] = lin.replace ( w, paths [ w ] )
                                                    
    fil.close()
    
    """open file for writing"""
    fil = open ( fname, "w" )
    fil.writelines ( lines )
    fil.close()
    
    return True

class UiCheckDependenciesMaya ( apps.UiCheckDependencies ):
    
    launcher = "maya"
            
    def getPaths ( self ):
        "Get the references from self.path"
        return getRefsFromFile ( self.fpath )
                                            
    def switchReferences ( self, paths ):
        "Replace the references from paths to self.path"
        setRefsToFile ( paths, self.fpath )
        cmds.file ( self.fpath, o =True )
