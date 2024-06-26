#!/usr/bin/env python3

from models.base_model import BaseModel


class User(BaseModel):

    first_name = ""
    last_name = ""
    email = ""
    username = ""
    password = ""

    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)