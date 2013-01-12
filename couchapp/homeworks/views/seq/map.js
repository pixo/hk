function(doc) {
  if(doc.type == "seq") {
    emit(doc._id, doc);
  }  
}

