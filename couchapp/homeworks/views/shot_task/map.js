function(doc) {
  if(doc.type == "chr") {
    emit(doc._id, doc);
  }  
}

