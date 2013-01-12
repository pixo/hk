function(doc) {
  if(doc.task == "rig") {
    emit(doc._id, doc);
  }  
}

