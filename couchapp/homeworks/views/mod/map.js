function(doc) {
  if(doc.task == "mod") {
    emit(doc._id, doc);
  }  
}

