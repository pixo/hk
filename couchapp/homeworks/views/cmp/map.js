function(doc) {
  if(doc.task == "cmp") {
    emit(doc._id, doc);
  }  
}

