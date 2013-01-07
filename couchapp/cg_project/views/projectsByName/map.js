function(doc) {
  if(doc.type == "project") {
    emit(doc.name, doc);
  }
}
