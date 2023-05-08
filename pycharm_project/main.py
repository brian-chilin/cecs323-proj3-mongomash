# used pycharm to install pymongo
from pymongo import MongoClient
from pprint import pprint

def connect():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['project3']

if __name__ == "__main__":
    db = connect()

    cookieTypes = [
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "price": 1,
                "ingredients": 1
            }
        }
    ]
    results = db["cookietypes"].aggregate(cookieTypes)
    pprint(list(results))
