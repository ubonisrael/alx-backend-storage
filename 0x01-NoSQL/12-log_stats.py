#!/usr/bin/env python3
"""
Write a Python script that provides some stats about Nginx logs stored
in MongoDB:

- Database: logs
- Collection: nginx
- Display (same as the example):
- first line: x logs where x is the number of documents in this collection
- second line: Methods:
- 5 lines with the number of documents with the method = ["GET", "POST",
    "PUT", "PATCH", "DELETE"] in this order (see example below - warning: it’s
    a tabulation before each line)
- one line with the number of documents with:
- method=GET
- path=/status
"""
if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient()
    db = client['logs']
    collection = db['nginx']

    methods_dict = {
        'GET': 0,
        'POST': 0,
        'PUT': 0,
        'PATCH': 0,
        'DELETE': 0
        }

    get_status_path = 0
    count = collection.count_documents({})

    for doc in collection.find():
        if doc['method'] in methods_dict:
            if doc['method'] == 'GET' and doc['path'] == '/status':
                get_status_path += 1
            methods_dict[doc['method']] = \
                methods_dict.get(doc['method'], 0) + 1

    print("{} logs".format(count))
    print("Methods:")
    for k, v in methods_dict.items():
        print("    method {}: {}".format(k, v))
        # print("\tmethod {}: {}".format(k, v))
    print("{} status check".format(get_status_path))
