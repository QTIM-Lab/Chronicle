function (doc) {
	if(doc.fileNamePath){
	  emit(doc._id, 1);
	}
}