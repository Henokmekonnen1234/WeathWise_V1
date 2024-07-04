#!/usr/bin/env python3

from models import storage
from models.user import User
from models.transaction import Transaction

user = User()
user.first_name = "Henok3"
user.last_name = "Mekonnen3"
user.email = "someon333e@gmail.com"
user.username = "Henokmac333"
user.password = "@Enok123333"
user.save()
ts = Transaction()
ts.user_id = user._id
ts.amount = 40.40
ts.type = "expense"
ts.catagory = "food"
ts.description = "for coffee"
ts.save()
print(storage.all())
print("=============")
