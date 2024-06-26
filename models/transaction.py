#!/usr/bin/env python3

from models.base_model import BaseModel


class Transaction(BaseModel):

    user_id = ""
    amount = 0.0
    type = ""
    catagory = ""
    description = ""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)