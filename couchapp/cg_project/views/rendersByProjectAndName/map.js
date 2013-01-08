function(doc) {
  if(doc.type == "render") {
    emit(doc._id, doc);
  }  
}

