#!/usr/bin/env python3
"""
Transaction class definition module.

This module contains the definition of the Transaction class, which inherits from
BaseModel. The Transaction class includes various attributes to store transaction details.
"""

from models.base_model import BaseModel

class Transaction(BaseModel):
    """
    Transaction class that inherits from BaseModel.

    Attributes:
        user_id (str): The ID of the user associated with the transaction.
        amount (float): The amount of the transaction.
        type (str): The type of transaction (e.g., income, expense).
        category (str): The category of the transaction.
        description (str): A description of the transaction.
    """
    
    user_id: str = ""
    amount: float = 0.0
    type: str = ""
    category: str = ""
    description:str = ""

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize a new Transaction instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
