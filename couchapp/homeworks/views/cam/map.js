function(doc) {
  if(doc.task == "cam") {
    emit(doc._id, doc);
  }  
}

