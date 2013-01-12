function(doc) {
  if(doc.type == "prp") {
    emit(doc._id, doc);
  }  
}

