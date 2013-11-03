import pipeline.utils as utils

db = utils.getDb ()
dbname = db.name

if not ( db.name in db ) :
    print False

dbproj = db [ db.name ]

print dbproj
if not ( "type" in dbproj ) :
    print False

doctype = dbproj [ "type" ]

# if doctype == "project":
#     return True

print dbproj["users"]