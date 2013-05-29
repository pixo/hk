import pipeline.core as core
import pipeline

# source = "/homeworks/projects/bls/chr/belanus/mod/main/001/bls_chr_belanus_mod_main.mb"
# destination = "/homeworks/projects/bls/chr/belanus/mod/main/001" 
# core.assetExport ( source, destination )

db = pipeline.utils.getDb("projects", "http://admin:admin@127.0.0.1:5984/")
pipeline.utils.createDbViews(db)