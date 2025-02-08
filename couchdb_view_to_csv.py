import pdb, os
import requests, json
import pandas as pd, numpy as np
import couchdb

USERNAME="admin_slce"
PASSWORD="slce_couchdb_password"
DNS="localhost"
DB_PORT="5984"
IMAGES_DB="axispacs"
IMAGES_DB="axispacs_sample"
IMAGES_DB="forum"
IMAGES_DB="forum_sample"


server = couchdb.Server(f"http://{USERNAME}:{PASSWORD}@{DNS}:{DB_PORT}")
db = server[IMAGES_DB]

header = [
'FileNamePath',
'PatientMRN',
'SOPInstanceUID',
'SeriesInstanceUID',
'StudyInstanceUID',
'AcquisitionDateTime',
'SOPClassUID',
'Modality',
'ModalityLUTSequence',
'ImageType',
'MIMETypeOfEncapsulatedDocument',
'InstitutionName',
'Manufacturer',
'ManufacturerModelName',
'Laterality',
'BitsAllocated',
'PhotometricInterpretation',
'PixelSpacing',
'StationName',
'SeriesDescription',
'StudyDate',
'StudyTime',
'DocType_non_standard_tag',
'AverageRNFLThickness_micrometers_non_standard_tag',
'OpticCupVolume_mm_squared_non_standard_tag',
'OpticDiskArea_mm_squared_non_standard_tag',
'RimArea_mm_squared_non_standard_tag',
'AvgCDR_non_standard_tag',
'VerticalCDR_non_standard_tag'
]

count = 0
# pdb.set_trace()
# Grab all results
view_result = db.view('instances/indexed_tags')
view_result_list = list(view_result)

rows = []
for doc in view_result_list:
    key = doc['key']
    value = doc['value']
    row = {k:v for k,v in zip(header,value)}
    rows.append(row)


df = pd.DataFrame(rows)
df.head()
df.shape
df.columns



# To manage smaller pieces (row by row)
# df = pd.DataFrame()
# for doc in db.view('instances/indexed_tags'):
#     count += 1
#     if count % 10000 == 0: print(count)
#     key = doc['key']
#     value = doc['value']
#     row = {k:[v] for k,v in zip(header,value)}
#     # pdb.set_trace()
#     row_df = pd.DataFrame(row, columns=header)
#     df = pd.concat((df, row_df))

df.to_csv(os.path.join('/projects/coris_db/axispacs_dir_scan', 'axispacs_dicom_headers_parsed.csv'), index=False)
df.to_csv(os.path.join('/projects/coris_db/forum_dir_scan', 'forum_dicom_headers_parsed.csv'), index=False)

# du -sBM /projects/coris_db/postgres/queries_and_stats/axispacs_directory_scan/axispacs_dicom_headers_parsed.csv