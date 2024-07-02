
from copy import deepcopy
from datetime import datetime, timezone
import models
from uuid import uuid4

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """This class is the base for all other classes containing methods for
       saving and changing to dictionary format.

    Attributes:
        id (str): Identifies each object uniquely.
        created_date (datetime): Stores the created date of the object.
        updated_date (datetime): Stores the updated date of the object.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the BaseModel"""
        if "_id" not in kwargs.keys() and "updated_date"\
                not in kwargs.keys() and "__class__"  not in\
                 kwargs.keys():
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
        """Save the object to the database"""
        self.updated_date = datetime.now(timezone.utc)
        models.storage.new(self)

    def to_dict(self):
        """Convert the class instance to a dictionary"""
        to_dict = self.__dict__.copy()
        to_dict["__class__"] = self.__class__.__name__
        if "created_date" in to_dict and not isinstance(to_dict["created_date"], str):
            to_dict["created_date"] = to_dict["created_date"].strftime("%Y-%m-%dT%H:%M:%S.%f")
        if "updated_date" in to_dict and not isinstance(to_dict["updated_date"], str):
            to_dict["updated_date"] = to_dict["updated_date"].strftime("%Y-%m-%dT%H:%M:%S.%f")
        if "password" in to_dict:
            del to_dict["password"]
        return to_dict

    def __str__(self):
        """Represent the class in string format"""
        return f"[{self.__class__.__name__}] ({self._id}) {self.__dict__}"

    def delete(self):
        """Delete the object from the database"""
        models.storage.delete(self)
