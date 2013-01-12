function(doc) {
  if(doc.type == "env") {
    emit(doc._id, doc);
  }  
}

