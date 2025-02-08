# the views.py file includes the map/reduce functions for the couchdb
# design as python dictionaries.

import os

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

