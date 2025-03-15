# Chronicle
An ordered record of events.


## Purpose
Chronicle is a system to manage a directed acyclic graph of data items. The items are represented as DICOM object instances stored as documents in CouchDB.


## Repository Contents
* bin: python utility scripts to transfer local (DICOM) data to a CouchDB instance.


## Prerequisites
* For the python scripts
 * pydicom
 * couchdb
 * pillow
 * numpy
* For the server
 * Apache CouchDB (Docker makes it easy)


## Installation
* Install a python environment with the prerequisites above (has been tested on mac and linux).
```bash
# Using pyenv\poetry
# pyenv virtualenv 3.10.0 Chronicle
source ~/.bashrc; pyenv deactivate; pyenv activate Chronicle;
```

* Run Apache CouchDB Docker:
```bash
# Get couchdb
DOCKER_IMAGE=couchdb:3.4.2
docker pull $DOCKER_IMAGE

# Make data directory
cd /scratch90/QTIM/Active/23-0284/EHR/Chronicle
DATABASE_LOCATION=/scratch90/QTIM/Active/23-0284/EHR/Chronicle/couchdb_data
echo $DATABASE_LOCATION

COUCHDB_USER=admin
COUCHDB_PASSWORD=password_qtim
CONTAINER_NAME=PACS_SCANS
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


```bash
url=http://$COUCHDB_USER:$COUCHDB_PASSWORD@localhost:5984;

dbname=axispacs_sample; DICOMS=/persist/PACS/DICOM;
echo $url; echo $dbname;
curl -X PUT $url/$dbname;

dbname=axispacs; DICOMS=/persist/PACS/DICOM;
echo $url; echo $dbname;
curl -X PUT $url/$dbname;

dbname=forum_sample; DICOMS=/persist/PACS/forum;
echo $url; echo $dbname;
curl -X PUT $url/$dbname;

dbname=forum; DICOMS=/persist/PACS/forum;
echo $url; echo $dbname;
curl -X PUT $url/$dbname;

dbname=forum_all_sample; DICOMS=/persist/PACS/forum_all;
echo $url; echo $dbname;
curl -X PUT $url/$dbname;

dbname=forum_all; DICOMS=/persist/PACS/forum_all;
echo $url; echo $dbname;
curl -X PUT $url/$dbname;

dbname=imagepools_sample; DICOMS=/persist/PACS/imagepools;
echo $url; echo $dbname;
curl -X PUT $url/$dbname;

dbname=imagepools; DICOMS=/persist/PACS/imagepools;
echo $url; echo $dbname;
curl -X PUT $url/$dbname;

dbname=hyex-spectralis_sample;
echo $url; echo $dbname;
curl -X PUT $url/$dbname;

dbname=hyex-spectralis;
echo $url; echo $dbname;
curl -X PUT $url/$dbname;
```

At this point you should have some databases in the couchdb instance.  The next step is to install some DICOM data into the database, which can be done as follows from the chronicle directory: `./bin/record.py <path to dicom data>`
[http://localhost:5984/_utils/#](http://localhost:5984/_utils/#)

We can load in a particular DICOM or a dolder in the second example:
```bash
SAMPLE_DICOM=<Enter DICOM path>
python ./bin/record.py $SAMPLE_DICOM \
  --url $url \
  --dbName $dbname \
  --dontAttachOriginals


python ./bin/record.py $DICOMS \
  --url $url \
  --dbName $dbname \
  --dontAttachOriginals
  
  --dontAttachImages # Won't attach pngs
```

## Load Views
```bash
# Use jq to ensure valid JSON:
curl -X PUT $url/$dbname/_design/instances -d '{
  "views": {
    "context": {
      "map": '"$(jq -Rs . < design/context.js)"'
    },
    "series_instances": {
      "map": '"$(jq -Rs . < design/series_instances.js)"'
    },
    "instance_references": {
      "map": '"$(jq -Rs . < design/instance_references.js)"'
    },
    "delete_all_dicoms": {
      "map": '"$(jq -Rs . < design/delete_all_dicoms.js)"'
    },
    "indexed_tags": {
      "map": '"$(jq -Rs . < design/indexed_tags.js)"'
    }
  },
  "language": "javascript"
}'

```

## Count DICOMs in directories
```bash
# Ex
find ..../PACS/DICOM -type f -name "*.dcm" | wc -l
```


## Delete all dicoms from CouchDB
```python
import couchdb

COUCHDB_USER='admin'
COUCHDB_PASSWORD=''
url=f"http://{COUCHDB_USER}:{COUCHDB_PASSWORD}@localhost:5984"
dbname='axispacs' # example

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
> Note that only pixel formats (transfer syntaxes) supported by pydicom can be used, so some compressed images cannot be loaded currently.



## Support
> This is a fork so not related but leaving for history
This work is supported by NIH National Cancer Institute (NCI) through award U24 CA180918 (QIICR: Quantitative Image Informatics for Cancer Research) and the National Institute of Biomedical Imaging and Bioengineering (NIBIB) through awards P41 EB015902 (NAC: Neuroimage Analysis Center) and U54 EB005149 (NA-MIC: National Alliance for Medical Image Computing).  Additional support provided by Novartis AG.
