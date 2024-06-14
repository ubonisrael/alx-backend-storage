"""
Write a Python function that returns all students sorted by average score:

Prototype: def top_students(mongo_collection):
mongo_collection will be the pymongo collection object
The top must be ordered
The average score must be part of each item returns with key = averageScore
"""


def top_students(mongo_collection):
    """
    returns all students sorted by average score
    """
    lst = mongo_collection.aggregate([
        {'$unwind': '$topics'},
        {'$group': {'_id': '$_id',
                    'name': {'$first': "$name"},
                    'averageScore': {'$avg': '$topics.score'}}},
        {'$sort': {'averageScore': -1}}
    ])
    return lst
