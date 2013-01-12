function(doc) {
  if(doc.task == "lay") {
    emit(doc._id, doc);
  }  
}

