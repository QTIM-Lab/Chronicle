// TODO: this needs to be generalized to instance->instance reference
// for now this is specific to instancePoints
function(doc) {
if (doc.instancePoints) {
	instanceUIDs = Object.keys(doc.instancePoints);
	for (var i in instanceUIDs) {
	emit( instanceUIDs[i], doc._id );
	}
}
}