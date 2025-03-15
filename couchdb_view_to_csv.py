import pdb, os
import requests, json
import pandas as pd, numpy as np
import couchdb

USERNAME="admin"
PASSWORD="password_qtim"
DNS="0.0.0.0"
DB_PORT="5984"


IMAGES_DB_and_DATAFOLDER_KEY={
    "axispacs": 'AXISPACS',
    "axispacs_sample": 'AXISPACS',
    "forum": 'FORUM',
    "forum_sample": 'FORUM',
    "forum_all": 'FORUM_ALL',
    "forum_all_sample": 'FORUM_ALL',
    "imagepools": 'IMAGEPOOLS',
    "imagepools_sample": 'IMAGEPOOLS',
}


def get_and_save_csv(IMAGES_DB, DATAFOLDER):
    server = couchdb.Server(f"http://{USERNAME}:{PASSWORD}@{DNS}:{DB_PORT}")
    db = server[IMAGES_DB]
    header_COUCHDB = ['FileNamePath','PatientMRN','SOPInstanceUID','SeriesInstanceUID','StudyInstanceUID','AcquisitionDateTime','SOPClassUID','Modality','ModalityLUTSequence','ImageType','MIMETypeOfEncapsulatedDocument','InstitutionName','Manufacturer','ManufacturerModelName','Laterality','BitsAllocated','PhotometricInterpretation','PixelSpacing','StationName','SeriesDescription','StudyDate','StudyTime','DocType_non_standard_tag','AverageRNFLThickness_micrometers_non_standard_tag','OpticCupVolume_mm_squared_non_standard_tag','OpticDiskArea_mm_squared_non_standard_tag','RimArea_mm_squared_non_standard_tag','AvgCDR_non_standard_tag','VerticalCDR_non_standard_tag']
    header_final = ['FileNamePath','PatientMRN','SOPInstanceUID','SeriesInstanceUID','StudyInstanceUID','AcquisitionDateTime','SOPClassUID','SOPClassUID_Description','Modality','ModalityLUTSequence','ImageType','MIMETypeOfEncapsulatedDocument','InstitutionName','Manufacturer','ManufacturerModelName','Laterality','BitsAllocated','PhotometricInterpretation','PixelSpacing','StationName','SeriesDescription','StudyDate','StudyTime','DocType_non_standard_tag','AverageRNFLThickness_micrometers_non_standard_tag','OpticCupVolume_mm_squared_non_standard_tag','OpticDiskArea_mm_squared_non_standard_tag','RimArea_mm_squared_non_standard_tag','AvgCDR_non_standard_tag','VerticalCDR_non_standard_tag']
    # set(header_final) - set(header_COUCHDB) # Find only in header_final
    # This is being added as a column to the final csv...This is a look up table for SOPClassUID
    ophthalmology_sop_classes = {
        "1.2.840.10008.5.1.4.1.1.77.1.5.1": "Ophthalmic Photography 8 Bit Image Storage",
        "1.2.840.10008.5.1.4.1.1.77.1.5.2": "Ophthalmic Photography 16 Bit Image Storage",
        "1.2.840.10008.5.1.4.1.1.77.1.5.5": "Wide Field Ophthalmic Photography Stereographic Projection Image Storage",
        "1.2.840.10008.5.1.4.1.1.77.1.5.6": "Wide Field Ophthalmic Photography 3D Coordinates Image Storage",
        "1.2.840.10008.5.1.4.1.1.77.1.5.4": "Ophthalmic Tomography Image Storage",
        "1.2.840.10008.5.1.4.1.1.77.1.5.7": "Ophthalmic Optical Coherence Tomography En Face Image Storage",
        "1.2.840.10008.5.1.4.1.1.77.1.5.8": "Ophthalmic Optical Coherence Tomography B-scan Volume Analysis Storage",
        "1.2.840.10008.5.1.4.1.1.78.7": "Ophthalmic Axial Measurements Storage",
        "1.2.840.10008.5.1.4.1.1.78.8": "Intraocular Lens Calculations Storage",
        "1.2.840.10008.5.1.4.1.1.81.1": "Ophthalmic Thickness Map Storage",
        "1.2.840.10008.5.1.4.1.1.82.1": "Corneal Topography Map Storage",
        "1.2.840.10008.5.1.4.1.1.79.1": "Macular Grid Thickness and Volume Report Storage",
        "1.2.840.10008.5.1.4.1.1.80.1": "Ophthalmic Visual Field Static Perimetry Measurements Storage",
        "1.2.840.10008.5.1.4.1.1.78.1": "Lensometry Measurements Storage",
        "1.2.840.10008.5.1.4.1.1.78.2": "Autorefraction Measurements Storage",
        "1.2.840.10008.5.1.4.1.1.78.3": "Keratometry Measurements Storage",
        "1.2.840.10008.5.1.4.1.1.78.4": "Subjective Refraction Measurements Storage",
        "1.2.840.10008.5.1.4.1.1.78.5": "Visual Acuity Measurements Storage",
        "1.2.840.10008.5.1.4.1.1.78.6": "Spectacle Prescription Report Storage",
        "1.2.840.10008.5.1.4.1.1.7": "Secondary Capture Image Storage",
        "1.2.840.10008.5.1.4.1.1.7.2": "Multi-frame True Color Secondary Capture Image Storage",
        "1.2.840.10008.5.1.4.1.1.104.1": "Encapsulated PDF Storage",
        "1.2.840.10008.5.1.4.1.1.66": "Spatial Registration Storage"
    }
    # Convert the ophthalmology_sop_classes dictionary to a pandas DataFrame
    ophthalmology_sop_classes_df = pd.DataFrame(list(ophthalmology_sop_classes.items()), columns=['SOPClassUID', 'SOPClassUID_Description'])
    ophthalmology_sop_classes_df.head()
    count = 0
    # Grab all results
    view_result = db.view('instances/indexed_tags', timeout=100000)
    view_result_list = list(view_result)
    # view_result_list
    rows = []
    for doc in view_result_list:
        key = doc['key']
        value = doc['value']
        row = {k:v for k,v in zip(header_COUCHDB,value)}
        rows.append(row)
    df = pd.DataFrame(rows)
    # pdb.set_trace()
    # df.head()
    # df.shape
    # df.columns
    # Get SOPClassUID_Description
    df = pd.merge(df, ophthalmology_sop_classes_df, on='SOPClassUID', how='left')
    df.head()
    df.columns
    # Use below to find new SOPClassUIDs I need to add to the ophthalmology_sop_classes dictionary
    # df[df['SOPClassUID_Description'].notnull()].shape
    # df[df['SOPClassUID_Description'].isnull()].shape
    # df[df['SOPClassUID_Description'].isnull()]['SOPClassUID'].unique()
    df[header_final].to_csv(os.path.join(f'/scratch90/QTIM/Active/23-0284/EHR/{DATAFOLDER}', f'{IMAGES_DB}_dicom_headers_parsed.csv'), index=False)


# One at a time
# IMAGES_DB = 'forum_all'
# DATAFOLDER = IMAGES_DB_and_DATAFOLDER_KEY[IMAGES_DB]
# get_and_save_csv(IMAGES_DB, DATAFOLDER)

# BULK samples
get_and_save_csv("axispacs_sample", 'AXISPACS')
get_and_save_csv("forum_sample", 'FORUM')
get_and_save_csv("forum_all_sample", 'FORUM_ALL')
get_and_save_csv("imagepools_sample", 'IMAGEPOOLS')

# BULK
get_and_save_csv("axispacs", 'AXISPACS')
get_and_save_csv("forum", 'FORUM') # HAd to split this up because it was too big, look in map reduce func in couchdb
get_and_save_csv("forum_all", 'FORUM_ALL')
get_and_save_csv("imagepools", 'IMAGEPOOLS')
