# the views.py file includes the map/reduce functions for the couchdb
# design as python dictionaries.


# Might be redundant as the README.md has a curl version that is more succint
import os, pprint as pp

view_funcs = {'indexed_tags.js': None, 'delete_all_dicoms.js': None, 'context.js': None, 'series_instances.js': None, 'instance_references.js': None}
for view in view_funcs.keys():
    with open(os.path.join("design",view)) as view_file:
        view_func = view_file.read()
        view_funcs[view] = view_func


global views
views = { "instances" : {
    "language" : "javascript",
    "views" : {
        "context" : {
            "map" : view_funcs['context.js'],
            "reduce" : "_count()",
        },
        "series_instances" : {
            "map" : view_funcs['series_instances.js'],
            "reduce" : "_count()",
        },
        "instance_references" : {
            "map" : view_funcs['instance_references.js'],
            "reduce" : "_count()",
        },
        "delete_all_dicoms": {
            "map": view_funcs['delete_all_dicoms.js'],
            "reduce" : "_count()",
        },
        "indexed_tags": {
            "map": view_funcs['indexed_tags.js'],
            "reduce" : "_count()",
        }
    }
  }
}

import requests
import json

def upload_views_to_couchdb(couchdb_url, dbname, design_doc_name, views):
    """
    Uploads the views to the specified CouchDB database.

    :param couchdb_url: The base URL of the CouchDB server.
    :param dbname: The name of the database to upload the views to.
    :param design_doc_name: The name of the design document.
    :param views: The views dictionary to upload.
    """
    url = f"{couchdb_url}/{dbname}/_design/{design_doc_name}"
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, headers=headers, data=json.dumps(views))

    if response.status_code == 201:
        print("Views uploaded successfully.")
    else:
        print(f"Failed to upload views. Status code: {response.status_code}, Response: {response.text}")

# Example usage
couchdb_url = "http://localhost:5984"
dbname = "axispacs_sample"
design_doc_name = "instances"
upload_views_to_couchdb(couchdb_url, dbname, design_doc_name, views)
