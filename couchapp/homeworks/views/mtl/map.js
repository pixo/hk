function(doc) {
  if(doc.type == "mtl") {
    emit(doc._id, doc);
  }  
}

