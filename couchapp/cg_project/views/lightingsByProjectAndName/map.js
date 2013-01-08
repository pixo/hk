function(doc) {
  if(doc.type == "lighting") {
    emit(doc._id, doc);
  }  
}

