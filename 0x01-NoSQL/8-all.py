#!/usr/bin/env python3
"""
Write a Python function that lists all documents in a collection:

Prototype: def list_all(mongo_collection):
Return an empty list if no document in the collection
mongo_collection will be the pymongo collection object
"""
from pymongo import MongoClient


def list_all(mongo_collection):
    """lists all documents in a collection"""
    lst = []
    for doc in mongo_collection.find():
        lst.append(doc)
    return lst
