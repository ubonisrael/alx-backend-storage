#!/usr/bin/env python3
"""
Improve 12-log_stats.py by adding the top 10 of the most present
IPs in the collection nginx of the database logs:

The IPs top must be sorted (like the example below)
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
    ips_dict = {}
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
    print("{} status check".format(get_status_path))

    print('IPs:')
    request_logs = collection.aggregate(
        [
            {
                '$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}
            },
            {
                '$sort': {'totalRequests': -1}
            },
            {
                '$limit': 10
            },
        ]
    )
    for request_log in request_logs:
        ip = request_log['_id']
        ip_requests_count = request_log['totalRequests']
        print('    {}: {}'.format(ip, ip_requests_count))
