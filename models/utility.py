#!/usr/bin/python3
"""
Module utility.py
This module contains utility functions used throughout the application.
"""

from datetime import datetime, timedelta
from uuid import uuid4
from models import storage
import bcrypt
import os

not_found = {"error": "Data not found"}
expired = {"error": "Log in again please"}
internal_error = {"error": "Internal Error occurred"}

def encrypt(value=None):
    """
    Encrypt a given string value using bcrypt.
    
    Args:
        value (str): The string to be encrypted.
    
    Returns:
        str: The encrypted string.
    """
    if value:
        result = bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        return result
    else:
        return bcrypt.hashpw(b"None", bcrypt.gensalt()).decode("utf-8")

def decrypt(user_input=None, stored_hash=None):
    """
    Check if the user input matches the stored hash.
    
    Args:
        user_input (str): The user-provided string.
        stored_hash (str): The stored hash to compare against.
    
    Returns:
        bool: True if the user input matches the stored hash, False otherwise.
    """
    if user_input and stored_hash:
        return bcrypt.checkpw(user_input.encode("utf-8"), stored_hash.encode("utf-8"))
    else:
        return False

def taken_value(cls, **kwargs):
    """
    Check if the provided values are already present in the stored objects.
    
    Args:
        cls: The class to check the values against.
        **kwargs: Arbitrary keyword arguments representing field names and values.
    
    Returns:
        str: An error message if a value is already present, False otherwise.
    """
    obj = None
    if kwargs.get("password"):
        del kwargs["password"]
    if kwargs:
        for key, value in kwargs.items():
            if key == "email":
                obj = storage.filter(cls, key, value)
                if obj:
                    return f"{key} already present, change your {key}"
            elif key == "username":
                obj = storage.filter(cls, key, value)
                if obj:
                    return f"{key} already present, change your {key}"
        return False
    else:
        return "No value passed"

def is_user_valid(data: dict = None):
    """
    Check if the user data contains all required fields.
    
    Args:
        data (dict): The user data to validate.
    
    Returns:
        str: An error message if a required field is missing, False otherwise.
    """
    required_fields = [
        'first_name', 'last_name', 'email', 'username', 'password'
    ]
    for field in required_fields:
        md_field = field.replace('_', ' ').capitalize()
        if not data.get(field):
            return f"{md_field} is required"
    else:
        return False
