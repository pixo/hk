function(doc) {
  if(doc.type == "comp") {
    emit(doc._id, doc);
  }  
}

