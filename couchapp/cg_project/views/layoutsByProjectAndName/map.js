function(doc) {
  if(doc.type == "layout") {
    emit(doc._id, doc);
  }  
}

