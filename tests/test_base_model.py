#!/usr/bin/python3
"""
Contains the TestBaseModelDocs and TestBaseModel classes
"""

from datetime import datetime, timezone
import inspect
import unittest
import models
from models.base_model import BaseModel
import pep8
from unittest import mock
from uuid import UUID


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.base_model_f = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance_base_model(self):
        """Test that models/base_model.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_base_model(self):
        """Test that tests/test_models/test_base_model.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_base_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_base_model_module_docstring(self):
        """Test for the base_model.py module docstring"""
        self.assertIsNot(models.base_model.__doc__, None,
                         "base_model.py needs a docstring")
        self.assertTrue(len(models.base_model.__doc__) >= 1,
                        "base_model.py needs a docstring")

    def test_base_model_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_base_model_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_model_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def test_is_subclass(self):
        """Test that BaseModel is a subclass of BaseModel"""
        base = BaseModel()
        self.assertIsInstance(base, BaseModel)
        self.assertTrue(hasattr(base, "_id"))
        self.assertTrue(hasattr(base, "created_date"))
        self.assertTrue(hasattr(base, "updated_date"))

    def test_id_is_uuid(self):
        """Test that id is a valid UUID"""
        base = BaseModel()
        self.assertTrue(isinstance(base._id, str))
        self.assertTrue(UUID(base._id, version=4))

    def test_dates_are_datetime(self):
        """Test that created_date and updated_date are datetime objects"""
        base = BaseModel()
        self.assertTrue(isinstance(base.created_date, datetime))
        self.assertTrue(isinstance(base.updated_date, datetime))

    def test_save_updates_updated_date(self):
        """Test that save method updates the updated_date"""
        base = BaseModel()
        old_updated_date = base.updated_date
        base.save()
        self.assertNotEqual(old_updated_date, base.updated_date)

    def test_to_dict_creates_dict(self):
        """Test that to_dict method creates a dictionary with proper attrs"""
        base = BaseModel()
        new_d = base.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        self.assertTrue("__class__" in new_d)
        self.assertEqual(new_d["__class__"], "BaseModel")

    def test_to_dict_values(self):
        """Test that values in dict returned from to_dict are correct"""
        base = BaseModel()
        new_d = base.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_date"]), str)
        self.assertEqual(type(new_d["updated_date"]), str)
        self.assertEqual(new_d["created_date"],
                         base.created_date.strftime("%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(new_d["updated_date"],
                         base.updated_date.strftime("%Y-%m-%dT%H:%M:%S.%f"))

    def test_str(self):
        """Test that the str method has the correct output"""
        base = BaseModel()
        string = "[BaseModel] ({}) {}".format(base._id, base.__dict__)
        self.assertEqual(string, str(base))

    def test_kwargs_instantiation(self):
        """Test that a new instance can be created with a dictionary of
            attributes"""
        base = BaseModel(_id="1234", created_date="2023-01-01T00:00:00.000000",
                         updated_date="2023-01-01T00:00:00.000000")
        self.assertEqual(base._id, "1234")
        self.assertTrue(isinstance(base.created_date, datetime))
        self.assertTrue(isinstance(base.updated_date, datetime))
        self.assertEqual(base.created_date.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                         "2023-01-01T00:00:00.000000")
        self.assertEqual(base.updated_date.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                         "2023-01-01T00:00:00.000000")

    def test_delete(self):
        """Test that delete method calls storage.delete"""
        base = BaseModel()
        with mock.patch('models.storage.delete') as mock_delete:
            base.delete()
            mock_delete.assert_called_once_with(base)
