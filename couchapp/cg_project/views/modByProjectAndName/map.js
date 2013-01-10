function(doc) {
  if(doc.type == "mod") {
    emit(doc._id, doc);
  }  
}

