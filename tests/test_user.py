#!/usr/bin/python3
"""
Contains the TestUserDocs and TestUser classes
"""

import inspect
import pep8
import unittest
from models.base_model import BaseModel
from models.user import User


class TestUserDocs(unittest.TestCase):
    """Tests to check the documentation and style of User class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.user_f = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance_user(self):
        """Test that models/user.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_user(self):
        """Test that tests/test_user.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_user_module_docstring(self):
        """Test for the models/user.py module docstring"""
        self.assertIsNot(User.__doc__, None,
                         "User class needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1,
                        "User class needs a docstring")

    def test_user_func_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for func in self.user_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a\
                                docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a\
                                docstring".format(func[0]))


class TestUser(unittest.TestCase):
    """Test the User class"""

    def setUp(self):
        """Set up for each test"""
        self.user = User()

    def test_is_subclass(self):
        """Test that User is a subclass of BaseModel"""
        self.assertTrue(issubclass(type(self.user), BaseModel))

    def test_init_user(self):
        """Test that User is properly initialized"""
        self.assertIsInstance(self.user, User)

    def test_default_attributes(self):
        """Test that the default attributes are set correctly"""
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.username, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.transactions, [])

    def test_setting_attributes(self):
        """Test that attributes can be set correctly"""
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.email = "johndoe@example.com"
        self.user.username = "johndoe"
        self.user.password = "securepassword"
        self.user.transactions = ["txn1", "txn2"]

        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "johndoe@example.com")
        self.assertEqual(self.user.username, "johndoe")
        self.assertEqual(self.user.password, "securepassword")
        self.assertEqual(self.user.transactions, ["txn1", "txn2"])

    def test_to_dict(self):
        """Test that to_dict method creates a dictionary with correct
            attributes"""
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict['first_name'], "")
        self.assertEqual(user_dict['last_name'], "")
        self.assertEqual(user_dict['email'], "")
        self.assertEqual(user_dict['username'], "")
        self.assertEqual(user_dict['password'], "")
        self.assertEqual(user_dict['transactions'], [])
        self.assertIn('created_at', user_dict)
        self.assertIn('updated_at', user_dict)
        self.assertIn('id', user_dict)

    def test_kwargs_initialization(self):
        """Test that a User can be initialized with keyword arguments"""
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "janedoe@example.com",
            "username": "janedoe",
            "password": "anothersecurepassword",
            "transactions": ["txn3", "txn4"]
        }
        user = User(**data)
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "janedoe@example.com")
        self.assertEqual(user.username, "janedoe")
        self.assertEqual(user.password, "anothersecurepassword")
        self.assertEqual(user.transactions, ["txn3", "txn4"])


if __name__ == "__main__":
    unittest.main()
