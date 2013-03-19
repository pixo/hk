import pipeline.utils as utils


asset = utils.getAssetTypes ()
task = utils.getTaskTypes()
views = dict()
views['project']= {'map': 'function(doc) {\n  if(doc.type == "project") {\n    emit(doc.name, doc);\n}\n}'}
for key in asset:
    views[key] = {'map': 'function(doc) {\n  if(doc.type == "%s") {\n    emit(doc._id, doc);\n}\n}' % key}

for key in task:
    views[key] = {'map': 'function(doc) {\n  if(doc.task == "%s") {\n    emit(doc._id, doc);\n}\n}' % key}
    
# 'asset_task': {'map': 'function(doc) {\n  if(doc.task && !doc.shot_id) {\n    emit(doc._id, doc);\n}\n}'}
# 'shot_task': {'map': 'function(doc) {\n  if(doc.task && doc.shot_id) {\n    emit(doc._id, doc);\n}\n}'}
    
doc = {
       "_id" : "_design/AssetManager",
       "language" : "javascript",
       "views" : views
       }