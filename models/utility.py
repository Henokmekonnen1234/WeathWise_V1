#!/usr/bin/python3
"""
Module utility.py
This file is used to utilities
"""

from datetime import datetime, timedelta
from uuid import uuid4
from models import storage
import bcrypt
import os

UPLOAD_FOLDER = "/home/drogo/Alx/VolunEase_v1/web_flask/static/images/uploaded"
#"/home/drogo/ALX/VolunEase_v1/web_flask/static/images/uploaded"

def encrypt(value=None):
    """This method is used to encrypt strings"""
    if value:
        result = bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        return result
    else:
        return bcrypt.hashpw(b"None", bcrypt.gensalt()).decode("utf-8")

def decrypt(user_input=None, stored_hash=None):
    """This method will check if the user input matches the stored hash"""
    if user_input and stored_hash:
        return bcrypt.checkpw(user_input.encode("utf-8"), stored_hash.encode("utf-8"))
    else:
        return False

def taken_value(cls, **kwargs):
    """This method will check if the value is present in the saved
    object
    """
    obj = None
    if kwargs.get("password"):
        del kwargs["password"]
    if kwargs:
        for key, value in kwargs.items():
            if key == "name":
                obj = storage.filter(cls, key, value)
                if obj:
                    return f"{key} already present, change your {key}"
            elif key == "email":
                obj = storage.filter(cls, key, value)
                if obj:
                    return f"{key} already present, change your {key}"
            elif key == "phone_no":
                obj = storage.filter(cls, key, value)
                if obj:
                    return f"Phone number already present, change your phone number"
            elif key == "website":
                obj = storage.filter(cls, key, value)
                if obj:
                    return f"{key} already present, change your {key}"
            elif key == "description":
                obj = storage.filter(cls, key, value)
                if obj:
                    return f"{key} already present, change your {key}"
        return False
    else:
        return f"No value passed"