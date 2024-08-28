#!/usr/bin/python3

"""
db_storage.py

This module defines the DBStorage class, responsible for connecting to
and interacting with the MongoDB database for the WealthWise
application. It provides methods for CRUD operations on User
and Transaction data.

Classes:
    DBStorage: Handles database operations for User and Transaction
                models.

Attributes:
    classes (dict): Dictionary mapping class names to their respective
                    classes.
"""

from datetime import datetime
import math
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
    """
    DBStorage Class

    This class provides methods to connect to the MongoDB database and
    perform CRUD operations on User and Transaction data.

    Attributes:
        __client (MongoClient): MongoDB client instance.
        __db (Database): MongoDB database instance.
    """

    __client = None
    __db = None

    def __init__(self):
        """
        Initializes the DBStorage instance by establishing a connection
        to the MongoDB database.
        """
        self.connect()

    def connect(self):
        """
        Establishes a connection to the MongoDB database using environment
        variables for configuration. If a connection already exists,
        it does nothing.
        """
        if not self.__client:
            MONGO_HOST = getenv('MONGO_HOST', 'localhost')
            MONGO_PORT = int(getenv('MONGO_PORT', 27017))
            MONGO_DB = getenv('MONGO_DB', 'wealthwise')
            self.__client = MongoClient(MONGO_HOST, MONGO_PORT)
            self.__db = self.__client[MONGO_DB]

    def get_collection(self, collection_name):
        """
        Retrieves a MongoDB collection by its name.

        Args:
            collection_name (str): The name of the collection to retrieve.

        Returns:
            Collection: The MongoDB collection object.
        """
        return self.__db[collection_name]

    def new(self, obj):
        """
        Inserts a new object into the corresponding MongoDB collection.

        Args:
            obj (BaseModel): The object to be inserted into the database.
        """
        collection = self.get_collection(obj.__class__.__name__.lower() +
                                         "s")
        data = obj.to_dict()
        if obj.__class__.__name__ == "User":
            data["password"] = obj.password
            data["transactions"] = []
        if data.get("__class__"):
            del data["__class__"]
        collection.insert_one(data)

    def update(self, obj):
        """
        Updates an existing object in the corresponding MongoDB collection.

        Args:
            obj (BaseModel): The object with updated data to be saved in the
            database.
        """
        collection = self.get_collection(obj.__class__.__name__.lower() +
                                         "s")
        data = obj.to_dict()
        if obj.__class__.__name__ == "User":
            data["password"] = obj.password
        if data.get("__class__"):
            del data["__class__"]
        collection.update_one({"_id": obj._id}, {"$set": data})

    def delete(self, obj=None):
        """
        Deletes an object from the corresponding MongoDB collection.

        Args:
            obj (BaseModel, optional): The object to be deleted from the
            database.
                                       Defaults to None.
        """
        if obj is not None:
            collection = self.get_collection(obj.__class__.__name__.lower()
                                             + "s")
            collection.delete_one({"_id": obj._id})

    def reload(self):
        """
        Re-establishes the connection to the MongoDB database.
        """
        self.connect()

    def close(self):
        """
        Closes the connection to the MongoDB database.
        """
        self.__client.close()
        self.__client = None

    def get(self, cls, id):
        """
        Retrieves an object by class and ID from the MongoDB database.

        Args:
            cls (BaseModel): The class of the object to retrieve.
            id (str): The ID of the object to retrieve.

        Returns:
            BaseModel: The retrieved object, or None if not found.
        """
        if cls not in classes.values():
            return None
        collection = self.get_collection(cls.__name__.lower() + "s")
        data = collection.find_one({"_id": id})
        if data:
            return cls(**data)
        return None

    def filter(self, cls, column_name, value):
        """
        Retrieves an object by class and a specified column value from the
        MongoDB database.

        Args:
            cls (BaseModel): The class of the object to retrieve.
            column_name (str): The column name to filter by.
            value (str): The value to filter by.

        Returns:
            BaseModel: The retrieved object, or None if not found.
        """
        collection = self.get_collection(cls.__name__.lower() + "s")
        data = collection.find_one({column_name: value})
        if data:
            return cls(**data)
        return None

    def search(self, obj, year, month, page, page_size):
        """
        Searches for transactions based on year and month, with
        pagination.

        Args:
            obj (User): The user object to retrieve transactions for.
            year (int): The year to filter transactions by.
            month (int): The month to filter transactions by.
            page (int): The page number for pagination.
            page_size (int): The number of transactions per page.

        Returns:
            dict: A dictionary containing pagination details, summary,
            and transactions.
        """
        transaction = self.get_collection(Transaction.__name__.lower() + "s")
        transaction_ids = obj.transactions
        skip = (page - 1) * page_size
        if not transaction_ids:
            return {}
        if year and month:
            string = f"{year}-{str(month).zfill(2)}"
        elif year:
            string = f"{year}"

        pipeline = [
            {"$match": {"_id": {"$in": transaction_ids}}},
            {"$match": {"created_date": {"$regex": string}}},
            {
                "$facet": {
                    "summery": [
                        {"$group": {
                            "_id": "$type",
                            "total_amount": {"$sum": "$amount"}
                        }}
                    ],
                    "transactions": [
                        {"$skip": skip},
                        {"$limit": page_size},
                        {"$project": {
                            "_id": 1,
                            "created_date": 1,
                            "updated_date": 1,
                            "amount": 1,
                            "type": 1,
                            "catagory": 1,
                            "description": 1
                        }}
                    ],
                    "total_count": [
                        {"$count": "total_documents"}
                    ]
                }
            },
        ]

        results = list(transaction.aggregate(pipeline))

        total_documents = results[0]["total_count"][0]["total_documents"]
        total_pages = math.ceil(total_documents / page_size)
        summery = {}
        transactions = []
        for values in results[0]["transactions"]:
            txn = Transaction(**values)
            transactions.append(txn.to_dict())
        for value in results[0]["summery"]:
            summery[value["_id"]] = value["total_amount"]
        return {
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "total_documents": total_documents,
            "summery": summery,
            "transactions": transactions
        }

    def filter_all(self, obj, page, page_size):
        """
        Retrieves all transactions for a user with pagination.

        Args:
            obj (User): The user object to retrieve transactions for.
            page (int): The page number for pagination.
            page_size (int): The number of transactions per page.

        Returns:
            dict: A dictionary containing pagination details and transactions.
        """
        transaction = self.get_collection(Transaction.__name__.lower() + "s")
        transaction_ids = obj.transactions
        if not transaction_ids:
            return {}
        skip = (page - 1) * page_size
        pipeline = [
            {"$match": {"_id": {"$in": transaction_ids}}},
            {
                "$facet": {
                    "summery": [
                        {"$group": {
                            "_id": "$type",
                            "total_amount": {"$sum": "$amount"}
                        }}
                    ],
                    "transactions": [
                        {"$skip": skip},
                        {"$limit": page_size},
                        {"$project": {
                            "_id": 1,
                            "created_date": 1,
                            "updated_date": 1,
                            "amount": 1,
                            "type": 1,
                            "catagory": 1,
                            "description": 1
                        }}
                    ],
                    "total_count": [
                        {"$count": "total_documents"}
                    ]
                }
            },
        ]

        results = list(transaction.aggregate(pipeline))
        total_documents = results[0]["total_count"][0]["total_documents"]
        total_pages = math.ceil(total_documents / page_size)
        transactions = []
        for values in results[0]["transactions"]:
            txn = Transaction(**values)
            transactions.append(txn.to_dict())
        return {
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "total_documents": total_documents,
            "transactions": transactions
        }
