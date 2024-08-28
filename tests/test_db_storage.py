#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import inspect
import pep8
import unittest
from unittest.mock import patch, MagicMock
from models.base_model import BaseModel
from models.user import User
from models.transaction import Transaction
from models.engine.db_storage import DBStorage


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.db_storage_f = inspect.getmembers(DBStorage, 
                                              inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test that tests/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_db_storage_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.db_storage_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs\
                              a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs\
                                a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    def setUp(self):
        """Set up for each test"""
        self.storage = DBStorage()

    @patch('models.engine.db_storage.MongoClient')
    def test_connect(self, mock_mongo_client):
        """Test that the connect method initializes MongoDB connection"""
        self.storage.connect()
        mock_mongo_client.assert_called_once()

    @patch('models.engine.db_storage.MongoClient')
    def test_get_collection(self, mock_mongo_client):
        """Test that get_collection returns the correct MongoDB
        collection"""
        self.storage.connect()
        collection = self.storage.get_collection('users')
        self.assertTrue(mock_mongo_client()[self.__db["users"]],
                        collection)

    @patch('models.engine.db_storage.MongoClient')
    def test_new(self, mock_mongo_client):
        """Test that new method inserts a new object into the database"""
        user = User()
        with patch.object(self.storage, 'get_collection') as\
                mock_get_collection:
            mock_collection = MagicMock()
            mock_get_collection.return_value = mock_collection
            self.storage.new(user)
            mock_collection.insert_one.assert_called_once()

    @patch('models.engine.db_storage.MongoClient')
    def test_update(self, mock_mongo_client):
        """Test that update method modifies an existing object in
            the database"""
        user = User()
        with patch.object(self.storage, 'get_collection') as\
                mock_get_collection:
            mock_collection = MagicMock()
            mock_get_collection.return_value = mock_collection
            self.storage.update(user)
            mock_collection.update_one.assert_called_once()

    @patch('models.engine.db_storage.MongoClient')
    def test_delete(self, mock_mongo_client):
        """Test that delete method removes an object from the database"""
        user = User()
        with patch.object(self.storage, 'get_collection') as\
                mock_get_collection:
            mock_collection = MagicMock()
            mock_get_collection.return_value = mock_collection
            self.storage.delete(user)
            mock_collection.delete_one.assert_called_once()

    @patch('models.engine.db_storage.MongoClient')
    def test_get(self, mock_mongo_client):
        """Test that get method retrieves an object by class and ID"""
        user = User()
        with patch.object(self.storage, 'get_collection') as\
                mock_get_collection:
            mock_collection = MagicMock()
            mock_get_collection.return_value = mock_collection
            mock_collection.find_one.return_value = user.to_dict()
            result = self.storage.get(User, user._id)
            self.assertIsInstance(result, User)

    @patch('models.engine.db_storage.MongoClient')
    def test_filter(self, mock_mongo_client):
        """Test that filter method retrieves an object by class
            and column value"""
        user = User()
        with patch.object(self.storage, 'get_collection') as\
                mock_get_collection:
            mock_collection = MagicMock()
            mock_get_collection.return_value = mock_collection
            mock_collection.find_one.return_value = user.to_dict()
            result = self.storage.filter(User, 'email', user.email)
            self.assertIsInstance(result, User)

    @patch('models.engine.db_storage.MongoClient')
    def test_search(self, mock_mongo_client):
        """Test that search method returns paginated transaction data"""
        user = User()
        with patch.object(self.storage, 'get_collection') as\
                mock_get_collection:
            mock_collection = MagicMock()
            mock_get_collection.return_value = mock_collection
            mock_collection.aggregate.return_value = [{
                "summery": [{"_id": "income", "total_amount": 1000}],
                "transactions": [Transaction().to_dict()],
                "total_count": [{"total_documents": 1}]
            }]
            result = self.storage.search(user, 2023, 8, 1, 10)
            self.assertIn("transactions", result)
            self.assertIn("summery", result)

    @patch('models.engine.db_storage.MongoClient')
    def test_filter_all(self, mock_mongo_client):
        """Test that filter_all method returns all paginated transactions"""
        user = User()
        with patch.object(self.storage, 'get_collection') as mock_get_collection:
            mock_collection = MagicMock()
            mock_get_collection.return_value = mock_collection
            mock_collection.aggregate.return_value = [{
                "summery": [{"_id": "expense", "total_amount": 500}],
                "transactions": [Transaction().to_dict()],
                "total_count": [{"total_documents": 1}]
            }]
            result = self.storage.filter_all(user, 1, 10)
            self.assertIn("transactions", result)

    @patch('models.engine.db_storage.MongoClient')
    def test_close(self, mock_mongo_client):
        """Test that close method closes the MongoDB connection"""
        self.storage.close()
        mock_mongo_client().close.assert_called_once()

