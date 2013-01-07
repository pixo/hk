function(doc) {
  if(doc.type == "shot") {
    emit(doc.project_id, doc);
  }  
}

