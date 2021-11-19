#!/usr/bin/env python3

import os
from elasticsearch import Elasticsearch
es = Elasticsearch()
indexname = 'customfiles'
config = {
    'host': 'elastic'
}
es = Elasticsearch([config,], timeout=300)

request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
}

es.indices.create(index = 'customfiles', body = request_body)

def stat_path(path):
    bulk_data = list()

    file_list = list(os.listdir(path))
    file_dict_pretty = dict()
    for item in file_list:
        fullname = path +'/'+ item
        stats = os.stat(fullname)
        if(os.path.isdir(fullname)):
            stat_path(fullname)
            continue
        file_dict_pretty[fullname] = stats

    for item in file_dict_pretty:
        bulk_update = dict()
        bulk_update['name'] = item;
        bulk_update['size'] = file_dict_pretty[item].st_size;
        # debug
        print("name: {:30s}\n  - size: {:d}b".format(item, file_dict_pretty[item].st_size))

    op_dict = {
        "index": {
            "_index": indexname,
            "_type": 'file'
        }
    }
    bulk_data.append(op_dict)
    bulk_data.append(bulk_update)
    res = es.bulk(index = indexname, body = bulk_data)
    #debug
    print(res);
    res = es.search(body={"query": {"match_all": {} } }, index = indexname)
    print(res);
    res = es.indices.get_mapping(index = indexname)
    print(res);

if __name__ == '__main__':
    path = "."
    stat_path(path)