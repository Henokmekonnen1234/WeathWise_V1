#!/usr/bin/env python3
"""
User class definition module.

This module contains the definition of the User class, which inherits from
BaseModel. The User class includes various attributes to store user details.
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    User class that inherits from BaseModel.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        username (str): The username of the user.
        password (str): The password of the user.
        transactions (list): A list of transactions associated with the user.
    """
    
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    username: str = ""
    password: str = ""
    transactions: str = []

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize a new User instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
