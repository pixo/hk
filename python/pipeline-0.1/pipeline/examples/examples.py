import pipeline.core as core
import pipeline.utils as utils

# versions = core.getAssetVersions ( docid )

# If db is not provided get the current project DB

docid = "bls_chr_belanus_mod_main"
db = utils.getDb()    
versions = db [ docid ]["versions"]
last = str ( len ( versions ) )
path = versions [ last ][ "path" ] 
print versions [ last ]