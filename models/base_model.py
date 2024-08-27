#!/usr/bin/env python3

"""
BaseModel class definition module.

This module contains the definition of the BaseModel class, which provides
the foundational methods for saving, updating, and converting instances
to dictionary format for all other classes that inherit from it.
"""

from datetime import datetime, timezone
import models
from uuid import uuid4

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """
    This class is the base for all other classes containing methods for
    saving and converting to dictionary format.

    Attributes:
        _id (str): Identifies each object uniquely.
        created_date (datetime): Stores the created date of the object.
        updated_date (datetime): Stores the updated date of the object.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the BaseModel.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if "_id" not in kwargs.keys() and "updated_date" not in \
                kwargs.keys() and "__class__" not in kwargs.keys():
            self._id = str(uuid4())
            self.created_date = datetime.now(timezone.utc)
            self.updated_date = self.created_date
            for key, value in kwargs.items():
                if "created_date" == key or "updated_date" == key:
                    value = datetime.strptime(value, time)
                setattr(self, key, value)
        elif kwargs:
            if kwargs.get("__class__"):
                del kwargs["__class__"]
            for key, value in kwargs.items():
                if "created_date" == key or "updated_date" == key:
                    value = datetime.strptime(value, time)
                setattr(self, key, value)

    def save(self):
        """
        Save the object to the database.
        """
        self.updated_date = datetime.now(timezone.utc)
        models.storage.new(self)

    def update(self):
        """
        Update the object in the database.
        """
        self.updated_date = datetime.now(timezone.utc)
        models.storage.update(self)

    def to_dict(self):
        """
        Convert the class instance to a dictionary.

        Returns:
            dict: A dictionary representation of the instance.
        """
        to_dict = {}
        for key, value in self.__dict__.items():
            if key != "password":
                to_dict[key] = value
        to_dict["__class__"] = self.__class__.__name__
        if "created_date" in to_dict and not\
                isinstance(to_dict["created_date"], str):
            to_dict["created_date"] = \
                    to_dict["created_date"].strftime("%Y-%m-%dT%H:%M:%S.%f")
        if "updated_date" in\
                to_dict and not isinstance(to_dict["updated_date"], str):
            to_dict["updated_date"] =\
                to_dict["updated_date"].strftime("%Y-%m-%dT%H:%M:%S.%f")
        return to_dict

    def __str__(self):
        """
        Represent the class in string format.

        Returns:
            str: A string representation of the instance.
        """
        return f"[{self.__class__.__name__}] ({self._id}) {self.__dict__}"

    def delete(self):
        """
        Delete the object from the database.
        """
        models.storage.delete(self)
