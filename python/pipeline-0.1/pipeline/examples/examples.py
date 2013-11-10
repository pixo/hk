import pipeline.core as core
import pipeline.utils as utils


def getAllAssetVersions ():
    """
    This is a simple example to get all asset versions.
    """
    db = utils.getDb()
    versions = core.getVersions ( db = db, doc_id = "bls_chr_belanus_mod_main" )
    print versions
    return versions

def getAnAssetVersion ():
    """
    This is a simple example to get a particular asset version path.
    """
    db = utils.getDb()
    version = core.getVersionPath ( db = db, doc_id = "bls_chr_belanus_mod_main", version = "last" )
    print version
    return version

def pullAnAssetVersion ():
    """
    This is a simple example to pull to workspace a particular asset version.
    """
    db = utils.getDb ()
    version = 2
    result = core.pull ( db = db, doc_id = "bls_chr_belanus_mod_main", version = version )
    print result
