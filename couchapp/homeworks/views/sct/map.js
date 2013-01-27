function(doc) {
  if(doc.task == "sct") {
    emit(doc._id, doc);
  }  
}

