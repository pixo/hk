function(doc) {
  if(doc.type == "vfx") {
    emit(doc._id, doc);
  }  
}

