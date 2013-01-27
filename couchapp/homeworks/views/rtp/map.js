function(doc) {
  if(doc.task == "rtp") {
    emit(doc._id, doc);
  }  
}

