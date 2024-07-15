#!/usr/bin/python3
"""
Module db_storage.py
This module interacts with the MongoDB database for saving and
retrieving data.
"""

from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.transaction import Transaction
from pymongo import MongoClient
from os import getenv

classes = {
    "User": User,
    "transaction": Transaction
}


class DBStorage:
    """This class is used to interact with MongoDB"""
    __client = None
    __db = None

    def __init__(self):
        self.connect()

    def connect(self):
        if not self.__client:
            MONGO_HOST = getenv('MONGO_HOST', 'localhost')
            MONGO_PORT = int(getenv('MONGO_PORT', 27017))
            MONGO_DB = getenv('MONGO_DB', 'wealthwise')
            self.__client = MongoClient(MONGO_HOST, MONGO_PORT)
            self.__db = self.__client[MONGO_DB]


    def get_collection(self, collection_name):
        """Get a collection from the database"""
        return self.__db[collection_name]

    def all(self, cls=None):
        """Query all objects from the database"""
        new_dict = {}
        for class_name, class_type in classes.items():
            if cls is None or cls is class_type or cls is class_name:
                collection = self.get_collection(class_name.lower() + "s")
                for obj in collection.find():
                    obj_instance = class_type(**obj)
                    new_dict[f"{obj_instance.__class__.__name__}.{obj_instance._id}"] = obj_instance.to_dict()
        return new_dict

    def new(self, obj):
        """Add the object to the database"""
        collection = self.get_collection(obj.__class__.__name__.lower() + "s")
        data = obj.to_dict()
        if obj.__class__.__name__ == "User":
            data["password"] = obj.password
            data["transactions"] = []
        del data["__class__"]
        collection.insert_one(data)

    def update(self, obj):
        collection = self.get_collection(obj.__class__.__name__.lower() + "s")
        data = obj.to_dict()
        if obj.__class__.__name__ == "User":
            data["password"] = obj.password
        del data["__class__"]
        collection.update_one({"_id": obj._id},{"$set": data})

    def delete(self, obj=None):
        """Delete the object from the database"""
        if obj is not None:
            collection = self.get_collection(obj.__class__.__name__.lower() + "s")
            collection.delete_one({"_id": obj._id})

    def reload(self):
        """Reloads data from the database"""
        self.connect()

    def close(self):
        """Close the database connection"""
        self.__client.close()
        self.__client = None

    def get(self, cls, id):
        """Returns the object based on the class name and its ID, or None if not found"""
        if cls not in classes.values():
            return None
        collection = self.get_collection(cls.__name__.lower() + "s")
        data = collection.find_one({"_id": id})
        if data:
            return cls(**data)
        return None

    def filter(self, cls, column_name, value):
        """Filter objects by a column value"""
        collection = self.get_collection(cls.__name__.lower() + "s")
        data = collection.find_one({column_name: value})
        if data:
            return cls(**data)
        return None
    

    def search(self, obj, year, month):
        transaction = self.get_collection(Transaction.__name__.lower() + "s")
        transaction_ids = obj.transactions
        if not transaction_ids:
            return {}
        pipeline = [
        {"$match": {"_id": {"$in": transaction_ids}}},
        {"$project": {
            "type": 1,
            "amount": 1,
            "created_date": 1,
            "year": {"$substr": ["$created_date", 0, 4]},  
            "month": {"$substr": ["$created_date", 5, 2]}  
        }},
        {"$match": {"year": str(year), "month": str(month).zfill(2)}},
        {"$group": {
            "_id": "$type",
            "total_amount": {"$sum": "$amount"}
        }}
    ]

        summary = list(transaction.aggregate(pipeline))
        
        result = {"income": 0, "expense": 0}
        for item in summary:
            transaction_type = item['_id']
            result[transaction_type] = item['total_amount']
        return result
    
    def filter_all(self, obj, year, month):
        transaction = self.get_collection(Transaction.__name__.lower() + "s")
        transaction_ids = obj.transactions
        if not transaction_ids:
            return {}
        pipeline = [
        {"$match": {"_id": {"$in": transaction_ids}}},
         {"$project": {
            "type": 1,
            "amount": 1,
            "created_date": 1,
            "year": {"$substr": ["$created_date", 0, 4]},  
            "month": {"$substr": ["$created_date", 5, 2]}  
        }},
        {"$match": {"year": str(year), "month": str(month).zfill(2)}}
        
        ]

        filtered_data = transaction.aggregate(pipeline)
        return filtered_data