'''
Created on Nov 12, 2013

@author: pixo
'''
import os, re

def getBadassVersion ():
    """
    This function return the version of the AssetManager Badass.
    :returns:  str -- The assetmanager used version
    
    **Example:**
    
    >>> getBadassVersion ()
    >>> '0.1.0'
    
    """

    from badass import version as VERSION
    return VERSION

def getBadassVersions ():
    """
    This function return all the versions of the AssetManager Badass.
    :returns:  list -- The assetmanager used version
    
    **Example:**
    
    >>> getBadassVersions ()
    >>> ["0.1.0", "0.2.0"]
    """
    code=os.getenv("HK_CODE_PATH")
    versions=list()
    if code:
        path=os.path.join(code, "python", "asset-manager")
        if os.path.exists(path):
            amdir=os.listdir(path)
            for i in amdir :
                if re.findall ("\d.\d.\d*", i):
                    versions.append(i)
        versions.sort(reverse = True)

    return versions

def getCurrentUser():
    return os.getenv ("USER")
