function(doc) {
  if(doc.task == "lit") {
    emit(doc._id, doc);
  }  
}

