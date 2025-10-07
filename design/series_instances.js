function(doc) {
	var tags = [
	  ['seriesUID', '0020000E', 'UnspecifiedSeriesUID'],
	  ['classUID', '00080016', 'UnspecifiedClassUID'],
	  ['instanceUID', '00080018', 'UnspecifiedInstanceUID'],
	];
	var key = {};
	if (doc.dataset) {
	  var i;
	  for (i = 0; i < tags.length; i++) {
		var tag = tags[i];
		var name     = tag[0];
		var t        = tag[1];
		var fallback = tag[2];
		key[name] = fallback;
		if (doc.dataset[t] && doc.dataset[t].Value) {
		  key[name] = doc.dataset[t].Value || fallback;
		}
	  }
	  emit( key.seriesUID, [key.classUID, key.instanceUID] );
	}
}