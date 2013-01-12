function(doc) {
  if(doc.task == "tex") {
    emit(doc._id, doc);
  }  
}

