Chronicle
=========

An ordered record of events.

Purpose
=======

Chronicle is a system to manage a directed acyclic graph of data items.

The items are represented as DICOM object instances stored as documents in CouchDB.

Repository Contents
===================

* site: a web app (html5/js/css) to be hosted from CouchDB for interacting with the data.

* bin: python utility scripts to transfer local (DICOM) data to a CouchDB instance.


Prerequisites
=============

* For the python scripts
 * pydicom
 * couchdb
 * pillow
 * numpy
* For the server
 * Apache CouchDB
* For the browser
 * HTML5 compliant browser (Chrome, Desktop Safari, Firefox, IE should all work with the WebGL rendering)

Use https://github.com/pieper/couchSite to upload design documents and site (html/css/javascript)

Installation
============

* Install a python environment with the prerequisites above (has been tested on mac and linux).
```bash
# Using pdm
pdm venv create --name Chronicle 3.10
eval $(pdm venv activate Chronicle)
pdm add pydicom
pdm add CouchDB
pdm add Pillow
pdm add numpy
pdm add python-gdcm
pdm add pylibjpeg[all]
pdm add PyMuPDF
pdm add ipython
pdm add bpython
pdm add pandas
```

* Use singulaity image
```bash
DOCKER_IMAGE=ubuntu:latest
# SIGULARITY_IMAGE=


```

* Install Apache couchdb
``bash
# Get couchdb
DOCKER_IMAGE=couchdb:3.3.2
docker pull $DOCKER_IMAGE

# Make data directory
cd /scratch90/QTIM/Active/23-0284/EHR/ # probably
DATABASE_LOCATION=/data/couchdb_data


COUCHDB_USER=admin_slce
COUCHDB_PASSWORD=slce_couchdb_password
CONTAINER_NAME=slce_couchdb
docker run \
  -e COUCHDB_USER=$COUCHDB_USER \
  -e COUCHDB_PASSWORD=$COUCHDB_PASSWORD \
  -v $DATABASE_LOCATION:/opt/couchdb/data \
  -d \
  -p 5984:5984 \
  --name $CONTAINER_NAME \
  $DOCKER_IMAGE

# Stop if need be
docker stop $CONTAINER_NAME
# Remove
docker rm $CONTAINER_NAME
```

* Clone the chronicle respository: `git clone https://github.com/QTIM-Lab/Chronicle`

* DEPRECATED - Get the couchSite utility: `git clone https://github.com/QTIM-Lab/couchSite.git`:
  - File now in root directory

* Install chronicle into couchdb: `cd Chronicle; ../couchSite/couchSite.py . coris`
```bash
# IS THIS NEEDED?
url=http://$COUCHDB_USER:$COUCHDB_PASSWORD@localhost:5984
# dbname=axispacs
# dbname=axispacs_sample
dbname=forum_sample
dbname=forum
echo $url; echo $dbname;
python couchSite.py . $url $dbname
```
****
At this point you should have an empty chronicle database and the web app.  The next step is to install some DICOM data into the database, which can be done as follows from the chronicle directory: `./bin/record.py <path to dicom data>`

```bin
ls ..../PACS/VisupacImages/35913/201546
SAMPLE_DICOM=..../PACS/forum/2015/10/14/1.2.276.0.75.2.2.42.116521752646.20151014111008218.261261399.dcm
python ./bin/record.py $SAMPLE_DICOM \
  --url $url \
  --dbName $dbname \
  --dontAttachOriginals



# DICOMS=..../PACS/DICOM
DICOMS=..../PACS/forum
python ./bin/record.py $DICOMS \
  --url $url \
  --dbName $dbname \
  --dontAttachOriginals
  
  --dontAttachImages # Won't attach pngs
```

# Count axispacs and forum directories
## axispacs
```bash
find ..../PACS/DICOM -type f -name "*.dcm" | wc -l
# 
```

## forum
```bash
find ..../PACS/forum -type f -name "*.dcm" | wc -l
# 
```


# Delete all dicoms
```python
import couchdb

COUCHDB_USER='admin'
COUCHDB_PASSWORD=''
url=f"http://{COUCHDB_USER}:{COUCHDB_PASSWORD}@localhost:5984"
dbname='axispacs'

couch = couchdb.Server(url)
db = couch[dbname]

view_name = 'delete_all_dicoms'
view_results = db.view(f"instances/{view_name}")
# view_results = db.view('_all_docs')
for row in view_results:
    print(f"deleting doc {row.id}")
    doc = db[row.id]  # Get the document using its ID
    db.delete(doc)    


```

Note that only pixel formats (transfer syntaxes) supported by pydicom can be used, so some compressed images cannot be loaded currently.

The current Chronicle prototype includes functionality for viewing control-point curves on a per-slice basis and for 3D rendering of these structures.  At this point there is no way to create these using the user interface and there are no publicly available datasets that include these annotations.

Status
======

This is a pre-release project and is subject to change at any time with no assurance of
backward compatibility.

Support
=======

This work is supported by NIH National Cancer Institute (NCI) through award U24 CA180918 (QIICR: Quantitative Image Informatics for Cancer Research) and the National Institute of Biomedical Imaging and Bioengineering (NIBIB) through awards P41 EB015902 (NAC: Neuroimage Analysis Center) and U54 EB005149 (NA-MIC: National Alliance for Medical Image Computing).  Additional support provided by Novartis AG.
