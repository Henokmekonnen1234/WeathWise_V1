#!/usr/bin/python3
"""
Contains the TestTransactionDocs and TestTransaction classes
"""

import inspect
import pep8
import unittest
from models.base_model import BaseModel
from models.transaction import Transaction


class TestTransactionDocs(unittest.TestCase):
    """Tests to check the documentation and style of Transaction class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.transaction_f = inspect.getmembers(Transaction, inspect.isfunction)

    def test_pep8_conformance_transaction(self):
        """Test that models/transaction.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/transaction.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_transaction(self):
        """Test that tests/test_transaction.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_transaction.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_transaction_module_docstring(self):
        """Test for the models/transaction.py module docstring"""
        self.assertIsNot(Transaction.__doc__, None,
                         "Transaction class needs a docstring")
        self.assertTrue(len(Transaction.__doc__) >= 1,
                        "Transaction class needs a docstring")

    def test_transaction_func_docstrings(self):
        """Test for the presence of docstrings in Transaction methods"""
        for func in self.transaction_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestTransaction(unittest.TestCase):
    """Test the Transaction class"""

    def setUp(self):
        """Set up for each test"""
        self.transaction = Transaction()

    def test_is_subclass(self):
        """Test that Transaction is a subclass of BaseModel"""
        self.assertTrue(issubclass(type(self.transaction), BaseModel))

    def test_init_transaction(self):
        """Test that Transaction is properly initialized"""
        self.assertIsInstance(self.transaction, Transaction)

    def test_default_attributes(self):
        """Test that the default attributes are set correctly"""
        self.assertEqual(self.transaction.user_id, "")
        self.assertEqual(self.transaction.amount, 0.0)
        self.assertEqual(self.transaction.type, "")
        self.assertEqual(self.transaction.category, "")
        self.assertEqual(self.transaction.description, "")

    def test_setting_attributes(self):
        """Test that attributes can be set correctly"""
        self.transaction.user_id = "user123"
        self.transaction.amount = 250.75
        self.transaction.type = "expense"
        self.transaction.category = "food"
        self.transaction.description = "Grocery shopping"

        self.assertEqual(self.transaction.user_id, "user123")
        self.assertEqual(self.transaction.amount, 250.75)
        self.assertEqual(self.transaction.type, "expense")
        self.assertEqual(self.transaction.category, "food")
        self.assertEqual(self.transaction.description, "Grocery shopping")

    def test_to_dict(self):
        """Test that to_dict method creates a dictionary with correct attributes"""
        transaction_dict = self.transaction.to_dict()
        self.assertEqual(transaction_dict['user_id'], "")
        self.assertEqual(transaction_dict['amount'], 0.0)
        self.assertEqual(transaction_dict['type'], "")
        self.assertEqual(transaction_dict['category'], "")
        self.assertEqual(transaction_dict['description'], "")
        self.assertIn('created_at', transaction_dict)
        self.assertIn('updated_at', transaction_dict)
        self.assertIn('id', transaction_dict)

    def test_kwargs_initialization(self):
        """Test that a Transaction can be initialized with keyword arguments"""
        data = {
            "user_id": "user456",
            "amount": 500.0,
            "type": "income",
            "category": "salary",
            "description": "Freelance work"
        }
        transaction = Transaction(**data)
        self.assertEqual(transaction.user_id, "user456")
        self.assertEqual(transaction.amount, 500.0)
        self.assertEqual(transaction.type, "income")
        self.assertEqual(transaction.category, "salary")
        self.assertEqual(transaction.description, "Freelance work")


if __name__ == "__main__":
    unittest.main()
