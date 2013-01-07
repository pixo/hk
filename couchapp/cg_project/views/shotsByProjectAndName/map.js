function(doc) {
  if(doc.type == "shot") {
    emit(doc._id, doc);
  }  
}

