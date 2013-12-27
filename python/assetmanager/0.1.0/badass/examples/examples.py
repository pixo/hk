import badass.core as core
import badass.utils as utils


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

def getFileTexType ():
    """
    This is a simple example to pull to workspace a particular asset version.
    """
    path = "bls_chr_belanus_tex_spec1.1001.tif"
    result = core.getTextureAttr ( path )
    print result

def getEnv ():
    env_data = "source $HOME/.bashrc\n"
    env_data += "source $HK_ROOT/users/$USER/.hk/$HK_PROJECT\n\n"
    env_data += "#Set environment variables\n"
    env_data += "export HK_DB=$HK_PROJECT\n"
    env_data += "export HK_COAT_VER=4-0-03\n"
    env_data += "export HK_COAT_VER_T=4-0-03\n"
    env_data += "export HK_GUERILLA_VER=0.17.0b12\n"
    env_data += "export HK_GUERILLA_VER_T=0.17.0b12\n"
    env_data += "export HK_HIERO_VER=1.6v1\n"
    env_data += "export HK_HIERO_PLAYER_VER=1.6v1\n"
    env_data += "export HK_HOUDINI_VER=12.5\n"
    env_data += "export HK_MARI_VER=2.0v1\n"
    env_data += "export HK_MARI_VER_T=2.1v1a1\n"
    env_data += "export HK_MAYA_ROOT=/usr/autodesk\n"
    env_data += "export HK_MAYA_VER=2013\n"
    env_data += "export HK_MODO_VER=701\n"
    env_data += "export HK_MUDBOX_VER=2013\n"
    env_data += "export HK_NUKE_VER=7.0v2\n"
    env_data += "export HK_BADASS_VER=%s\n\n" % utils.getBadassVersion ()
    env_data += "if $HK_DEV_MODE\n"
    env_data += "    then\n"
    env_data += "        hkmode=\"dev\"\n"
    env_data += "fi\n\n"
    env_data += "alias work='cd $HK_HOME'\n\n"
    env_data += "logpath=\"$HK_USER_REPO\"\n"
    env_data += "export HK_BADASS=\"$HK_CODE_PATH/python/assetmanager/$HK_BADASS_VER\"\n"
    env_data += "export HK_COUCHDB=\"$HK_CODE_PATH/python/couchdb-python\"\n"
    env_data += "export HK_PYSIDE=\"$HK_CODE_PATH/python/pyside\"\n"
    env_data += "argparse=\"$HK_CODE_PATH/python/argparse\"\n"
    env_data += "json=\"$HK_CODE_PATH/python/json\"\n"
    env_data += "export PYTHONPATH=\"$HK_BADASS:$json:$argparse:$PYTHONPATH\"\n\n"
    env_data += "#Set PS1\n"
    env_data += r"export PS1='\[\033[1;34m\]|\u@\h\[\033[1;37m\]|\t\[\033[1;31m\]|$HK_PROJECT|$hkmode>\[\033[0;33m\]\w$ \[\033[00m\]'" + "\n\n"
    env_data += "#Set the current directory\n"
    env_data += "if ! ([ -d $logpath ])\n"
    env_data += "      then\n"
    env_data += "        mkdir -p $logpath\n"
    env_data += "fi\n"

    return env_data
    
# getEnv ()
