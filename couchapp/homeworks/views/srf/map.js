function(doc) {
  if(doc.task == "srf") {
    emit(doc._id, doc);
  }  
}

