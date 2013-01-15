function(doc) {
  if(doc.task && !doc.shot_id) {
    emit(doc._id, doc);
  }  
}