function(doc) {
  if(doc.type == "vcl") {
    emit(doc._id, doc);
  }  
}

