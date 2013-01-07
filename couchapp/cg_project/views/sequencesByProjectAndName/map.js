function(doc) {
  if(doc.type == "sequence") {
    emit(doc._id, doc);
  }  
}

