function(doc) {
  if(doc.task == "dmp") {
    emit(doc._id, doc);
  }  
}

