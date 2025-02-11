function (doc) {
	FileNamePath = doc['fileNamePath'] ? doc['fileNamePath'] : 'Tag not found'
	PatientID = doc['dataset']['00100020'] ? doc['dataset']['00100020']['Value'] : 'Tag not found'
	SOPInstanceUID = doc['dataset']['00080018'] ? doc['dataset']['00080018']['Value'] : 'Tag not found'
	SeriesInstanceUID = doc['dataset']['0020000E'] ? doc['dataset']['0020000E']['Value'] : 'Tag not found'
	StudyInstanceUID = doc['dataset']['0020000D'] ? doc['dataset']['0020000D']['Value'] : 'Tag not found'
	AcquisitionDateTime = doc['dataset']['0008002A'] ? doc['dataset']['0008002A']['Value'] : 'Tag not found'
	SOPClassUID = doc['dataset']['00080016'] ? doc['dataset']['00080016']['Value'] : 'Tag not found'
	Modality = doc['dataset']['00080060'] ? doc['dataset']['00080060']['Value'] : 'Tag not found'
	ModalityLUTSequence = doc['dataset']['00283000'] ? doc['dataset']['00283000']['Value'] : 'Tag not found'
	ImageType = doc['dataset']['00080008'] ? doc['dataset']['00080008']['Value'] : 'Tag not found'
	MIMETypeOfEncapsulatedDocument = doc['dataset']['00420012'] ? doc['dataset']['00420012']['Value'] : 'Tag not found'
	InstitutionName = doc['dataset']['00080080'] ? doc['dataset']['00080080']['Value'] : 'Tag not found'
	Manufacturer = doc['dataset']['00080070'] ? doc['dataset']['00080070']['Value'] : 'Tag not found'
	ManufacturerModelName = doc['dataset']['00081090'] ? doc['dataset']['00081090']['Value'] : 'Tag not found'
	Laterality = doc['dataset']['00200060'] ? doc['dataset']['00200060']['Value'] : 'Tag not found'
	BitsAllocated = doc['dataset']['00280100'] ? doc['dataset']['00280100']['Value'] : 'Tag not found'
	PhotometricInterpretation = doc['dataset']['00280004'] ? doc['dataset']['00280004']['Value'] : 'Tag not found'
	PixelSpacing = doc['dataset']['00280030'] ? doc['dataset']['00280030']['Value'] : 'Tag not found'
	StationName = doc['dataset']['00081010'] ? doc['dataset']['00081010']['Value'] : 'Tag not found'
	SeriesDescription = doc['dataset']['0008103E'] ? doc['dataset']['0008103E']['Value'] : 'Tag not found'
	StudyDate = doc['dataset']['00080020'] ? doc['dataset']['00080020']['Value'] : 'Tag not found'
	StudyTime = doc['dataset']['00080033'] ? doc['dataset']['00080033']['Value'] : 'Tag not found'
	DocType_non_standard_tag = doc['dataset']['22010010'] ? doc['dataset']['22010010']['Value'] : 'Tag not found'
	AverageRNFLThickness_micrometers_non_standard_tag = doc['dataset']['040910E4'] ? doc['dataset']['040910E4']['Value'] : 'Tag not found'
	OpticCupVolume_mm_squared_non_standard_tag = doc['dataset']['040910E5'] ? doc['dataset']['040910E5']['Value'] : 'Tag not found'
	OpticDiskArea_mm_squared_non_standard_tag = doc['dataset']['040910E6'] ? doc['dataset']['040910E6']['Value'] : 'Tag not found'
	RimArea_mm_squared_non_standard_tag = doc['dataset']['040910E7'] ? doc['dataset']['040910E7']['Value'] : 'Tag not found'
	AvgCDR_non_standard_tag = doc['dataset']['040910E8'] ? doc['dataset']['040910E8']['Value'] : 'Tag not found'
	VerticalCDR_non_standard_tag = doc['dataset']['040910E9'] ? doc['dataset']['040910E9']['Value'] : 'Tag not found'
	values=[FileNamePath,PatientID,SOPInstanceUID,SeriesInstanceUID,StudyInstanceUID,AcquisitionDateTime,SOPClassUID,Modality,ModalityLUTSequence,ImageType,MIMETypeOfEncapsulatedDocument,InstitutionName,Manufacturer,ManufacturerModelName,Laterality,BitsAllocated,PhotometricInterpretation,PixelSpacing,StationName,SeriesDescription,StudyDate,StudyTime,DocType_non_standard_tag,AverageRNFLThickness_micrometers_non_standard_tag,OpticCupVolume_mm_squared_non_standard_tag,OpticDiskArea_mm_squared_non_standard_tag,RimArea_mm_squared_non_standard_tag,AvgCDR_non_standard_tag,VerticalCDR_non_standard_tag]
	emit(doc._id, values);
  }