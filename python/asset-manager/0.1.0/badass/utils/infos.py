'''
Created on Nov 12, 2013

@author: pixo
'''

def getBadassVersion ():
    """
    This function return the version of the AssetManager Badass.
    :returns:  str -- The assetmanaget used version
    
    **Example:**
    
    >>> getBadassVersion ()
    >>> '0.1.0'
    
    """
    
    from badass import version as VERSION
    return VERSION
